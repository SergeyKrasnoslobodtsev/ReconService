"""
Тест v2 архитектуры с правильными данными из API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.v2.domain.value_objects.process_id import ProcessId
from src.v2.domain.value_objects.organization import Organization
from src.v2.domain.value_objects.period import Period
from src.v2.domain.value_objects.act_entry import ActEntry, RowIdentifier
from src.v2.domain.entities.process import ReconciliationProcess, DocumentStructure
from src.v2.domain.enums.process_status import ProcessStatus

def test_api_compatibility():
    print("=== Тестирование совместимости с API ===")
    
    # Создаем процесс
    process_id = ProcessId.generate()
    process = ReconciliationProcess.create(process_id)
    print(f"Создан процесс: {process}")
    
    # Создаем организации как в API
    seller = Organization(name="ООО Продавец", role="продавец")
    buyer = Organization(name="ООО Покупатель", role="покупатель")
    print(f"Продавец: {seller}")
    print(f"Покупатель: {buyer}")
    
    # Создаем период как в API
    period = Period(from_date="01.01.2024", to_date="31.03.2024")
    print(f"Период: {period}")
    print(f"API dict: {period.to_api_dict()}")
    
    # Создаем записи как в API
    debit_entry = ActEntry(
        row_identifier=RowIdentifier(table_id=0, row_id=1),
        record="Поставка товаров",
        value=1000.50,
        date="15.01.2024"
    )
    
    credit_entry = ActEntry(
        row_identifier=RowIdentifier(table_id=0, row_id=2),
        record="Оплата за товары",
        value=1000.50,
        date="20.01.2024"
    )
    
    print(f"Дебет: {debit_entry}")
    print(f"Кредит: {credit_entry}")
    
    # Завершаем процесс
    document_structure = DocumentStructure(
        pdf_bytes=b"fake_pdf_content",
        tables=[],
        metadata={}
    )
    
    process.complete_processing(
        seller=seller,
        buyer=buyer,
        period=period,
        debit_entries=[debit_entry],
        credit_entries=[credit_entry],
        document_structure=document_structure
    )
    
    # Проверяем статус
    print(f"\nСтатус процесса: {process.status}")
    print(f"Завершен: {process.is_completed()}")
    
    # Проверяем API ответ
    api_response = process.to_status_response()
    print(f"\nAPI ответ: {api_response}")
    
    # Проверяем суммы
    print(f"\nДебет итого: {process.get_debit_total()}")
    print(f"Кредит итого: {process.get_credit_total()}")
    print(f"Баланс: {process.get_balance()}")
    
    return process

def test_error_handling():
    print("\n=== Тестирование обработки ошибок ===")
    
    process_id = ProcessId.generate()
    process = ReconciliationProcess.create(process_id)
    
    # Симулируем ошибку
    process.mark_as_failed("Не удалось извлечь таблицы из PDF")
    
    print(f"Статус: {process.status}")
    print(f"Ошибка: {process.error_message}")
    print(f"API ответ: {process.to_status_response()}")

if __name__ == "__main__":
    try:
        process = test_api_compatibility()
        test_error_handling()
        print("\n✅ Все тесты API совместимости прошли успешно!")
        
        # Проверяем что статусы соответствуют API
        print(f"\n📊 Статусы в API:")
        for status in ProcessStatus:
            print(f"  {status.name}: {status.value}")
            
    except Exception as e:
        print(f"❌ Ошибка в тестах: {e}")
        import traceback
        traceback.print_exc()
