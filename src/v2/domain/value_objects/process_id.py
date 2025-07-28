"""
Объект значения для ID процесса (Pydantic модель)
"""

import uuid
from pydantic import BaseModel, field_validator
from typing import Union


class ProcessId(BaseModel):
    """Уникальный идентификатор процесса"""
    
    value: str
    
    model_config = {
        "frozen": True
    }
    
    @field_validator('value')
    @classmethod
    def validate_process_id(cls, v):
        """Валидация ID процесса"""
        if not v:
            raise ValueError("ID процесса не может быть пустым")
        
        if not isinstance(v, str):
            raise ValueError("ID процесса должен быть строкой")
        
        # Проверяем формат UUID
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError("Неверный формат ID процесса")
        
        return v
    
    @classmethod
    def generate(cls) -> 'ProcessId':
        """Генерирует новый уникальный ID процесса"""
        return cls(value=str(uuid.uuid4()))
    
    @classmethod
    def from_string(cls, value: Union[str, 'ProcessId']) -> 'ProcessId':
        """Создает ProcessId из строки или возвращает существующий"""
        if isinstance(value, ProcessId):
            return value
        return cls(value=value)
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"ProcessId('{self.value}')"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, ProcessId):
            return self.value == other.value
        if isinstance(other, str):
            return self.value == other
        return False
    
    def __hash__(self) -> int:
        return hash(self.value)
