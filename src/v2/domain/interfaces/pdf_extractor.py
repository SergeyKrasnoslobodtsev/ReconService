"""
Базовый интерфейс для экстрактора PDF документов
"""
from abc import ABC, abstractmethod
from typing import Protocol

from ...domain.entities.document import Document


class PDFExtractor(Protocol):
    """Протокол для экстракторов PDF документов"""
    
    def extract(self, pdf_bytes: bytes) -> Document:
        """
        Извлекает структуру документа из PDF байтов
        
        Args:
            pdf_bytes: Байты PDF документа
            
        Returns:
            Document: Структурированное представление документа
        """
        ...


class IPDFExtractionService(ABC):
    """Интерфейс сервиса извлечения данных из PDF"""
    
    @abstractmethod
    async def extract_document(self, pdf_bytes: bytes) -> Document:
        """
        Извлекает структуру документа из PDF
        
        Args:
            pdf_bytes: Байты PDF документа
            
        Returns:
            Document: Извлеченная структура документа
        """
        pass
