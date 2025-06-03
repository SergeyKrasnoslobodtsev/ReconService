import logging
import logging.config
import os
import threading 
from concurrent.futures import ThreadPoolExecutor
import yaml
import uuid
from typing import List, Optional, Dict, Any # Any убран, если не используется где-то еще


from .PDFExtractor.base_extractor import Document, Table
from .PDFExtractor.scan_extractor import ScanExtractor
from .NER.ner_service import NERService
from pullenti.Sdk import Sdk


from .schemas import ( 
    FillReconciliationActRequestModel,
    ProcessStatus,
    RowIdModel,
    ActEntryModel,
    PeriodModel,
    ReconciliationActResponseModel, 
    InternalProcessDataModel,
    StatusResponseModel 
)

from .pdf_renderer import convert_to_bytes
from .pdf_renderer import convert_to_pil
from .pdf_renderer import draw_text_to_cell

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
            status_enum=ProcessStatus.WAIT 
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
        local_buyer_org_data: Optional[Dict[str, Any]] = None
        local_period: Optional[PeriodModel] = None 
        local_debit_seller: List[ActEntryModel] = []
        local_credit_seller: List[ActEntryModel] = []
        final_status_for_update: ProcessStatus
        final_error_message_for_update: Optional[str] = None
        processed_document_structure: Optional[Document] = None 

        try:
            self.logger.info(f"(_process_document) Начало обработки PDF для ID: {process_id}")
            
            # Извлекаем структуру документа
            extractor = ScanExtractor() 
            processed_document_structure = extractor.extract(pdf_bytes)
            self.logger.info(f"(_process_document) Структура документа извлечена для ID: {process_id}")

            # Инициализируем NER сервис
            ner_service = NERService(processed_document_structure) 
            organizations = ner_service.find_document_organizations()
            
            # Ищем организации
            seller_org_info = next((org for org in organizations if org.get('role') == 'продавец'), None)
            buyer_org_info = next((org for org in organizations if org.get('role') == 'покупатель'), None)

            local_seller = seller_org_info.get('str_repr') if seller_org_info else None
            local_buyer = buyer_org_info.get('str_repr') if buyer_org_info else None
            local_buyer_org_data = buyer_org_info 
            
            self.logger.info(f"(_process_document) Продавец: {local_seller}, Покупатель: {local_buyer} для ID: {process_id}")

            # Проверяем критичные данные
            if not seller_org_info:
                final_status_for_update = ProcessStatus.ERROR
                final_error_message_for_update = "Информация о продавце не найдена в документе."
                self.logger.error(f"(_process_document) Информация о продавце не найдена для ID: {process_id}")
            elif not buyer_org_info:
                final_status_for_update = ProcessStatus.ERROR
                final_error_message_for_update = "Информация о покупателе не найдена в документе."
                self.logger.error(f"(_process_document) Информация о покупателе не найдена для ID: {process_id}")
            else:
                # Извлекаем детали сверки продавца
                reconciliation_output = ner_service.extract_seller_reconciliation_details(seller_org_info)
                if reconciliation_output:
                    period_from = reconciliation_output.get('period_from')
                    period_to = reconciliation_output.get('period_to')
                    
                    if period_from and period_to:
                        local_period = PeriodModel(from_date=period_from, to_date=period_to)
                        self.logger.info(f"(_process_document) Период акта сверки извлечен: {local_period.model_dump_json(by_alias=True)} для ID: {process_id}")
                    else:
                        final_status_for_update = ProcessStatus.ERROR  
                        final_error_message_for_update = "Не удалось определить период сверки."
                        self.logger.error(f"(_process_document) Период сверки не найден для ID: {process_id}")

                    if local_period:  # Только если период найден
                        debit_entries_data_from_ner = reconciliation_output.get('debit_entries_data', [])
                        credit_entries_data_from_ner = reconciliation_output.get('credit_entries_data', [])

                        local_debit_seller = self._transform_ner_table_data_to_act_entries(debit_entries_data_from_ner)
                        local_credit_seller = self._transform_ner_table_data_to_act_entries(credit_entries_data_from_ner)
                        self.logger.info(f"(_process_document) Данные по дебету/кредиту продавца извлечены для ID: {process_id}")
                        
                        # Все ключевые данные получены
                        final_status_for_update = ProcessStatus.DONE
                else:
                    final_status_for_update = ProcessStatus.ERROR
                    final_error_message_for_update = "NERService не вернул деталей сверки для продавца."
                    self.logger.error(f"(_process_document) NERService не вернул деталей сверки для продавца для ID: {process_id}")

        except Exception as e:
            self.logger.exception(f"(_process_document) Ошибка при обработке документа для ID {process_id}: {e}")
            final_status_for_update = ProcessStatus.ERROR
            final_error_message_for_update = f"Ошибка обработки документа: {str(e)}"
        
        # Обновляем запись о процессе под блокировкой (ваш существующий код)
        with self._data_lock:
            entry_to_update = self.process_data.get(process_id)
            if entry_to_update:
                entry_to_update.status_enum = final_status_for_update
                entry_to_update.error_message_detail = final_error_message_for_update
                entry_to_update.document_structure = processed_document_structure
                if final_status_for_update == ProcessStatus.DONE:
                    entry_to_update.seller = local_seller
                    entry_to_update.buyer = local_buyer
                    entry_to_update.buyer_org_data = local_buyer_org_data 
                    entry_to_update.period = local_period
                    entry_to_update.debit_seller = local_debit_seller
                    entry_to_update.credit_seller = local_credit_seller
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
                status=ProcessStatus.NOT_FOUND.value, 
                message="Процесс с указанным ID не найден."
            ).model_dump()

        if process_entry.status_enum == ProcessStatus.WAIT:
            return StatusResponseModel(
                status=ProcessStatus.WAIT.value,
                message="Документ в обработке, попробуйте позже."
            ).model_dump()
        
        elif process_entry.status_enum == ProcessStatus.ERROR:
            return StatusResponseModel(
                status=ProcessStatus.ERROR.value,
                message=process_entry.error_message_detail or "Произошла ошибка при обработке документа."
            ).model_dump()

        elif process_entry.status_enum == ProcessStatus.DONE:
            if not all([process_entry.seller, process_entry.buyer, process_entry.period]):
                 # Если основные данные не извлечены, но статус DONE, возвращаем ошибку или специальный статус
                 self.logger.warning(f"get_process_status: Неполные данные для DONE статуса ID {process_id}. Продавец: {process_entry.seller}, Покупатель: {process_entry.buyer}, Период: {process_entry.period}")
                 # Можно вернуть StatusResponseModel с сообщением о неполных данных
                 return StatusResponseModel(
                    status=ProcessStatus.ERROR.value, # Или другой статус, например, кастомный "PARTIALLY_DONE"
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
                status=ProcessStatus.DONE.value,
                message="Документ успешно обработан.",
                seller=process_entry.seller, # Гарантированно не None из-за проверки выше
                buyer=process_entry.buyer,   # Гарантированно не None
                period=process_entry.period, # Гарантированно не None
                debit=process_entry.debit_seller, # Пока только данные продавца
                credit=process_entry.credit_seller # Пока только данные продавца
            )
            return response_data.model_dump(by_alias=True)

        # На случай, если появится новый статус, который не обработан
        return StatusResponseModel(
            status=ProcessStatus.ERROR.value,
            message="Неизвестный статус процесса."
        ).model_dump()

        target_cell = None
    
    def fill_reconciliation_act(self, request: FillReconciliationActRequestModel) -> bytes:
        """
        Заполняет акт сверки на основе предоставленных данных.
        Заполняет только те ячейки, где значения отличаются.
        Возвращает PDF в виде байтов.
        """
        process_id = request.process_id
        with self._data_lock:
            process_entry = self.process_data.get(process_id)
        if not process_entry:
            raise ValueError(f"Процесс с ID {process_id} не найден.")
        if process_entry.status_enum != ProcessStatus.DONE:
            raise ValueError(f"Невозможно заполнить акт сверки для процесса с ID {process_id}, статус: {process_entry.status_enum.name}.")

        doc:Document = process_entry.document_structure

        # Получаем изображения страниц
        images = convert_to_pil(doc.pdf_bytes)
        tables: list[Table] = doc.get_tables()
        render_images = images.copy()

        # Получаем значения из оригинального документа для buyer (по новым правилам)
        ner_service = NERService(doc)
        buyer_extracted = ner_service.extract_buyer_reconciliation_details(process_entry.buyer_org_data)
        # buyer_extracted: dict с debit_entries_data и credit_entries_data
        buyer_debit = {(d['ner_table_idx'], d['ner_row_idx'], d['ner_col_idx']): d for d in buyer_extracted.get('debit_entries_data', [])}
        buyer_credit = {(d['ner_table_idx'], d['ner_row_idx'], d['ner_col_idx']): d for d in buyer_extracted.get('credit_entries_data', [])}

        # Объединяем все записи для заполнения: debit и credit
        all_entries = [(entry, 'debit') for entry in request.debit] + [(entry, 'credit') for entry in request.credit]

        for entry, entry_type in all_entries:
            table_idx = entry.row_id.id_table
            row_idx = entry.row_id.id_row
            value = entry.value
            # Определяем индекс колонки
            if entry_type == 'debit':
                # Найти col по buyer_debit
                key = next((k for k in buyer_debit if k[0] == table_idx and k[1] == row_idx), None)
                if not key:
                    continue
                col_idx = key[2]
                orig_val = buyer_debit[key]['value']
            else:
                key = next((k for k in buyer_credit if k[0] == table_idx and k[1] == row_idx), None)
                if not key:
                    continue
                col_idx = key[2]
                orig_val = buyer_credit[key]['value']

            # Сравниваем значения
            if float(orig_val) == float(value):
                continue  # Не заполняем, если значения совпадают

            # Найти таблицу и ячейку
            if table_idx >= len(tables):
                continue
            table = tables[table_idx]
            cell = next((c for c in table.cells if c.row == row_idx and c.col == col_idx), None)
            if not cell:
                continue
            # Определить страницу
            page_num = cell.original_page_num if cell.original_page_num is not None else table.start_page_num
            if page_num is None or page_num >= len(render_images):
                continue
            img = render_images[page_num]
            font_size = int(table.average_blob_height)
            # преобразуем значение строки в денежный формат 10 000,00
            value = f"{value:,.2f}".replace(',', ' ').replace('.', ',')
            # Вписываем новое значение
            render_images[page_num] = draw_text_to_cell(img, cell, value, font_size=font_size)

        self.logger.info(f"(_fill_reconciliation_act) Акт сверки успешно заполнен для ID: {process_id}.")
        filled_pdf_bytes = convert_to_bytes(render_images)
        return filled_pdf_bytes

    def shutdown(self):
        """
        Корректно останавливает ThreadPoolExecutor.
        Рекомендуется вызывать при завершении работы приложения.
        """
        self.logger.info("Запрос на остановку ReconciliationActService. Ожидание завершения активных задач...")
        self.executor.shutdown(wait=True)
        self.logger.info("ThreadPoolExecutor успешно остановлен.")



