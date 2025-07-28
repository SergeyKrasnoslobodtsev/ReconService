"""
Реализация сервиса рендеринга PDF с использованием существующего кода
"""
import logging
from typing import List
from PIL import Image

from ....pdf_renderer import (
    convert_to_pil, convert_to_bytes, 
    draw_text_to_cell_with_context, get_row_context
)
from ...domain.entities.document import Cell
from ...domain.interfaces.pdf_renderer import IPDFRenderingService
from ...shared.exceptions import RenderingError


class PDFRenderingService(IPDFRenderingService):
    """Реализация сервиса рендеринга PDF"""
    
    def __init__(self):
        self._logger = logging.getLogger("v2.PDFRenderingService")
    
    async def convert_to_images(self, pdf_bytes: bytes) -> List[Image.Image]:
        """Конвертирует PDF в список изображений"""
        try:
            self._logger.debug(f"Конвертация PDF в изображения, размер: {len(pdf_bytes)} байт")
            
            images = convert_to_pil(pdf_bytes)
            
            self._logger.debug(f"Конвертировано {len(images)} страниц")
            return images
            
        except Exception as e:
            self._logger.exception("Ошибка при конвертации PDF в изображения")
            raise RenderingError(f"Ошибка конвертации PDF в изображения: {str(e)}") from e
    
    async def convert_to_pdf(self, images: List[Image.Image]) -> bytes:
        """Конвертирует список изображений обратно в PDF"""
        try:
            self._logger.debug(f"Конвертация {len(images)} изображений в PDF")
            
            if not images:
                raise ValueError("Список изображений пуст")
            
            pdf_bytes = convert_to_bytes(images)
            
            self._logger.debug(f"Создан PDF размером {len(pdf_bytes)} байт")
            return pdf_bytes
            
        except Exception as e:
            self._logger.exception("Ошибка при конвертации изображений в PDF")
            raise RenderingError(f"Ошибка конвертации изображений в PDF: {str(e)}") from e
    
    async def fill_cell(
        self, 
        image: Image.Image, 
        cell: Cell, 
        text: str,
        font_size: int = 24,
        context_cells: List[Cell] = None
    ) -> Image.Image:
        """Заполняет ячейку текстом на изображении"""
        try:
            self._logger.debug(f"Заполнение ячейки [{cell.row}, {cell.col}] текстом: '{text[:20]}...'")
            
            # Преобразуем v2 структуры в legacy для совместимости
            legacy_cell = self._convert_cell_to_legacy(cell)
            legacy_context_cells = []
            
            if context_cells:
                legacy_context_cells = [self._convert_cell_to_legacy(c) for c in context_cells]
            else:
                legacy_context_cells = [legacy_cell]
            
            # Используем существующую функцию рендеринга
            filled_image = draw_text_to_cell_with_context(
                image=image,
                cell=legacy_cell,
                new_text=text,
                font_size=font_size,
                row_cells=legacy_context_cells
            )
            
            self._logger.debug(f"Ячейка [{cell.row}, {cell.col}] успешно заполнена")
            return filled_image
            
        except Exception as e:
            self._logger.exception(f"Ошибка при заполнении ячейки [{cell.row}, {cell.col}]")
            raise RenderingError(f"Ошибка заполнения ячейки: {str(e)}") from e
    
    def _convert_cell_to_legacy(self, cell: Cell):
        """Конвертирует v2 Cell в legacy Cell для совместимости"""
        # Импортируем legacy классы
        from ....PDFExtractor.base_extractor import Cell as LegacyCell, BBox as LegacyBBox
        
        # Создаем legacy bbox
        legacy_bbox = LegacyBBox(
            x1=cell.bbox.x1,
            y1=cell.bbox.y1,
            x2=cell.bbox.x2,
            y2=cell.bbox.y2
        )
        
        # Создаем legacy blobs
        legacy_blobs = []
        for blob in cell.blobs:
            legacy_blob = LegacyBBox(
                x1=blob.x1,
                y1=blob.y1,
                x2=blob.x2,
                y2=blob.y2
            )
            legacy_blobs.append(legacy_blob)
        
        # Создаем legacy cell
        legacy_cell = LegacyCell(
            bbox=legacy_bbox,
            row=cell.row,
            col=cell.col,
            colspan=cell.colspan,
            rowspan=cell.rowspan,
            text=cell.text,
            blobs=legacy_blobs
        )
        
        # Добавляем дополнительные атрибуты если есть
        if cell.original_page_num is not None:
            legacy_cell.original_page_num = cell.original_page_num
        
        return legacy_cell
