
from pathlib import Path
from typing import Tuple
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np

from src.DocumentProcessor.LayoutAnalisis.TableDetector.table import BBox
from src.DocumentProcessor.pdf_converter import convert_pdf_to_images
from src.DocumentProcessor.LayoutAnalisis.utils import convert_cv_to_pill

DIR_PDF = Path(__file__).resolve().parent.parent.parent / "pdf"

def load_document_pdf(file_num: int = 0) -> list[Image.Image]:
    """
    Загружает страницы из PDF-файла в виде списка изображений PIL.
    
    Args:
        file_num: Номер файла для загрузки (0 - первый, 1 - второй и т.д.)  
    Returns:
        Список изображений PIL, представляющих страницы PDF.
    """
    files = _get_files()
    if not files:
        raise FileNotFoundError("Нет доступных PDF файлов в директории.")
    
    if file_num >= len(files):
        raise IndexError(f"Файл с номером {file_num} не найден. Доступные файлы: {len(files)}.")
    
    pdf_path = files[file_num]
    images = convert_pdf_to_images(pdf_path.read_bytes(), 400)
    return images

def load_pdf_bytes(file_num: int = 0) -> bytes:
    """
    Загружает PDF-файл из тестовой директории в виде байтов.
    
    Args:
        file_num: Номер файла для загрузки (0 - первый, 1 - второй и т.д.)  
    Returns:
        Байты PDF-файла.
    """
    files = _get_files()
    if not files:
        raise FileNotFoundError("Нет доступных PDF файлов в директории.")
    
    if file_num >= len(files):
        raise IndexError(f"Файл с номером {file_num} не найден. Доступные файлы: {len(files)}.")
    
    pdf_path = files[file_num]
    return pdf_path.read_bytes()

def _get_files() -> list[Path]:
    """
    Получает список PDF файлов в директории DIR_PDF.
    
    Returns:
        Список путей к PDF файлам.
    """
    return list(DIR_PDF.glob("*.pdf"))


def _draw_label(draw: ImageDraw, text: str, position: Tuple[int, int]) -> ImageDraw:
    position = (position[0] + 5, position[1] - 35)
    font = ImageFont.truetype("arial.ttf", 24)
    bbox = draw.textbbox(position, text, font=font)
    padded_bbox = (bbox[0]-5, bbox[1]-5, bbox[2]+5, bbox[3]+5)
    draw.rectangle(padded_bbox, fill="blue")
    draw.text(position, text, font=font, fill='white')
    return draw

def draw_table(image: np.ndarray, tables: list[BBox]):
    
    pil_img = convert_cv_to_pill(image)

    draw = ImageDraw.Draw(pil_img)
    
    for id_t, item in enumerate(tables): 
        item: BBox = item
        draw = _draw_label(draw, f'Table: {id_t}', (item.x, item.y))
        draw.rectangle(item.pillow_bbox, outline='blue', width=3)
    
    return pil_img
    
             