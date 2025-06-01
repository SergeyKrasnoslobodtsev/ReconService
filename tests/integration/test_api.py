import base64
import time
import pytest
from fastapi.testclient import TestClient

# Импортируем экземпляр FastAPI приложения и Enum статусов
from src.main import app
from src.init import ProcessStatusEnum 
from tests.integration.common_test import get_pdf_scan # Утилита для получения PDF

# Фикстура для создания TestClient один раз для всех тестов в модуле
@pytest.fixture(scope="module")
def client():
    # ServiceInitialize.initialize() вызывается в src/main.py при импорте app,
    # поэтому дополнительная инициализация здесь обычно не требуется.
    with TestClient(app) as c:
        yield c

def test_api_send_reconciliation_act_and_get_status(client: TestClient):
    """
    Тестирует полный API-сценарий: отправка акта сверки и опрос его статуса.
    """
    pdf_bytes = get_pdf_scan()  # Получаем байты тестового PDF
    assert pdf_bytes is not None, "Не удалось загрузить PDF для теста."
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    # 1. Отправка документа на обработку
    response_send = client.post("/send_reconciliation_act", json={"document": pdf_base64})
    
    assert response_send.status_code == 202, \
        f"Ожидался HTTP статус 202, получен {response_send.status_code}. Ответ: {response_send.text}"
    send_data = response_send.json()
    assert "process_id" in send_data, "Ответ должен содержать 'process_id'."
    process_id = send_data["process_id"]
    assert isinstance(process_id, str) and len(process_id) > 0, "'process_id' должен быть непустой строкой."

    # 2. Опрос статуса обработки
    start_time = time.time()
    timeout_seconds = 60  # Максимальное время ожидания обработки (секунды)
    poll_interval_seconds = 2  # Интервал опроса статуса (секунды)

    final_response_data = None
    final_http_status_code = None

    while time.time() - start_time < timeout_seconds:
        response_status_obj = client.post("/process_status", json={"process_id": process_id})
        status_payload = response_status_obj.json()

        if response_status_obj.status_code == 200:  # Статус DONE от сервиса
            assert "status" in status_payload and status_payload["status"] == ProcessStatusEnum.DONE.value
            final_response_data = status_payload
            final_http_status_code = 200
            break 
        elif response_status_obj.status_code == 202:  # Статус WAIT от сервиса
            assert "status" in status_payload and status_payload["status"] == ProcessStatusEnum.WAIT.value
            assert status_payload.get("message") == "wait", "Сообщение для статуса WAIT должно быть 'wait'."
            time.sleep(poll_interval_seconds)
        elif response_status_obj.status_code == 500:  # Статус ERROR от сервиса
            assert "detail" in status_payload, "Ответ FastAPI об ошибке должен содержать ключ 'detail'."
            service_error_data = status_payload["detail"]
            assert "status" in service_error_data and service_error_data["status"] == ProcessStatusEnum.ERROR.value
            # Если тестовый PDF не должен вызывать ошибку, тест должен упасть
            pytest.fail(f"Обработка документа завершилась с ошибкой: {service_error_data.get('message', service_error_data)}")
        elif response_status_obj.status_code == 404:  # Статус NOT_FOUND от сервиса
            assert "detail" in status_payload, "Ответ FastAPI об ошибке 404 должен содержать ключ 'detail'."
            service_error_data = status_payload["detail"]
            assert "status" in service_error_data and service_error_data["status"] == ProcessStatusEnum.NOT_FOUND.value
            pytest.fail(f"Process ID {process_id} не найден: {service_error_data.get('message', service_error_data)}")
        else:
            pytest.fail(f"Получен неожиданный HTTP статус {response_status_obj.status_code}. Ответ: {status_payload}")
    else:  # Цикл завершился по таймауту
        last_payload_info = status_payload if 'status_payload' in locals() else 'N/A'
        pytest.fail(f"Таймаут: Обработка документа не завершилась за {timeout_seconds} секунд. Последний ответ: {last_payload_info}")

    # 3. Проверка финального результата (ожидаем DONE для стандартного тестового PDF)
    assert final_response_data is not None, "Опрос завершился без получения финального ответа DONE."
    assert final_http_status_code == 200, f"Ожидался финальный HTTP статус 200, получен {final_http_status_code}."
    
    assert final_response_data["status"] == ProcessStatusEnum.DONE.value, \
        f"Ожидался финальный статус обработки DONE ({ProcessStatusEnum.DONE.value}), получен {final_response_data['status']}."
    assert final_response_data["message"] == "done", "Сообщение для финального статуса DONE должно быть 'done'."

    # Проверка наличия ожидаемых полей в ответе DONE
    assert "seller" in final_response_data
    assert "buyer" in final_response_data
    assert "period" in final_response_data
    assert isinstance(final_response_data["period"], dict)
    assert "from" in final_response_data["period"]
    assert "to" in final_response_data["period"]
    assert "debit" in final_response_data
    assert isinstance(final_response_data["debit"], list)
    assert "credit" in final_response_data
    assert isinstance(final_response_data["credit"], list)

    # Опционально: можно добавить более детальные проверки содержимого,
    # если вы знаете точные данные, которые должны быть извлечены из тестового PDF.
    # print(f"Тест API пройден успешно. Извлеченные данные: Продавец='{final_response_data.get('seller')}', Покупатель='{final_response_data.get('buyer')}'")

