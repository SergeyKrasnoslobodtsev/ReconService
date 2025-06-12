from abc import ABC, abstractmethod
from typing import Optional
from datetime import timedelta

from ..models.process import ReconciliationProcess
from ..value_objects.process_id import ProcessId


class IProcessRepository(ABC):
    """Интерфейс репозитория для процессов обработки"""
    
    @abstractmethod
    async def save(self, process: ReconciliationProcess) -> None:
        """Сохраняет процесс"""
        pass
    
    @abstractmethod
    async def get_by_id(self, process_id: ProcessId) -> Optional[ReconciliationProcess]:
        """Получает процесс по идентификатору"""
        pass
    
    @abstractmethod
    async def update(self, process: ReconciliationProcess) -> None:
        """Обновляет существующий процесс"""
        pass
    
    @abstractmethod
    async def delete(self, process_id: ProcessId) -> bool:
        """Удаляет процесс"""
        pass
    
    @abstractmethod
    async def cleanup_expired(self, ttl: timedelta) -> int:
        """Удаляет истекшие процессы"""
        pass
    
    @abstractmethod
    async def get_count(self) -> int:
        """Возвращает количество процессов"""
        pass