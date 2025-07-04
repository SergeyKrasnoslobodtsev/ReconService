import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pullenti.Sdk import Sdk

from ..presentation.route import ReconciliationController
from ..presentation.route_docs import create_docs_router
from ..infrastructure.factories.service_factory import ServiceFactory
from ..config import AppConfig, load_config


# Глобальные переменные для хранения сервисов
service_factory: ServiceFactory = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения"""
    global service_factory
    
    # Startup
    logger = logging.getLogger("app.lifespan")
    logger.info("Запуск приложения...")
    
    try:
        # Инициализация Pullenti SDK
        Sdk.initialize_all()
        logger.info("Pullenti SDK инициализирован")
        
        yield
        
    finally:
        # Shutdown
        logger.info("Завершение работы приложения...")
        if service_factory:
            await service_factory.shutdown()
        logger.info("Приложение остановлено")


def create_app(config: AppConfig) -> FastAPI:
    """Создает и настраивает FastAPI приложение с новой архитектурой"""
    global service_factory
    
    # Создаем фабрику сервисов
    service_factory = ServiceFactory(config)
    
    # Создаем FastAPI приложение
    app = FastAPI(
        lifespan=lifespan,
        title=config.api.title,
        description=config.api.description,
        version=config.api.version,
        docs_url=None, 
        redoc_url=None
    )
    
    # Настраиваем CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Статические файлы 
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
    except Exception:
        # Игнорируем, если папка static не существует
        pass
    
    # Создаем контроллер
    reconciliation_controller = ReconciliationController(
        create_process_use_case=service_factory.create_create_process_use_case(),
        get_process_status_use_case=service_factory.create_get_process_status_use_case(),
        fill_document_use_case=service_factory.create_fill_document_use_case()
    )
    docs_router = create_docs_router(app)
    # Подключаем роуты
    app.include_router(
        reconciliation_controller.router
    )
    app.include_router(docs_router)

    # # Добавляем роут для совместимости со старым API
    # app.include_router(
    #     reconciliation_controller.router,
    #     tags=["Legacy API"]  # Без префикса для обратной совместимости
    # )
    
    return app


def get_app() -> FastAPI:
    """Точка входа для uvicorn"""
    config = load_config()
    return create_app(config)


# Создаем приложение для uvicorn
app = get_app()