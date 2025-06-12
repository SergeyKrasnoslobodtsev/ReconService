import logging
from datetime import datetime

from ..dto.process_dto import ProcessStatusDto
from ...domain.value_objects.process_id import ProcessId
from ...domain.interfaces.process_repository import IProcessRepository
from ...domain.models.process import ProcessStatus


class GetProcessStatusUseCase:
    """Случай использования: получение статуса процесса"""
    
    def __init__(self, process_repository: IProcessRepository):
        self._process_repository = process_repository
        self._logger = logging.getLogger(f"app.{self.__class__.__name__}")
    
    async def execute(self, process_id_str: str) -> ProcessStatusDto:
        """Получает статус процесса"""
        
        try:
            process_id = ProcessId(value=process_id_str)
        except ValueError as e:
            return ProcessStatusDto(
                process_id=process_id_str,
                status=ProcessStatus.ERROR,
                message=f"Некорректный идентификатор процесса: {str(e)}",
                created_at=datetime.now()
            )
        
        # Получаем процесс
        process = await self._process_repository.get_by_id(process_id)
        
        if not process:
            return ProcessStatusDto(
                process_id=process_id_str,
                status=ProcessStatus.NOT_FOUND,
                message="Процесс не найден",
                created_at=datetime.now()
            )
        
        # Преобразуем в DTO
        if process.is_processing():
            return ProcessStatusDto(
                process_id=process_id_str,
                status=process.status,
                message="Документ в обработке",
                created_at=process.created_at
            )
        
        elif process.is_failed():
            return ProcessStatusDto(
                process_id=process_id_str,
                status=process.status,
                message=process.error_message or "Произошла ошибка при обработке",
                created_at=process.created_at,
                error_message=process.error_message
            )
        
        elif process.is_completed():
            return ProcessStatusDto(
                process_id=process_id_str,
                status=process.status,
                message="Документ успешно обработан",
                created_at=process.created_at,
                seller=process.seller.name if process.seller else None,
                buyer=process.buyer.name if process.buyer else None,
                period_from=process.period.from_date if process.period else None,
                period_to=process.period.to_date if process.period else None,
                debit_entries=[entry.to_dict() for entry in process.debit_entries],
                credit_entries=[entry.to_dict() for entry in process.credit_entries]
            )
        
        else:
            return ProcessStatusDto(
                process_id=process_id_str,
                status=ProcessStatus.ERROR,
                message="Неизвестный статус процесса",
                created_at=process.created_at
            )