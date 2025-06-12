from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class Period(BaseModel):
    """Период акта сверки"""
    from_date: str = Field(..., description="Дата начала периода")
    to_date: str = Field(..., description="Дата окончания периода")
    
    model_config = {
        "frozen": True
    }
    
    @field_validator('from_date', 'to_date')
    def validate_dates(cls, v):
        """Базовая валидация дат"""
        if not v or not v.strip():
            raise ValueError("Дата не может быть пустой")
        return v.strip()
    
    def is_valid(self) -> bool:
        """Проверяет валидность периода"""
        return self.from_date != "None" and self.to_date != "None"
    
    def to_api_dict(self) -> dict:
        """Преобразует в словарь для API ответа"""
        return {
            "from": self.from_date,
            "to": self.to_date
        }