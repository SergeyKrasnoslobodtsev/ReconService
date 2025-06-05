import logging
import logging.config
import os
import threading 
from concurrent.futures import ThreadPoolExecutor
import yaml
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import time

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
    
    def __init__(self, process_ttl_hours: int = 1, cleanup_interval_hours: int = 0.5):
        self.logger = logging.getLogger("app." + __name__)

        self.process_data: Dict[str, InternalProcessDataModel] = {} 
        self._data_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=2) 

        self.process_ttl = timedelta(hours=process_ttl_hours)
        self.cleanup_interval = timedelta(hours=cleanup_interval_hours)

        self._start_cleanup_task()

    def _start_cleanup_task(self):
        """Запускает фоновую задачу для периодической очистки старых процессов."""
        def cleanup_worker():
            while not getattr(self, '_shutdown_requested', False):
                try:
                    time.sleep(self.cleanup_interval.total_seconds())
                    self._cleanup_old_processes()
                except Exception as e:
                    self.logger.error(f"Ошибка в задаче очистки процессов: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True, name="ProcessCleanup")
        cleanup_thread.start()
        self.logger.info(f"Запущена фоновая задача очистки процессов (интервал: {self.cleanup_interval.total_seconds()}s, TTL: {self.process_ttl.total_seconds()}s)")

    def _cleanup_old_processes(self):
        """Удаляет процессы старше TTL."""
        current_time = datetime.now()
        processes_to_remove = []
        
        with self._data_lock:
            for process_id, process_data in self.process_data.items():
                # Проверяем время создания процесса
                if hasattr(process_data, 'created_at'):
                    if current_time - process_data.created_at > self.process_ttl:
                        processes_to_remove.append(process_id)
                else:
                    # Для старых процессов без created_at - удаляем сразу
                    processes_to_remove.append(process_id)
            
            # Удаляем старые процессы
            for process_id in processes_to_remove:
                del self.process_data[process_id]
                self.logger.info(f"Процесс {process_id} удален по TTL")
        
        if processes_to_remove:
            self.logger.info(f"Очищено {len(processes_to_remove)} старых процессов")

    def _generate_process_id(self) -> str:
        """
        Генерирует уникальный идентификатор процесса.
        """
        return str(uuid.uuid4())
    

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
        final_status_for_update = ProcessStatus.ERROR
        final_error_message_for_update: Optional[str] = None
        processed_document_structure: Optional[Document] = None

        try:
            self.logger.info(f"(_process_document) Начало обработки PDF для ID: {process_id}")
            
            # Извлекаем структуру документа
            extractor = ScanExtractor() 
            processed_document_structure = extractor.extract(pdf_bytes)
            self.logger.info(f"(_process_document) Структура документа извлечена для ID: {process_id}")

            # Инициализируем NER сервис и извлекаем организации
            ner_service = NERService(processed_document_structure) 
            ner_service.find_document_organizations()
            
            # Проверяем наличие продавца
            if not ner_service.get_seller_info:
                final_error_message_for_update = "Информация о продавце не найдена в документе."
                self.logger.error(f"(_process_document) {final_error_message_for_update} для ID: {process_id}")
                return
            
            # Проверяем наличие покупателя
            if not ner_service.get_buyer_info:
                final_error_message_for_update = "Информация о покупателе не найдена в документе."
                self.logger.error(f"(_process_document) {final_error_message_for_update} для ID: {process_id}")
                return
                
            self.logger.info(f"(_process_document) Продавец: {ner_service.get_seller_name}, Покупатель: {ner_service.get_buyer_name} для ID: {process_id}")

            # Извлекаем детали сверки продавца
            reconciliation_output = ner_service.extract_seller_reconciliation_details(ner_service.get_seller_info)
            if not reconciliation_output:
                final_error_message_for_update = "NERService не вернул деталей сверки для продавца."
                self.logger.error(f"(_process_document) {final_error_message_for_update} для ID: {process_id}")
                return

            # Проверяем период сверки
            period_from = reconciliation_output.get('period_from')
            period_to = reconciliation_output.get('period_to')

            local_period = None
            if period_from and period_to:
                local_period = PeriodModel(from_date=period_from, to_date=period_to)
                self.logger.info(f"(_process_document) Период акта сверки извлечен: {local_period.model_dump_json(by_alias=True)} для ID: {process_id}")
            else:
                local_period = PeriodModel(from_date="None", to_date="None")
                self.logger.info(f"(_process_document) Период сверки не найден для ID: {process_id}")

            # Преобразуем данные дебета/кредита
            debit_entries_data = reconciliation_output.get('debit_entries_data', [])
            credit_entries_data = reconciliation_output.get('credit_entries_data', [])
            
            local_debit_seller = self._transform_ner_table_data_to_act_entries(debit_entries_data)
            local_credit_seller = self._transform_ner_table_data_to_act_entries(credit_entries_data)
            self.logger.info(f"(_process_document) Данные по дебету/кредиту продавца извлечены для ID: {process_id}")

            # Все данные успешно извлечены
            final_status_for_update = ProcessStatus.DONE
            final_error_message_for_update = None

        except Exception as e:
            self.logger.exception(f"(_process_document) Ошибка при обработке документа для ID {process_id}: {e}")
            final_error_message_for_update = f"Ошибка обработки документа: {str(e)}"
        
        finally:
            # Обновляем запись о процессе под блокировкой
            self._update_process_entry(
                process_id=process_id,
                status=final_status_for_update,
                error_message=final_error_message_for_update,
                document_structure=processed_document_structure,
                ner_service=ner_service if final_status_for_update == ProcessStatus.DONE else None,
                period=local_period if final_status_for_update == ProcessStatus.DONE else None,
                debit_seller=local_debit_seller if final_status_for_update == ProcessStatus.DONE else [],
                credit_seller=local_credit_seller if final_status_for_update == ProcessStatus.DONE else []
            )

    def _update_process_entry(
        self, 
        process_id: str, 
        status: ProcessStatus, 
        error_message: Optional[str],
        document_structure: Optional[Document],
        ner_service: Optional[NERService] = None,
        period: Optional[PeriodModel] = None,
        debit_seller: List[ActEntryModel] = None,
        credit_seller: List[ActEntryModel] = None
    ) -> None:
        """Обновляет запись о процессе обработки документа."""
        with self._data_lock:
            entry_to_update = self.process_data.get(process_id)
            if not entry_to_update:
                self.logger.error(f"(_update_process_entry) Запись о процессе с ID {process_id} не найдена для обновления статуса.")
                return

            entry_to_update.status_enum = status
            entry_to_update.error_message_detail = error_message
            entry_to_update.document_structure = document_structure
            
            if status == ProcessStatus.DONE and ner_service:
                entry_to_update.seller = ner_service.get_seller_name
                entry_to_update.buyer = ner_service.get_buyer_name
                entry_to_update.buyer_org_data = ner_service.get_buyer_info
                entry_to_update.period = period
                entry_to_update.debit_seller = debit_seller or []
                entry_to_update.credit_seller = credit_seller or []
            
            self.logger.info(f"(_update_process_entry) Завершение обработки для ID: {process_id}. Статус: {status.name}")

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
            if not all([process_entry.seller, process_entry.buyer]):
                 # Если основные данные не извлечены, но статус DONE, возвращаем ошибку или специальный статус
                 self.logger.warning(f"get_process_status: Неполные данные для DONE статуса ID {process_id}. Продавец: {process_entry.seller}, Покупатель: {process_entry.buyer}, Период: {process_entry.period}")
                 # Можно вернуть StatusResponseModel с сообщением о неполных данных
                 return StatusResponseModel(
                    status=ProcessStatus.ERROR.value, 
                    message="Документ обработан, но не все ключевые данные удалось извлечь."
                 ).model_dump()

            # Формируем ReconciliationActResponseModel
            response_data = ReconciliationActResponseModel(
                process_id=process_entry.process_id,
                status=ProcessStatus.DONE.value,
                message="Документ успешно обработан.",
                seller=process_entry.seller, # Гарантированно не None из-за проверки выше
                buyer=process_entry.buyer,   # Гарантированно не None
                period=process_entry.period, # Может быть None
                debit=process_entry.debit_seller, # Пока только данные продавца
                credit=process_entry.credit_seller # Пока только данные продавца 
            )
            return response_data.model_dump(by_alias=True)

        # На случай, если появится новый статус, который не обработан
        return StatusResponseModel(
            status=ProcessStatus.ERROR.value,
            message="Неизвестный статус процесса."
        ).model_dump()

    
    def fill_reconciliation_act(self, request: FillReconciliationActRequestModel) -> bytes:
        """
        Заполняет акт сверки на основе предоставленных данных.
        Заполняет только те ячейки, где значения отличаются.
        Возвращает PDF в виде байтов.
        """
        process_id = request.process_id
        
        try:
            # Получаем процесс под блокировкой
            with self._data_lock:
                process_entry = self.process_data.get(process_id)
            
            if not process_entry:
                error_msg = f"Процесс с ID {process_id} не найден."
                self.logger.error(f"(fill_reconciliation_act) {error_msg}")
                raise ValueError(error_msg)
            
            if process_entry.status_enum != ProcessStatus.DONE:
                error_msg = f"Невозможно заполнить акт сверки для процесса с ID {process_id}, статус: {process_entry.status_enum.name}."
                self.logger.error(f"(fill_reconciliation_act) {error_msg}")
                raise ValueError(error_msg)

            self.logger.info(f"(fill_reconciliation_act) Начало заполнения акта сверки для ID: {process_id}")

            doc: Document = process_entry.document_structure

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

            filled_cells_count = 0
            
            for entry, entry_type in all_entries:
                try:
                    table_idx = entry.row_id.id_table
                    row_idx = entry.row_id.id_row
                    value = entry.value
                    
                    # Определяем индекс колонки
                    if entry_type == 'debit':
                        # Найти col по buyer_debit
                        key = next((k for k in buyer_debit if k[0] == table_idx and k[1] == row_idx), None)
                        if not key:
                            self.logger.warning(f"(fill_reconciliation_act) Не найдена ячейка debit для таблицы {table_idx}, строки {row_idx}")
                            continue
                        col_idx = key[2]
                        orig_val = buyer_debit[key]['value']
                    else:
                        key = next((k for k in buyer_credit if k[0] == table_idx and k[1] == row_idx), None)
                        if not key:
                            self.logger.warning(f"(fill_reconciliation_act) Не найдена ячейка credit для таблицы {table_idx}, строки {row_idx}")
                            continue
                        col_idx = key[2]
                        orig_val = buyer_credit[key]['value']

                    # Сравниваем значения
                    if float(orig_val) == float(value):
                        continue  # Не заполняем, если значения совпадают

                    # Найти таблицу и ячейку
                    if table_idx >= len(tables):
                        self.logger.warning(f"(fill_reconciliation_act) Индекс таблицы {table_idx} превышает количество таблиц {len(tables)}")
                        continue
                    
                    table = tables[table_idx]
                    cell = next((c for c in table.cells if c.row == row_idx and c.col == col_idx), None)
                    if not cell:
                        self.logger.warning(f"(fill_reconciliation_act) Не найдена ячейка таблицы {table_idx}, строка {row_idx}, колонка {col_idx}")
                        continue
                    
                    # Определить страницу
                    page_num = cell.original_page_num if cell.original_page_num is not None else table.start_page_num
                    if page_num is None or page_num >= len(render_images):
                        self.logger.warning(f"(fill_reconciliation_act) Некорректный номер страницы {page_num} для ячейки")
                        continue
                    
                    img = render_images[page_num]
                    font_size = int(table.average_blob_height) if hasattr(table, 'average_blob_height') else 24
                    
                    formatted_value = f"{value:,.2f}".replace(',', ' ').replace('.', ',')
                    
                    # Вписываем новое значение
                    render_images[page_num] = draw_text_to_cell(img, cell, formatted_value, font_size=font_size)
                    filled_cells_count += 1
                    
                except Exception as cell_error:
                    self.logger.error(f"(fill_reconciliation_act) Ошибка при заполнении ячейки {entry_type} таблицы {table_idx}, строки {row_idx}: {cell_error}")
                    continue

            self.logger.info(f"(fill_reconciliation_act) Заполнено {filled_cells_count} ячеек для ID: {process_id}")
            
            # Конвертируем обратно в PDF
            filled_pdf_bytes = convert_to_bytes(render_images)
            
            self.logger.info(f"(fill_reconciliation_act) Акт сверки успешно заполнен для ID: {process_id}")

            
            return filled_pdf_bytes
            
        except Exception as e:
            # Неожиданные ошибки при заполнении
            error_msg = f"Ошибка при заполнении акта сверки: {str(e)}"
            self.logger.exception(f"(fill_reconciliation_act) {error_msg} для ID: {process_id}")
            
            # Обновляем статус процесса на ERROR
            with self._data_lock:
                process_entry = self.process_data.get(process_id)
                if process_entry:
                    process_entry.status_enum = ProcessStatus.ERROR
                    process_entry.error_message_detail = error_msg
                    self.logger.info(f"(fill_reconciliation_act) Статус процесса {process_id} изменен на ERROR")
            
            raise RuntimeError(error_msg)

    def shutdown(self):
        """
        Корректно останавливает ThreadPoolExecutor.
        Рекомендуется вызывать при завершении работы приложения.
        """
        self.logger.info("Запрос на остановку ReconciliationActService. Ожидание завершения активных задач...")
        self.executor.shutdown(wait=True)
        self.logger.info("ThreadPoolExecutor успешно остановлен.")



