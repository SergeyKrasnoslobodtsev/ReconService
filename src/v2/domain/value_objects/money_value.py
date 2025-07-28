"""
Value Objects для полей записи акта сверки (Pydantic модели)
"""

from pydantic import BaseModel, field_validator
from typing import Optional


class MoneyValue(BaseModel):
    """Денежное значение - Value Object"""
    
    amount: float
    
    model_config = {
        "frozen": True
    }
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError("Денежное значение не может быть отрицательным")
        return v
    
    def __str__(self) -> str:
        return f"{self.amount:.2f}"


class OperationDate(BaseModel):
    """Дата операции - Value Object"""
    
    value: Optional[str] = None
    
    model_config = {
        "frozen": True
    }
    
    def is_empty(self) -> bool:
        return self.value is None or self.value.strip() == ""
    
    def __str__(self) -> str:
        return self.value or "без даты"


class OperationRecord(BaseModel):
    """Описание операции - Value Object"""
    
    text: str
    
    model_config = {
        "frozen": True
    }
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Описание операции не может быть пустым")
        return v.strip()
    
    def __str__(self) -> str:
        return self.text
