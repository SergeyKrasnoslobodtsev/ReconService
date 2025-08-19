import logging
from typing import Any, List, Optional, Tuple
import cv2
import numpy as np


from .image_processing import find_lines
from .image_processing import find_max_contours
from .image_processing import detected_text
from .image_processing import remove_lines_by_mask


from .utils import page_to_image
from .utils import find_line_positions 
from .utils import has_line

from .base_extractor import (BBox, 
                             BaseExtractor, 
                             Cell, Page, 
                             Paragraph, 
                             ParagraphType, 
                             Table)

from PIL import Image

from .ocr_engine import OCR, OcrEngine
from concurrent.futures import ThreadPoolExecutor, as_completed

from .adaptive_image_processing import AdaptiveImageProcessing

CELL_ROI_PADDING = 0

# http://ieeexplore.ieee.org/document/9752204
class ScanExtractor(BaseExtractor):
    '''Извлекает структуру документа если он отсканирован'''
    def __init__(self, ocr:Optional[OcrEngine]=OcrEngine.TESSERACT, max_workers: int = 4):
        self.ocr = OCR(ocr_engine=ocr)
        self.max_workers = max_workers
        self.logger = logging.getLogger('app.' + __class__.__name__)
    
    def _process(self, page) -> Tuple[List[Paragraph], List[Table]]:
        self.logger.debug(f'Находим таблицы на странице')

        image = page_to_image(page)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        # На простых файлах работает, но нужен алгоритм обработки
        cleaned = AdaptiveImageProcessing().process(gray)
        h_lines, v_lines = find_lines(cleaned)

        mask = h_lines + v_lines
        # Image.fromarray(mask).show()
        # найдем контуры таблиц
        contours = find_max_contours(mask, max=5)
        self.logger.debug(f'Найдено {len(contours)} таблиц на странице')
        # находим абзацы
        
        paragraphs = self._extract_paragraph_blocks(cleaned, contours, margin=2)
        tables: List[Table] = []
        for x, y, w, h in contours:
            roi_v = v_lines[y:y+h, x:x+w]
            roi_h = h_lines[y:y+h, x:x+w]
            # нужно удалить таблицу(линии) из основного изображения
            # иначе распознавание плохо работает
            mask_roi = cv2.bitwise_or(
                v_lines[y:y+h, x:x+w],
                h_lines[y:y+h, x:x+w]
            )
            
            cleaned[y:y+h, x:x+w] = remove_lines_by_mask(
                cleaned[y:y+h, x:x+w],
                mask_roi
            )
            # получаем сетку таблицы (по умолчанию объединим только столбцы)
            # можно объдинить и столбцы и строки, но есть таблицы, где строки объединены 
            # не логично, либо линия скрыта. 
            # -------|-----------|
            #  text  |    0.00   |
            #        |-----------|  
            #  text  |    0.00   |
            # -------|-----------|
            cells = self._grid_table(x, y, roi_v, roi_h, span_mode=1)
            if len(cells) > 1:
                tables.append(
                    Table(
                        bbox=BBox(x, y, x+w, y+h),
                        cells=cells, 
                    )
            )
            else:
                paragraphs.append(
                    Paragraph(
                        bbox=BBox(x, y, x+w, y+h),
                        type= ParagraphType.NONE,
                        text='',
                        blobs= [cell.blobs for cell in cells]
                    )
                )

        # cleaned = gray
        # посмотри что получилось
        # Image.fromarray(cleaned).show()
        
        tasks: List[Tuple[Any, np.ndarray]] = []
        for p in paragraphs:
            roi = cleaned[p.bbox.y1:p.bbox.y2, p.bbox.x1:p.bbox.x2]
            tasks.append((p, roi))
        for tbl in tables:
            for c in tbl.cells:
                
                pad_box = c.bbox.padding(CELL_ROI_PADDING)
                roi = cleaned[c.bbox.y1:c.bbox.y2, c.bbox.x1:c.bbox.x2]
                
                    
                tasks.append((c, roi))

        # распараллеливаем вызовы OCR в потоках
        with ThreadPoolExecutor(max_workers=self.max_workers) as exe:
            future_to_obj = {
                exe.submit(self.ocr.extract, roi): obj
                for obj, roi in tasks
            }
            for fut in as_completed(future_to_obj):
                obj = future_to_obj[fut]
                try:
                    # Предполагаем, что fut.result() возвращает кортеж (текст, список_боксов_относительно_ROI).
                    # OCR-движок должен сам корректировать координаты с учетом внутренних преобразований (например, полей).
                    (ocr_text_result, boxes_from_ocr) = fut.result()
                    obj.text = ocr_text_result

                    # Определяем координаты верхнего левого угла ROI на странице,
                    # из которого был извлечен текст для данного obj.
                    # Эта логика должна соответствовать тому, как создавались ROI в списке tasks.
                    if isinstance(obj, Paragraph):
                        # Для абзацев ROI обычно берется из obj.bbox
                        roi_origin_x_on_page = obj.bbox.x1
                        roi_origin_y_on_page = obj.bbox.y1
                    elif isinstance(obj, Cell):

                        
                        padded_bbox_for_cell_roi = obj.bbox.padding(CELL_ROI_PADDING)
                        roi_origin_x_on_page = padded_bbox_for_cell_roi.x1
                        roi_origin_y_on_page = padded_bbox_for_cell_roi.y1
                    else:
                        # Неизвестный тип объекта, пропускаем добавление blobs.
                        # Можно добавить логирование или обработку ошибки.
                        continue

                    for x_roi, y_roi, w_roi, h_roi in boxes_from_ocr:
                        # x_roi, y_roi - координаты относительно верхнего левого угла ROI.
                        # Преобразуем в абсолютные координаты страницы.
                        abs_x1 = roi_origin_x_on_page + x_roi
                        abs_y1 = roi_origin_y_on_page + y_roi
                        abs_x2 = abs_x1 + w_roi # x2 = x1 + ширина
                        abs_y2 = abs_y1 + h_roi # y2 = y1 + высота
                        
                        obj.blobs.append(BBox(x1=abs_x1, y1=abs_y1, x2=abs_x2, y2=abs_y2)) 

                except Exception as e:
                    self.logger.error(f'Ошибка при извлечении текста с помощью OCR: {e}', exc_info=True)
                    obj.text = ''
        # self._invisible_lines_detection(tables)
        self._post_process_tables(tables, cleaned)
        return paragraphs, tables

    def _get_lines_in_cell(self, cell: Cell) -> List[List[BBox]]:
        """Группирует blobs в ячейке в строки и возвращает их."""
        if not cell.blobs:
            return []

        blobs_in_cell = sorted(cell.blobs, key=lambda b: b.y1)
        
        lines = []
        current_line = [blobs_in_cell[0]]
        for blob in blobs_in_cell[1:]:
            last_blob_in_line = current_line[-1]
            tolerance = last_blob_in_line.height / 2

            if abs(blob.y1 - last_blob_in_line.y1) <= tolerance:
                current_line.append(blob)
            else:
                lines.append(current_line)
                current_line = [blob]
        lines.append(current_line)
        return lines

    def _post_process_tables(self, tables: List[Table], image: np.ndarray):
        """
        Постобработка таблиц для разделения строк на основе расположения текста.
        Разделяет строки с множественными значениями в финансовых колонках.
        """
        self.logger.info(f"Начинаем постобработку {len(tables)} таблиц")
        
        for table_idx, table in enumerate(tables):
            self.logger.info(f"Обрабатываем таблицу {table_idx + 1}/{len(tables)} с {len(table.cells)} ячейками")
            
            # ИСПРАВЛЕНИЕ: Определяем финансовые колонки один раз для всей таблицы
            table_financial_columns = self._identify_table_financial_columns(table.cells)
            self.logger.info(f"Финансовые колонки таблицы: debit={table_financial_columns['debit']}, credit={table_financial_columns['credit']}")
            
            final_cells = []
            rows = self._group_cells_by_row(table.cells)
            self.logger.info(f"Таблица разделена на {len(rows)} строк")
            
            new_row_counter = 0
            for row_idx, row_cells in enumerate(rows):
                self.logger.debug(f"Обрабатываем строку {row_idx + 1}/{len(rows)} с {len(row_cells)} ячейками")
                
                processed_rows = self._process_table_row(row_cells, image, new_row_counter, row_idx, table_financial_columns)
                final_cells.extend(processed_rows['cells'])
                new_row_counter = processed_rows['next_row_index']
                
                original_count = len(row_cells)
                new_count = len(processed_rows['cells'])
                if new_count > original_count:
                    self.logger.info(f"Строка {row_idx + 1} разделена: было {original_count} ячеек, стало {new_count}")

            table.cells = final_cells
            self.logger.info(f"Таблица {table_idx + 1} обработана: итого {len(final_cells)} ячеек")
        
        return tables

    def _identify_table_financial_columns(self, all_cells: List[Cell]) -> dict:
        """Определяет финансовые колонки для всей таблицы на основе заголовков и содержимого."""
        financial_cols = {'debit': [], 'credit': []}
        
        # Первый проход - поиск заголовков дебет/кредит
        for cell in all_cells:
            text_lower = cell.text.lower()
            if any(keyword in text_lower for keyword in ['дебет', 'debit', 'дебит']):
                if cell.col not in financial_cols['debit']:
                    financial_cols['debit'].append(cell.col)
            elif any(keyword in text_lower for keyword in ['кредит', 'credit']):
                if cell.col not in financial_cols['credit']:
                    financial_cols['credit'].append(cell.col)
        
        if financial_cols['debit'] or financial_cols['credit']:
            self.logger.debug(f"Найдены финансовые колонки по заголовкам: debit={financial_cols['debit']}, credit={financial_cols['credit']}")
            return financial_cols
        
        # Второй проход - анализируем содержимое всех ячеек
        cols_with_financial_data = {}
        for cell in all_cells:
            if self._contains_financial_value(cell.text):
                if cell.col not in cols_with_financial_data:
                    cols_with_financial_data[cell.col] = 0
                cols_with_financial_data[cell.col] += len(self._extract_financial_values(cell.text))
        
        # Сортируем колонки по количеству финансовых значений
        sorted_financial_cols = sorted(cols_with_financial_data.items(), key=lambda x: x[1], reverse=True)
        self.logger.debug(f"Колонки с финансовыми данными: {sorted_financial_cols}")
        
        if len(sorted_financial_cols) >= 2:
            # Берем две колонки с наибольшим количеством финансовых данных
            col1, col2 = sorted_financial_cols[0][0], sorted_financial_cols[1][0]
            # Левую считаем дебетом, правую - кредитом
            if col1 < col2:
                financial_cols['debit'] = [col1]
                financial_cols['credit'] = [col2]
            else:
                financial_cols['debit'] = [col2]
                financial_cols['credit'] = [col1]
            self.logger.debug(f"Найдены финансовые колонки по содержимому: debit={financial_cols['debit']}, credit={financial_cols['credit']}")
            return financial_cols
        
        # Третий вариант - используем позицию (последние 2 колонки)
        if all_cells:
            max_col = max(cell.col for cell in all_cells)
            if max_col >= 1:
                financial_cols['debit'] = [max_col - 1]
                financial_cols['credit'] = [max_col]
                self.logger.debug(f"Используем финансовые колонки по позиции: debit={financial_cols['debit']}, credit={financial_cols['credit']}")
        
        return financial_cols

    def _group_cells_by_row(self, cells: List[Cell]) -> List[List[Cell]]:
        """Группирует ячейки по строкам."""
        from itertools import groupby
        
        sorted_cells = sorted(cells, key=lambda c: (c.row, c.col))
        return [list(group) for _, group in groupby(sorted_cells, key=lambda c: c.row)]

    def _process_table_row(self, row_cells: List[Cell], image: np.ndarray, start_row_index: int, debug_row_idx: int, financial_columns: dict) -> dict:
        """
        Обрабатывает одну строку таблицы, определяя нужно ли её разделить.
        Возвращает обработанные ячейки и следующий индекс строки.
        """
        self.logger.debug(f"=== Анализ строки {debug_row_idx + 1} ===")
        
        # Логируем содержимое ячеек
        for i, cell in enumerate(row_cells):
            self.logger.debug(f"  Ячейка {i} (col={cell.col}): '{cell.text[:50]}...' blobs={len(cell.blobs)}")
        
        text_lines = self._extract_text_lines_from_row(row_cells)
        self.logger.debug(f"Извлечено {len(text_lines)} текстовых линий")
        
        # Если нет текста или только одна линия - не разделяем
        if len(text_lines) <= 1:
            self.logger.debug("Разделение не требуется: недостаточно текстовых линий")
            return self._create_single_row(row_cells, start_row_index)
        
        self.logger.debug(f"Используем финансовые колонки: debit={financial_columns['debit']}, credit={financial_columns['credit']}")
        
        # Проверяем наличие множественных финансовых значений
        has_multiple = self._has_multiple_financial_values(row_cells, financial_columns)
        self.logger.debug(f"Есть множественные финансовые значения: {has_multiple}")
        
        if not has_multiple:
            self.logger.debug("Разделение не требуется: нет множественных финансовых значений")
            return self._create_single_row(row_cells, start_row_index)
        
        # Разделяем строку на основе финансовых значений
        self.logger.info(f"Строка {debug_row_idx + 1} будет разделена на основе финансовых значений")
        return self._split_row_by_financial_values(row_cells, text_lines, financial_columns, image, start_row_index, debug_row_idx)

    def _has_multiple_financial_values(self, row_cells: List[Cell], financial_columns: dict) -> bool:
        """Проверяет наличие множественных финансовых значений в строке."""
        all_financial_cols = financial_columns['debit'] + financial_columns['credit']
        self.logger.debug(f"Проверяем колонки: {all_financial_cols}")
        
        for cell in row_cells:
            if cell.col in all_financial_cols:
                values = self._extract_financial_values(cell.text)
                self.logger.debug(f"  Ячейка col={cell.col}, text='{cell.text}' -> значения: {values}")
                if len(values) > 1:
                    self.logger.debug(f"    НАЙДЕНО множественное значение в колонке {cell.col}: {values}")
                    return True
        
        self.logger.debug("Множественных финансовых значений не найдено")
        return False

    def _extract_financial_values(self, text: str) -> List[str]:
        """Извлекает финансовые значения из текста."""
        import re
        
        self.logger.debug(f"Извлекаем финансовые значения из: '{text}'")
        
        # Паттерн для российских финансовых значений
        pattern = r'\b\d{1,3}(?:\s\d{3})*(?:,\d{1,2})?\b'
        matches = re.findall(pattern, text)
        self.logger.debug(f"  Найдены совпадения по паттерну: {matches}")
        
        # Фильтруем значения (больше 100 рублей)
        valid_values = []
        for match in matches:
            try:
                numeric_value = float(match.replace(' ', '').replace(',', '.'))
                self.logger.debug(f"    '{match}' -> {numeric_value}")
                if numeric_value >= 100:
                    valid_values.append(match)
                    self.logger.debug(f"      ПРИНЯТО: {match}")
                else:
                    self.logger.debug(f"      ОТКЛОНЕНО (< 100): {match}")
            except ValueError as e:
                self.logger.debug(f"      ОШИБКА парсинга '{match}': {e}")
                continue
        
        self.logger.debug(f"  Итоговые финансовые значения: {valid_values}")
        return valid_values

    def _split_row_by_financial_values(self, row_cells: List[Cell], text_lines: List[dict], 
                                     financial_columns: dict, image: np.ndarray, start_row_index: int, debug_row_idx: int) -> dict:
        """Разделяет строку на основе финансовых значений."""
        
        self.logger.debug(f"=== Разделение строки {debug_row_idx + 1} ===")
        
        # Определяем логические строки на основе финансовых данных
        logical_rows = self._create_logical_rows_from_financial_data(text_lines, financial_columns)
        self.logger.debug(f"Создано {len(logical_rows)} логических строк")
        
        if len(logical_rows) <= 1:
            self.logger.debug("Недостаточно логических строк для разделения")
            return self._create_single_row(row_cells, start_row_index)
        
        # Вычисляем позиции разделения
        split_positions = self._calculate_split_positions(logical_rows)
        self.logger.debug(f"Позиции разделения: {split_positions}")
        
        # Создаем новые ячейки
        result = self._create_split_cells(row_cells, split_positions, image, start_row_index, debug_row_idx)
        self.logger.info(f"Строка {debug_row_idx + 1} разделена на {len(result['cells']) // len(row_cells)} подстрок")
        
        return result

    def _create_logical_rows_from_financial_data(self, text_lines: List[dict], financial_columns: dict) -> List[List[dict]]:
        """Создает логические строки на основе финансовых данных."""
        all_financial_cols = financial_columns['debit'] + financial_columns['credit']
        self.logger.debug(f"Анализируем финансовые колонки: {all_financial_cols}")
        
        # Фильтруем только линии с финансовыми данными
        financial_lines = []
        for line in text_lines:
            cell = line['cell']
            if cell.col in all_financial_cols:
                has_financial = self._contains_financial_value(cell.text)
                self.logger.debug(f"  Линия col={cell.col}, y_center={line['y_center']:.1f}, text='{cell.text}', has_financial={has_financial}")
                if has_financial:
                    financial_lines.append(line)
        
        self.logger.debug(f"Найдено {len(financial_lines)} линий с финансовыми данными")
        
        if len(financial_lines) <= 1:
            self.logger.debug("Недостаточно финансовых линий для группировки")
            return []
        
        # Группируем по вертикальной позиции
        logical_rows = []
        tolerance = 15  # увеличиваем толерантность
        
        current_row = [financial_lines[0]]
        self.logger.debug(f"Начинаем группировку с толерантностью {tolerance} пикселей")
        self.logger.debug(f"  Первая группа: y_center={financial_lines[0]['y_center']:.1f}")
        
        for i, line in enumerate(financial_lines[1:], 1):
            last_y = current_row[-1]['y_center']
            current_y = line['y_center']
            distance = abs(current_y - last_y)
            
            self.logger.debug(f"  Линия {i}: y_center={current_y:.1f}, расстояние до предыдущей={distance:.1f}")
            
            if distance <= tolerance:
                current_row.append(line)
                self.logger.debug(f"    ДОБАВЛЕНО в текущую группу")
            else:
                logical_rows.append(current_row)
                self.logger.debug(f"    НОВАЯ группа (группа {len(logical_rows)} закрыта с {len(current_row)} элементами)")
                current_row = [line]
        
        if current_row:
            logical_rows.append(current_row)
            self.logger.debug(f"Последняя группа {len(logical_rows)} с {len(current_row)} элементами")
        
        self.logger.debug(f"Итого создано {len(logical_rows)} логических строк")
        for i, row in enumerate(logical_rows):
            y_positions = [line['y_center'] for line in row]
            self.logger.debug(f"  Логическая строка {i+1}: {len(row)} элементов, y_positions={y_positions}")
        
        return logical_rows

    def _create_split_cells(self, row_cells: List[Cell], split_positions: List[int], 
                           image: np.ndarray, start_row_index: int, debug_row_idx: int) -> dict:
        """Создает новые ячейки на основе позиций разделения."""
        
        row_y_min = min(cell.bbox.y1 for cell in row_cells)
        row_y_max = max(cell.bbox.y2 for cell in row_cells)
        
        self.logger.debug(f"Границы исходной строки: y_min={row_y_min}, y_max={row_y_max}")
        self.logger.debug(f"Позиции разделения: {split_positions}")
        
        # Создаем зоны разделения
        y_boundaries = [row_y_min] + split_positions + [row_y_max]
        zones = list(zip(y_boundaries[:-1], y_boundaries[1:]))
        
        self.logger.debug(f"Созданы зоны: {zones}")
        
        new_cells = []
        
        for zone_index, (y_start, y_end) in enumerate(zones):
            current_row_index = start_row_index + zone_index
            self.logger.debug(f"  Зона {zone_index+1}: y={y_start}-{y_end}, новая строка={current_row_index}")
            
            for cell_idx, cell in enumerate(row_cells):
                # Находим blobs в текущей зоне
                blobs_in_zone = [
                    blob for blob in cell.blobs 
                    if y_start <= (blob.y1 + blob.y2) / 2 < y_end
                ]
                
                self.logger.debug(f"    Ячейка {cell_idx} (col={cell.col}): {len(blobs_in_zone)}/{len(cell.blobs)} blobs в зоне")
                
                # Создаем новую ячейку
                new_bbox = BBox(cell.bbox.x1, y_start, cell.bbox.x2, y_end)
                
                if blobs_in_zone:
                    # Извлекаем текст из зоны
                    roi = image[y_start:y_end, cell.bbox.x1:cell.bbox.x2]
                    text, _ = self.ocr.extract(roi)
                    
                    self.logger.debug(f"      OCR результат: '{text.strip()}'")
                    
                    new_cell = Cell(
                        bbox=new_bbox,
                        row=current_row_index,
                        col=cell.col,
                        text=text.strip(),
                        blobs=blobs_in_zone,
                        colspan=cell.colspan,
                        rowspan=1
                    )
                else:
                    self.logger.debug(f"      Пустая ячейка")
                    new_cell = Cell(
                        bbox=new_bbox,
                        row=current_row_index,
                        col=cell.col,
                        text="",
                        blobs=[],
                        colspan=cell.colspan,
                        rowspan=1
                    )
                
                new_cells.append(new_cell)
        
        self.logger.debug(f"Создано {len(new_cells)} новых ячеек из {len(zones)} зон")
        
        return {
            'cells': new_cells,
            'next_row_index': start_row_index + len(zones)
        }

    def _extract_paragraph_blocks(
        self,
        gray: np.ndarray,
        table_contours: List[Tuple[int, int, int, int]], 
        margin: int = 5
    ) -> List[Paragraph]:
        h_img, w_img = gray.shape[:2]
        
        # 1. Создать копию изображения gray для модификации
        gray_for_text_detection = gray.copy()

        # 2. Если есть контуры таблиц, "закрасить" эти области
        if table_contours:
            for x, y, w, h in table_contours:
                cv2.rectangle(gray_for_text_detection, (x, y), (x + w, y + h), (255), -1) # Закрасить белым

        # 3. На модифицированном изображении получить маску текстовых регионов
        text_mask = detected_text(gray_for_text_detection, 70, 30)
        # Image.fromarray(text_mask).show()

        # 4. Найти контуры абзацев
        paragraph_cv_contours, _ = cv2.findContours(
            text_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        accepted_boxes = []

        for cnt in paragraph_cv_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Игнорируем слишком маленькие контуры
            if w < 20 or h < 20: 
                continue
            
            pad = 5 # Отступ для bbox абзаца
            para_bbox = BBox(
                x1=max(0, x - pad),
                y1=max(0, y - pad),
                x2=min(w_img, x + w + pad),
                y2=min(h_img, y + h + pad)
            )
            is_nested = any(parent.contains(para_bbox) for parent in accepted_boxes)
            
            if is_nested:
                continue
            
            accepted_boxes = [
                parent for parent in accepted_boxes
                if not para_bbox.contains(parent)
            ]

            accepted_boxes.append(para_bbox)

        header_region_y_end = 0
        footer_region_y_start = h_img

        if table_contours:
            # table_contours отсортированы по y в _process
            first_table_x, first_table_y, first_table_w, first_table_h = table_contours[0]
            last_table_x, last_table_y, last_table_w, last_table_h = table_contours[-1]
            
            header_region_y_end = max(0, first_table_y - margin)
            footer_region_y_start = min(h_img, last_table_y + last_table_h + margin)
            # Определяем тип абзаца
            current_para_type = ParagraphType.NONE # По умолчанию NONE
        
        paragraphs: List[Paragraph] = []
        for bbox in accepted_boxes:
            if table_contours:
                # Если абзац полностью находится в области HEADER (выше первой таблицы)
                if bbox.y2 <= header_region_y_end:
                    current_para_type = ParagraphType.HEADER
                # Если абзац полностью находится в области FOOTER (ниже последней таблицы)
                elif bbox.y1 >= footer_region_y_start:
                    current_para_type = ParagraphType.FOOTER
                # Иначе остается NONE (текст между таблицами или рядом с ними, но не в header/footer зонах)
            else:
                current_para_type = ParagraphType.NONE

            paragraphs.append(
                Paragraph(
                    bbox=bbox,
                    type=current_para_type,
                    text='' # Текст будет извлечен позже OCR
                )
            )
        
        # Сортируем абзацы по их вертикальному положению
        paragraphs.sort(key=lambda p: p.bbox.y1)
        return paragraphs
    

    def _grid_table(self, x:int, y:int,
                        pure_v: np.ndarray,
                        pure_h: np.ndarray,
                        span_mode: int = 0) -> list[Cell]:
        """Возвращает список ячеек с colspan/rowspan."""

        xs = find_line_positions(pure_v, axis=0)
        ys_detected = find_line_positions(pure_h, axis=1)

        if len(xs) < 2:
            return []
        
        # заплатка на случай отсутствия нижней горизонтальной линииииии
        # в конце таблицы
        # |--------|------|-------|
        # |        |      |       |

        ys = list(ys_detected) # Создаем изменяемую копию
        
        table_roi_height = pure_h.shape[0]
        # Минимальная высота, чтобы считать пространство под последней линией потенциальной строкой
        min_row_height_threshold = 10 

        # Если были обнаружены горизонтальные линии, и последняя из них находится не у самого низа ROI,
        # и есть достаточно места для еще одной строки, добавляем нижнюю границу ROI как виртуальную линию.
        if ys: # Если найдена хотя бы одна горизонтальная линия
            if ys[-1] < table_roi_height - min_row_height_threshold:
                # Подразумевается, что есть потенциальная последняя строка, у которой отсутствует нижняя линия.
                # Мы предполагаем, что вертикальные линии (xs) корректно определяют столбцы до низа ROI.
                ys.append(table_roi_height)
        # Если ys_detected был пуст, ys останется пустым.
        # Это будет обработано следующей проверкой.

        if len(ys) < 2: # Необходимо как минимум две y-координаты для определения строки
            return []

        # матрица посещения, чтоб не создавать ячейку дважды
        n_rows, n_cols = len(ys) - 1, len(xs) - 1
        used = [[False]*n_cols for _ in range(n_rows)]
        margin = 0  # Отступ от краев ячейки при проверке линии
        line_frac = 0.2 # Минимальная доля длины линии относительно высоты/ширины ячейки
        line_check_thickness = 3 # Толщина области вокруг линии для проверки (в пикселях в каждую сторону)
        
        cells: list[Cell] = []
        for r_idx in range(n_rows):
            for c_idx in range(n_cols):
                if used[r_idx][c_idx]:
                    continue
                
                # Начальные границы базовой ячейки (координаты относительно ROI таблицы)
                x0_base_cell, y0_base_cell = xs[c_idx], ys[r_idx]
                x1_base_cell, y1_base_cell = xs[c_idx+1], ys[r_idx+1]
                
                # Текущие границы объединяемой ячейки, будут расширяться
                current_x1_merged = x1_base_cell
                current_y1_merged = y1_base_cell
                
                col_span = 1
                # Проверка colspan (объединение столбцов)
                if span_mode in (0, 1): # 0: оба, 1: только colspan
                    for next_c in range(c_idx + 1, n_cols):
                        # Потенциальная вертикальная линия-разделитель находится на xs[next_c]
                        # Эта линия разделяет столбец (next_c - 1) и столбец next_c
                        
                        # Определяем y-диапазон для проверки (высота текущей строки с отступами)
                        y_check_s = y0_base_cell + margin
                        y_check_e = y1_base_cell - margin

                        # Определяем x-диапазон (узкая полоса) вокруг потенциальной вертикальной линии xs[next_c]
                        x_line_candidate_pos = xs[next_c]
                        x_check_s = max(0, x_line_candidate_pos - line_check_thickness)
                        x_check_e = min(pure_v.shape[1], x_line_candidate_pos + line_check_thickness + 1) # +1 для среза

                        if y_check_e <= y_check_s or x_check_e <= x_check_s: # Невалидный регион
                            break

                        # Извлекаем узкую вертикальную полосу из маски вертикальных линий
                        region_to_check_for_line = pure_v[y_check_s:y_check_e, x_check_s:x_check_e]
                        
                        min_len_for_separator = int((y_check_e - y_check_s) * line_frac)
                        
                        if has_line(region_to_check_for_line, min_len_for_separator, axis=0): # axis=0 для вертикальной линии
                            break # Найдена разделяющая линия, прекращаем объединение столбцов
                        
                        # Линия не найдена, расширяем colspan
                        current_x1_merged = xs[next_c + 1] # Обновляем правую границу объединенной ячейки
                        col_span += 1
                
                row_span = 1
                # Проверка rowspan (объединение строк)
                if span_mode in (0, 2): # 0: оба, 2: только rowspan
                    for next_r in range(r_idx + 1, n_rows):
                        # Потенциальная горизонтальная линия-разделитель находится на ys[next_r]
                        
                        # Определяем x-диапазон для проверки (ширина текущей объединенной по столбцам ячейки с отступами)
                        x_check_s = x0_base_cell + margin
                        x_check_e = current_x1_merged - margin # Используем current_x1_merged, т.к. colspan уже учтен

                        # Определяем y-диапазон (узкая полоса) вокруг потенциальной горизонтальной линии ys[next_r]
                        y_line_candidate_pos = ys[next_r]
                        y_check_s = max(0, y_line_candidate_pos - line_check_thickness)
                        y_check_e = min(pure_h.shape[0], y_line_candidate_pos + line_check_thickness + 1)

                        if x_check_e <= x_check_s or y_check_e <= y_check_s: # Невалидный регион
                            break
                        
                        region_to_check_for_line = pure_h[y_check_s:y_check_e, x_check_s:x_check_e]
                        min_len_for_separator = int((x_check_e - x_check_s) * line_frac)

                        if has_line(region_to_check_for_line, min_len_for_separator, axis=1): # axis=1 для горизонтальной линии
                            break # Найдена разделяющая линия, прекращаем объединение строк
                        
                        current_y1_merged = ys[next_r + 1] # Обновляем нижнюю границу
                        row_span += 1
                
                # Помечаем ячейки как использованные
                for rr in range(r_idx, r_idx + row_span):
                    for cc in range(c_idx, c_idx + col_span):
                        if rr < n_rows and cc < n_cols: # Проверка границ для used
                            used[rr][cc] = True
                
                cells.append(
                    Cell(
                        # Координаты BBox абсолютные (относительно страницы)
                        # x0_base_cell, y0_base_cell, current_x1_merged, current_y1_merged - относительно ROI таблицы
                        bbox=BBox(x0_base_cell + x, y0_base_cell + y, current_x1_merged + x, current_y1_merged + y),
                        row=r_idx, # Индекс строки оригинальной сетки
                        col=c_idx, # Индекс столбца оригинальной сетки
                        colspan=col_span,
                        rowspan=row_span,
                        text='',       
                    )
                )
        return cells

    def _extract_text_lines_from_row(self, row_cells: List[Cell]) -> List[dict]:
        """Извлекает все текстовые линии из ячеек строки с метаданными."""
        text_lines = []
        
        for cell in row_cells:
            cell_lines = self._get_lines_in_cell(cell)
            for line_blobs in cell_lines:
                text_lines.append({
                    'blobs': line_blobs,
                    'cell': cell,
                    'y_center': sum(blob.y1 + blob.height / 2 for blob in line_blobs) / len(line_blobs)
                })
        
        return sorted(text_lines, key=lambda x: x['y_center'])

    def _identify_financial_columns(self, row_cells: List[Cell]) -> dict:
        """Определяет финансовые колонки по содержимому или позиции."""
        financial_cols = {'debit': [], 'credit': []}
        
        # Первый проход - поиск по ключевым словам в заголовках
        for cell in row_cells:
            text_lower = cell.text.lower()
            if any(keyword in text_lower for keyword in ['дебет', 'debit', 'дебит']):
                financial_cols['debit'].append(cell.col)
            elif any(keyword in text_lower for keyword in ['кредит', 'credit']):
                financial_cols['credit'].append(cell.col)
        
        # Если найдены заголовки, используем их
        if financial_cols['debit'] or financial_cols['credit']:
            self.logger.debug(f"Найдены финансовые колонки по заголовкам: debit={financial_cols['debit']}, credit={financial_cols['credit']}")
            return financial_cols
        
        # Второй проход - ищем колонки с финансовыми значениями
        cols_with_financial_data = []
        for cell in row_cells:
            if self._contains_financial_value(cell.text):
                cols_with_financial_data.append(cell.col)
        
        if len(cols_with_financial_data) >= 2:
            # Если найдено 2 или больше колонок с финансовыми данными
            # Считаем первую - дебет, вторую - кредит
            cols_with_financial_data.sort()
            financial_cols['debit'] = [cols_with_financial_data[0]]
            financial_cols['credit'] = [cols_with_financial_data[1]]
            self.logger.debug(f"Найдены финансовые колонки по данным: debit={financial_cols['debit']}, credit={financial_cols['credit']}")
            return financial_cols
        
        # Третий вариант - используем позицию (последние 2 колонки)
        max_col = max(cell.col for cell in row_cells)
        if max_col >= 1:
            financial_cols['debit'] = [max_col - 1]
            financial_cols['credit'] = [max_col]
            self.logger.debug(f"Используем финансовые колонки по позиции: debit={financial_cols['debit']}, credit={financial_cols['credit']}")
        
        return financial_cols

    def _create_single_row(self, row_cells: List[Cell], row_index: int) -> dict:
        """Создает одну строку без разделения."""
        cells = []
        for cell in row_cells:
            cell.row = row_index
            cells.append(cell)
        
        return {
            'cells': cells,
            'next_row_index': row_index + 1
        }

    def _contains_financial_value(self, text: str) -> bool:
        """Проверяет содержит ли текст финансовое значение."""
        return len(self._extract_financial_values(text)) > 0

    def _calculate_split_positions(self, logical_rows: List[List[dict]]) -> List[int]:
        """Вычисляет Y-позиции для разделения строк."""
        split_positions = []
        
        for i in range(len(logical_rows) - 1):
            current_row_max_y = max(
                max(blob.y2 for blob in line['blobs']) 
                for line in logical_rows[i]
            )
            next_row_min_y = min(
                min(blob.y1 for blob in line['blobs']) 
                for line in logical_rows[i + 1]
            )
            
            split_y = (current_row_max_y + next_row_min_y) // 2
            split_positions.append(split_y)
        
        return split_positions