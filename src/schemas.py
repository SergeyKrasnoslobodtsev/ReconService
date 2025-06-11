from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class ReconciliationAct(BaseModel):
    """Модель для работы с актами сверки (загрузка и возврат заполненного документа)."""
    document: str = Field(description="PDF документ в формате base64")

class ProcessIdResponse(BaseModel):
    """Ответ  с идентивикатором процесса обработки."""
    process_id: str = Field(description="Уникальный идентификатор процесса")

class ProcessStatus(Enum):
    """Статусы процесса обработки акта сверки."""
    WAIT = 0
    DONE = 1
    NOT_FOUND = -1
    ERROR = -2

class RowIdModel(BaseModel):
    """Идентификатор строки."""
    id_table: int = Field(description="Номер таблицы")
    id_row: int = Field(description="Номер строки")

class ActEntryModel(BaseModel):
    """Запись акта сверки с информацией о дебете или кредите."""
    row_id: RowIdModel = Field(description="Идентификатор строки")
    record: str = Field(description="Описание операции")
    value: float = Field(description="Сумма операции")
    date: str | None = Field(description="Дата операции")

class PeriodModel(BaseModel):
    """Период акта сверки."""
    from_date: str | None = Field(alias="from", description="Дата начала периода")
    to_date: str | None = Field(alias="to", description="Дата окончания периода")

    model_config = {
        "populate_by_name": True, 
        "from_attributes": True   
    }


class ReconciliationActResponse(BaseModel):
    """Ответ с данными извлеченными из акта сверки."""
    process_id: str = Field(description="Уникальный идентификатор процесса")
    status: int = Field(description="Статус обработки акта сверки")
    message: str = Field(description="Сообщение о статусе")
    seller: str = Field(description="Продавец")
    buyer: str = Field(description="Покупатель")
    period: PeriodModel = Field(description="Период акта сверки")
    debit: List[ActEntryModel] = Field(default_factory=list, description="Список записей дебета")
    credit: List[ActEntryModel] = Field(default_factory=list, description="Список записей кредита")

    model_config = {
        "from_attributes": True   
    }

class FillReconciliationActRequest(BaseModel):
    """Запрос для заполнения акта сверки данными о покупателе."""
    process_id: str = Field(description="Уникальный идентификатор процесса")
    debit: List[ActEntryModel] = Field(description="Список записей дебета")
    credit: List[ActEntryModel] = Field(description="Список записей кредита")


# Модель для запроса /process_status
class StatusRequest(BaseModel):
    """Запрос для получения статуса процесса обработки акта сверки."""
    process_id: str = Field(description="Уникальный идентификатор процесса")

class StatusResponse(BaseModel): # Общая модель для статусов WAIT, ERROR, NOT_FOUND
    """Ответ с информацией о статусе процесса."""
    status: int = Field(description="Статус процесса")
    message: str = Field(description="Сообщение о статусе")

# Модель для внутреннего представления данных процесса
class InternalProcessDataModel(BaseModel):
    process_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    status_enum: ProcessStatus = ProcessStatus.WAIT
    seller: Optional[str] = None
    buyer: Optional[str] = None
    buyer_org_data: Optional[Dict[str, Any]] = None # Добавлено поле для хранения информации о покупателе
    period: Optional[PeriodModel] = None
    debit_seller: List[ActEntryModel] = [] 
    credit_seller: List[ActEntryModel] = [] 
    debit_buyer: List[ActEntryModel] = []
    credit_buyer: List[ActEntryModel] = []
    error_message_detail: Optional[str] = None
    # Это структура документа Document из классы base_extractor.py уже хранит в себе данные PDF в виде байтов,
    # поэтому здесь можно использовать тип Any
    document_structure: Optional[Any] = None

    model_config = {
        "arbitrary_types_allowed": True
        # "from_attributes": True # Если нужно создавать из атрибутов объекта
    }
