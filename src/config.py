import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ServerConfig:
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = False
    workers: int = 1

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

@dataclass
class SecurityConfig:
    max_requests_per_minute: int = 60
    allowed_origins: list = None

@dataclass
class AppConfig:
    server: ServerConfig
    api: APIConfig
    processing: ProcessingConfig
    storage: StorageConfig
    ocr: OCRConfig
    security: SecurityConfig
    environment: str = "development"

class ConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self._config: Optional[AppConfig] = None
        
    def load_config(self, environment: Optional[str] = None) -> AppConfig:
        """Загружает конфигурацию для указанного окружения"""
        
        # Определяем окружение
        env = environment or os.getenv('ENVIRONMENT', 'development')
        
        # Загружаем базовую конфигурацию
        base_config = self._load_yaml_file("app_config.yaml")
        
        # Загружаем конфигурацию для окружения
        env_config_file = f"{env}.yaml"
        if (self.config_dir / env_config_file).exists():
            env_config = self._load_yaml_file(env_config_file)
            base_config = self._merge_configs(base_config, env_config)
        
        # Загружаем локальную конфигурацию (если есть)
        local_config_file = "local.yaml"
        if (self.config_dir / local_config_file).exists():
            local_config = self._load_yaml_file(local_config_file)
            base_config = self._merge_configs(base_config, local_config)
        
        # Переопределяем значения из переменных окружения
        base_config = self._override_from_env(base_config)
        
        # Создаем объект конфигурации
        self._config = self._create_config_object(base_config)
        
        # Создаем необходимые директории
        self._ensure_directories()
        
        return self._config
    
    def _load_yaml_file(self, filename: str) -> Dict[str, Any]:
        """Загружает YAML файл"""
        file_path = self.config_dir / filename
        if not file_path.exists():
            return {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Рекурсивно объединяет конфигурации"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _override_from_env(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Переопределяет значения из переменных окружения"""
        
        # Маппинг переменных окружения
        env_mappings = {
            'HOST': ('server', 'host'),
            'PORT': ('server', 'port'),
            'WORKERS': ('server', 'workers'),
            'MAX_WORKERS': ('processing', 'max_workers'),
            'TIMEOUT': ('processing', 'timeout'),
            'LOG_LEVEL': ('logging', 'level'),
            'ENVIRONMENT': ('environment',),
        }
        
        for env_var, config_path in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                # Устанавливаем значение в конфигурации
                current = config
                for key in config_path[:-1]:
                    if key not in current:
                        current[key] = {}
                    current = current[key]
                
                # Преобразуем тип
                if config_path[-1] in ['port', 'workers', 'max_workers', 'timeout']:
                    env_value = int(env_value)
                elif config_path[-1] in ['reload']:
                    env_value = env_value.lower() in ('true', '1', 'yes')
                
                current[config_path[-1]] = env_value
        
        return config
    
    def _create_config_object(self, config_dict: Dict[str, Any]) -> AppConfig:
        """Создает объект конфигурации из словаря"""
        
        return AppConfig(
            server=ServerConfig(**config_dict.get('server', {})),
            api=APIConfig(**config_dict.get('api', {})),
            processing=ProcessingConfig(**config_dict.get('processing', {})),
            storage=StorageConfig(**config_dict.get('storage', {})),
            ocr=OCRConfig(**config_dict.get('ocr', {})),
            security=SecurityConfig(
                allowed_origins=config_dict.get('security', {}).get('allowed_origins', ["*"]),
                **{k: v for k, v in config_dict.get('security', {}).items() if k != 'allowed_origins'}
            ),
            environment=config_dict.get('environment', 'development')
        )
    
    def _ensure_directories(self):
        """Создает необходимые директории"""
        if self._config:
            # Создаем директории для логов и временных файлов
            Path(self._config.storage.logs_dir).mkdir(exist_ok=True)
            Path(self._config.storage.temp_dir).mkdir(exist_ok=True)
    
    @property
    def config(self) -> AppConfig:
        """Получает текущую конфигурацию"""
        if self._config is None:
            self.load_config()
        return self._config

# Глобальный экземпляр менеджера конфигурации
config_manager = ConfigManager()