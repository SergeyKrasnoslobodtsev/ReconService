"""
Перечисления для статусов процессов (в соответствии с существующим API)
"""

from enum import Enum


class ProcessStatus(Enum):
    """Статусы процесса обработки документа (как в оригинальном API)"""
    
    WAIT = 0        # Процесс в ожидании/обработке
    DONE = 1        # Процесс завершен успешно
    NOT_FOUND = -1  # Процесс не найден
    ERROR = -2      # Процесс завершен с ошибкой
    
    def is_final(self) -> bool:
        """Проверяет, является ли статус финальным"""
        return self in (ProcessStatus.DONE, ProcessStatus.ERROR)
    
    def is_completed(self) -> bool:
        """Проверяет, завершена ли обработка успешно"""
        return self == ProcessStatus.DONE
    
    def is_failed(self) -> bool:
        """Проверяет, завершена ли обработка с ошибкой"""
        return self == ProcessStatus.ERROR
    
    def is_processing(self) -> bool:
        """Проверяет, выполняется ли обработка"""
        return self == ProcessStatus.WAIT
    
    def is_not_found(self) -> bool:
        """Проверяет, что процесс не найден"""
        return self == ProcessStatus.NOT_FOUND


class DocumentType(Enum):
    """Типы документов"""
    
    RECONCILIATION_ACT = "reconciliation_act"  # Акт сверки
    NATIVE_PDF = "native_pdf"                  # Нативный PDF
    SCANNED_PDF = "scanned_pdf"               # Отсканированный PDF
