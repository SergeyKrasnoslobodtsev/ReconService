import os

import base64
import time
import pytest
from fastapi.testclient import TestClient


from src.main import app
from src.service import ProcessStatus 
from common_test import get_pdf_scan


@pytest.fixture(scope="module")
def client():

    with TestClient(app) as c:
        yield c

def test_api_send_reconciliation_act_and_get_status(client: TestClient):
    """
    Тестирует полный API-сценарий: отправка акта сверки и опрос его статуса.
    """
    pdf_bytes = get_pdf_scan()  # Получаем байты тестового PDF
    assert pdf_bytes is not None, "Не удалось загрузить PDF для теста."
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    # Отправка документа на обработку
    response_send = client.post("/send_reconciliation_act", json={"document": pdf_base64})
    
    assert response_send.status_code == 201, \
        f"Ожидался HTTP статус 201, получен {response_send.status_code}. Ответ: {response_send.text}"
    send_data = response_send.json()
    assert "process_id" in send_data, "Ответ должен содержать 'process_id'."
    process_id = send_data["process_id"]
    assert isinstance(process_id, str) and len(process_id) > 0, "'process_id' должен быть непустой строкой."

    # Опрос статуса обработки
    start_time = time.time()
    timeout_seconds = 60  # Максимальное время ожидания обработки (секунды)
    poll_interval_seconds = 2  # Интервал опроса статуса (секунды)

    final_response_data = None
    final_http_status_code = None

    while time.time() - start_time < timeout_seconds:
        response_status_obj = client.post("/process_status", json={"process_id": process_id})
        status_payload = response_status_obj.json()

        if response_status_obj.status_code == 200:  # Статус DONE от сервиса
            assert "status" in status_payload and status_payload["status"] == ProcessStatus.DONE.value
            final_response_data = status_payload
            final_http_status_code = 200
            break 
        elif response_status_obj.status_code == 201:  # Статус WAIT от сервиса
            assert "status" in status_payload and status_payload["status"] == ProcessStatus.WAIT.value
            assert status_payload.get("message") == "Документ в обработке, попробуйте позже.", "Сообщение для статуса WAIT не соответствует ожидаемому." # Исправлено ожидаемое сообщение
            time.sleep(poll_interval_seconds)
        elif response_status_obj.status_code == 500:  # Статус ERROR от сервиса
            assert "detail" in status_payload, "Ответ FastAPI об ошибке должен содержать ключ 'detail'."
            service_error_data = status_payload["detail"]
            assert "status" in service_error_data and service_error_data["status"] == ProcessStatus.ERROR.value

            pytest.fail(f"Обработка документа завершилась с ошибкой: {service_error_data.get('message', service_error_data)}")
        elif response_status_obj.status_code == 404:  # Статус NOT_FOUND от сервиса
            assert "detail" in status_payload, "Ответ FastAPI об ошибке 404 должен содержать ключ 'detail'."
            service_error_data = status_payload["detail"]
            assert "status" in service_error_data and service_error_data["status"] == ProcessStatus.NOT_FOUND.value
            pytest.fail(f"Process ID {process_id} не найден: {service_error_data.get('message', service_error_data)}")
        else:
            pytest.fail(f"Получен неожиданный HTTP статус {response_status_obj.status_code}. Ответ: {status_payload}")
    else: 
        last_payload_info = status_payload if 'status_payload' in locals() else 'N/A'
        pytest.fail(f"Таймаут: Обработка документа не завершилась за {timeout_seconds} секунд. Последний ответ: {last_payload_info}")

    assert final_response_data is not None, "Опрос завершился без получения финального ответа DONE."
    assert final_http_status_code == 200, f"Ожидался финальный HTTP статус 200, получен {final_http_status_code}."
    
    assert final_response_data["status"] == ProcessStatus.DONE.value, \
        f"Ожидался финальный статус обработки DONE ({ProcessStatus.DONE.value}), получен {final_response_data['status']}."
    assert final_response_data["message"] == "Документ успешно обработан.", "Сообщение для финального статуса DONE не соответствует ожидаемому."

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


def test_api_fill_reconciliation_act(client: TestClient):
    """
    Тестирует endpoint /fill_reconciliation_act: отправляет debit/credit, получает PDF, сохраняет его в корень под именем process_id.pdf
    """
    pdf_bytes = get_pdf_scan()
    assert pdf_bytes is not None, "Не удалось загрузить PDF для теста."
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    # 1. Отправляем документ на обработку
    response_send = client.post("/send_reconciliation_act", json={"document": pdf_base64})
    assert response_send.status_code == 201, f"Ожидался HTTP статус 201, получен {response_send.status_code}. Ответ: {response_send.text}"
    process_id = response_send.json()["process_id"]

    # 2. Ждем завершения обработки
    start_time = time.time()
    timeout_seconds = 60
    poll_interval_seconds = 2
    while time.time() - start_time < timeout_seconds:
        response_status_obj = client.post("/process_status", json={"process_id": process_id})
        status_payload = response_status_obj.json()
        if response_status_obj.status_code == 200 and status_payload["status"] == ProcessStatus.DONE.value:
            break
        elif response_status_obj.status_code == 201:
            time.sleep(poll_interval_seconds)
        elif response_status_obj.status_code in (404, 500):
            pytest.fail(f"Ошибка при ожидании статуса: {status_payload}")
    else:
        pytest.fail(f"Таймаут ожидания обработки документа для fill_reconciliation_act. Последний ответ: {status_payload}")

    # 3. Получаем финальные данные debit/credit
    debit = status_payload["debit"]
    credit = status_payload["credit"]
    assert isinstance(debit, list) and isinstance(credit, list)

    # 4. Отправляем на /fill_reconciliation_act
    response_fill = client.post("/fill_reconciliation_act", json={
        "process_id": process_id,
        "debit": debit,
        "credit": credit
    })
    assert response_fill.status_code == 200, f"Ожидался HTTP статус 200, получен {response_fill.status_code}. Ответ: {response_fill.text}"
    fill_data = response_fill.json()
    assert "document" in fill_data, "Ответ должен содержать ключ 'document' с base64 PDF."
    pdf_filled_bytes = base64.b64decode(fill_data["document"])
    assert pdf_filled_bytes[:4] == b'%PDF', "Результат не похож на PDF."

    # 5. Сохраняем PDF в корень под именем process_id.pdf
    out_path = os.path.join(os.path.dirname(__file__), "..", "../temp", f"{process_id}.pdf")
    out_path = os.path.abspath(out_path)
    with open(out_path, "wb") as f:
        f.write(pdf_filled_bytes)
    print(f"PDF успешно сохранён: {out_path}")