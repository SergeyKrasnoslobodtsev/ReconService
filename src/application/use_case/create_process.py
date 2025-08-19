import logging
from datetime import datetime

from ..dto.process_dto import CreateProcessDto, DocumentProcessingResultDto
from ...domain.models.process import ReconciliationProcess, ProcessStatus, DocumentStructure
from ...domain.value_objects.process_id import ProcessId
from ...domain.value_objects.organization import Organization
from ...domain.value_objects.period import Period
from ...domain.value_objects.act_entry import ActEntry
from ...domain.interfaces.process_repository import IProcessRepository
from ..interfaces.document_processor import IDocumentProcessor
from ..interfaces.background_executor import IBackgroundExecutor


class CreateProcessUseCase:
    """Случай использования: создание процесса обработки документа"""
    
    def __init__(
        self,
        process_repository: IProcessRepository,
        document_processor: IDocumentProcessor,
        background_executor: IBackgroundExecutor
    ):
        self._process_repository = process_repository
        self._document_processor = document_processor
        self._background_executor = background_executor
        self._logger = logging.getLogger(f"app.{self.__class__.__name__}")
    
    async def execute(self, dto: CreateProcessDto) -> str:
        """Создает новый процесс и запускает обработку документа"""
        
        # Создаем новый процесс
        process_id = ProcessId.generate()
        process = ReconciliationProcess(
            id=process_id,
            status=ProcessStatus.WAIT,
            created_at=datetime.now()
        )
        
        # Сохраняем процесс
        await self._process_repository.save(process)
        
        self._logger.info(f"Создан процесс: {process_id}")
        
        # Запускаем фоновую обработку
        await self._background_executor.submit(
            self._process_document,
            process_id.value,
            dto.pdf_bytes
        )
        
        return process_id.value
    
    async def _process_document(self, process_id_str: str, pdf_bytes: bytes) -> None:
        """Фоновая обработка документа"""
        process_id = ProcessId(value=process_id_str)
        
        try:
            # Получаем процесс
            process = await self._process_repository.get_by_id(process_id)
            if not process:
                self._logger.error(f"Процесс не найден: {process_id}")
                return
            
            # Отмечаем как обрабатывающийся
            process.mark_as_processing()
            await self._process_repository.update(process)
            
            # Обрабатываем документ
            result: DocumentProcessingResultDto = await self._document_processor.process(pdf_bytes)
            
            if result.success:
                # Создаем доменные объекты с валидацией
                seller = Organization(
                    name=result.seller_name,
                    role='продавец'
                )
                
                buyer = Organization(
                    name=result.buyer_name,
                    role='покупатель',
                    raw_data=result.buyer_raw_data
                )
                
                period = Period(
                    from_date=result.period_from or "None",
                    to_date=result.period_to or "None"
                )
                
                debit_entries = [ActEntry.from_dict(entry) for entry in result.debit_entries]
                credit_entries = [ActEntry.from_dict(entry) for entry in result.credit_entries]
                
                document_structure = DocumentStructure(
                    pdf_bytes=pdf_bytes,
                    tables=result.document_structure.get('tables', []),
                    metadata=result.document_structure.get('metadata', {}),
                    last_page_with_table=result.document_structure.get('last_page_with_table', 0)
)
                
                # Завершаем успешно
                process.complete_processing(
                    seller=seller,
                    buyer=buyer,
                    period=period,
                    debit_entries=debit_entries,
                    credit_entries=credit_entries,
                    document_structure=document_structure
                )
                self._logger.info(f"Процесс завершен успешно: {process_id}")
            else:
                # Отмечаем как неудачный
                process.mark_as_failed(result.error_message or "Неизвестная ошибка")
                self._logger.error(f"Процесс завершен с ошибкой: {process_id}")
            
            # Сохраняем изменения
            await self._process_repository.update(process)
            
        except Exception as e:
            self._logger.exception(f"Ошибка при обработке документа {process_id}: {e}")
            
            # Пытаемся отметить процесс как неудачный
            try:
                process = await self._process_repository.get_by_id(process_id)
                if process:
                    process.mark_as_failed(f"Внутренняя ошибка: {str(e)}")
                    await self._process_repository.update(process)
            except Exception as update_error:
                self._logger.error(f"Не удалось обновить статус процесса {process_id}: {update_error}")