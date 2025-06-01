from fastapi import FastAPI, HTTPException, status as fastapi_status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .init import ReconciliationActService, ServiceInitialize, ProcessStatusEnum
from contextlib import asynccontextmanager # Импортируем asynccontextmanager

# Контекстный менеджер для lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код, выполняемый при старте приложения
    # ServiceInitialize.initialize() уже вызывается глобально при импорте,
    # но если бы была специфичная для старта FastAPI логика, она была бы здесь.
    reconciliation_service.logger.info("FastAPI приложение запускается.")
    yield
    # Код, выполняемый при остановке приложения
    reconciliation_service.logger.info("FastAPI приложение останавливается, вызываем shutdown для ReconciliationActService.")
    reconciliation_service.shutdown()

app = FastAPI(lifespan=lifespan) # Используем lifespan

# Инициализация сервисов (остается здесь, т.к. reconciliation_service используется глобально)
ServiceInitialize.initialize()
reconciliation_service = ReconciliationActService()

# Pydantic модели для запросов
class DocumentInput(BaseModel):
    document: str # base64 encoded PDF

class ProcessIdInput(BaseModel):
    process_id: str

@app.post("/send_reconciliation_act", status_code=fastapi_status.HTTP_202_ACCEPTED)
async def handle_send_reconciliation_act(input_data: DocumentInput):
    try:
        process_id = reconciliation_service.send_reconciliation_act(document_b64=input_data.document)
        return {"process_id": process_id}
    except Exception as e:
        reconciliation_service.logger.error(f"Ошибка при вызове send_reconciliation_act: {e}", exc_info=True)
        raise HTTPException(status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/process_status") 
async def handle_get_process_status(input_data: ProcessIdInput):
    process_id = input_data.process_id
    response_data, http_status_code = reconciliation_service.get_process_status(process_id)
    
    if http_status_code == 200: # DONE
        return response_data
    elif http_status_code == 202: # WAIT
        return JSONResponse(content=response_data, status_code=fastapi_status.HTTP_202_ACCEPTED)
    elif http_status_code == 404: # NOT_FOUND
        # В response_data уже есть нужная структура {"status": -1, "message": "not found"}
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail=response_data)
    elif http_status_code == 500: # ERROR
        # В response_data уже есть нужная структура {"status": -2, "message": "ERROR_DESCRIPTION"}
        raise HTTPException(status_code=fastapi_status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response_data)
    else:
        reconciliation_service.logger.warning(f"Неожиданный HTTP статус {http_status_code} от ReconciliationActService для process_id {process_id}")
        return JSONResponse(content=response_data, status_code=http_status_code)

# Для локального запуска (не для продакшена с uvicorn)
if __name__ == "__main__":
    import uvicorn
    print("Для запуска используйте: uvicorn src.main:app --reload")
