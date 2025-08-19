import asyncio
import logging
import threading
from typing import Optional, Dict
from datetime import datetime, timedelta

from ...domain.interfaces.process_repository import IProcessRepository
from ...domain.models.process import ReconciliationProcess
from ...domain.value_objects.process_id import ProcessId


class MemoryProcessRepository(IProcessRepository):
    """Репозиторий процессов в памяти с поддержкой синхронного доступа"""
    
    def __init__(self, ttl_hours: int = 24, cleanup_interval_hours: int = 1):
        self._storage: Dict[str, ReconciliationProcess] = {}
        # Используем threading.Lock для совместимости с синхронным кодом
        self._lock = threading.RLock()
        self._logger = logging.getLogger(f"app.{self.__class__.__name__}")
        self._ttl = timedelta(hours=ttl_hours)
        self._cleanup_interval = timedelta(hours=cleanup_interval_hours)
        self._shutdown_requested = False
        
        # Запускаем задачу очистки в отдельном потоке
        self._start_cleanup_task()
    
    async def save(self, process: ReconciliationProcess) -> None:
        """Сохраняет процесс"""
        with self._lock:
            self._storage[process.id.value] = process
        
        self._logger.debug(f"Сохранен процесс: {process.id}")
    
    async def get_by_id(self, process_id: ProcessId) -> Optional[ReconciliationProcess]:
        """Получает процесс по идентификатору"""
        with self._lock:
            return self._storage.get(process_id.value)
    
    async def update(self, process: ReconciliationProcess) -> None:
        """Обновляет существующий процесс"""
        with self._lock:
            if process.id.value in self._storage:
                self._storage[process.id.value] = process
                self._logger.debug(f"Обновлен процесс: {process.id}")
            else:
                raise ValueError(f"Процесс не найден для обновления: {process.id}")
    
    async def delete(self, process_id: ProcessId) -> bool:
        """Удаляет процесс"""
        with self._lock:
            if process_id.value in self._storage:
                del self._storage[process_id.value]
                self._logger.debug(f"Удален процесс: {process_id}")
                return True
            return False
    
    async def cleanup_expired(self, ttl: timedelta) -> int:
        """Удаляет истекшие процессы"""
        current_time = datetime.now()
        expired_ids = []
        
        with self._lock:
            for process_id, process in self._storage.items():
                if current_time - process.created_at > ttl:
                    expired_ids.append(process_id)
            
            for process_id in expired_ids:
                del self._storage[process_id]
        
        if expired_ids:
            for id in expired_ids:
                self._logger.info(f"Процесс {id} удален по истекшему времени жизненного цикла")
        
        return len(expired_ids)
    
    async def get_count(self) -> int:
        """Возвращает количество процессов"""
        with self._lock:
            return len(self._storage)
    
    def _start_cleanup_task(self) -> None:
        """Запускает задачу очистки в отдельном потоке"""
        def cleanup_worker():
            while not self._shutdown_requested:
                try:
                    import time
                    time.sleep(self._cleanup_interval.total_seconds())
                    if not self._shutdown_requested:
                        # Выполняем очистку синхронно
                        asyncio.run(self.cleanup_expired(self._ttl))
                except Exception as e:
                    self._logger.error(f"Ошибка в задаче очистки: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True, name="ProcessCleanup")
        cleanup_thread.start()
        self._logger.info(f"Запущена задача очистки (TTL: {self._ttl.total_seconds()}s)")
    
    async def shutdown(self) -> None:
        """Останавливает репозиторий"""
        self._shutdown_requested = True
        self._logger.info("Репозиторий остановлен")