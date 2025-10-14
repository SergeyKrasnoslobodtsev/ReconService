from pydantic import BaseModel, Field, field_validator
from typing import Optional


class RowIdentifier(BaseModel):
    """Идентификатор строки в таблице"""
    table_id: int = Field(..., ge=0, description="Номер таблицы")
    row_id: int = Field(..., ge=0, description="Номер строки")
    
    model_config = {
        "frozen": True
    }


class ActEntry(BaseModel):
    """Запись акта сверки (дебет или кредит)"""
    row_identifier: RowIdentifier
    record: str = Field(..., description="Описание операции")
    value: float = Field(..., ge=0, description="Значение записи")
    date: Optional[str] = Field(default=None, description="Дата операции")
    
    model_config = {
        "frozen": True
    }
    
    @field_validator('record')
    def validate_record(cls, v):
        """Валидация описания операции"""
        if not v or not v.strip():
            raise ValueError("Описание операции не может быть пустым")
        return v.strip()
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ActEntry':
        """Создает ActEntry из словаря"""
        return cls(
            row_identifier=RowIdentifier(
                table_id=data.get('ner_table_idx', 0),
                row_id=data['ner_row_idx']
            ),
            record=str(data.get('record', '')),
            value=float(data.get('value', 0.0)),
            date=data.get('date')
        )
    
    def to_dict(self) -> dict:
        """Преобразует в словарь для API ответа"""
        return {
            "row_id": {
                "id_table": self.row_identifier.table_id,
                "id_row": self.row_identifier.row_id
            },
            "record": self.record,
            "value": self.value,
            "date": self.date
        }