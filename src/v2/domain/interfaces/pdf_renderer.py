"""
Интерфейс для рендеринга PDF документов
"""
from abc import ABC, abstractmethod
from typing import List
from PIL import Image

from ...domain.entities.document import Document, Cell


class IPDFRenderingService(ABC):
    """Интерфейс сервиса рендеринга PDF"""
    
    @abstractmethod
    async def convert_to_images(self, pdf_bytes: bytes) -> List[Image.Image]:
        """
        Конвертирует PDF в список изображений
        
        Args:
            pdf_bytes: Байты PDF документа
            
        Returns:
            List[Image.Image]: Список изображений страниц
        """
        pass
    
    @abstractmethod
    async def convert_to_pdf(self, images: List[Image.Image]) -> bytes:
        """
        Конвертирует список изображений обратно в PDF
        
        Args:
            images: Список изображений страниц
            
        Returns:
            bytes: PDF документ в байтах
        """
        pass
    
    @abstractmethod
    async def fill_cell(
        self, 
        image: Image.Image, 
        cell: Cell, 
        text: str,
        font_size: int = 24,
        context_cells: List[Cell] = None
    ) -> Image.Image:
        """
        Заполняет ячейку текстом на изображении
        
        Args:
            image: Изображение страницы
            cell: Ячейка для заполнения
            text: Текст для вставки
            font_size: Размер шрифта
            context_cells: Контекстные ячейки для выравнивания
            
        Returns:
            Image.Image: Изображение с заполненной ячейкой
        """
        pass
