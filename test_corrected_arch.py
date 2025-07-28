"""
Тест исправленной архитектуры v2
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.v2.domain.value_objects.process_id import ProcessId
from src.v2.domain.value_objects.organization import Organization
from src.v2.domain.value_objects.period import Period
from src.v2.domain.value_objects.money_value import MoneyValue, OperationDate, OperationRecord
from src.v2.domain.entities.act_entry import ActEntry, RowIdentifier
from src.v2.domain.entities.process import ReconciliationProcess, DocumentStructure
from src.v2.domain.enums.process_status import ProcessStatus

def test_corrected_architecture():
    print("=== Тестирование исправленной архитектуры ===")
    
    # Создаем процесс
    process_id = ProcessId.generate()
    process = ReconciliationProcess.create(process_id)
    print(f"Создан процесс: {process}")
    
    # Организации - только то что нужно
    seller = Organization(name="ООО Рога и Копыта", role="продавец")
    buyer = Organization(name="АО Покупатель", role="покупатель")
    print(f"Продавец: {seller.name} ({seller.role})")
    print(f"Покупатель: {buyer.name} ({buyer.role})")
    
    # Период - как в оригинале
    period = Period(from_date="01.01.2024", to_date="31.03.2024")
    print(f"Период: {period}")
    
    # Value Objects для полей
    money_val = MoneyValue(1000.50)
    date_val = OperationDate("15.01.2024")
    record_val = OperationRecord("Поставка товаров")
    
    print(f"Денежное значение: {money_val}")
    print(f"Дата: {date_val}")
    print(f"Запись: {record_val}")
    
    # Entity ActEntry с Value Objects
    debit_entry = ActEntry(
        row_identifier=RowIdentifier(table_id=0, row_id=1),
        record=record_val,
        value=money_val,
        date=date_val
    )
    
    credit_entry = ActEntry(
        row_identifier=RowIdentifier(table_id=0, row_id=2),
        record=OperationRecord("Оплата за товары"),
        value=MoneyValue(1000.50),
        date=OperationDate("20.01.2024")
    )
    
    print(f"Дебет entry: {debit_entry}")
    print(f"Кредит entry: {credit_entry}")
    
    # API совместимость
    print(f"Дебет API dict: {debit_entry.to_dict()}")
    
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
    
    # Проверяем суммы
    print(f"\nДебет итого: {process.get_debit_total()}")
    print(f"Кредит итого: {process.get_credit_total()}")
    print(f"Баланс: {process.get_balance()}")
    
    # API ответ
    api_response = process.to_status_response()
    print(f"\nAPI ответ (первые записи):")
    print(f"  status: {api_response['status']}")
    print(f"  seller: {api_response['seller']}")
    print(f"  debit[0]: {api_response['debit'][0]}")

if __name__ == "__main__":
    try:
        test_corrected_architecture()
        print("\n✅ Исправленная архитектура работает!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
