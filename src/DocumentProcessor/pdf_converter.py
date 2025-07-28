from typing import List
import pymupdf
from PIL import Image
import logging

logger = logging.getLogger(__name__)


def convert_pdf_to_bytes(pdf_path: str) -> bytes:
    """
    Конвертирует PDF файл в байты
    
    Args:
        pdf_path: Путь к PDF файлу
        
    Returns:
        Содержимое PDF файла в байтах
    """
    try:
        with open(pdf_path, "rb") as f:
            content = f.read()
        logger.debug(f"PDF файл {pdf_path} успешно прочитан, размер: {len(content)} байт")
        return content
    except Exception as e:
        logger.error(f"Ошибка при чтении PDF файла {pdf_path}: {str(e)}")
        raise

def convert_bytes_to_pdf(pdf_bytes: bytes, output_path: str):
        """
        Сохраняет байты PDF в файл
        
        Args:
            pdf_bytes: Содержимое PDF в байтах
            output_path: Путь для сохранения PDF файла
        """
        try:
            with open(output_path, "wb") as f:
                f.write(pdf_bytes)
            logger.debug(f"PDF файл успешно сохранен по пути {output_path}")
        except Exception as e:
            logger.error(f"Ошибка при сохранении PDF файла {output_path}: {str(e)}")
            raise
        return output_path

def convert_pdf_to_images(pdf_bytes: bytes, dpi=400) -> List[Image.Image]:
        """
        Конвертирует PDF в список изображений
        
        Args:
            pdf_bytes: Содержимое PDF в байтах
            dpi: Разрешение для конвертации страниц PDF в изображения
            
        Returns:
            Список изображений
        """
        try:
            doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
            pages = []
            for page in doc:
                pix = page.get_pixmap(dpi=dpi)
                img = pix.pil_image()
                pages.append(img)
            doc.close()
            logger.debug(f"PDF успешно конвертирован в {len(pages)} изображений")
            return pages
        except Exception as e:
            logger.error(f"Ошибка при конвертации PDF в изображения: {str(e)}")
            raise