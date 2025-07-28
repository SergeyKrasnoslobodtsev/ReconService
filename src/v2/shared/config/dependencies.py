"""
Dependency Injection контейнер для ReconService v2

Простая система управления зависимостями без внешних библиотек
"""

from functools import lru_cache
from dataclasses import dataclass
from typing import Optional

from ..logging.logger import get_logger
from .settings import settings

logger = get_logger(__name__)


@dataclass
class Dependencies:
    """Контейнер для всех зависимостей приложения"""
    
    # Пока оставляем пустым, будем добавлять по мере создания компонентов
    pass


@lru_cache()
def get_dependencies() -> Dependencies:
    """
    Создает и возвращает контейнер зависимостей
    
    Returns:
        Настроенный контейнер зависимостей
    """
    logger.info("Инициализация контейнера зависимостей")
    
    # Здесь будем создавать все зависимости
    dependencies = Dependencies()
    
    logger.info("Контейнер зависимостей инициализирован")
    return dependencies


def setup_dependencies() -> Dependencies:
    """
    Настройка всех зависимостей приложения
    
    Returns:
        Настроенный контейнер зависимостей
    """
    logger.info("Настройка зависимостей приложения")
    
    # Создаем temp директорию если не существует
    settings.temp_path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Temp директория: {settings.temp_path}")
    
    return get_dependencies()
