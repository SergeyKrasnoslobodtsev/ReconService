from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, Optional


class Organization(BaseModel):
    """Организация (продавец или покупатель)"""
    name: str = Field(..., min_length=1, description="Название организации")
    role: str = Field(..., description="Роль организации")
    raw_data: Optional[Dict[str, Any]] = Field(default=None, description="Сырые данные организации")
    
    model_config = {
        "frozen": True
    }
    
    @field_validator('role')
    def validate_role(cls, v):
        """Валидация роли организации"""
        allowed_roles = ['продавец', 'покупатель']
        if v not in allowed_roles:
            raise ValueError(f"Роль должна быть одной из: {allowed_roles}")
        return v
    
    @field_validator('name')
    def validate_name(cls, v):
        """Валидация названия организации"""
        if not v or not v.strip():
            raise ValueError("Название организации не может быть пустым")
        return v.strip()
    
    def is_seller(self) -> bool:
        return self.role == 'продавец'
    
    def is_buyer(self) -> bool:
        return self.role == 'покупатель'