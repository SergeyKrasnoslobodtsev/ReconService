import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class APIConfig:
    title: str = "Reconciliation Act Service API"
    description: str = "API для обработки актов сверки"
    version: str = "1.0.0"
    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"

@dataclass
class ProcessingConfig:
    max_workers: int = 4
    timeout: int = 300
    max_file_size: int = 52428800

@dataclass
class StorageConfig:
    temp_dir: str = "temp"
    logs_dir: str = "logs"
    cleanup_interval: int = 3600
    max_storage_time: int = 86400

@dataclass
class OCRConfig:
    engine: str = "tesseract"
    language: str = "rus+eng"
    tessdata_dir: str = ""
    psm: int = 4
@dataclass
class SecurityConfig:
    max_requests_per_minute: int = 60
    allowed_origins: list = None

@dataclass
class AppConfig:
    api: APIConfig
    processing: ProcessingConfig
    storage: StorageConfig
    ocr: OCRConfig
    security: SecurityConfig
    environment: str = "development"

def load_env_file(env_file: str):
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
                if key not in os.environ:
                    os.environ[key] = value

def load_config(environment: Optional[str] = None) -> AppConfig:
    """Загружает конфигурацию"""
    env = environment or os.getenv('ENVIRONMENT', 'development')
    
    # Загружаем .env файл для окружения
    load_env_file(f'.env.{env}')
    load_env_file('.env.local')  # Локальные переопределения
    
    # Загружаем настройки приложения из YAML
    config_file = Path('config/app_config.yaml')
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f) or {}
    else:
        config_data = {}
    
    # Создаем конфигурацию
    app_config = AppConfig(
        api=APIConfig(**config_data.get('api', {})),
        processing=ProcessingConfig(**config_data.get('processing', {})),
        storage=StorageConfig(**config_data.get('storage', {})),
        ocr=OCRConfig(**config_data.get('ocr', {})),
        security=SecurityConfig(
            allowed_origins=config_data.get('security', {}).get('allowed_origins', ["*"]),
            **{k: v for k, v in config_data.get('security', {}).items() if k != 'allowed_origins'}
        )
    )
    
    # Создаем директории
    Path(app_config.storage.logs_dir).mkdir(exist_ok=True)
    Path(app_config.storage.temp_dir).mkdir(exist_ok=True)
    
    return app_config