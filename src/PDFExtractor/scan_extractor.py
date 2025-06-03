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
        h_lines, v_lines = find_lines(gray)

        mask = h_lines + v_lines
        # Image.fromarray(mask).show()
        # найдем контуры таблиц
        contours = find_max_contours(mask, max=5)
        self.logger.debug(f'Найдено {len(contours)} таблиц на странице')
        # находим абзацы
        paragraphs = self._extract_paragraph_blocks(gray, contours, margin=2)

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
            
            gray[y:y+h, x:x+w] = remove_lines_by_mask(
                gray[y:y+h, x:x+w],
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

            tables.append(
                Table(
                    bbox=BBox(x, y, x+w, y+h),
                    cells=cells, 
                )
            )
        # На простых файлах работает, но нужен алгоритм обработки
        cleaned = cv2.medianBlur(gray, 3)
        cleaned = cv2.threshold(cleaned, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # посмотри что получилось
        Image.fromarray(cleaned).show()
        
        tasks: List[Tuple[Any, np.ndarray]] = []
        for p in paragraphs:
            roi = cleaned[p.bbox.y1:p.bbox.y2, p.bbox.x1:p.bbox.x2]
            tasks.append((p, roi))
        for tbl in tables:
            for c in tbl.cells:
                
                pad_box = c.bbox.padding(0)
                roi = cleaned[pad_box.y1:pad_box.y2, pad_box.x1:pad_box.x2]
                
                    
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

                        CELL_ROI_PADDING = 5 
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
                    print(f"Error processing OCR result for object type {type(obj)} (bbox: {obj.bbox if hasattr(obj, 'bbox') else 'N/A'}). Exception: {e}")
                    obj.text = ''

        return paragraphs, tables


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
        text_mask = detected_text(gray_for_text_detection, 50, 30)
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
        
        # заплатка на случай отсутствия нижней горизонтальной линиии
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