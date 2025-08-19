from abc import ABC, abstractmethod
from ..dto.process_dto import DocumentProcessingResultDto


class IDocumentProcessor(ABC):
    """Интерфейс процессора документов"""
    
    @abstractmethod
    async def process(self, pdf_bytes: bytes) -> DocumentProcessingResultDto:
        """Обрабатывает PDF документ и возвращает результат"""
        pass