"""
Конфигурация приложения ReconService v2

Настройки загружаются из переменных окружения и .env файлов
"""

import os
from pydantic import BaseModel
from typing import Optional
from pathlib import Path


class Settings(BaseModel):
    """Настройки приложения"""
    
    # Настройки сервера
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    workers: int = 1
    
    # Настройки окружения
    environment: str = "development"
    
    # Настройки производительности
    max_ocr_workers: int = 4  # Максимум потоков для OCR
    file_cleanup_interval: int = 3600  # Очистка temp каждый час (сек)
    process_ttl_hours: int = 24  # Время жизни процесса в часах
    
    # Пути
    temp_dir: str = "temp"
    
    # Логирование
    log_level: str = "DEBUG"  # Будет переопределено в зависимости от environment
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Настройки API
    api_title: str = "ReconService API v2"
    api_description: str = "Сервис распознавания актов сверки"
    api_version: str = "2.0.0"
    
    # Настройки файлов
    max_file_size_mb: int = 50  # Максимальный размер PDF файла
    allowed_file_types: list[str] = ["application/pdf"]
    
    def __post_init__(self):
        """Пост-обработка настроек"""
        # Устанавливаем уровень логирования в зависимости от окружения
        if self.environment == "development":
            self.log_level = "DEBUG"
        elif self.environment == "production":
            self.log_level = "INFO"
        else:
            self.log_level = "WARNING"
    
    @property
    def temp_path(self) -> Path:
        """Путь к временной директории"""
        return Path(self.temp_dir)
    
    @property
    def is_development(self) -> bool:
        """Проверка, что окружение - разработка"""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Проверка, что окружение - продакшн"""
        return self.environment == "production"
    
    class Config:
        case_sensitive = False


def load_env_file(env_file: str) -> None:
    """Загружает переменные из .env файла"""
    env_path = Path(env_file)
    if not env_path.exists():
        return
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # Не переопределяем если переменная уже установлена
                if key.upper() not in os.environ:
                    os.environ[key.upper()] = value


def create_settings() -> Settings:
    """Создает экземпляр настроек с загрузкой из .env файлов"""
    
    # Определяем окружение
    environment = os.getenv('ENVIRONMENT', 'development')
    
    # Загружаем .env файл для текущего окружения
    env_file = f".env.{environment}"
    load_env_file(env_file)
    
    # Создаем настройки из переменных окружения
    settings_data = {
        'host': os.getenv('HOST', '127.0.0.1'),
        'port': int(os.getenv('PORT', '8000')),
        'reload': os.getenv('RELOAD', 'true').lower() == 'true',
        'workers': int(os.getenv('WORKERS', '1')),
        'environment': environment,
        'max_ocr_workers': int(os.getenv('MAX_OCR_WORKERS', '4')),
        'file_cleanup_interval': int(os.getenv('FILE_CLEANUP_INTERVAL', '3600')),
        'process_ttl_hours': int(os.getenv('PROCESS_TTL_HOURS', '24')),
        'temp_dir': os.getenv('TEMP_DIR', 'temp'),
        'log_level': os.getenv('LOG_LEVEL', 'DEBUG' if environment == 'development' else 'INFO'),
        'log_format': os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        'api_title': os.getenv('API_TITLE', 'ReconService API v2'),
        'api_description': os.getenv('API_DESCRIPTION', 'Сервис распознавания актов сверки'),
        'api_version': os.getenv('API_VERSION', '2.0.0'),
        'max_file_size_mb': int(os.getenv('MAX_FILE_SIZE_MB', '50')),
        'allowed_file_types': os.getenv('ALLOWED_FILE_TYPES', 'application/pdf').split(',')
    }
    
    return Settings(**settings_data)


# Глобальный экземпляр настроек
settings = create_settings()
