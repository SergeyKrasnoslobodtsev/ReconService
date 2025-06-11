
from fastapi import FastAPI, HTTPException, Request, status as fastapi_status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
import base64 

from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

from .service import ReconciliationActService, ServiceInitialize

from .schemas import ( 
    ProcessIdResponse,
    ProcessStatus,
    ReconciliationAct,
    FillReconciliationActRequest,
    ReconciliationActResponse,
    StatusResponse,
    StatusRequest
)

from .config import AppConfig

from contextlib import asynccontextmanager

reconciliation_service: ReconciliationActService = None
app_config: AppConfig = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контекстный менеджер для управления жизненным циклом приложения"""
    global reconciliation_service, app_config
    print("приложение запускается...")
    ServiceInitialize.initialize(config=app_config)
    reconciliation_service = ReconciliationActService(config=app_config)
    print("ReconciliationActService успешно инициализирован.")
    yield
    
    print("FastAPI приложение останавливается...")
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
        docs_url=None,
        redoc_url=None,
    )

    

    app.mount("/static", StaticFiles(directory="static"), name="static")
    # Настраиваем CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    
    return app

# Функция для обратной совместимости
def get_app():
    """Получает приложение для uvicorn"""
    from .config import load_config
    
    config = load_config()
    return create_app(config)

# Создаем приложение по умолчанию
app = get_app()

# Основные эндпоинты API

@app.post("/send_reconciliation_act",
            status_code=fastapi_status.HTTP_201_CREATED, 
            response_model=ProcessIdResponse)
async def handle_send_reconciliation_act(input_data: ReconciliationAct):
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

@app.post("/fill_reconciliation_act", response_class=JSONResponse,
          responses={ 
                fastapi_status.HTTP_200_OK: {"model": ReconciliationAct, "description": "Документ успешно обработан"},
                fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": StatusResponse, "description": "Ошибка обработки"}
            })
async def handle_fill_reconciliation_act(input_data: FillReconciliationActRequest):
    """
    Заполняет акт сверки данными покупателя и возвращает PDF в base64.
    Корректно обрабатывает все возможные ошибки процесса.
    """
    try:
        filled_pdf_bytes = reconciliation_service.fill_reconciliation_act(input_data)
        filled_pdf_b64 = base64.b64encode(filled_pdf_bytes).decode("utf-8")
        return JSONResponse(content={"document": filled_pdf_b64}, status_code=fastapi_status.HTTP_200_OK)
        
    except ValueError as ve:
        # Ошибки бизнес-логики
        reconciliation_service.logger.warning(f"Ошибка при заполнении акта: {ve}")
        error_response = StatusResponse(
            status=ProcessStatus.ERROR.value,
            message=str(ve)
        )
        return JSONResponse(content=error_response.model_dump(), status_code=fastapi_status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    except RuntimeError as re:
        # Ошибки при заполнении документа
        reconciliation_service.logger.error(f"Ошибка выполнения при заполнении акта: {re}")
        error_response = StatusResponse(
            status=ProcessStatus.ERROR.value,
            message=str(re)
        )
        return JSONResponse(content=error_response.model_dump(), status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        # Неожиданные ошибки
        reconciliation_service.logger.error(f"Неожиданная ошибка при заполнении акта сверки: {e}", exc_info=True)
        error_response = StatusResponse(
            status=ProcessStatus.ERROR.value,
            message="Внутренняя ошибка сервера при заполнении акта сверки."
        )
        return JSONResponse(content=error_response.model_dump(), status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/process_status",
            responses={ 
                fastapi_status.HTTP_200_OK: {"model": ReconciliationActResponse, "description": "Документ успешно обработан (статус 1)"},
                fastapi_status.HTTP_201_CREATED: {"model": StatusResponse, "description": "Документ в обработке (статус 0)"},
                fastapi_status.HTTP_404_NOT_FOUND: {"model": StatusResponse, "description": "Процесс не найден (статус -1)"},
                fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": StatusResponse, "description": "Ошибка обработки (статус -2)"}
            }) 
async def handle_get_process_status(input_data: StatusRequest):
    """
    Получает статус обработки процесса:
    """
    process_id = input_data.process_id
    
    try:
        response_dict = reconciliation_service.get_process_status(process_id)
        service_status_value = response_dict.get('status')

        if service_status_value == ProcessStatus.DONE.value:  # status: 1
            # Возвращаем полные данные с кодом 200
            return JSONResponse(content=response_dict, status_code=fastapi_status.HTTP_200_OK)
            
        elif service_status_value == ProcessStatus.WAIT.value:  # status: 0
            # Документ в обработке - возвращаем 201
            return JSONResponse(content=response_dict, status_code=fastapi_status.HTTP_201_CREATED)
            
        elif service_status_value == ProcessStatus.NOT_FOUND.value:  # status: -1
            # Процесс не найден - возвращаем 404
            return JSONResponse(content=response_dict, status_code=fastapi_status.HTTP_404_NOT_FOUND)
            
        elif service_status_value == ProcessStatus.ERROR.value:  # status: -2
            # Ошибка обработки - возвращаем 500
            return JSONResponse(content=response_dict, status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
            # Неизвестный статус
            reconciliation_service.logger.error(f"Неизвестный статус {service_status_value} для процесса {process_id}")
            error_response = StatusResponse(
                status=ProcessStatus.ERROR.value, 
                message="Внутренняя ошибка: неизвестный статус процесса."
            )
            return JSONResponse(content=error_response.model_dump(), status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        reconciliation_service.logger.error(f"Критическая ошибка в /process_status для ID {process_id}: {e}", exc_info=True)
        error_response = StatusResponse(
            status=ProcessStatus.ERROR.value, 
            message="Внутренняя ошибка сервера при запросе статуса."
        )
        return JSONResponse(content=error_response.model_dump(), status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=fastapi_status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

# Настройка документации OpenAPI

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )
