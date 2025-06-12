from pydantic import BaseModel, Field
from typing import Optional, List


class ReconciliationAct(BaseModel):
    """Акт сверки"""
    document: str = Field(..., description="PDF документ в формате base64")


class GetProcessStatusRequest(BaseModel):
    """Запрос для получения статуса процесса"""
    process_id: str = Field(..., description="Идентификатор процесса")


class ActEntryRequest(BaseModel):
    """Запись акта сверки для API"""
    row_id: dict = Field(..., description="Идентификатор строки")
    record: str = Field(..., description="Описание операции")
    value: float = Field(..., ge=0, description="Значение записи")
    date: Optional[str] = Field(None, description="Дата операции")


class FillReconciliationActRequest(BaseModel):
    """Запрос для заполнения акта сверки"""
    process_id: str = Field(..., description="Идентификатор процесса")
    debit: List[ActEntryRequest] = Field(..., description="Записи дебета")
    credit: List[ActEntryRequest] = Field(..., description="Записи кредита")

class ProcessIdResponse(BaseModel):
    """Ответ с идентификатором процесса"""
    process_id: str = Field(..., description="Уникальный идентификатор процесса")


class StatusResponse(BaseModel):
    """Базовый ответ статуса"""
    status: int = Field(description="Статус обработки акта сверки")
    message: str = Field(..., description="Сообщение")


class ActEntryResponse(BaseModel):
    """Запись акта сверки для ответа"""
    row_id: dict = Field(..., description="Идентификатор строки")
    record: str = Field(..., description="Описание операции")
    value: float = Field(..., description="Значение записи")
    date: Optional[str] = Field(None, description="Дата операции")


class ReconciliationDataResponse(BaseModel):
    """Полные данные акта сверки"""
    process_id: str = Field(..., description="Идентификатор процесса")
    status: int = Field(description="Статус обработки акта сверки")
    message: str = Field(..., description="Сообщение")
    seller: str = Field(..., description="Продавец")
    buyer: str = Field(..., description="Покупатель")
    period: dict = Field(..., description="Период сверки")
    debit: List[ActEntryResponse] = Field(default_factory=list, description="Записи дебета")
    credit: List[ActEntryResponse] = Field(default_factory=list, description="Записи кредита")

