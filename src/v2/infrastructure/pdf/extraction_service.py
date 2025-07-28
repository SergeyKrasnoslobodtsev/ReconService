"""
Адаптеры для существующих PDF экстракторов
"""
import logging
from typing import List, Optional

from ....PDFExtractor.base_extractor import BaseExtractor as LegacyBaseExtractor
from ....PDFExtractor.scan_extractor import ScanExtractor as LegacyScanExtractor
from ....PDFExtractor.native_extractor import NativeExtractor as LegacyNativeExtractor

from ...domain.entities.document import (
    Document, Page, Table, Cell, Paragraph, BBox, 
    ParagraphType, InsertionPosition
)
from ...domain.interfaces.pdf_extractor import IPDFExtractionService
from ...shared.exceptions import ExtractionError


class DocumentMapper:
    """Маппер для преобразования структур документа"""
    
    @staticmethod
    def map_bbox(legacy_bbox) -> BBox:
        """Преобразует legacy BBox в v2 BBox"""
        return BBox(
            x1=float(legacy_bbox.x1),
            y1=float(legacy_bbox.y1),
            x2=float(legacy_bbox.x2),
            y2=float(legacy_bbox.y2)
        )
    
    @staticmethod
    def map_cell(legacy_cell) -> Cell:
        """Преобразует legacy Cell в v2 Cell"""
        blobs = []
        if hasattr(legacy_cell, 'blobs') and legacy_cell.blobs:
            blobs = [DocumentMapper.map_bbox(blob) for blob in legacy_cell.blobs]
        
        return Cell(
            bbox=DocumentMapper.map_bbox(legacy_cell.bbox),
            row=legacy_cell.row,
            col=legacy_cell.col,
            colspan=getattr(legacy_cell, 'colspan', 1),
            rowspan=getattr(legacy_cell, 'rowspan', 1),
            text=legacy_cell.text or "",
            blobs=blobs,
            original_page_num=getattr(legacy_cell, 'original_page_num', None)
        )
    
    @staticmethod
    def map_table(legacy_table) -> Table:
        """Преобразует legacy Table в v2 Table"""
        cells = []
        if legacy_table.cells:
            cells = [DocumentMapper.map_cell(cell) for cell in legacy_table.cells]
        
        return Table(
            bbox=DocumentMapper.map_bbox(legacy_table.bbox),
            cells=cells,
            start_page_num=getattr(legacy_table, 'start_page_num', 0)
        )
    
    @staticmethod
    def map_paragraph(legacy_paragraph) -> Paragraph:
        """Преобразует legacy Paragraph в v2 Paragraph"""
        # Определяем тип параграфа
        paragraph_type = ParagraphType.NONE
        if hasattr(legacy_paragraph, 'paragraph_type'):
            if legacy_paragraph.paragraph_type == "HEADER":
                paragraph_type = ParagraphType.HEADER
            elif legacy_paragraph.paragraph_type == "FOOTER":
                paragraph_type = ParagraphType.FOOTER
        
        return Paragraph(
            bbox=DocumentMapper.map_bbox(legacy_paragraph.bbox),
            text=legacy_paragraph.text,
            paragraph_type=paragraph_type,
            page_num=getattr(legacy_paragraph, 'page_num', None)
        )
    
    @staticmethod
    def map_page(legacy_page, page_num: int) -> Page:
        """Преобразует legacy Page в v2 Page"""
        tables = []
        if hasattr(legacy_page, 'tables') and legacy_page.tables:
            tables = [DocumentMapper.map_table(table) for table in legacy_page.tables]
        
        paragraphs = []
        if hasattr(legacy_page, 'paragraphs') and legacy_page.paragraphs:
            paragraphs = [DocumentMapper.map_paragraph(para) for para in legacy_page.paragraphs]
        
        # Создаем bbox страницы (если не существует в legacy)
        if hasattr(legacy_page, 'bbox'):
            page_bbox = DocumentMapper.map_bbox(legacy_page.bbox)
        else:
            # Создаем bbox на основе контента или используем стандартный A4
            page_bbox = BBox(x1=0, y1=0, x2=595, y2=842)  # A4 в пунктах
        
        return Page(
            bbox=page_bbox,
            tables=tables,
            paragraphs=paragraphs,
            num_page=page_num
        )
    
    @staticmethod
    def map_document(legacy_document) -> Document:
        """Преобразует legacy Document в v2 Document"""
        pages = []
        if hasattr(legacy_document, 'pages') and legacy_document.pages:
            for i, legacy_page in enumerate(legacy_document.pages):
                pages.append(DocumentMapper.map_page(legacy_page, i))
        
        return Document(
            pdf_bytes=legacy_document.pdf_bytes,
            pages=pages,
            page_count=len(pages)
        )


