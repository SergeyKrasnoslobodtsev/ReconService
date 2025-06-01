import logging
import logging.config
import os
import threading 
from concurrent.futures import ThreadPoolExecutor
import time

import yaml

from .PDFExtractor.base_extractor import Document
from .PDFExtractor.scan_extractor import ScanExtractor
from .NER.ner_service import NERService
from pullenti.Sdk import Sdk


import base64
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from enum import Enum

def logger_configure(config_path: str = "./config/logging.yaml"):
        with open(config_path, "rt", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        for handler in cfg.get("handlers", {}).values():
            filename = handler.get("filename")
            if filename:
                log_dir = os.path.dirname(filename) or "."
                os.makedirs(log_dir, exist_ok=True)

        logging.config.dictConfig(cfg)

def InitializationPullenti():
    Sdk.initialize_all()

class ServiceInitialize:
    @staticmethod
    def initialize() -> None:
        logger_configure()
        InitializationPullenti()


class ProcessStatusEnum(Enum):
    """
    Перечисление для статусов обработки документа.
    Соответствует значениям 'status' в ответах API.
    """
    WAIT = 0  # В обработке (сообщение "wait")
    DONE = 1        # Успешно обработан (сообщение "done")
    NOT_FOUND = -1  # Не найден (сообщение "not found")
    ERROR = -2      # Ошибка обработки (сообщение содержит описание ошибки)

@dataclass
class RowId:
    """
    Представляет идентификатор строки в акте сверки.
    В виде JSON это будет словарь с ключами 'id_table' и 'id_row'.
    """
    id_table: int
    id_row: int

    def to_dict(self) -> Dict[str, int]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'RowId':
        return cls(**data)

@dataclass
class ActEntry:
    """
    Представляет одну запись (строку) в акте сверки (дебет/кредит).
    Используется для данных в полях 'debit' и 'credit'.
    """
    row_id: RowId
    record: str
    value: float  # Сумма, указана как float в описании
    date: Optional[str] = None # Дата, может отсутствовать

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект в словарь для JSON-сериализации."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActEntry':
        """Создает объект из словаря."""
        return cls(**data)

@dataclass
class Period:
    """
    Представляет период дат (с ... по ...).
    Используется для поля 'period'.
    """
    from_date: str # В API это ключ "from"
    to_date: str   # В API это ключ "to"

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект в словарь, адаптируя ключи для API ('from', 'to')."""
        return {"from": self.from_date, "to": self.to_date}

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Period':
        """Создает объект из словаря, ожидая ключи 'from' и 'to'."""
        return cls(from_date=data["from"], to_date=data["to"])

@dataclass
class ReconciliationAct:
    """
    Представляет акт сверки.
    """
    process_id: str
    status: int  # Статус обработки, соответствует ProcessStatusEnum
    message: str  # Сообщение для пользователя, например "wait", "done", "not found" или "error"
    seller: str
    buyer: str
    period: Period
    debit: List[ActEntry]
    credit: List[ActEntry]

@dataclass
class InternalProcessData:
    """
    Внутреннее представление данных процесса обработки акта сверки.
    Этот класс не является частью API, а используется сервисом для хранения состояния.
    """
    process_id: str
    original_document_b64: str  # Исходный документ, полученный от пользователя
    status_enum: ProcessStatusEnum = ProcessStatusEnum.WAIT # Текущий статус обработки
    # Поля, заполняемые после успешного парсинга документа (этап process_status -> done)
    seller: Optional[str] = None
    buyer: Optional[str] = None
    period: Optional[Period] = None
    debit_seller: List[ActEntry] = field(default_factory=list)  # Данные продавца
    credit_seller: List[ActEntry] = field(default_factory=list) # Данные продавца
    # Поля, заполняемые на этапе fill_reconciliation_act (данные от покупателя)
    debit_buyer: List[ActEntry] = field(default_factory=list)
    credit_buyer: List[ActEntry] = field(default_factory=list)
    # Заполненный документ (результат fill_reconciliation_act)
    filled_document_b64: Optional[str] = None
    error_message_detail: Optional[str] = None
    document_structure: Optional[Document] = None


class ReconciliationActService:
    """
    Сервис для обработки актов сверки.
    Предоставляет методы для парсинга, заполнения и получения статуса акта сверки.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("app." + __name__)
        self.process_data: Dict[str, InternalProcessData] = {}  # Хранит данные по каждому процессу по ID
        self._data_lock = threading.Lock() # Блокировка для синхронизации доступа к process_data
        # Инициализируем ThreadPoolExecutor с ограниченным количеством воркеров
        # Учитывая, что внутренняя обработка PDF уже может быть многопоточной (4 потока),
        # выбираем консервативное значение для max_workers на уровне сервиса.
        self.executor = ThreadPoolExecutor(max_workers=2) 
        self.logger.info("ReconciliationActService initialized with ThreadPoolExecutor (max_workers=2).")

    def _generate_process_id(self) -> str:
        """
        Генерирует уникальный идентификатор процесса.
        Используется UUID для обеспечения уникальности.
        """
        return str(uuid.uuid4())
    
    def send_reconciliation_act(self, document_b64: str) -> str:
        """
        Принимает документ акта сверки в виде base64 и инициирует его асинхронную обработку.
        
        Args:
            document_b64 (str): Исходный документ в формате base64.
        
        Returns:
            str: Уникальный идентификатор процесса обработки.
        """
        process_id = self._generate_process_id()
        
        # Начальное состояние процесса (статус WAIT)
        new_entry = InternalProcessData(
            process_id=process_id,
            original_document_b64=document_b64,
            status_enum=ProcessStatusEnum.WAIT # Явно устанавливаем начальный статус
        )
        
        with self._data_lock:
            self.process_data[process_id] = new_entry
        
        self.logger.info(f"Новый акт сверки поставлен в обработку. ID процесса: {process_id}. Запуск фоновой задачи.")
        
        # Запускаем ресурсоемкую обработку документа в фоновом потоке
        self.executor.submit(self._process_document, process_id)
        
        return process_id

    def _transform_ner_table_data_to_act_entries(self, ner_table_data: List[Dict[str, Any]]) -> List[ActEntry]:
        """Преобразует данные таблицы от NERService в список ActEntry.
        Ожидает, что каждый элемент в ner_table_data будет словарем, содержащим как минимум:
        'ner_row_idx': int (идентификатор строки от NER)
        'record': str
        'value': float (сумма операции в виде числа)
        'date': Optional[str]
        """
        act_entries = []
        if not ner_table_data:
            return act_entries
            
        for item in ner_table_data:

            row_id_from_ner = item.get('ner_row_idx')
            if row_id_from_ner is None:
                self.logger.warning(f"Отсутствует 'ner_row_idx' для элемента: {item}. Такой ActEntry не будет создан.")
                continue

            act_entries.append(ActEntry(
                row_id=RowId(
                    id_table=item.get('ner_table_idx', 0),
                    id_row=item.get('ner_row_idx', row_id_from_ner)
                ),
                record=str(item.get('record', '')),
                value=item.get('value', 0.0),
                date=item.get('date') 
            ))
        return act_entries

    def _process_document(self, process_id: str) -> None:
        """
        Выполняет внутреннюю обработку документа: декодирование, извлечение структуры,
        NER-анализ и сохранение результатов. Эта функция выполняется в фоновом потоке.
        """
        b64_content_to_process: Optional[str] = None
        initial_document_structure: Optional[Document] = None

        # Шаг 1: Получаем исходные данные для обработки под блокировкой
        with self._data_lock:
            process_entry_for_content = self.process_data.get(process_id)
            if process_entry_for_content:
                b64_content_to_process = process_entry_for_content.original_document_b64
            else:
                self.logger.error(f"(_process_document) Запись о процессе с ID {process_id} не найдена для извлечения контента.")
                return # Выход, если запись внезапно исчезла

        if not b64_content_to_process:
            # Эта ситуация не должна возникать, если send_reconciliation_act отработал корректно
            self.logger.error(f"(_process_document) Отсутствует контент для обработки для ID {process_id}.")
            # Можно обновить статус на ERROR здесь, если это необходимо
            with self._data_lock:
                entry_to_update = self.process_data.get(process_id)
                if entry_to_update:
                    entry_to_update.status_enum = ProcessStatusEnum.ERROR
                    entry_to_update.error_message_detail = "Internal error: Content for processing not found."
            return

        # Шаг 2: Выполняем ресурсоемкие операции ВНЕ блокировки
        local_seller: Optional[str] = None
        local_buyer: Optional[str] = None
        local_period: Optional[Period] = None
        local_debit_seller: List[ActEntry] = []
        local_credit_seller: List[ActEntry] = []
        final_status_for_update: ProcessStatusEnum
        final_error_message_for_update: Optional[str] = None
        processed_document_structure: Optional[Document] = None


        try:
            self.logger.info(f"(_process_document) Начало обработки PDF для ID: {process_id}")
            pdf_bytes = base64.b64decode(b64_content_to_process)

            extractor = ScanExtractor() 
            processed_document_structure = extractor.extract(pdf_bytes)
            # initial_document_structure теперь processed_document_structure
            self.logger.info(f"(_process_document) Структура документа извлечена для ID: {process_id}")

            ner_service = NERService(processed_document_structure)
            organizations = ner_service.find_document_organizations()
            
            seller_org_info = next((org for org in organizations if org.get('role') == 'продавец'), None)
            buyer_org_info = next((org for org in organizations if org.get('role') == 'покупатель'), None)

            local_seller = seller_org_info.get('str_repr') if seller_org_info else None
            local_buyer = buyer_org_info.get('str_repr') if buyer_org_info else None
            self.logger.info(f"(_process_document) Продавец: {local_seller}, Покупатель: {local_buyer} для ID: {process_id}")

            if seller_org_info:
                reconciliation_output = ner_service.extract_seller_reconciliation_details(seller_org_info)
                if reconciliation_output:
                    period_from = reconciliation_output.get('period_from')
                    period_to = reconciliation_output.get('period_to')
                    if period_from and period_to:
                        local_period = Period(from_date=period_from, to_date=period_to)
                        self.logger.info(f"(_process_document) Период акта сверки извлечен: {local_period} для ID: {process_id}")

                    debit_entries_data_from_ner = reconciliation_output.get('debit_entries_data', [])
                    credit_entries_data_from_ner = reconciliation_output.get('credit_entries_data', [])

                    local_debit_seller = self._transform_ner_table_data_to_act_entries(debit_entries_data_from_ner)
                    local_credit_seller = self._transform_ner_table_data_to_act_entries(credit_entries_data_from_ner)
                    self.logger.info(f"(_process_document) Данные по дебету/кредиту продавца извлечены для ID: {process_id}")
                else:
                    self.logger.warning(f"(_process_document) NERService не вернул деталей сверки для продавца для ID: {process_id}")
            else:
                self.logger.warning(f"(_process_document) Продавец не найден, невозможно извлечь детали сверки для ID: {process_id}")

            # Проверка на наличие обязательных данных для статуса DONE
            if local_seller and local_buyer and local_period:
                final_status_for_update = ProcessStatusEnum.DONE
                self.logger.info(f"(_process_document) Документ для ID: {process_id} успешно обработан.")
            else:
                final_status_for_update = ProcessStatusEnum.ERROR
                missing_fields = []
                if not local_seller: missing_fields.append("продавец")
                if not local_buyer: missing_fields.append("покупатель")
                if not local_period: missing_fields.append("период")
                final_error_message_for_update = f"Не удалось извлечь обязательные поля: {', '.join(missing_fields)}."
                self.logger.error(f"(_process_document) Ошибка для ID {process_id}: {final_error_message_for_update}")

        except Exception as e:
            self.logger.exception(f"(_process_document) Исключение при обработке документа для ID {process_id}: {e}")
            final_status_for_update = ProcessStatusEnum.ERROR
            final_error_message_for_update = str(e)

        # Шаг 3: Обновляем запись о процессе под блокировкой
        with self._data_lock:
            process_entry_to_update = self.process_data.get(process_id)
            if process_entry_to_update:
                process_entry_to_update.status_enum = final_status_for_update
                process_entry_to_update.error_message_detail = final_error_message_for_update
                process_entry_to_update.document_structure = processed_document_structure # Сохраняем извлеченную структуру
                
                if final_status_for_update == ProcessStatusEnum.DONE:
                    process_entry_to_update.seller = local_seller
                    process_entry_to_update.buyer = local_buyer
                    process_entry_to_update.period = local_period
                    process_entry_to_update.debit_seller = local_debit_seller
                    process_entry_to_update.credit_seller = local_credit_seller
            else:
                # Эта ситуация маловероятна, если запись была на Шаге 1
                self.logger.error(f"(_process_document) Запись о процессе с ID {process_id} исчезла перед финальным обновлением статуса.")


    def get_process_status(self, process_id: str) -> tuple[Dict[str, Any], int]:
        """
        Возвращает статус обработки документа и извлеченные данные, если обработка завершена.
        Доступ к данным процесса синхронизирован.
        """
        self.logger.info(f"(get_process_status) Запрос статуса для процесса ID: {process_id}")

        status_to_return: ProcessStatusEnum
        response_payload: Dict[str, Any]
        http_status_code: int

        with self._data_lock:
            process_entry = self.process_data.get(process_id)

            if not process_entry:
                self.logger.warning(f"(get_process_status) Процесс с ID: {process_id} не найден.")
                return ({"status": ProcessStatusEnum.NOT_FOUND.value, "message": "not found"}, 404)

            status_to_return = process_entry.status_enum

            if status_to_return == ProcessStatusEnum.WAIT:
                self.logger.debug(f"(get_process_status) Процесс ID: {process_id} все еще в обработке.")
                response_payload = {"status": ProcessStatusEnum.WAIT.value, "message": "wait"}
                http_status_code = 202
            
            elif status_to_return == ProcessStatusEnum.ERROR:
                self.logger.error(f"(get_process_status) Процесс ID: {process_id} завершился с ошибкой: {process_entry.error_message_detail}")
                response_payload = {
                    "status": ProcessStatusEnum.ERROR.value, 
                    "message": process_entry.error_message_detail or "Unknown error"
                }
                http_status_code = 500

            elif status_to_return == ProcessStatusEnum.DONE:
                # Проверка на полноту данных для DONE уже должна быть выполнена в _process_document
                self.logger.info(f"(get_process_status) Процесс ID: {process_id} успешно завершен.")
                
                # Формируем данные для ответа, используя сохраненные в process_entry значения
                # (которые были установлены в _process_document)
                
                # Сначала создаем словарь из ReconciliationAct с помощью asdict
                # Это даст нам {'period': {'from_date': '...', 'to_date': '...'}}
                temp_act_data_dict = asdict(ReconciliationAct(
                    process_id=process_entry.process_id,
                    status=ProcessStatusEnum.DONE.value,
                    message="done",
                    seller=str(process_entry.seller), 
                    buyer=str(process_entry.buyer),
                    period=process_entry.period, # Period object
                    debit=[entry.to_dict() for entry in process_entry.debit_seller], 
                    credit=[entry.to_dict() for entry in process_entry.credit_seller]
                ))

                # Теперь вручную заменяем значение ключа 'period'
                # на результат вызова process_entry.period.to_dict(),
                # если period существует.
                if process_entry.period:
                    temp_act_data_dict['period'] = process_entry.period.to_dict()
                
                # Также убедимся, что debit и credit содержат словари, а не объекты ActEntry
                # Это уже должно быть обработано вызовом entry.to_dict() выше,
                # но для дополнительной уверенности можно проверить и преобразовать, если необходимо.
                # В данном случае, если asdict(ReconciliationAct(...)) правильно обработал списки
                # ActEntry (преобразовав их в списки словарей через их собственные to_dict или asdict),
                # то дополнительных действий не требуется.
                # Однако, я явно указал entry.to_dict() при создании ReconciliationAct для ясности.

                response_payload = temp_act_data_dict
                http_status_code = 200
            
            else: # Непредвиденный статус (не должен возникать)
                self.logger.error(f"(get_process_status) Процесс ID: {process_id} имеет неизвестный статус: {status_to_return}")
                response_payload = {"status": ProcessStatusEnum.ERROR.value, "message": "Unknown process status"}
                http_status_code = 500
        
        return (response_payload, http_status_code)

    def shutdown(self):
        """
        Корректно останавливает ThreadPoolExecutor.
        Рекомендуется вызывать при завершении работы приложения.
        """
        self.logger.info("Запрос на остановку ReconciliationActService. Ожидание завершения активных задач...")
        self.executor.shutdown(wait=True)
        self.logger.info("ThreadPoolExecutor успешно остановлен.")



