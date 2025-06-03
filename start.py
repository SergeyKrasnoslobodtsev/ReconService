import os
import sys
from pathlib import Path

# Добавляем путь к проекту в PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.config import config_manager
from src.main import create_app

def main():
    """Главная функция запуска сервиса"""
    
    # Загружаем конфигурацию
    environment = os.getenv('ENVIRONMENT', 'development')
    config = config_manager.load_config(environment)
    
    print(f"🚀 Запуск ReconService в режиме: {config.environment}")
    print(f"📡 Сервер: {config.server.host}:{config.server.port}")
    print(f"👥 Воркеры: {config.processing.max_workers}")
    print(f"📚 Документация: {config.api.docs_url or 'отключена'}")
    

    os.environ['_RECON_CONFIG_ENVIRONMENT'] = environment
    
    # Запускаем сервер
    import uvicorn
    if config.server.reload and config.environment == "development":
        # Режим разработки с автоперезагрузкой
        uvicorn.run(
            "src.main:app",  # Строка импорта вместо объекта
            host=config.server.host,
            port=config.server.port,
            reload=True,
            log_level="debug",
            access_log=True
        )
    else:
        # Продакшен режим
        from src.main import create_app
        app = create_app(config)
        
        uvicorn.run(
            app,
            host=config.server.host,
            port=config.server.port,
            reload=False,
            log_level="info" if config.environment == "production" else "debug",
            access_log=True
    )

if __name__ == "__main__":
    main()