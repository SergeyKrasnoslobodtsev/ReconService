"""
Объект значения для организации (Pydantic модель как в оригинале)
"""

from pydantic import BaseModel, field_validator
from typing import Optional, Dict, Any


class Organization(BaseModel):
    """Организация - как в оригинальном коде с Pydantic"""
    
    name: str
    type: str  # Тип организации (ООО, АО и т.д.)
    role: str  # 'продавец' или 'покупатель'
    raw_data: Optional[Dict[str, Any]] = None
    
    model_config = {
        "frozen": True
    }
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        """Валидация роли как в оригинале"""
        allowed_roles = ['продавец', 'покупатель']
        if v not in allowed_roles:
            raise ValueError(f"Роль должна быть одной из: {allowed_roles}")
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Валидация названия как в оригинале"""
        if not v or not v.strip():
            raise ValueError("Название организации не может быть пустым")
        return v.strip()
    
    def is_seller(self) -> bool:
        """Как в оригинале"""
        return self.role == 'продавец'
    
    def is_buyer(self) -> bool:
        """Как в оригинале"""
        return self.role == 'покупатель'
    
    def to_string(self) -> str:
        """Возвращает строковое представление организации"""
        return f"{self.name}, {self.type}"
