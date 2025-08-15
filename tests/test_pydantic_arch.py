"""
Тест Pydantic архитектуры v2
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

def test_pydantic_architecture():
    print("=== Тестирование Pydantic архитектуры ===")
    
    # Создаем процесс
    process_id = ProcessId.generate()
    process = ReconciliationProcess(id=process_id)
    print(f"Создан процесс: {process}")
    
    # Организации с типом как вы добавили
    seller = Organization(name="ООО Рога и Копыта", type="ООО", role="продавец")
    buyer = Organization(name="Покупатель Иванов", type="ИП", role="покупатель")
    print(f"Продавец: {seller.to_string()}")
    print(f"Покупатель: {buyer.to_string()}")
    
    # Период
    period = Period(from_date="01.01.2024", to_date="31.03.2024")
    print(f"Период: {period}")
    print(f"Period valid: {period.is_valid()}")
    
    # Value Objects
    money_val = MoneyValue(amount=1000.50)
    date_val = OperationDate(value="15.01.2024")
    record_val = OperationRecord(text="Поставка товаров")
    
    print(f"Money: {money_val}")
    print(f"Date: {date_val}")
    print(f"Record: {record_val}")
    
    # Entity ActEntry
    debit_entry = ActEntry(
        row_identifier=RowIdentifier(table_id=0, row_id=1),
        record=record_val,
        value=money_val,
        date=date_val
    )
    
    print(f"Debit entry: {debit_entry}")
    print(f"API dict: {debit_entry.to_dict()}")
    
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
        credit_entries=[],
        document_structure=document_structure
    )
    
    print(f"\nСтатус: {process.status}")
    print(f"Продавец: {process.seller.to_string()}")
    
    # Проверяем Pydantic валидацию
    print("\n=== Проверка Pydantic валидации ===")
    
    try:
        # Попытка создать с неправильной ролью
        Organization(name="Test", type="ООО", role="неизвестная_роль")
    except Exception as e:
        print(f"✅ Валидация роли работает: {e}")
    
    try:
        # Попытка создать с отрицательной суммой
        MoneyValue(amount=-100)
    except Exception as e:
        print(f"✅ Валидация суммы работает: {e}")
    
    return process

if __name__ == "__main__":
    try:
        process = test_pydantic_architecture()
        print("\n✅ Pydantic архитектура работает!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
