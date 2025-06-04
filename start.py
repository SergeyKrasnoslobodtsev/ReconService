import os
import sys
from pathlib import Path

# Добавляем путь к проекту в PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Главная функция запуска сервиса"""
    
    # Загружаем конфигурацию
    environment = os.getenv('ENVIRONMENT', 'development')
    from src.config import load_env_file
    load_env_file(f'.env.{environment}')
    
    # Получаем параметры из переменных окружения
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '8000'))
    workers = int(os.getenv('WORKERS', '1'))
    reload = os.getenv('RELOAD', 'false').lower() in ('true', '1', 'yes')
    log_level = os.getenv('LOG_LEVEL', 'info').lower()
    
    print(f"🚀 Запуск ReconService в режиме: {environment}")
    print(f"📡 Сервер: {host}:{port}")
    print(f"👥 Воркеры: {workers}")
    print(f"🔄 Автоперезагрузка: {'да' if reload else 'нет'}")
    
    # Запускаем сервер
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        workers=workers if not reload else 1,  # reload не работает с workers > 1
        reload=reload,
        log_level=log_level,
        access_log=True
    )

if __name__ == "__main__":
    main()