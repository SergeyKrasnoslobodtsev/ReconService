from io import BytesIO
import pymupdf
from PIL import Image, ImageDraw, ImageFont

from dataclasses import dataclass
from typing import List, Tuple

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
        x_offset = page_width_pt - render_w  # вплотную вправо
        y_offset = page_height_pt - render_h  # вплотную вниз
        
        # Прямоугольник для вставки изображения на PDF странице
        image_rect_on_page = pymupdf.Rect(x_offset, y_offset, x_offset + render_w, y_offset + render_h)

        # Конвертируем PIL Image 
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

@dataclass
class PositioningContext:
    """Контекст позиционирования для строки таблицы."""
    has_financial_data: bool
    median_baseline_y: float
    avg_distance_from_bottom: float

def analyze_row_text_positioning(row_cells: List[Cell], target_cell: Cell) -> PositioningContext:
    """Анализирует позиционирование текста в строке."""
    import re
    
    # Находим ячейки с числовыми значениями (финансовые данные)
    financial_cells = [
        cell for cell in row_cells 
        if cell != target_cell 
        and cell.text
        and re.fullmatch(r'\s*\d+(?:\s\d{3})*(?:,\d{2})?\s*', cell.text.strip())
    ]
    
    if not financial_cells:
        return PositioningContext(
            has_financial_data=False,
            median_baseline_y=0,
            avg_distance_from_bottom=0
        )
    
    # Собираем baseline'ы текста
    baselines = []
    distances_from_bottom = []
    
    for cell in financial_cells:
        text_bottom = max(blob.y2 for blob in cell.blobs)
        baselines.append(text_bottom)
        distances_from_bottom.append(cell.bbox.y2 - text_bottom)
    
    baselines.sort()
    median_baseline = baselines[len(baselines) // 2]
    avg_distance = sum(distances_from_bottom) / len(distances_from_bottom)
    
    return PositioningContext(
        has_financial_data=True,
        median_baseline_y=median_baseline,
        avg_distance_from_bottom=avg_distance
    )

def calculate_text_position(cell: Cell, text_width: float, text_height: float, 
                          context: PositioningContext) -> Tuple[float, float]:
    """
    Вычисляет наилучшую позицию для нового текста в ячейке.
    Приоритеты размещения в занятой ячейке:
    1. СПРАВА от существующего текста
    2. СЛЕВА от существующего текста
    3. СНИЗУ от существующего текста
    4. СВЕРХУ от существующего текста
    5. ПО ЦЕНТРУ (fallback, если нигде нет места)
    
    Для пустой ячейки - центрирование с учетом контекста строки.
    """
    padding = 0
    
    # --- Если ячейка пуста ---
    if not cell.blobs:
        cell_center_x = (cell.bbox.x1 + cell.bbox.x2) / 2
        x = cell_center_x - text_width / 2
        
        if context.has_financial_data:
            y = context.median_baseline_y - text_height
            if y < cell.bbox.y1 + padding:
                y = cell.bbox.y2 - context.avg_distance_from_bottom - text_height
        else:
            cell_center_y = (cell.bbox.y1 + cell.bbox.y2) / 2
            y = cell_center_y - text_height / 2
        
        return x, y
    
    # --- Если ячейка занята, ищем свободное место ---
    existing_text_x1 = min(b.x1 for b in cell.blobs)
    existing_text_x2 = max(b.x2 for b in cell.blobs)
    existing_text_y1 = min(b.y1 for b in cell.blobs)
    existing_text_y2 = max(b.y2 for b in cell.blobs)
    
    # Вычисляем центр существующего текста для вертикального выравнивания
    existing_text_center_y = (existing_text_y1 + existing_text_y2) / 2
    
    # 1. Проверяем место СПРАВА (X: справа от текста, Y: выровнено по центру текста)
    space_right = cell.bbox.x2 - existing_text_x2 - padding * 2
    if text_width <= space_right:
        x = existing_text_x2 + padding
        y = existing_text_center_y - text_height / 2
        # Проверяем, что по Y тоже помещается
        if y >= cell.bbox.y1 and (y + text_height) <= cell.bbox.y2:
            return x, y
    
    # 2. Проверяем место СЛЕВА (X: слева от текста, Y: выровнено по центру текста)
    space_left = existing_text_x1 - cell.bbox.x1 - padding * 2
    if text_width <= space_left:
        x = existing_text_x1 - text_width - padding
        y = existing_text_center_y - text_height / 2
        # Проверяем, что по Y тоже помещается
        if y >= cell.bbox.y1 and (y + text_height) <= cell.bbox.y2:
            return x, y
    
    # Вычисляем центр существующего текста для горизонтального выравнивания
    existing_text_center_x = (existing_text_x1 + existing_text_x2) / 2
    
    # 3. Проверяем место СНИЗУ (Y: снизу от текста, X: выровнено по центру текста)
    space_bottom = cell.bbox.y2 - existing_text_y2 - padding * 2
    if text_height <= space_bottom:
        y = existing_text_y2 + padding
        x = existing_text_center_x - text_width / 2
        # Проверяем, что по X тоже помещается
        if x >= cell.bbox.x1 and (x + text_width) <= cell.bbox.x2:
            return x, y
    
    # 4. Проверяем место СВЕРХУ (Y: сверху от текста, X: выровнено по центру текста)
    space_top = existing_text_y1 - cell.bbox.y1 - padding * 2
    if text_height <= space_top:
        y = existing_text_y1 - text_height - padding
        x = existing_text_center_x - text_width / 2
        # Проверяем, что по X тоже помещается
        if x >= cell.bbox.x1 and (x + text_width) <= cell.bbox.x2:
            return x, y
    
    # 5. FALLBACK: Если нигде нет места, размещаем ПО ЦЕНТРУ существующего текста
    # (текст наложится, но это лучше, чем выход за границы)
    x = existing_text_center_x - text_width / 2
    y = existing_text_center_y - text_height / 2
    
    # Финальная проверка границ
    x = max(cell.bbox.x1, min(x, cell.bbox.x2 - text_width))
    y = max(cell.bbox.y1, min(y, cell.bbox.y2 - text_height))
    
    return x, y

def draw_text_to_cell_with_context(image: Image.Image, cell: Cell, new_text: str, 
                                 font_size: int, row_cells: List[Cell]) -> Image.Image:
    """Рисует текст в ячейке с учетом контекста строки."""
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default(font_size)
    
    # Зачеркиваем старый текст
    if cell.has_text:
        for blob in cell.blobs:
            mid_y = blob.y1 + (blob.y2 - blob.y1) // 2
            draw.line([(blob.x1, mid_y), (blob.x2, mid_y)], fill="black", width=3)
    
    # Получаем размеры текста
    _, top, _, bottom = font.getbbox(new_text)
    text_width = font.getlength(new_text)
    text_height = bottom - top
    
    # Анализируем контекст
    context = analyze_row_text_positioning(row_cells, cell)
    
    # Вычисляем позицию с учетом метрик шрифта
    x, y = calculate_text_position(cell, text_width, text_height, context)
    
    # Корректируем 'y' на основе 'top' из getbbox
    # y -= top

    # Рисуем текст
    draw.text((x, y), new_text, fill="black", font=font)
    
    return image


# Обратная совместимость - оставляем старую функцию
def draw_text_to_cell(image: Image.Image, cell: Cell, new_text: str, font_size: int = 24) -> Image.Image:
    """Оригинальная функция для обратной совместимости."""
    return draw_text_to_cell_with_context(image, cell, new_text, font_size, [cell])

def draw_comments_to_bottom_right(image: Image.Image, comments: str, font_size: int = 30, line_spacing: int = 0) -> Image.Image:
    """Рисует комментарии в правом нижнем углу страницы."""
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default(font_size)

    # Получаем размеры комментариев
    text_bbox_pil = draw.textbbox((0, 0), comments, font=font, spacing=line_spacing)
    text_width = text_bbox_pil[2] - text_bbox_pil[0]
    text_height = text_bbox_pil[3] - text_bbox_pil[1]
    
    # Позиционируем текст в правом нижнем углу ячейки четверть от высоты страницы
    final_x = image.width - text_width - 10 
    final_y = image.height - text_height - 10

    draw.multiline_text((final_x, final_y), comments, fill="blue", font=font, spacing=line_spacing)

    return image