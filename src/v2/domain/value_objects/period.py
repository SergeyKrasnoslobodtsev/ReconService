"""
Объект значения для периода (Pydantic модель как в оригинале)
"""

from pydantic import BaseModel, field_validator


class Period(BaseModel):
    """Период акта сверки - как в оригинальном API"""
    
    from_date: str  # Дата начала периода
    to_date: str    # Дата окончания периода
    
    model_config = {
        "frozen": True
    }
    
    @field_validator('from_date', 'to_date')
    @classmethod
    def validate_dates(cls, v):
        """Базовая валидация дат как в оригинале"""
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
    
    def __str__(self) -> str:
        return f"{self.from_date} - {self.to_date}"
