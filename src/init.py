import logging
import logging.config
import os

import yaml

from pullenti.Sdk import Sdk

def logger_configure(config_path: str = "./config/logging.yaml"):
        with open(config_path, "rt", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        # Проходим по всем хэндлерам и создаём директории, если есть filename
        for handler in cfg.get("handlers", {}).values():
            filename = handler.get("filename")
            if filename:
                log_dir = os.path.dirname(filename) or "."
                os.makedirs(log_dir, exist_ok=True)

        # Наконец, применяем конфигурацию
        logging.config.dictConfig(cfg)

def InitializationPullenti():
    Sdk.initialize_all()

class ServiceInitialize:
    @staticmethod
    def initialize() -> None:
        logger_configure()
        InitializationPullenti()

    