class BasePDFExtractionService(IPDFExtractionService):
    """Базовый адаптер для PDF экстракторов"""
    
    def __init__(self, legacy_extractor: LegacyBaseExtractor):
        self._legacy_extractor = legacy_extractor
        self._logger = logging.getLogger(f"v2.{self.__class__.__name__}")
    
    async def extract_document(self, pdf_bytes: bytes) -> Document:
        """Извлекает документ используя legacy экстрактор"""
        try:
            self._logger.debug(f"Начало извлечения документа, размер: {len(pdf_bytes)} байт")
            
            # Используем существующий экстрактор
            legacy_document = self._legacy_extractor.extract(pdf_bytes)
            
            self._logger.debug(f"Legacy экстрактор завершен, страниц: {len(legacy_document.pages)}")
            
            # Преобразуем в v2 структуру
            v2_document = DocumentMapper.map_document(legacy_document)
            
            self._logger.info(
                f"Документ извлечен: {v2_document.page_count} страниц, "
                f"{v2_document.total_tables} таблиц, {v2_document.total_paragraphs} параграфов"
            )
            
            return v2_document
            
        except Exception as e:
            self._logger.exception("Ошибка при извлечении документа")
            raise ExtractionError(f"Ошибка извлечения документа: {str(e)}") from e


class ScanPDFExtractionService(BasePDFExtractionService):
    """Сервис извлечения для сканированных PDF (OCR)"""
    
    def __init__(self):
        super().__init__(LegacyScanExtractor())
        self._logger = logging.getLogger("v2.ScanPDFExtractionService")


class NativePDFExtractionService(BasePDFExtractionService):
    """Сервис извлечения для нативных PDF"""
    
    def __init__(self):
        super().__init__(LegacyNativeExtractor())
        self._logger = logging.getLogger("v2.NativePDFExtractionService")


class AutoPDFExtractionService(IPDFExtractionService):
    """Автоматический выбор подходящего экстрактора"""
    
    def __init__(self):
        self._scan_service = ScanPDFExtractionService()
        self._native_service = NativePDFExtractionService()
        self._logger = logging.getLogger("v2.AutoPDFExtractionService")
    
    async def extract_document(self, pdf_bytes: bytes) -> Document:
        """
        Автоматически определяет тип PDF и использует подходящий экстрактор
        """
        try:
            self._logger.debug("Попытка извлечения нативным экстрактором")
            
            # Сначала пробуем нативный экстрактор
            try:
                document = await self._native_service.extract_document(pdf_bytes)
                
                # Проверяем качество извлечения
                if self._is_extraction_satisfactory(document):
                    self._logger.info("Использован нативный экстрактор")
                    return document
                else:
                    self._logger.debug("Нативное извлечение неудовлетворительно, переключаемся на OCR")
                    
            except Exception as e:
                self._logger.debug(f"Нативный экстрактор не сработал: {e}")
            
            # Используем OCR экстрактор как fallback
            self._logger.debug("Использование OCR экстрактора")
            document = await self._scan_service.extract_document(pdf_bytes)
            self._logger.info("Использован OCR экстрактор")
            return document
            
        except Exception as e:
            self._logger.exception("Ошибка при автоматическом извлечении")
            raise ExtractionError(f"Все экстракторы завершились ошибкой: {str(e)}") from e
    
    def _is_extraction_satisfactory(self, document: Document) -> bool:
        """Оценивает качество извлечения документа"""
        if document.is_empty:
            return False
        
        # Проверяем наличие таблиц с данными
        tables = document.get_all_tables()
        if not tables:
            return False
        
        # Проверяем наличие текста в ячейках
        cells_with_text = 0
        total_cells = 0
        
        for table in tables:
            for cell in table.cells:
                total_cells += 1
                if cell.has_text:
                    cells_with_text += 1
        
        if total_cells == 0:
            return False
        
        # Считаем удовлетворительным, если более 30% ячеек содержат текст
        text_ratio = cells_with_text / total_cells
        return text_ratio > 0.3
