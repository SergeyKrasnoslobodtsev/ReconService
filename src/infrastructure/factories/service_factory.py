import logging

from ...application.use_case.fill_document import FillDocumentUseCase
from ...application.use_case.create_process import CreateProcessUseCase
from ...application.use_case.get_process_status import GetProcessStatusUseCase
from ...domain.interfaces.process_repository import IProcessRepository
from ...application.interfaces.document_processor import IDocumentProcessor
from ...application.interfaces.background_executor import IBackgroundExecutor
from ..repositories.memory_process import MemoryProcessRepository
from ..processors.document_processor import DocumentProcessor
from ..executors.background_executor import ThreadPoolBackgroundExecutor
from ...config import AppConfig


class ServiceFactory:
    """Фабрика для создания сервисов и их зависимостей"""
    
    def __init__(self, config: AppConfig):
        self._config = config
        self._logger = logging.getLogger(f"app.{self.__class__.__name__}")
        
        # Создаем инфраструктурные компоненты
        self._process_repository = self._create_process_repository()
        self._document_processor = self._create_document_processor()
        self._background_executor = self._create_background_executor()
        
        self._logger.info("ServiceFactory инициализирована")
    
    def _create_process_repository(self) -> IProcessRepository:
        """Создает репозиторий процессов"""
        return MemoryProcessRepository(
            ttl_hours=self._config.service.process_ttl_hours,
            cleanup_interval_hours=self._config.service.cleanup_interval_hours
        )
    
    def _create_document_processor(self) -> IDocumentProcessor:
        """Создает процессор документов"""
        return DocumentProcessor()
    
    def _create_background_executor(self) -> IBackgroundExecutor:
        """Создает исполнитель фоновых задач"""
        return ThreadPoolBackgroundExecutor(
            max_workers=self._config.service.max_workers
        )
    
    def create_create_process_use_case(self) -> CreateProcessUseCase:
        """Создает use case для создания процесса"""
        return CreateProcessUseCase(
            process_repository=self._process_repository,
            document_processor=self._document_processor,
            background_executor=self._background_executor
        )
    
    def create_get_process_status_use_case(self) -> GetProcessStatusUseCase:
        """Создает use case для получения статуса процесса"""
        return GetProcessStatusUseCase(
            process_repository=self._process_repository
        )
    
    def create_fill_document_use_case(self) -> FillDocumentUseCase:
        """Создает use case для заполнения документа"""
        return FillDocumentUseCase(
            process_repository=self._process_repository
        )
    
    def get_process_repository(self) -> IProcessRepository:
        """Возвращает репозиторий процессов"""
        return self._process_repository
    
    def get_document_processor(self) -> IDocumentProcessor:
        """Возвращает процессор документов"""
        return self._document_processor
    
    def get_background_executor(self) -> IBackgroundExecutor:
        """Возвращает исполнитель фоновых задач"""
        return self._background_executor
    
    async def shutdown(self) -> None:
        """Корректно останавливает все сервисы"""
        self._logger.info("Остановка всех сервисов...")
        
        try:
            await self._background_executor.shutdown()
        except Exception as e:
            self._logger.error(f"Ошибка при остановке background executor: {e}")
        
        try:
            await self._process_repository.shutdown()
        except Exception as e:
            self._logger.error(f"Ошибка при остановке repository: {e}")
        
        self._logger.info("Все сервисы остановлены")