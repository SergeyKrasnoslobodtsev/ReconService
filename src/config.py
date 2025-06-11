import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class APIConfig:
    title: str = "Reconciliation Act Service API"
    description: str = "API для обработки актов сверки"
    version: str = "1.0.0"

@dataclass
class ServiceConfig:
    process_ttl_hours: int = 1
    cleanup_interval_hours: float = 0.5
    max_workers: int = 1


@dataclass
class OCRConfig:
    engine: str = "tesseract"
    language: str = "rus+eng"
    tessdata_dir: str = ""
    psm: int = 4
    max_workers: int = 4
    dpi_image: int = 300


@dataclass
class AppConfig:
    api: APIConfig
    service: ServiceConfig
    ocr: OCRConfig

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

def load_config(config_path: str = "./config/config.yaml") -> AppConfig:
    """Загружает конфигурацию из файла с переопределением через ENV"""
    
    # Загружаем базовую конфигурацию
    config_data = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f) or {}
    
    # Создаем конфигурации с учетом ENV переменных
    api_config = APIConfig(
        title=os.getenv("API_TITLE", config_data.get("api", {}).get("title", "ReconService API")),
        description=os.getenv("API_DESCRIPTION", config_data.get("api", {}).get("description", "Сервис обработки актов сверки")),
        version=os.getenv("API_VERSION", config_data.get("api", {}).get("version", "1.0.0"))
    )
    
    service_config = ServiceConfig(
        process_ttl_hours=int(os.getenv("RECON_PROCESS_TTL_HOURS", config_data.get("service", {}).get("process_ttl_hours", 24))),
        cleanup_interval_hours=int(os.getenv("RECON_CLEANUP_INTERVAL_HOURS", config_data.get("service", {}).get("cleanup_interval_hours", 1))),
        max_workers=int(os.getenv("RECON_MAX_WORKERS", config_data.get("service", {}).get("max_workers", 4)))
    )
    
    ocr_config = OCRConfig(
        engine=os.getenv("OCR_ENGINE", config_data.get("ocr", {}).get("engine", "tesseract")),
        language=os.getenv("OCR_LANGUAGE", config_data.get("ocr", {}).get("language", "rus+eng")),
        tessdata_dir=os.getenv("OCR_TESSDATA_DIR", config_data.get("ocr", {}).get("tessdata_dir", "")),
        psm=int(os.getenv("OCR_PSM", config_data.get("ocr", {}).get("psm", 4))),
        max_workers=int(os.getenv("OCR_MAX_WORKERS", config_data.get("ocr", {}).get("max_workers", 4))),
        dpi_image=int(os.getenv("OCR_DPI_IMAGE", config_data.get("ocr", {}).get("dpi_image", 300)))
    )

    
    return AppConfig(
        api=api_config,
        service=service_config,
        ocr=ocr_config
    )