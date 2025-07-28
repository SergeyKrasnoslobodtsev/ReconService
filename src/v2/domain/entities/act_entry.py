"""
Сущность записи акта сверки (Pydantic Entity)
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

from ..value_objects.money_value import MoneyValue, OperationDate, OperationRecord


class RowIdentifier(BaseModel):
    """Идентификатор строки в таблице"""
    table_id: int  # id_table
    row_id: int    # id_row
    
    model_config = {
        "frozen": True
    }
    
    def to_dict(self) -> Dict[str, int]:
        """Преобразует в словарь для API"""
        return {
            "id_table": self.table_id,
            "id_row": self.row_id
        }


class ActEntry(BaseModel):
    """Сущность записи акта сверки (Entity)"""
    
    row_identifier: RowIdentifier
    record: OperationRecord
    value: MoneyValue
    date: OperationDate
    
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ActEntry':
        """Создает ActEntry из словаря (как в оригинальном коде)"""
        return cls(
            row_identifier=RowIdentifier(
                table_id=data.get('ner_table_idx', 0),
                row_id=data['ner_row_idx']
            ),
            record=OperationRecord(text=str(data.get('record', ''))),
            value=MoneyValue(amount=float(data.get('value', 0.0))),
            date=OperationDate(value=data.get('date'))
        )
    
    @classmethod
    def from_api_request(cls, row_id_dict: dict, record: str, value: float, date: Optional[str] = None) -> 'ActEntry':
        """Создает ActEntry из данных API запроса"""
        return cls(
            row_identifier=RowIdentifier(
                table_id=row_id_dict.get('id_table', 0),
                row_id=row_id_dict.get('id_row', 0)
            ),
            record=OperationRecord(text=record),
            value=MoneyValue(amount=value),
            date=OperationDate(value=date)
        )
    
    def to_dict(self) -> dict:
        """Преобразует в словарь для API ответа - точно как в оригинале"""
        return {
            "row_id": self.row_identifier.to_dict(),
            "record": self.record.text,
            "value": self.value.amount,
            "date": self.date.value
        }
    
    def __str__(self) -> str:
        return f"{self.record}: {self.value} ({self.date})"
