"""
Утилиты для работы с файлами
"""

import os
import uuid
import asyncio
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta

from ..logging.logger import get_logger

logger = get_logger(__name__)


class FileUtils:
    """Утилиты для работы с файлами"""
    
    @staticmethod
    async def save_file(
        content: bytes, 
        directory: Path, 
        filename: Optional[str] = None,
        extension: str = ".pdf"
    ) -> str:
        """
        Сохраняет файл в указанную директорию
        
        Args:
            content: Содержимое файла в байтах
            directory: Директория для сохранения
            filename: Имя файла (если не указано, генерируется автоматически)
            extension: Расширение файла
            
        Returns:
            Полный путь к сохраненному файлу
        """
        # Создаем директорию если не существует
        directory.mkdir(parents=True, exist_ok=True)
        
        # Генерируем имя файла если не указано
        if filename is None:
            filename = f"{uuid.uuid4().hex[:12]}{extension}"
        elif not filename.endswith(extension):
            filename += extension
            
        file_path = directory / filename
        
        # Асинхронно сохраняем файл
        def _write_file():
            with open(file_path, "wb") as f:
                f.write(content)
                
        await asyncio.to_thread(_write_file)
        
        logger.debug(f"Файл сохранен: {file_path}")
        return str(file_path)
    
    @staticmethod
    async def load_file(file_path: str) -> bytes:
        """
        Загружает файл
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            Содержимое файла в байтах
        """
        def _read_file():
            with open(file_path, "rb") as f:
                return f.read()
                
        content = await asyncio.to_thread(_read_file)
        logger.debug(f"Файл загружен: {file_path}")
        return content
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Проверяет существование файла"""
        return Path(file_path).exists()
    
    @staticmethod
    async def delete_file(file_path: str) -> bool:
        """
        Удаляет файл
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            True если файл был удален, False если файла не было
        """
        path = Path(file_path)
        if path.exists():
            def _delete_file():
                path.unlink()
                
            await asyncio.to_thread(_delete_file)
            logger.debug(f"Файл удален: {file_path}")
            return True
        return False
    
    @staticmethod
    async def cleanup_old_files(
        directory: Path, 
        max_age_hours: int = 24,
        pattern: str = "*.pdf"
    ) -> int:
        """
        Очищает старые файлы в директории
        
        Args:
            directory: Директория для очистки
            max_age_hours: Максимальный возраст файлов в часах
            pattern: Паттерн файлов для удаления
            
        Returns:
            Количество удаленных файлов
        """
        if not directory.exists():
            return 0
            
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        deleted_count = 0
        
        def _cleanup():
            nonlocal deleted_count
            for file_path in directory.glob(pattern):
                try:
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_time:
                        file_path.unlink()
                        deleted_count += 1
                        logger.debug(f"Удален старый файл: {file_path}")
                except Exception as e:
                    logger.warning(f"Не удалось удалить файл {file_path}: {e}")
        
        await asyncio.to_thread(_cleanup)
        
        if deleted_count > 0:
            logger.info(f"Очищено {deleted_count} старых файлов из {directory}")
            
        return deleted_count
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Получает размер файла в байтах
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            Размер файла в байтах
        """
        return Path(file_path).stat().st_size
    
    @staticmethod
    def generate_unique_filename(prefix: str = "", extension: str = ".pdf") -> str:
        """
        Генерирует уникальное имя файла
        
        Args:
            prefix: Префикс имени файла
            extension: Расширение файла
            
        Returns:
            Уникальное имя файла
        """
        unique_id = uuid.uuid4().hex[:12]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if prefix:
            return f"{prefix}_{timestamp}_{unique_id}{extension}"
        else:
            return f"{timestamp}_{unique_id}{extension}"
