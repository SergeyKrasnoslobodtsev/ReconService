import json
import logging.config
import os
from pydantic import BaseModel
import yaml
from pathlib import Path
from dataclasses import dataclass

class APIConfig(BaseModel):
    title: str
    description: str 
    version: str 
class ServiceConfig(BaseModel):
    process_ttl_hours: int 
    cleanup_interval_hours: float 
    max_workers: int 
class OCRConfig(BaseModel):
    engine: str 
    language: str
    tessdata_dir: str 
    psm: int 
    max_workers: int 
    dpi_image: int 
class AppConfig(BaseModel):
    api: APIConfig
    service: ServiceConfig
    ocr: OCRConfig

def load_config(config_path: str = "./config/app_config.yaml"):
    """Загружает конфигурацию из файла с переопределением через ENV"""
    
    # Загружаем базовую конфигурацию
    config_data = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f) or {}
    return AppConfig(
        api=APIConfig(**config_data.get("api", {})),
        service=ServiceConfig(**config_data.get("service", {})),
        ocr=OCRConfig(**config_data.get("ocr", {}))
    )

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

