"""
Доменная сущность процесса обработки (Pydantic модель)
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Any, Dict

from ..enums.process_status import ProcessStatus
from ..value_objects.process_id import ProcessId
from ..value_objects.organization import Organization
from ..value_objects.period import Period
from .act_entry import ActEntry
from ...shared.logging.logger import get_logger

logger = get_logger(__name__)


class DocumentStructure(BaseModel):
    """Структура документа - как в оригинальном коде"""
    pdf_bytes: bytes
    tables: List[Any] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    model_config = {
        "arbitrary_types_allowed": True
    }


class ReconciliationProcess(BaseModel):
    """
    Основная сущность - процесс обработки акта сверки
    Соответствует оригинальной модели из domain/models/process.py
    """
    
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
    
    @classmethod
    def create(cls, process_id: ProcessId) -> 'ReconciliationProcess':
        """Создает новый процесс обработки"""
        logger.info(f"Создан новый процесс: {process_id}")
        return cls(id=process_id)
    
    def mark_as_processing(self) -> None:
        """Отмечает процесс как находящийся в обработке"""
        logger.debug(f"Процесс {self.id} переведен в статус WAIT")
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
        """Завершает обработку процесса успешно"""
        logger.info(f"Процесс {self.id} успешно завершен")
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
        logger.error(f"Процесс {self.id} завершен с ошибкой: {error_message}")
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
        return self.status == ProcessStatus.WAIT
    
    def is_not_found(self) -> bool:
        """Проверяет, что процесс не найден"""
        return self.status == ProcessStatus.NOT_FOUND
    
    def to_status_response(self) -> Dict[str, Any]:
        """Преобразует в ответ для API статуса"""
        base_response = {
            "status": self.status.value,
            "message": self._get_status_message()
        }
        
        # Если процесс завершен успешно, добавляем полные данные
        if self.is_completed():
            base_response.update({
                "process_id": str(self.id),
                "seller": self.seller.name if self.seller else "",
                "buyer": self.buyer.name if self.buyer else "",
                "period": self.period.to_api_dict() if self.period else {"from": "", "to": ""},
                "debit": [entry.to_dict() for entry in self.debit_entries],
                "credit": [entry.to_dict() for entry in self.credit_entries]
            })
        
        return base_response
    
    def _get_status_message(self) -> str:
        """Возвращает сообщение в зависимости от статуса"""
        if self.status == ProcessStatus.WAIT:
            return "Процесс обработки"
        elif self.status == ProcessStatus.DONE:
            return "Процесс завершен"
        elif self.status == ProcessStatus.ERROR:
            return self.error_message or "Произошла ошибка при обработке"
        elif self.status == ProcessStatus.NOT_FOUND:
            return "Процесс не найден"
        else:
            return "Неизвестный статус"
    
    def get_debit_total(self) -> float:
        """Возвращает общую сумму дебета"""
        return sum(entry.value.amount for entry in self.debit_entries)
    
    def get_credit_total(self) -> float:
        """Возвращает общую сумму кредита"""
        return sum(entry.value.amount for entry in self.credit_entries)
    
    def get_balance(self) -> float:
        """Возвращает баланс (дебет - кредит)"""
        return self.get_debit_total() - self.get_credit_total()
    
    def __str__(self) -> str:
        return f"Process({self.id}, status={self.status.name})"
