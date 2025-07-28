"""
Утилиты для валидации
"""

import re
from typing import Any, List, Optional, Union
from pathlib import Path

from ..exceptions.base_exceptions import ValidationError


class ValidationUtils:
    """Утилиты для валидации данных"""
    
    @staticmethod
    def validate_process_id(process_id: str) -> str:
        """
        Валидация ID процесса
        
        Args:
            process_id: ID процесса для валидации
            
        Returns:
            Валидный ID процесса
            
        Raises:
            ValidationError: Если ID невалиден
        """
        if not process_id:
            raise ValidationError("ID процесса не может быть пустым")
        
        if not isinstance(process_id, str):
            raise ValidationError("ID процесса должен быть строкой")
        
        # Проверяем формат UUID
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        
        if not uuid_pattern.match(process_id):
            raise ValidationError("Неверный формат ID процесса")
        
        return process_id
    
    @staticmethod
    def validate_pdf_content(content: bytes, max_size_mb: int = 50) -> bytes:
        """
        Валидация PDF контента
        
        Args:
            content: Содержимое PDF файла
            max_size_mb: Максимальный размер в мегабайтах
            
        Returns:
            Валидный PDF контент
            
        Raises:
            ValidationError: Если контент невалиден
        """
        if not content:
            raise ValidationError("PDF контент не может быть пустым")
        
        if not isinstance(content, bytes):
            raise ValidationError("PDF контент должен быть в байтах")
        
        # Проверяем размер
        size_mb = len(content) / (1024 * 1024)
        if size_mb > max_size_mb:
            raise ValidationError(
                f"Размер файла ({size_mb:.1f}MB) превышает максимально допустимый ({max_size_mb}MB)"
            )
        
        # Проверяем PDF заголовок
        if not content.startswith(b'%PDF-'):
            raise ValidationError("Файл не является валидным PDF документом")
        
        return content
    
    @staticmethod
    def validate_file_path(file_path: str) -> str:
        """
        Валидация пути к файлу
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            Валидный путь к файлу
            
        Raises:
            ValidationError: Если путь невалиден
        """
        if not file_path:
            raise ValidationError("Путь к файлу не может быть пустым")
        
        if not isinstance(file_path, str):
            raise ValidationError("Путь к файлу должен быть строкой")
        
        path = Path(file_path)
        
        # Проверяем существование файла
        if not path.exists():
            raise ValidationError(f"Файл не найден: {file_path}")
        
        # Проверяем что это файл, а не директория
        if not path.is_file():
            raise ValidationError(f"Указанный путь не является файлом: {file_path}")
        
        return file_path
    
    @staticmethod
    def validate_non_empty_string(value: Any, field_name: str) -> str:
        """
        Валидация непустой строки
        
        Args:
            value: Значение для валидации
            field_name: Название поля для сообщения об ошибке
            
        Returns:
            Валидная строка
            
        Raises:
            ValidationError: Если значение невалидно
        """
        if value is None:
            raise ValidationError(f"Поле '{field_name}' не может быть None")
        
        if not isinstance(value, str):
            raise ValidationError(f"Поле '{field_name}' должно быть строкой")
        
        if not value.strip():
            raise ValidationError(f"Поле '{field_name}' не может быть пустым")
        
        return value.strip()
    
    @staticmethod
    def validate_positive_integer(value: Any, field_name: str) -> int:
        """
        Валидация положительного целого числа
        
        Args:
            value: Значение для валидации
            field_name: Название поля для сообщения об ошибке
            
        Returns:
            Валидное целое число
            
        Raises:
            ValidationError: Если значение невалидно
        """
        if value is None:
            raise ValidationError(f"Поле '{field_name}' не может быть None")
        
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Поле '{field_name}' должно быть целым числом")
        
        if int_value <= 0:
            raise ValidationError(f"Поле '{field_name}' должно быть положительным числом")
        
        return int_value
    
    @staticmethod
    def validate_list_not_empty(value: Any, field_name: str) -> List[Any]:
        """
        Валидация непустого списка
        
        Args:
            value: Значение для валидации
            field_name: Название поля для сообщения об ошибке
            
        Returns:
            Валидный список
            
        Raises:
            ValidationError: Если значение невалидно
        """
        if value is None:
            raise ValidationError(f"Поле '{field_name}' не может быть None")
        
        if not isinstance(value, list):
            raise ValidationError(f"Поле '{field_name}' должно быть списком")
        
        if not value:
            raise ValidationError(f"Поле '{field_name}' не может быть пустым списком")
        
        return value
    
    @staticmethod
    def validate_email(email: str) -> str:
        """
        Валидация email адреса
        
        Args:
            email: Email для валидации
            
        Returns:
            Валидный email
            
        Raises:
            ValidationError: Если email невалиден
        """
        if not email:
            raise ValidationError("Email не может быть пустым")
        
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        if not email_pattern.match(email):
            raise ValidationError("Неверный формат email адреса")
        
        return email.lower().strip()
