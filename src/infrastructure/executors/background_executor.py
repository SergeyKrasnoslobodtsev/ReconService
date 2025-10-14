import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any, Awaitable

from ...application.interfaces.background_executor import IBackgroundExecutor


class ThreadPoolBackgroundExecutor(IBackgroundExecutor):
    """Исполнитель фоновых задач на основе ThreadPoolExecutor"""
    
    def __init__(self, max_workers: int = 4):
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._logger = logging.getLogger(f"app.{self.__class__.__name__}")
        self._loop = None
        self._logger.info(f"Инициализирован ThreadPoolBackgroundExecutor с {max_workers} воркерами")
    
    async def submit(self, func: Callable[..., Awaitable[None]], *args: Any) -> None:
        """Запускает асинхронную функцию в фоновом режиме"""
        
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        
        def run_async_in_thread():
            """Обертка для запуска асинхронной функции в отдельном потоке"""
            try:
                # Создаем новый event loop для потока
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                
                # Запускаем асинхронную функцию
                new_loop.run_until_complete(func(*args))
                
            except Exception as e:
                self._logger.exception(f"Ошибка в фоновой задаче: {e}")
            finally:
                # Закрываем loop
                try:
                    new_loop.close()
                except Exception as e:
                    self._logger.warning(f"Ошибка при закрытии event loop: {e}")
        
        # Отправляем задачу в ThreadPoolExecutor
        self._executor.submit(run_async_in_thread)
        self._logger.debug("Фоновая задача отправлена в пул потоков")
    
    async def shutdown(self) -> None:
        """Останавливает исполнитель"""
        self._logger.info("Остановка ThreadPoolBackgroundExecutor...")
        self._executor.shutdown(wait=True)
        self._logger.info("ThreadPoolBackgroundExecutor остановлен")