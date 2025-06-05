import os
from pathlib import Path
from typing import List, Tuple
from PIL import Image
from PIL.ImageDraw import ImageDraw
from PIL import ImageFont
import pymupdf
from pdf2image import convert_from_path


# ---- настройка имён -----------------------------------------------------------
SCAN_PDF_NAME = "scan_v1.pdf"          # ожидаем True (скан)
STRUCTURED_PDF_NAME = "АСР СДД 2 кв.2024 (подп. к-а).pdf"  # ожидаем False (цифровой)
# ------------------------------------------------------------------------------

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent.parent
PDF_DIR = PROJECT_ROOT / "pdf"

SCAN_PDF = PDF_DIR / SCAN_PDF_NAME
STRUCTURED_PDF = PDF_DIR / STRUCTURED_PDF_NAME

def get_pdf_structure():
    return _read_pdf_bytes(STRUCTURED_PDF)

def get_pdf_scan():
    return _read_pdf_bytes(SCAN_PDF)

def _read_pdf_bytes(pdf_path: Path) -> bytes:
    """Читает файл и возвращает его содержимое в виде bytes."""
    assert pdf_path.exists(), f"Файл {pdf_path} не найден"
    return pdf_path.read_bytes()

def convert_to_pil(pdf_bytes: bytes) -> List[Image.Image]:
    """Convert bytes to PIL image

    Args:
        pdf_bytes (bytes): bytes file pdf

    Returns:
        List[Image]: List PIL images
    """
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = pix.pil_image()
        pages.append(img)
    return pages

def load_document_pdf() -> List[Image.Image]:
    """Загружает страницы из PDF-файла SCAN_PDF в виде списка изображений PIL."""
    images = convert_from_path(str(SCAN_PDF.resolve()), dpi=300)
    return images

def draw_label(draw: ImageDraw, text: str, position: Tuple[int, int]) -> ImageDraw:
    position = (position[0] + 5, position[1] - 35)
    font = ImageFont.truetype("arial.ttf", 24)
    bbox = draw.textbbox(position, text, font=font)
    padded_bbox = (bbox[0]-5, bbox[1]-5, bbox[2]+5, bbox[3]+5)
    draw.rectangle(padded_bbox, fill="blue")
    draw.text(position, text, font=font, fill='white')
    return draw