from abc import ABC, abstractmethod
from typing import Callable, Any


class IBackgroundExecutor(ABC):
    """Интерфейс для выполнения фоновых задач"""
    
    @abstractmethod
    async def submit(self, func: Callable, *args: Any) -> None:
        """Запускает функцию в фоновом режиме"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Останавливает исполнитель"""
        pass