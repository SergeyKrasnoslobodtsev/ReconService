from typing import List, Tuple
from typing import List
from io import BytesIO
import pymupdf
from PIL import Image, ImageDraw, ImageFont

from .PDFExtractor.base_extractor import Cell, Table, BBox

_DEFAULT_DPI = 300

def convert_to_pil(pdf_bytes: bytes) -> List[Image.Image]:
    '''Преобразуем pdf байты в список изображений'''
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=_DEFAULT_DPI)
        img = pix.pil_image()
        pages.append(img)
    return pages

def convert_to_bytes(images: List[Image.Image]) -> bytes:
    '''
    Преобразуем список изображений обратно в PDF байты.
    Каждое изображение помещается на новую страницу стандартного размера A4
    (210мм x 297мм) с указанной ориентацией.
    Изображение масштабируется для заполнения страницы с сохранением пропорций и центрируется.
    
    Args:
        images: Список изображений PIL.Image.
        
    Returns:
        bytes: PDF документ в виде байтов.
    '''
    if not images:
        raise ValueError("Список изображений пуст")

    # Размеры A4 в пунктах (1 пункт = 1/72 дюйма)
    a4_size_pt = pymupdf.paper_size("a4")  # Возвращает (ширина, высота) для A4 портретной ориентации

    pdf_doc = pymupdf.open()  # Создаем новый пустой PDF документ

    for img_pil in images:
        # Создаем новую страницу с заданными размерами A4 и ориентацией
        if img_pil.width > img_pil.height:
            page_width_pt, page_height_pt = a4_size_pt[1], a4_size_pt[0]
        else:
            page_width_pt, page_height_pt = a4_size_pt[0], a4_size_pt[1]
        
        page = pdf_doc.new_page(width=page_width_pt, height=page_height_pt)

        img_w_px = img_pil.width
        img_h_px = img_pil.height

        if img_w_px == 0 or img_h_px == 0:
            # Пропускаем пустое изображение, страница A4 останется пустой
            continue

        # Рассчитываем прямоугольник для вставки изображения на страницу PDF,
        # сохраняя пропорции изображения и центрируя его.
        
        # Масштабные коэффициенты по ширине и высоте
        scale_factor_w = page_width_pt / img_w_px
        scale_factor_h = page_height_pt / img_h_px
        
        # Используем наименьший коэффициент, чтобы изображение полностью поместилось
        scale_factor = min(scale_factor_w, scale_factor_h)
        
        # Размеры отрендеренного изображения на странице PDF
        render_w = img_w_px * scale_factor
        render_h = img_h_px * scale_factor
        
        # Смещения для центрирования изображения
        x_offset = (page_width_pt - render_w) / 2
        y_offset = (page_height_pt - render_h) / 2
        
        # Прямоугольник для вставки изображения на PDF странице
        image_rect_on_page = pymupdf.Rect(x_offset, y_offset, x_offset + render_w, y_offset + render_h)

        # Конвертируем PIL Image в байты PNG
        img_byte_io = BytesIO()
        img_pil.save(img_byte_io, format="JPEG", quality=85)
        img_byte_io.seek(0)
        
        # Вставляем изображение в рассчитанный прямоугольник
        page.insert_image(image_rect_on_page, stream=img_byte_io)

    # Сохраняем PDF в буфер BytesIO
    output_pdf_buffer = BytesIO()
    pdf_doc.save(output_pdf_buffer)
    pdf_bytes_result = output_pdf_buffer.getvalue()
    
    output_pdf_buffer.close() # Закрываем буфер
    pdf_doc.close()           # Закрываем документ PDF
    
    return pdf_bytes_result


def get_row_context(target_cell: Cell, all_tables: List[Table]) -> List[Cell]:
    """Получает все ячейки из той же строки для анализа контекста позиционирования."""
    target_table = None
    for table in all_tables:
        if target_cell in table.cells:
            target_table = table
            break
    
    if not target_table:
        return [target_cell]
    
    # Находим все ячейки в той же строке
    row_cells = [cell for cell in target_table.cells if cell.row == target_cell.row]
    return sorted(row_cells, key=lambda c: c.col)

