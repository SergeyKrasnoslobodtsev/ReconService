import logging
import base64
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from .models import (
    ReconciliationAct, 
    GetProcessStatusRequest, 
    FillReconciliationActRequest,
    ProcessIdResponse, 
    StatusResponse, 
    ReconciliationDataResponse
)

from ..application.use_case.create_process import CreateProcessUseCase
from ..application.use_case.get_process_status import GetProcessStatusUseCase
from ..application.use_case.fill_document import FillDocumentUseCase
from ..application.dto.process_dto import CreateProcessDto, FillDocumentDto
from ..domain.models.process import ProcessStatus
from ..exceptions import ProcessIdNotFoundError


class ReconciliationController:
    """Контроллер для операций с актами сверки"""
    
    def __init__(
        self,
        create_process_use_case: CreateProcessUseCase,
        get_process_status_use_case: GetProcessStatusUseCase,
        fill_document_use_case: FillDocumentUseCase
    ):
        self._create_process_use_case = create_process_use_case
        self._get_process_status_use_case = get_process_status_use_case
        self._fill_document_use_case = fill_document_use_case
        self._logger = logging.getLogger(f"app.{self.__class__.__name__}")
        
        # Создаем роутер
        self.router = APIRouter()
        self._setup_routes()
    
    def _setup_routes(self):
        """Настраивает маршруты API"""
        
        @self.router.post(
            "/send_reconciliation_act",
            status_code=status.HTTP_201_CREATED,
            response_model=ProcessIdResponse,
            responses={
                status.HTTP_400_BAD_REQUEST: {"model": StatusResponse},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": StatusResponse}
            }
        )
        async def send_reconciliation_act(request: ReconciliationAct):
            """Инициирует обработку акта сверки"""
            try:
                # Декодируем base64
                try:
                    pdf_bytes = base64.b64decode(request.document)
                except Exception as e:
                    self._logger.error(f"Ошибка декодирования base64: {e}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Некорректный формат base64"
                    )
                
                # Создаем DTO и вызываем use case
                dto = CreateProcessDto(pdf_bytes=pdf_bytes)
                process_id = await self._create_process_use_case.execute(dto)
                
                self._logger.info(f"Создан процесс: {process_id}")
                return ProcessIdResponse(process_id=process_id)
                
            except HTTPException:
                raise
            except Exception as e:
                self._logger.exception("Ошибка при создании процесса")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Внутренняя ошибка сервера"
                )
        
        @self.router.post(
            "/process_status",
            responses={
                status.HTTP_200_OK: {"model": ReconciliationDataResponse},
                status.HTTP_201_CREATED: {"model": StatusResponse},
                status.HTTP_404_NOT_FOUND: {"model": StatusResponse},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": StatusResponse}
            }
        )
        async def get_process_status(request: GetProcessStatusRequest):
            """Получает статус процесса обработки"""
            try:

                status_dto = await self._get_process_status_use_case.execute(request.process_id)
                
                # Определяем HTTP статус код на основе статуса процесса
                if status_dto.status == ProcessStatus.DONE:
                    http_status = status.HTTP_200_OK
                    response_data = ReconciliationDataResponse(
                        process_id=status_dto.process_id,
                        status=status_dto.status.value,
                        message=status_dto.message,
                        seller=status_dto.seller,
                        buyer=status_dto.buyer,
                        period={"from": status_dto.period_from, "to": status_dto.period_to} if status_dto.period_from else None,
                        debit=status_dto.debit_entries,
                        credit=status_dto.credit_entries
                    )
                elif status_dto.status == ProcessStatus.WAIT:
                    http_status = status.HTTP_201_CREATED
                    response_data = StatusResponse(
                        status=status_dto.status.value,
                        message=status_dto.message
                    )
                elif status_dto.status == ProcessStatus.NOT_FOUND:
                    http_status = status.HTTP_404_NOT_FOUND
                    response_data = StatusResponse(
                        status=status_dto.status.value,
                        message=status_dto.message
                    )
                else:  # ERROR
                    http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                    response_data = StatusResponse(
                        status=status_dto.status.value,
                        message=status_dto.message
                    )
                
                return JSONResponse(
                    content=response_data.model_dump(),
                    status_code=http_status
                )
                
            except Exception as e:
                self._logger.exception("Ошибка при получении статуса процесса")
                return JSONResponse(
                    content=StatusResponse(
                        status=ProcessStatus.ERROR.value,
                        message="Внутренняя ошибка сервера"
                    ).model_dump(),
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        @self.router.post(
            "/fill_reconciliation_act",
            response_model=ReconciliationAct,
            responses={
                status.HTTP_200_OK: {"model": ReconciliationAct},
                status.HTTP_404_NOT_FOUND: {"model": StatusResponse},
                status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": StatusResponse},
                status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": StatusResponse}
            }
        )
        async def fill_reconciliation_act(request: FillReconciliationActRequest):
            """Заполняет акт сверки данными"""
            try:
                # Преобразуем request в DTO
                dto = FillDocumentDto(
                    process_id=request.process_id,
                    debit_entries=[entry.model_dump() for entry in request.debit],
                    credit_entries=[entry.model_dump() for entry in request.credit]
                )
                
                # Вызываем use case
                filled_pdf_bytes = await self._fill_document_use_case.execute(dto)
                
                self._logger.info(f"Документ заполнен для процесса: {request.process_id}")
                
                import base64
                filled_pdf_b64 = base64.b64encode(filled_pdf_bytes).decode("utf-8")
                
                # Возвращаем простой JSON с base64 строкой
                return ReconciliationAct(document=filled_pdf_b64)
                
            except ProcessIdNotFoundError:
                return JSONResponse(
                    content=StatusResponse(
                        status=ProcessStatus.ERROR.value,
                        message="Процесс не найден"
                    ).model_dump(),
                    status_code=status.HTTP_404_NOT_FOUND
                )
            except ValueError as e:
                return JSONResponse(
                    content=StatusResponse(
                        status=ProcessStatus.ERROR.value,
                        message=str(e)
                    ).model_dump(),
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except RuntimeError as e:
                return JSONResponse(
                    content=StatusResponse(
                        status=ProcessStatus.ERROR.value,
                        message=str(e)
                    ).model_dump(),
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                self._logger.exception("Ошибка при заполнении документа")
                return JSONResponse(
                    content=StatusResponse(
                        status=ProcessStatus.ERROR.value,
                        message="Внутренняя ошибка сервера"
                    ).model_dump(),
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
    


