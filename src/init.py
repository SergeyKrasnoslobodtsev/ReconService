import logging
import logging.config
import os
import threading 
from concurrent.futures import ThreadPoolExecutor
import yaml
import uuid
from typing import List, Optional, Dict, Any # Any убран, если не используется где-то еще


from .PDFExtractor.base_extractor import Document
from .PDFExtractor.scan_extractor import ScanExtractor
from .NER.ner_service import NERService
from pullenti.Sdk import Sdk


from .schemas import ( 
    ProcessStatusEnum,
    RowIdModel,
    ActEntryModel,
    PeriodModel,
    ReconciliationActResponseModel, 
    InternalProcessDataModel,
    StatusResponseModel 
)

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


class ReconciliationActService:
    """
    Сервис для обработки актов сверки.
    Предоставляет методы для парсинга, заполнения и получения статуса акта сверки.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("app." + __name__)
        # Используем InternalProcessDataModel из schemas.py
        self.process_data: Dict[str, InternalProcessDataModel] = {} 
        self._data_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=2) 
        self.logger.info("ReconciliationActService initialized with ThreadPoolExecutor (max_workers=2).")

    def _generate_process_id(self) -> str:
        """
        Генерирует уникальный идентификатор процесса.
        """
        return str(uuid.uuid4())
    
    # document_b64 меняем на pdf_bytes, так как декодирование будет в main.py
    def send_reconciliation_act(self, pdf_bytes: bytes) -> str:
        """
        Принимает документ акта сверки в виде байтов и инициирует его асинхронную обработку.
        
        Args:
            pdf_bytes (bytes): Исходный документ в виде байтов.
        
        Returns:
            str: Уникальный идентификатор процесса обработки.
        """
        process_id = self._generate_process_id()
        
        # Используем InternalProcessDataModel
        # document_structure будет заполнен в _process_document
        new_entry = InternalProcessDataModel(
            process_id=process_id,
            status_enum=ProcessStatusEnum.WAIT 
            # Остальные поля (seller, buyer, buyer_org_data, period, etc.) будут None или [] по умолчанию
        )
        
        with self._data_lock:
            self.process_data[process_id] = new_entry
        
        self.logger.info(f"Новый акт сверки поставлен в обработку. ID процесса: {process_id}. Запуск фоновой задачи.")
        
        # Передаем pdf_bytes и process_id в фоновую задачу
        self.executor.submit(self._process_document, process_id, pdf_bytes)
        
        return process_id

    def _transform_ner_table_data_to_act_entries(self, ner_table_data: List[Dict[str, Any]]) -> List[ActEntryModel]:
        """Преобразует данные таблицы от NERService в список ActEntryModel."""
        act_entries = []
        if not ner_table_data:
            return act_entries
            
        for item in ner_table_data:
            row_id_from_ner = item.get('ner_row_idx')
            if row_id_from_ner is None:
                self.logger.warning(f"Отсутствует 'ner_row_idx' для элемента: {item}. Такой ActEntryModel не будет создан.")
                continue

            # Используем RowIdModel и ActEntryModel
            act_entries.append(ActEntryModel(
                row_id=RowIdModel(
                    id_table=item.get('ner_table_idx', 0), # Предполагаем 0, если не указано
                    id_row=row_id_from_ner 
                ),
                record=str(item.get('record', '')),
                value=float(item.get('value', 0.0)), # Убедимся, что value это float
                date=item.get('date') 
            ))
        return act_entries

    def _process_document(self, process_id: str, pdf_bytes: bytes) -> None:
        """
        Выполняет внутреннюю обработку документа: извлечение структуры,
        NER-анализ и сохранение результатов. Эта функция выполняется в фоновом потоке.
        """
        # Локальные переменные для хранения результатов перед обновлением process_entry
        local_seller: Optional[str] = None
        local_buyer: Optional[str] = None
        local_buyer_org_data: Optional[Dict[str, Any]] = None # Добавлено
        local_period: Optional[PeriodModel] = None 
        local_debit_seller: List[ActEntryModel] = []
        local_credit_seller: List[ActEntryModel] = []
        final_status_for_update: ProcessStatusEnum
        final_error_message_for_update: Optional[str] = None
        processed_document_structure: Optional[Document] = None 

        try:
            self.logger.info(f"(_process_document) Начало обработки PDF для ID: {process_id}")
            
            # pdf_bytes уже переданы в метод
            extractor = ScanExtractor() 
            processed_document_structure = extractor.extract(pdf_bytes)
            self.logger.info(f"(_process_document) Структура документа извлечена для ID: {process_id}")

            ner_service = NERService(processed_document_structure) # Передаем структуру документа
            organizations = ner_service.find_document_organizations()
            
            seller_org_info = next((org for org in organizations if org.get('role') == 'продавец'), None)
            buyer_org_info = next((org for org in organizations if org.get('role') == 'покупатель'), None)

            local_seller = seller_org_info.get('str_repr') if seller_org_info else None
            local_buyer = buyer_org_info.get('str_repr') if buyer_org_info else None
            local_buyer_org_data = buyer_org_info # Сохраняем весь словарь buyer_org_info
            self.logger.info(f"(_process_document) Продавец: {local_seller}, Покупатель: {local_buyer} для ID: {process_id}")

            if seller_org_info: # Продолжаем, только если есть информация о продавце
                reconciliation_output = ner_service.extract_seller_reconciliation_details(seller_org_info)
                if reconciliation_output:
                    period_from = reconciliation_output.get('period_from')
                    period_to = reconciliation_output.get('period_to')
                    if period_from and period_to:

                        local_period = PeriodModel(from_date=period_from, to_date=period_to)
                        self.logger.info(f"(_process_document) Период акта сверки извлечен: {local_period.model_dump_json(by_alias=True)} для ID: {process_id}")

                    debit_entries_data_from_ner = reconciliation_output.get('debit_entries_data', [])
                    credit_entries_data_from_ner = reconciliation_output.get('credit_entries_data', [])

                    local_debit_seller = self._transform_ner_table_data_to_act_entries(debit_entries_data_from_ner)
                    local_credit_seller = self._transform_ner_table_data_to_act_entries(credit_entries_data_from_ner)
                    self.logger.info(f"(_process_document) Данные по дебету/кредиту продавца извлечены для ID: {process_id}")
                else:
                    self.logger.warning(f"(_process_document) NERService не вернул деталей сверки для продавца для ID: {process_id}")
            else: # Если продавец не найден, это может быть ошибкой 
                 final_status_for_update = ProcessStatusEnum.ERROR
                 final_error_message_for_update = "Информация о продавце не найдена в документе."
                 self.logger.warning(f"(_process_document) Информация о продавце не найдена для ID: {process_id}")


            # Если все прошло успешно (или частично успешно, но без критических ошибок)
            final_status_for_update = ProcessStatusEnum.DONE
            if not local_seller or not local_buyer or not local_period:
                 self.logger.warning(f"(_process_document) Не все ключевые данные (продавец, покупатель, период) были извлечены для ID: {process_id}. Статус DONE, но данные могут быть неполными.")
                 # Можно решить, считать ли это ошибкой или нет. Пока оставляем DONE.

        except Exception as e:
            self.logger.exception(f"(_process_document) Ошибка при обработке документа для ID {process_id}: {e}")
            final_status_for_update = ProcessStatusEnum.ERROR
            final_error_message_for_update = f"Ошибка обработки документа: {str(e)}"
        
        # Обновляем запись о процессе под блокировкой
        with self._data_lock:
            entry_to_update = self.process_data.get(process_id)
            if entry_to_update:
                entry_to_update.status_enum = final_status_for_update
                entry_to_update.error_message_detail = final_error_message_for_update
                entry_to_update.document_structure = processed_document_structure
                if final_status_for_update == ProcessStatusEnum.DONE:
                    entry_to_update.seller = local_seller
                    entry_to_update.buyer = local_buyer
                    entry_to_update.buyer_org_data = local_buyer_org_data # Сохраняем buyer_org_data
                    entry_to_update.period = local_period
                    entry_to_update.debit_seller = local_debit_seller
                    entry_to_update.credit_seller = local_credit_seller
                    # debit_buyer и credit_buyer остаются пустыми на этом этапе
                self.logger.info(f"(_process_document) Завершение обработки для ID: {process_id}. Статус: {final_status_for_update.name}")
            else:
                self.logger.error(f"(_process_document) Запись о процессе с ID {process_id} не найдена для обновления статуса.")

    def get_process_status(self, process_id: str) -> Dict[str, Any]:
        """
        Возвращает статус и результат обработки акта сверки.
        """
        with self._data_lock:
            process_entry = self.process_data.get(process_id)

        if not process_entry:
            # Используем StatusResponseModel для NOT_FOUND
            return StatusResponseModel(
                status=ProcessStatusEnum.NOT_FOUND.value, 
                message="Процесс с указанным ID не найден."
            ).model_dump()

        if process_entry.status_enum == ProcessStatusEnum.WAIT:
            return StatusResponseModel(
                status=ProcessStatusEnum.WAIT.value,
                message="Документ в обработке, попробуйте позже."
            ).model_dump()
        
        elif process_entry.status_enum == ProcessStatusEnum.ERROR:
            return StatusResponseModel(
                status=ProcessStatusEnum.ERROR.value,
                message=process_entry.error_message_detail or "Произошла ошибка при обработке документа."
            ).model_dump()

        elif process_entry.status_enum == ProcessStatusEnum.DONE:
            if not all([process_entry.seller, process_entry.buyer, process_entry.period]):
                 # Если основные данные не извлечены, но статус DONE, возвращаем ошибку или специальный статус
                 self.logger.warning(f"get_process_status: Неполные данные для DONE статуса ID {process_id}. Продавец: {process_entry.seller}, Покупатель: {process_entry.buyer}, Период: {process_entry.period}")
                 # Можно вернуть StatusResponseModel с сообщением о неполных данных
                 return StatusResponseModel(
                    status=ProcessStatusEnum.ERROR.value, # Или другой статус, например, кастомный "PARTIALLY_DONE"
                    message="Документ обработан, но не все ключевые данные удалось извлечь."
                 ).model_dump()

            # Формируем ReconciliationActResponseModel
            # Агрегируем debit_seller и debit_buyer (пока buyer пуст)
            # Агрегируем credit_seller и credit_buyer (пока buyer пуст)
            # В вашей ReconciliationActResponseModel поля debit и credit - это общие списки.
            # На данном этапе у нас есть только debit_seller и credit_seller.
            # Если в будущем появятся debit_buyer/credit_buyer, их нужно будет добавить сюда.
            response_data = ReconciliationActResponseModel(
                process_id=process_entry.process_id,
                status=ProcessStatusEnum.DONE.value,
                message="Документ успешно обработан.",
                seller=process_entry.seller, # Гарантированно не None из-за проверки выше
                buyer=process_entry.buyer,   # Гарантированно не None
                period=process_entry.period, # Гарантированно не None
                debit=process_entry.debit_seller, # Пока только данные продавца
                credit=process_entry.credit_seller # Пока только данные продавца
            )
            return response_data.model_dump(by_alias=True) # by_alias=True для корректной сериализации PeriodModel

        # На случай, если появится новый статус, который не обработан
        return StatusResponseModel(
            status=ProcessStatusEnum.ERROR.value,
            message="Неизвестный статус процесса."
        ).model_dump()

    def shutdown(self):
        """
        Корректно останавливает ThreadPoolExecutor.
        Рекомендуется вызывать при завершении работы приложения.
        """
        self.logger.info("Запрос на остановку ReconciliationActService. Ожидание завершения активных задач...")
        self.executor.shutdown(wait=True)
        self.logger.info("ThreadPoolExecutor успешно остановлен.")



