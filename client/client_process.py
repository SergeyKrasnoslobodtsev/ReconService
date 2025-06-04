import requests
import base64
import json
import time
from pathlib import Path
from typing import Dict, Any

class ReconServiceClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def send_pdf(self, pdf_path: str) -> str:
        """Отправляет PDF файл на обработку и возвращает process_id"""
        print(f"📤 Отправка PDF файла: {pdf_path}")
        
        # Читаем PDF файл
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        
        # Кодируем в base64
        pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        # Отправляем запрос
        response = self.session.post(
            f"{self.base_url}/send_reconciliation_act",
            json={"document": pdf_b64}
        )
        
        if response.status_code == 201:
            process_id = response.json()["process_id"]
            print(f"✅ PDF отправлен успешно. Process ID: {process_id}")
            return process_id
        else:
            print(f"❌ Ошибка отправки PDF: {response.status_code} - {response.text}")
            raise Exception(f"Failed to send PDF: {response.status_code}")
    
    def wait_for_processing(self, process_id: str, timeout: int = 10000) -> Dict[str, Any]:
        """Ждет завершения обработки и возвращает результат"""
        print(f"⏳ Ожидание обработки документа (Process ID: {process_id})")
        
        start_time = time.time()
        poll_interval = 10
        while time.time() - start_time < timeout:
            response = self.session.post(
                f"{self.base_url}/process_status",
                json={"process_id": process_id}
            )
            
            if response.status_code == 200:
                # Обработка завершена успешно
                result = response.json()
                print("✅ Документ успешно обработан!")
                self._print_extraction_results(result)
                return result
            
            elif response.status_code == 201:
                # Документ еще обрабатывается
                print(f"⏳ Документ в обработке... {response.text}")
                time.sleep(poll_interval)
                continue
            
            elif response.status_code == 404:
                print(f"❌ Процесс не найден: {response.json()}")
                raise Exception("Process not found")
            
            elif response.status_code == 500:
                error_detail = response.json()
                print(f"❌ Ошибка обработки: {error_detail}")
                raise Exception(f"Processing error: {error_detail}")
            
            else:
                print(f"❌ Неожиданный статус: {response.status_code} - {response.text}")
                raise Exception(f"Unexpected status: {response.status_code}")
        
        raise Exception(f"Timeout: обработка не завершена за {timeout} секунд")
    
    def fill_and_get_pdf(self, process_id: str, debit_entries: list, credit_entries: list, output_path: str = None) -> str:
        """Заполняет акт сверки и сохраняет результат"""
        print(f"📝 Заполнение акта сверки (Process ID: {process_id})")
        
        # Подготавливаем данные для заполнения
        fill_request = {
            "process_id": process_id,
            "debit": debit_entries,
            "credit": credit_entries
        }
        
        print(f"📊 Отправляем {len(debit_entries)} записей дебета и {len(credit_entries)} записей кредита")
        
        # Отправляем запрос на заполнение
        response = self.session.post(
            f"{self.base_url}/fill_reconciliation_act",
            json=fill_request
        )
        
        if response.status_code == 200:
            result = response.json()
            filled_pdf_b64 = result["document"]
            
            # Декодируем и сохраняем PDF
            filled_pdf_bytes = base64.b64decode(filled_pdf_b64)
            
            if output_path is None:
                output_path = f"filled_document_{process_id[:8]}.pdf"
            
            with open(output_path, 'wb') as f:
                f.write(filled_pdf_bytes)
            
            print(f"✅ Заполненный документ сохранен: {output_path}")
            return output_path
        
        else:
            print(f"❌ Ошибка заполнения: {response.status_code} - {response.text}")
            raise Exception(f"Failed to fill document: {response.status_code}")
    
    def _print_extraction_results(self, result: Dict[str, Any]):
        """Выводит результаты извлечения данных"""
        print("\n📋 Извлеченные данные:")
        print(f"   Продавец: {result.get('seller', 'Не найден')}")
        print(f"   Покупатель: {result.get('buyer', 'Не найден')}")
        
        period = result.get('period', {})
        if period:
            print(f"   Период: {period.get('from')} - {period.get('to')}")
        
        debit = result.get('debit', [])
        credit = result.get('credit', [])
        print(f"   Записей дебета: {len(debit)}")
        print(f"   Записей кредита: {len(credit)}")
        
        if debit:
            print("   📈 Дебет (первые 3 записи):")
            for i, entry in enumerate(debit[:3]):
                print(f"      {i+1}. Таблица {entry['row_id']['id_table']}, строка {entry['row_id']['id_row']}: {entry['value']}")
        
        if credit:
            print("   📉 Кредит (первые 3 записи):")
            for i, entry in enumerate(credit[:3]):
                print(f"      {i+1}. Таблица {entry['row_id']['id_table']}, строка {entry['row_id']['id_row']}: {entry['value']}")
        print()