def analyze_row_text_positioning(row_cells: List[Cell], target_cell: Cell) -> dict:
    """Анализирует позиционирование текста в строке для определения паттерна."""
    
    # Находим финансовые колонки (колонки с числовыми значениями)
    financial_cells = []
    for cell in row_cells:
        if cell != target_cell and cell.blobs and cell.text.strip():
            # Проверяем, содержит ли ячейка числовое значение
            import re
            if re.search(r'\d+(?:\s\d{3})*(?:,\d{1,2})?', cell.text):
                financial_cells.append(cell)
    
    if not financial_cells:
        # Если нет финансовых ячеек, анализируем все ячейки с текстом
        financial_cells = [cell for cell in row_cells if cell != target_cell and cell.blobs and cell.text.strip()]
    
    # Анализируем Y-позиции текста в финансовых ячейках
    text_y_positions = []
    baseline_infos = []
    
    for cell in financial_cells:
        if cell.blobs:
            # Вычисляем нижнюю границу текста (baseline) - это более стабильная метрика
            text_bottom = max(blob.y2 for blob in cell.blobs)
            cell_bottom = cell.bbox.y2
            
            # Расстояние от нижней границы ячейки до нижней границы текста
            distance_from_bottom = cell_bottom - text_bottom
            
            # Также сохраняем абсолютную позицию для выравнивания
            text_y_positions.append(text_bottom)
            baseline_infos.append({
                'cell': cell,
                'text_bottom': text_bottom,
                'distance_from_bottom': distance_from_bottom,
                'cell_height': cell.bbox.height
            })
    
    # Определяем консенсус позиционирования
    if baseline_infos:
        # Метод 1: Используем медианную позицию baseline
        text_y_positions.sort()
        median_y = text_y_positions[len(text_y_positions) // 2]
        
        # Метод 2: Используем среднее расстояние от нижней границы ячейки
        avg_distance_from_bottom = sum(info['distance_from_bottom'] for info in baseline_infos) / len(baseline_infos)
        
        return {
            'has_context': True,
            'median_text_y': median_y,
            'avg_distance_from_bottom': avg_distance_from_bottom,
            'sample_cells': baseline_infos[:3],  # Первые 3 для отладки
            'positioning_method': 'baseline_alignment'
        }
    
    return {
        'has_context': False,
        'positioning_method': 'center_fallback'
    }

def find_best_insertion_position(target_cell: Cell, new_text: str, font, 
                               positioning_info: dict, text_gap: int = 6) -> Tuple[int, int, str]:
    """
    Находит лучшую позицию для вставки нового текста с учетом существующих blobs.
    Возвращает (x, y, position_type) где position_type - описание выбранной позиции.
    """
    
    # Вычисляем размеры нового текста
    draw_temp = ImageDraw.Draw(Image.new('RGB', (100, 100)))
    text_bbox = draw_temp.textbbox((0, 0), new_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    cell_padding = 3
    
    # Если в ячейке нет текста, используем обычное позиционирование
    if not target_cell.blobs:
        if positioning_info['has_context']:
            # Используем контекстное выравнивание
            if positioning_info['positioning_method'] == 'baseline_alignment':
                target_text_bottom = positioning_info['median_text_y']
                text_y = int(target_text_bottom - text_height)
                
                # Проверяем границы ячейки
                if text_y < target_cell.bbox.y1 + cell_padding:
                    target_text_bottom = target_cell.bbox.y2 - positioning_info['avg_distance_from_bottom']
                    text_y = int(target_text_bottom - text_height)
            else:
                # Fallback к центрированию
                cell_center_y = (target_cell.bbox.y1 + target_cell.bbox.y2) / 2
                text_y = int(cell_center_y - text_height / 2)
        else:
            # Центрируем в пустой ячейке
            cell_center_y = (target_cell.bbox.y1 + target_cell.bbox.y2) / 2
            text_y = int(cell_center_y - text_height / 2)
        
        # X по центру
        cell_center_x = (target_cell.bbox.x1 + target_cell.bbox.x2) / 2
        text_x = int(cell_center_x - text_width / 2)
        
        return text_x, text_y, "empty_cell"
    
    # Если есть существующий текст, найдем место с отступом
    existing_blobs = target_cell.blobs
    
    # Вычисляем занятые области
    min_blob_y = min(blob.y1 for blob in existing_blobs)
    max_blob_y = max(blob.y2 for blob in existing_blobs)
    min_blob_x = min(blob.x1 for blob in existing_blobs)
    max_blob_x = max(blob.x2 for blob in existing_blobs)
    
    # Возможные позиции для размещения (в порядке приоритета)
    positions_to_try = []
    
    # 1. Под существующим текстом (приоритет 1)
    bottom_y = max_blob_y + text_gap
    if bottom_y + text_height <= target_cell.bbox.y2 - cell_padding:
        cell_center_x = (target_cell.bbox.x1 + target_cell.bbox.x2) / 2
        text_x = int(cell_center_x - text_width / 2)
        positions_to_try.append((text_x, bottom_y, "below_existing"))
    
    # 2. Над существующим текстом (приоритет 2)
    top_y = min_blob_y - text_gap - text_height
    if top_y >= target_cell.bbox.y1 + cell_padding:
        cell_center_x = (target_cell.bbox.x1 + target_cell.bbox.x2) / 2
        text_x = int(cell_center_x - text_width / 2)
        positions_to_try.append((text_x, top_y, "above_existing"))
    
    # 3. Справа от существующего текста (приоритет 3)
    right_x = max_blob_x + text_gap
    if right_x + text_width <= target_cell.bbox.x2 - cell_padding:
        # Выравниваем по baseline с существующим текстом
        if positioning_info['has_context']:
            target_text_bottom = positioning_info['median_text_y']
            text_y = int(target_text_bottom - text_height)
        else:
            # Выравниваем по центру существующего текста
            existing_center_y = (min_blob_y + max_blob_y) / 2
            text_y = int(existing_center_y - text_height / 2)
        positions_to_try.append((right_x, text_y, "right_of_existing"))
    
    # 4. Слева от существующего текста (приоритет 4)
    left_x = min_blob_x - text_gap - text_width
    if left_x >= target_cell.bbox.x1 + cell_padding:
        # Выравниваем по baseline с существующим текстом
        if positioning_info['has_context']:
            target_text_bottom = positioning_info['median_text_y']
            text_y = int(target_text_bottom - text_height)
        else:
            existing_center_y = (min_blob_y + max_blob_y) / 2
            text_y = int(existing_center_y - text_height / 2)
        positions_to_try.append((left_x, text_y, "left_of_existing"))
    
    # Выбираем первую подходящую позицию
    for text_x, text_y, position_type in positions_to_try:
        # Проверяем финальные границы
        final_text_x = max(target_cell.bbox.x1 + cell_padding,
                          min(text_x, target_cell.bbox.x2 - text_width - cell_padding))
        final_text_y = max(target_cell.bbox.y1 + cell_padding,
                          min(text_y, target_cell.bbox.y2 - text_height - cell_padding))
        
        # Проверяем, что позиция не пересекается с существующими blobs
        new_text_rect = {
            'x1': final_text_x,
            'y1': final_text_y,
            'x2': final_text_x + text_width,
            'y2': final_text_y + text_height
        }
        
        has_overlap = False
        for blob in existing_blobs:
            if (new_text_rect['x1'] < blob.x2 + text_gap and 
                new_text_rect['x2'] > blob.x1 - text_gap and
                new_text_rect['y1'] < blob.y2 + text_gap and 
                new_text_rect['y2'] > blob.y1 - text_gap):
                has_overlap = True
                break
        
        if not has_overlap:
            return final_text_x, final_text_y, position_type
    
    # Если ничего не подошло, используем безопасную позицию внизу ячейки
    safe_y = target_cell.bbox.y2 - text_height - cell_padding
    safe_x = (target_cell.bbox.x1 + target_cell.bbox.x2 - text_width) // 2
    return safe_x, safe_y, "fallback_bottom"

def draw_text_to_cell_with_context(image: Image.Image, cell: Cell, new_text: str, 
                                 font_size: int, row_cells: List[Cell]) -> Image.Image:
    """Улучшенная версия draw_text_to_cell с учетом контекста строки и отступами от существующего текста."""
    
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default(font_size)

    # Анализируем позиционирование текста в строке
    positioning_info = analyze_row_text_positioning(row_cells, cell)
    
    # Зачеркиваем существующий текст в целевой ячейке
    if cell.has_text:
        for blob in cell.blobs:
            mid_y = blob.y1 + (blob.y2 - blob.y1) // 2
            draw.line([(blob.x1, mid_y), (blob.x2, mid_y)], fill="black", width=3)
    
    # Получаем размеры нового текста
    text_bbox_pil = draw.textbbox((0, 0), new_text, font=font)
    text_width = text_bbox_pil[2] - text_bbox_pil[0]
    text_height = text_bbox_pil[3] - text_bbox_pil[1]
    
    # Проверяем, помещается ли текст в ячейку
    padding = 5
    available_width = cell.bbox.width - 2 * padding
    available_height = cell.bbox.height - 2 * padding
    
    if text_width <= available_width and text_height <= available_height:
        # Находим оптимальную позицию с учетом существующего текста
        final_x, final_y, position_type = find_best_insertion_position(
            cell, new_text, font, positioning_info, text_gap=6
        )
        
        # Отладочное логирование
        if positioning_info['has_context']:
            print(f"DEBUG: Позиционирование с контекстом - method: {positioning_info['positioning_method']}, position: {position_type}")
            if 'median_text_y' in positioning_info:
                print(f"DEBUG: median_text_y: {positioning_info['median_text_y']}, final_y: {final_y}, position_type: {position_type}")
        else:
            print(f"DEBUG: Fallback позиционирование - final_y: {final_y}, position_type: {position_type}")
        
        draw.text((final_x, final_y), new_text, fill="black", font=font)
    
    return image

# Обратная совместимость - оставляем старую функцию
def draw_text_to_cell(image: Image.Image, cell: Cell, new_text: str, font_size: int = 24) -> Image.Image:
    """Оригинальная функция для обратной совместимости."""
    return draw_text_to_cell_with_context(image, cell, new_text, font_size, [cell])

def draw_comments_to_bottom_right(image: Image.Image, bbox_table: BBox, comments: str, font_size: int = 20) -> Image.Image:
    """Рисует комментарии в правом нижнем углу страницы."""
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default(font_size)

    # Получаем размеры комментариев
    text_bbox_pil = draw.textbbox((0, 0), comments, font=font)
    text_width = text_bbox_pil[2] - text_bbox_pil[0]
    text_height = text_bbox_pil[3] - text_bbox_pil[1]

    # Позиционируем текст в правом нижнем углу ячейки четверть от высоты страницы
    final_x = image.width - text_width - 10 
    final_y = (image.height - image.height // 4)
    # Опустим текст если наезжает на таблицу
    if bbox_table:
        if final_x < bbox_table.x2 and final_y < bbox_table.y2:
            final_y = bbox_table.y2 + 5
    draw.text((final_x, final_y), comments, fill="blue", font=font)
    return image