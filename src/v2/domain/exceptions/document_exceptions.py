"""
Доменные исключения для документов
"""

from typing import Optional, Dict, Any

from ...shared.exceptions.base_exceptions import BusinessLogicError, TechnicalError


class DocumentError(BusinessLogicError):
    """Базовое исключение для ошибок документов"""
    pass


class DocumentProcessingError(DocumentError):
    """Ошибка обработки документа"""
    
    def __init__(self, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(f"Ошибка обработки документа: {reason}")
        self.reason = reason
        self.details = details or {}


class DocumentExtractionError(DocumentError):
    """Ошибка извлечения данных из документа"""
    
    def __init__(self, extraction_type: str, reason: str):
        super().__init__(f"Ошибка извлечения {extraction_type}: {reason}")
        self.extraction_type = extraction_type
        self.reason = reason


class InvalidDocumentFormatError(DocumentError):
    """Ошибка - неверный формат документа"""
    
    def __init__(self, expected_format: str, actual_format: str):
        super().__init__(
            f"Неверный формат документа. Ожидался '{expected_format}', получен '{actual_format}'"
        )
        self.expected_format = expected_format
        self.actual_format = actual_format


class DocumentNotReadableError(TechnicalError):
    """Ошибка - документ не читается"""
    
    def __init__(self, reason: str):
        super().__init__(f"Документ не может быть прочитан: {reason}")
        self.reason = reason


class DocumentFillingError(DocumentError):
    """Ошибка заполнения документа"""
    
    def __init__(self, reason: str, field: Optional[str] = None):
        message = f"Ошибка заполнения документа: {reason}"
        if field:
            message += f" (поле: {field})"
        super().__init__(message)
        self.reason = reason
        self.field = field