def process_document(pdf_path: str, server_url: str = "http://127.0.0.1:8000"):
    """Полный цикл обработки документа"""
    client = ReconServiceClient(server_url)
    
    try:
        print("🚀 Начинаем обработку документа")
        
        # 1. Отправляем PDF
        process_id = client.send_pdf(pdf_path)
        
        # 2. Ждем обработки
        result = client.wait_for_processing(process_id)
        
        # 3. Получаем данные дебета и кредита
        debit_entries = result.get('debit', [])
        credit_entries = result.get('credit', [])
        
        # 4. Заполняем документ теми же данными (для демонстрации)
        output_path = client.fill_and_get_pdf(process_id, debit_entries, credit_entries)
        
        print(f"🎉 Обработка завершена! Результат сохранен в: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"💥 Ошибка обработки: {e}")
        return None

def modify_values_example(pdf_path: str, server_url: str = "http://127.0.0.1:8000"):
    """Пример с изменением значений"""
    client = ReconServiceClient(server_url)
    
    try:
        print("🚀 Начинаем обработку с изменением значений")
        
        # 1. Отправляем PDF
        process_id = client.send_pdf(pdf_path)
        
        # 2. Ждем обработки
        result = client.wait_for_processing(process_id)
        
        # 3. Получаем и модифицируем данные
        debit_entries = result.get('debit', [])
        credit_entries = result.get('credit', [])
        
        print("🔧 Изменяем значения для демонстрации...")
        
        # Изменяем первые несколько значений
        for i, entry in enumerate(debit_entries[:3]):
            old_value = entry['value']
            entry['value'] = round(float(old_value) * 1.1, 2)  # Увеличиваем на 10%
            print(f"   Дебет {i+1}: {old_value} → {entry['value']}")
        
        for i, entry in enumerate(credit_entries[:3]):
            old_value = entry['value']
            entry['value'] = round(float(old_value) * 0.9, 2)  # Уменьшаем на 10%
            print(f"   Кредит {i+1}: {old_value} → {entry['value']}")
        
        # 4. Заполняем документ измененными данными
        output_path = client.fill_and_get_pdf(
            process_id, debit_entries, credit_entries, 
            f"modified_document_{process_id[:8]}.pdf"
        )
        
        print(f"🎉 Документ с изменениями сохранен в: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"💥 Ошибка обработки: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Использование: python client.py <путь_к_pdf> [url_сервера]")
        print("Пример: python client.py document.pdf")
        print("Пример: python client.py document.pdf http://192.168.1.100:8000")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    server_url = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8000"
    
    if not Path(pdf_path).exists():
        print(f"❌ Файл не найден: {pdf_path}")
        sys.exit(1)
    
    print("Выберите режим:")
    print("1. Обычная обработка (возврат тех же данных)")
    print("2. Обработка с изменением значений")
    
    choice = input("Введите номер (1 или 2): ").strip()
    
    if choice == "1":
        process_document(pdf_path, server_url)
    elif choice == "2":
        modify_values_example(pdf_path, server_url)
    else:
        print("❌ Неверный выбор")