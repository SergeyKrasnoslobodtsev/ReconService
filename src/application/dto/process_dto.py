from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from ...domain.models.process import ProcessStatus


class ProcessStatusDto(BaseModel):
    """DTO для статуса процесса"""
    process_id: str = Field(..., description="Идентификатор процесса")
    status: ProcessStatus = Field(..., description="Статус процесса")
    message: str = Field(..., description="Сообщение о статусе")
    created_at: datetime = Field(..., description="Время создания процесса")
    seller: Optional[str] = Field(default=None, description="Продавец")
    buyer: Optional[str] = Field(default=None, description="Покупатель")
    period_from: Optional[str] = Field(default=None, description="Начало периода")
    period_to: Optional[str] = Field(default=None, description="Конец периода")
    debit_entries: List[dict] = Field(default_factory=list, description="Записи дебета")
    credit_entries: List[dict] = Field(default_factory=list, description="Записи кредита")
    error_message: Optional[str] = Field(default=None, description="Сообщение об ошибке")


class CreateProcessDto(BaseModel):
    """DTO для создания процесса"""
    pdf_bytes: bytes = Field(..., description="PDF документ в байтах")
    
    model_config = {
        "arbitrary_types_allowed": True
    }


class FillDocumentDto(BaseModel):
    """DTO для заполнения документа"""
    process_id: str = Field(..., description="Идентификатор процесса")
    debit_entries: List[dict] = Field(..., description="Записи дебета")
    credit_entries: List[dict] = Field(..., description="Записи кредита")


class DocumentProcessingResultDto(BaseModel):
    """DTO для результата обработки документа"""
    success: bool = Field(..., description="Успешность обработки")
    seller_name: Optional[str] = Field(default=None, description="Имя продавца")
    buyer_name: Optional[str] = Field(default=None, description="Имя покупателя")
    buyer_raw_data: Optional[dict] = Field(default=None, description="Сырые данные покупателя")
    period_from: Optional[str] = Field(default=None, description="Начало периода")
    period_to: Optional[str] = Field(default=None, description="Конец периода")
    debit_entries: List[dict] = Field(default_factory=list, description="Записи дебета")
    credit_entries: List[dict] = Field(default_factory=list, description="Записи кредита")
    document_structure: Optional[dict] = Field(default=None, description="Структура документа")
    error_message: Optional[str] = Field(default=None, description="Сообщение об ошибке")