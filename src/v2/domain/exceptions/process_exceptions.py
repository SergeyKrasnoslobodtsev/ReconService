"""
Доменные исключения для процессов
"""

from typing import Optional, Dict, Any

from ...shared.exceptions.base_exceptions import BusinessLogicError


class ProcessError(BusinessLogicError):
    """Базовое исключение для ошибок процессов"""
    pass


class ProcessNotFoundError(ProcessError):
    """Ошибка - процесс не найден"""
    
    def __init__(self, process_id: str):
        super().__init__(f"Процесс с ID '{process_id}' не найден")
        self.process_id = process_id


class InvalidProcessStatusError(ProcessError):
    """Ошибка - недопустимый статус процесса"""
    
    def __init__(self, current_status: str, attempted_status: str):
        super().__init__(
            f"Невозможно изменить статус с '{current_status}' на '{attempted_status}'"
        )
        self.current_status = current_status
        self.attempted_status = attempted_status


class ProcessAlreadyCompletedError(ProcessError):
    """Ошибка - процесс уже завершен"""
    
    def __init__(self, process_id: str, status: str):
        super().__init__(f"Процесс '{process_id}' уже завершен со статусом '{status}'")
        self.process_id = process_id
        self.status = status


class ProcessExecutionError(ProcessError):
    """Ошибка выполнения процесса"""
    
    def __init__(self, process_id: str, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(f"Ошибка выполнения процесса '{process_id}': {reason}")
        self.process_id = process_id
        self.reason = reason
        self.details = details or {}
