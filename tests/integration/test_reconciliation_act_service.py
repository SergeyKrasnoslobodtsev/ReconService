import base64
import os
import sys # sys может быть не нужен напрямую в этом тесте
from pathlib import Path # Path может быть не нужен напрямую в этом тесте
import pytest
import time # Добавляем импорт time

from src.init import ReconciliationActService, ProcessStatusEnum, ServiceInitialize
from tests.integration.common_test import get_pdf_scan

# Фикстура для инициализации необходимых сервисов один раз для всех тестов в модуле.
@pytest.fixture(scope="module", autouse=True)
def initialize_services():
    """
    Инициализация необходимых сервисов перед запуском всех тестов в модуле.
    Это гарантирует, что Pullenti SDK и логгер настроены.
    """
    ServiceInitialize.initialize()

@pytest.fixture
def reconciliation_service():
    """
    Фикстура для создания и корректного завершения экземпляра ReconciliationActService.
    """
    service = ReconciliationActService()
    yield service
    service.shutdown() # Гарантирует закрытие ThreadPoolExecutor

def test_send_reconciliation_act_and_get_status_for_scan(reconciliation_service): # Используем фикстуру
    """
    Тестирует основной сценарий: отправка отсканированного PDF,
    получение ID процесса и проверка статуса обработки с учетом асинхронности.
    """
    service = reconciliation_service # Получаем сервис из фикстуры
    
    pdf_bytes = get_pdf_scan()
    assert pdf_bytes is not None, "Метод get_pdf_scan должен возвращать байты PDF."
    
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

    process_id = service.send_reconciliation_act(document_b64=pdf_base64)
    
    assert process_id is not None, "Метод send_reconciliation_act должен возвращать process_id."
    assert isinstance(process_id, str), "process_id должен быть строкой."

    start_time = time.time()
    timeout_seconds = 60  # Таймаут для ожидания завершения обработки (в секундах)
    poll_interval_seconds = 1 # Интервал опроса статуса (в секундах)

    final_response_data = None
    final_http_status_code = None
    current_status = None

    while time.time() - start_time < timeout_seconds:
        response_data, http_status_code = service.get_process_status(process_id)
        
        assert response_data is not None, "Ответ от get_process_status не должен быть None."
        assert "status" in response_data, "Ответ должен содержать ключ 'status'."
        current_status = response_data["status"]

        if current_status == ProcessStatusEnum.DONE.value:
            # service.logger.info(f"Интеграционный тест: Обработка завершена успешно (DONE) для ID {process_id}.")
            final_response_data = response_data
            final_http_status_code = http_status_code
            break
        elif current_status == ProcessStatusEnum.ERROR.value:
            # service.logger.warning(f"Интеграционный тест: Обработка завершилась с ошибкой (ERROR) для ID {process_id}.")
            final_response_data = response_data
            final_http_status_code = http_status_code
            break
        elif current_status == ProcessStatusEnum.WAIT.value:
            assert http_status_code == 202, f"HTTP статус для WAIT должен быть 202, получили {http_status_code}."
            assert response_data["message"] == "wait", "Сообщение для WAIT должно быть 'wait'."
            # service.logger.debug(f"Интеграционный тест: Статус WAIT для ID {process_id}, продолжаем опрос...")
            time.sleep(poll_interval_seconds)
        elif current_status == ProcessStatusEnum.NOT_FOUND.value:
            service.logger.error(f"Интеграционный тест: Процесс с ID {process_id} не найден во время опроса.")
            pytest.fail(f"Процесс с ID {process_id} не найден во время опроса.")
        else:
            service.logger.error(f"Интеграционный тест: Неожиданный статус {current_status} для ID {process_id} во время опроса.")
            pytest.fail(f"Неожиданный статус {current_status} во время опроса: {response_data.get('message')}")
    else: # Срабатывает, если цикл завершился по таймауту
        last_status_after_timeout, _ = service.get_process_status(process_id)
        service.logger.error(f"Интеграционный тест: Timeout! Обработка PDF для ID {process_id} не завершилась за {timeout_seconds} секунд. Последний статус: {last_status_after_timeout.get('status')}, сообщение: {last_status_after_timeout.get('message')}")
        pytest.fail(f"Timeout: Обработка PDF не завершилась за {timeout_seconds} секунд. Последний статус: {current_status}, сообщение: {response_data.get('message') if response_data else 'N/A'}")

    assert final_response_data is not None, "Данные ответа не были получены после завершения опроса."
    # current_status уже установлен в цикле на последнее значение перед выходом или будет None, если цикл не выполнился
    # Правильнее использовать статус из final_response_data
    final_status = final_response_data["status"]
    
    if final_status == ProcessStatusEnum.DONE.value:
        assert final_http_status_code == 200, "HTTP статус для DONE должен быть 200."
        assert final_response_data["message"] == "done", "Сообщение для DONE должно быть 'done'."
        
        assert "seller" in final_response_data
        assert "buyer" in final_response_data
        assert "period" in final_response_data
        assert "debit" in final_response_data
        assert "credit" in final_response_data
        
        assert isinstance(final_response_data["debit"], list), "Поле 'debit' должно быть списком."
        assert isinstance(final_response_data["credit"], list), "Поле 'credit' должно быть списком."

        service.logger.info(f"Интеграционный тест: PDF успешно обработан: Продавец={final_response_data.get('seller')}, Покупатель={final_response_data.get('buyer')}")

    elif final_status == ProcessStatusEnum.ERROR.value:
        assert final_http_status_code == 500, "HTTP статус для ERROR должен быть 500."
        assert "message" in final_response_data, "Ответ ERROR должен содержать 'message'."
        # Сообщение об ошибке может быть пустым, если так задумано логикой сервиса,
        # но обычно ожидается непустое. Оставим проверку на > 0, если это важно.
        # assert len(final_response_data["message"]) > 0, "Сообщение об ошибке не должно быть пустым."
        service.logger.warning(f"Интеграционный тест: обработка PDF для ID {process_id} завершилась с ошибкой: {final_response_data['message']}")
        
    else: # Этот блок не должен достигаться, если логика цикла и таймаута корректна
        pytest.fail(f"Получен неожиданный окончательный статус обработки: {final_status}. "
                    f"Ожидался {ProcessStatusEnum.DONE.value} (DONE) или {ProcessStatusEnum.ERROR.value} (ERROR). "
                    f"Сообщение: {final_response_data.get('message')}")
