import os
from fastapi import FastAPI, HTTPException, status as fastapi_status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import base64 

from .service import ReconciliationActService, ServiceInitialize
from .schemas import ( 
    ProcessIdResponse,
    ProcessStatus, 
    ReconciliationActResponseModel, 
    StatusResponseModel,
    ReconciliationActRequestModel,
    ProcessStatusRequest,
    FillReconciliationActRequestModel
)
from .config import AppConfig

from contextlib import asynccontextmanager

reconciliation_service: ReconciliationActService = None
app_config: AppConfig = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контекстный менеджер для управления жизненным циклом приложения"""
    global reconciliation_service
    
    print("🚀 FastAPI приложение запускается...")
    ServiceInitialize.initialize()
    reconciliation_service = ReconciliationActService()
    print("✅ ReconciliationActService успешно инициализирован.")
    yield
    
    print("🛑 FastAPI приложение останавливается...")
    if reconciliation_service:
        reconciliation_service.shutdown()

def create_app(config: AppConfig) -> FastAPI:
    """Создает и настраивает FastAPI приложение"""
    global app_config
    app_config = config
    
    # Создаем FastAPI приложение
    app = FastAPI(
        lifespan=lifespan,
        title=config.api.title,
        description=config.api.description,
        version=config.api.version,
        docs_url=config.api.docs_url,
        redoc_url=config.api.redoc_url,
    )
    
    # Настраиваем CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.security.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    
    return app

# Функция для обратной совместимости
def get_app():
    """Получает приложение для uvicorn"""
    from .config import config_manager
    
    # Пытаемся получить окружение из переменной, установленной start.py
    environment = os.getenv('_RECON_CONFIG_ENVIRONMENT') or os.getenv('ENVIRONMENT', 'development')
    config = config_manager.load_config(environment)
    return create_app(config)

# Создаем приложение по умолчанию
app = get_app()

# Основные эндпоинты API
@app.get("/")
async def read_root():
    return {"message": "Reconciliation Act Service is running"}

@app.post("/send_reconciliation_act",
            status_code=fastapi_status.HTTP_201_CREATED, 
            response_model=ProcessIdResponse)
async def handle_send_reconciliation_act(input_data: ReconciliationActRequestModel):
    """ Инициирует обработку акта сверки, принимая PDF в base64. """
    try:
        try:
            pdf_bytes = base64.b64decode(input_data.document)
        except base64.binascii.Error as e:
            reconciliation_service.logger.error(f"Ошибка декодирования base64: {e}")
            raise HTTPException(status_code=fastapi_status.HTTP_400_BAD_REQUEST, detail="Некорректный формат base64.")
        
        process_id = reconciliation_service.send_reconciliation_act(pdf_bytes=pdf_bytes)
        return ProcessIdResponse(process_id=process_id) 
    except HTTPException:
        raise
    except Exception as e:
        reconciliation_service.logger.error(f"Ошибка при вызове send_reconciliation_act: {e}", exc_info=True)
        # Возвращаем ошибку в формате StatusResponseModel, если это уместно, или общую ошибку
        # В данном случае, если сам вызов сервиса падает, это внутренняя ошибка сервера
        raise HTTPException(status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка сервера при инициации обработки документа.")

@app.post("/fill_reconciliation_act", response_class=JSONResponse)
async def handle_fill_reconciliation_act(input_data: FillReconciliationActRequestModel):
    """
    Заполняет акт сверки на основе предоставленных данных (debit/credit).
    Возвращает PDF в base64.
    """
    try:
        filled_pdf_bytes = reconciliation_service.fill_reconciliation_act(input_data)
        filled_pdf_b64 = base64.b64encode(filled_pdf_bytes).decode("utf-8")
        return {"document": filled_pdf_b64}
    except Exception as e:
        reconciliation_service.logger.error(f"Ошибка при заполнении акта сверки: {e}", exc_info=True)
        raise HTTPException(status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка при заполнении акта сверки.")



@app.post("/process_status",
            # response_model не указываем глобально, так как он разный для разных статусов
            responses={ 
                fastapi_status.HTTP_200_OK: {"model": ReconciliationActResponseModel, "description": "Документ успешно обработан (статус 1)"},
                fastapi_status.HTTP_201_CREATED: {"model": StatusResponseModel, "description": "Документ в обработке (статус 0)"},
                fastapi_status.HTTP_404_NOT_FOUND: {"model": StatusResponseModel, "description": "Процесс не найден (статус -1)"},
                fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": StatusResponseModel, "description": "Ошибка обработки (статус -2)"}
            }) 
async def handle_get_process_status(input_data: ProcessStatusRequest):
    process_id = input_data.process_id
    
    try:
        response_dict = reconciliation_service.get_process_status(process_id)
        service_status_value = response_dict.get('status')

        # Согласно описанию API:
        # status 0 (WAIT) -> HTTP 201
        # status 1 (DONE) -> HTTP 200
        # status -1 (NOT_FOUND) -> HTTP 404
        # status -2 (ERROR) -> HTTP 500

        if service_status_value == ProcessStatus.DONE.value: # status: 1
            # response_dict здесь это ReconciliationActResponseModel.model_dump()
            return JSONResponse(content=response_dict, status_code=fastapi_status.HTTP_200_OK)
        
        elif service_status_value == ProcessStatus.WAIT.value: # status: 0
            # response_dict здесь это StatusResponseModel.model_dump() с message="wait"
            return JSONResponse(content=response_dict, status_code=fastapi_status.HTTP_201_CREATED)
        
        elif service_status_value == ProcessStatus.NOT_FOUND.value: # status: -1
            # response_dict здесь это StatusResponseModel.model_dump() с message="not found"
            # Важно: FastAPI автоматически преобразует detail в JSON, если это dict или Pydantic модель
            raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail=response_dict)
        
        elif service_status_value == ProcessStatus.ERROR.value: # status: -2
            # response_dict здесь это StatusResponseModel.model_dump() с message="ERROR_DESCRIPTION"
            raise HTTPException(status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response_dict)
        
        else:
            reconciliation_service.logger.error(f"Неизвестный service_status_value {service_status_value} от get_process_status для ID {process_id}")
            # Формируем стандартный StatusResponseModel для непредвиденной ошибки
            error_detail = StatusResponseModel(status=ProcessStatus.ERROR.value, message="Внутренняя ошибка: неизвестный статус от сервиса.").model_dump()
            raise HTTPException(status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

    except HTTPException: # Перехватываем HTTPException, чтобы не попасть в общий Exception handler ниже
        raise
    except Exception as e:
        reconciliation_service.logger.error(f"Критическая ошибка в эндпоинте /process_status для ID {process_id}: {e}", exc_info=True)
        # Общая ошибка сервера, если что-то пошло не так до вызова сервиса или при неожиданном исключении
        error_detail = StatusResponseModel(status=ProcessStatus.ERROR.value, message="Внутренняя ошибка сервера при запросе статуса.").model_dump()
        raise HTTPException(status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)



