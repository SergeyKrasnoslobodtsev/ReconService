from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Any, Optional, List
from enum import Enum

from ..value_objects.process_id import ProcessId
from ..value_objects.organization import Organization
from ..value_objects.period import Period
from ..value_objects.act_entry import ActEntry


class ProcessStatus(Enum):
    WAIT = 0
    DONE = 1
    NOT_FOUND = -1
    ERROR = -2


class DocumentStructure(BaseModel):
    """Структура документа"""
    pdf_bytes: bytes
    tables: List[Any] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
    
    model_config = {
        "arbitrary_types_allowed": True
    }


class ReconciliationProcess(BaseModel):
    """Основная сущность - процесс обработки акта сверки"""
    id: ProcessId
    status: ProcessStatus = ProcessStatus.WAIT
    created_at: datetime = Field(default_factory=datetime.now)
    seller: Optional[Organization] = None
    buyer: Optional[Organization] = None
    period: Optional[Period] = None
    debit_entries: List[ActEntry] = Field(default_factory=list)
    credit_entries: List[ActEntry] = Field(default_factory=list)
    document_structure: Optional[DocumentStructure] = None
    error_message: Optional[str] = None
    
    model_config = {
        "arbitrary_types_allowed": True,
        "validate_assignment": True 
    }
    
    def mark_as_processing(self) -> None:
        """Отмечает процесс как находящийся в обработке"""
        self.status = ProcessStatus.WAIT
    
    def complete_processing(
        self,
        seller: Organization,
        buyer: Organization,
        period: Period,
        debit_entries: List[ActEntry],
        credit_entries: List[ActEntry],
        document_structure: DocumentStructure
    ) -> None:
        """Завершает обработку процесса"""
        self.status = ProcessStatus.DONE
        self.seller = seller
        self.buyer = buyer
        self.period = period
        self.debit_entries = debit_entries
        self.credit_entries = credit_entries
        self.document_structure = document_structure
        self.error_message = None
    
    def mark_as_failed(self, error_message: str) -> None:
        """Отмечает процесс как завершившийся с ошибкой"""
        self.status = ProcessStatus.ERROR
        self.error_message = error_message
    
    def is_completed(self) -> bool:
        """Проверяет, завершен ли процесс успешно"""
        return self.status == ProcessStatus.DONE
    
    def is_failed(self) -> bool:
        """Проверяет, завершен ли процесс с ошибкой"""
        return self.status == ProcessStatus.ERROR
    
    def is_processing(self) -> bool:
        """Проверяет, находится ли процесс в обработке"""
        return self.status in [ProcessStatus.WAIT]
    
    # Исправляем валидатор - добавляем правильную обработку values
    @field_validator('error_message')
    @classmethod
    def validate_error_message(cls, v, info):
        """Валидация: сообщение об ошибке должно быть заполнено при статусе ERROR"""
        if hasattr(info, 'data') and info.data:
            status = info.data.get('status')
            if status == ProcessStatus.ERROR and not v:
                raise ValueError('Сообщение об ошибке обязательно при статусе ERROR')
        return v