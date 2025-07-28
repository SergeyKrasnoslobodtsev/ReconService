"""
Система логирования для ReconService v2

Обеспечивает структурированное логирование с настройками 
в зависимости от окружения
"""

import logging
import logging.config
import sys
from typing import Optional
from pathlib import Path


def setup_logging(
    level: str = "INFO",
    log_format: Optional[str] = None,
    log_file: Optional[str] = None
) -> None:
    """
    Настройка системы логирования
    
    Args:
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
        log_format: Формат сообщений
        log_file: Файл для записи логов (опционально)
    """
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Базовая конфигурация
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "default",
                "stream": sys.stdout
            }
        },
        "loggers": {
            "": {  # Root logger
                "level": level,
                "handlers": ["console"],
                "propagate": False
            },
            "v2": {  # Наше приложение
                "level": level,
                "handlers": ["console"],
                "propagate": False
            }
        }
    }
    
    # Добавляем файловый обработчик если указан файл
    if log_file:
        # Создаем директорию для логов если не существует
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logging_config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": level,
            "formatter": "detailed",
            "filename": log_file,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf-8"
        }
        
        # Добавляем файловый обработчик к логгерам
        logging_config["loggers"][""]["handlers"].append("file")
        logging_config["loggers"]["v2"]["handlers"].append("file")
    
    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """
    Получить логгер с указанным именем
    
    Args:
        name: Имя логгера (обычно __name__)
        
    Returns:
        Настроенный логгер
    """
    return logging.getLogger(f"v2.{name}")


# Настройка по умолчанию при импорте модуля
try:
    from ..config.settings import settings
    setup_logging(
        level=settings.log_level,
        log_format=settings.log_format,
        log_file="logs/v2.log" if not settings.is_development else None
    )
except ImportError:
    # Если настройки недоступны, используем базовую конфигурацию
    setup_logging(level="INFO")
