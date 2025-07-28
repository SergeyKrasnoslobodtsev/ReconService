"""
Базовые исключения для ReconService v2

Иерархия исключений для единообразной обработки ошибок
"""

from typing import Optional, Dict, Any


class ReconServiceError(Exception):
    """Базовое исключение для всех ошибок ReconService"""
    
    def __init__(
        self, 
        message: str,
        details: Optional[Dict[str, Any]] = None,
        code: Optional[str] = None
    ):
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.code = code or self.__class__.__name__
    
    def __str__(self) -> str:
        return f"{self.code}: {self.message}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь для API ответов"""
        return {
            "error": self.code,
            "message": self.message,
            "details": self.details
        }


class BusinessLogicError(ReconServiceError):
    """Ошибки бизнес-логики"""
    pass


class ValidationError(ReconServiceError):
    """Ошибки валидации входных данных"""
    pass


class TechnicalError(ReconServiceError):
    """Технические ошибки системы"""
    pass


class ExternalServiceError(TechnicalError):
    """Ошибки внешних сервисов"""
    pass


class ConfigurationError(TechnicalError):
    """Ошибки конфигурации"""
    pass
