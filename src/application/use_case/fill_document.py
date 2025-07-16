import logging
from typing import List, Dict, Any

from ..dto.process_dto import FillDocumentDto
from ...domain.value_objects.process_id import ProcessId
from ...domain.interfaces.process_repository import IProcessRepository
from ...exceptions import ProcessIdNotFoundError
from ...NER.ner_service import NERService
from ...pdf_renderer import convert_to_pil, convert_to_bytes, draw_text_to_cell_with_context, get_row_context


class FillDocumentUseCase:
    """Случай использования: заполнение документа данными"""
    
    def __init__(self, process_repository: IProcessRepository):
        self._process_repository = process_repository
        self._logger = logging.getLogger(f"app.{self.__class__.__name__}")
    
    async def execute(self, dto: FillDocumentDto) -> bytes:
        """Заполняет документ и возвращает PDF в байтах"""
        
        try:
            process_id = ProcessId(value=dto.process_id)
        except ValueError as e:
            raise ValueError(f"Некорректный идентификатор процесса: {str(e)}")
        
        # Получаем процесс
        process = await self._process_repository.get_by_id(process_id)
        
        if not process:
            raise ProcessIdNotFoundError(dto.process_id)
        
        if not process.is_completed():
            raise ValueError(f"Процесс {dto.process_id} не завершен или завершен с ошибкой")
        
        try:
            self._logger.info(f"Начало заполнения документа для процесса: {process_id}")
            
            # Получаем структуру документа
            document_structure = process.document_structure
            if not document_structure:
                raise ValueError("Структура документа не найдена")
            
            # Получаем изображения страниц
            images = convert_to_pil(document_structure.pdf_bytes)
            tables = self._get_tables_from_structure(document_structure)
            render_images = images.copy()
            
            # Получаем данные покупателя для сравнения - ИСПРАВЛЯЕМ ЭТОТ МЕТОД
            buyer_data = self._extract_buyer_data(tables, process.buyer.raw_data)
            
            # Заполняем ячейки
            filled_count = self._fill_cells(
                debit_entries=dto.debit_entries,
                credit_entries=dto.credit_entries,
                buyer_data=buyer_data,
                tables=tables,
                render_images=render_images
            )
            
            self._logger.info(f"Заполнено {filled_count} ячеек для процесса: {process_id}")
            
            # Конвертируем обратно в PDF
            filled_pdf_bytes = convert_to_bytes(render_images)
            
            return filled_pdf_bytes
            
        except Exception as e:
            self._logger.exception(f"Ошибка при заполнении документа для процесса {process_id}")
            
            # Обновляем статус процесса на ERROR
            try:
                process.mark_as_failed(f"Ошибка заполнения документа: {str(e)}")
                await self._process_repository.update(process)
            except Exception as update_error:
                self._logger.error(f"Не удалось обновить статус процесса: {update_error}")
            
            raise RuntimeError(f"Ошибка при заполнении документа: {str(e)}")
    
    def _get_tables_from_structure(self, document_structure) -> List[Any]:
        """Извлекает таблицы из структуры документа"""

        if hasattr(document_structure, 'tables') and document_structure.tables:
            # Если в metadata есть сохраненные таблицы, используем их
            return document_structure.tables
        else:
            # Fallback - пересоздаем из PDF
            from ...PDFExtractor.scan_extractor import ScanExtractor
            extractor = ScanExtractor()
            temp_doc = extractor.extract(document_structure.pdf_bytes)
            return temp_doc.get_tables()
    
    def _extract_buyer_data(self, tables: List[Any], buyer_raw_data: Dict[str, Any]) -> Dict[str, Dict]:
        """Извлекает данные покупателя из документа"""
        try:
            # ИСПРАВЛЯЕМ - создаем Document с правильными таблицами
            from ...PDFExtractor.base_extractor import Document
            
            # Создаем временный Document для NER, но передаем существующие таблицы
            class TempDocument:
                def __init__(self, pdf_bytes: bytes, tables: List[Any]):
                    self.pdf_bytes = pdf_bytes
                    self._tables = tables
                
                def get_tables(self):
                    return self._tables
            
            temp_doc = TempDocument(pdf_bytes=None, tables=tables)  # PDF bytes не нужны для NER
            
            ner_service = NERService(temp_doc)
            buyer_extracted = ner_service.extract_buyer_reconciliation_details(buyer_raw_data)
            
            buyer_debit = {
                (d['ner_table_idx'], d['ner_row_idx'], d['ner_col_idx']): d 
                for d in buyer_extracted.get('debit_entries_data', [])
            }
            
            buyer_credit = {
                (d['ner_table_idx'], d['ner_row_idx'], d['ner_col_idx']): d 
                for d in buyer_extracted.get('credit_entries_data', [])
            }
            
            self._logger.debug(f"Извлечено данных покупателя - дебет: {len(buyer_debit)}, кредит: {len(buyer_credit)}")
            
            return {
                'debit': buyer_debit,
                'credit': buyer_credit
            }
            
        except Exception as e:
            self._logger.error(f"Ошибка при извлечении данных покупателя: {e}")
            return {'debit': {}, 'credit': {}}
    
    def _fill_cells(
        self,
        debit_entries: List[dict],
        credit_entries: List[dict],
        buyer_data: Dict[str, Dict],
        tables: List[Any],
        render_images: List[Any]
    ) -> int:
        """Заполняет ячейки документа"""
        
        filled_count = 0
        buyer_debit = buyer_data['debit']
        buyer_credit = buyer_data['credit']
        
        self._logger.debug(f"Начало заполнения: debit_entries={len(debit_entries)}, credit_entries={len(credit_entries)}")
        self._logger.debug(f"Данные покупателя: buyer_debit={len(buyer_debit)}, buyer_credit={len(buyer_credit)}")
        
        # Объединяем все записи для заполнения
        all_entries = [
            (entry, 'debit', buyer_debit) for entry in debit_entries
        ] + [
            (entry, 'credit', buyer_credit) for entry in credit_entries
        ]
        
        for entry, entry_type, buyer_lookup in all_entries:
            try:
                if self._fill_single_cell(entry, entry_type, buyer_lookup, tables, render_images):
                    filled_count += 1
            except Exception as e:
                self._logger.error(f"Ошибка при заполнении ячейки {entry_type}: {e}")
                continue
        
        return filled_count
    
    def _fill_single_cell(
        self,
        entry: dict,
        entry_type: str,
        buyer_lookup: Dict[tuple, Dict],
        tables: List[Any],
        render_images: List[Any]
    ) -> bool:
        """Заполняет одну ячейку с учетом контекста строки."""
        
        # Извлекаем данные из entry
        row_id = entry.get('row_id', {})
        table_idx = row_id.get('id_table', 0)
        row_idx = row_id.get('id_row', 0)
        value = entry.get('value', 0.0)
        
        self._logger.debug(f"Попытка заполнить {entry_type} [{table_idx}, {row_idx}] значением {value}")
        
        # Находим координаты колонки в данных покупателя
        key = next(
            (k for k in buyer_lookup if k[0] == table_idx and k[1] == row_idx),
            None
        )
        
        if not key:
            # ИСПРАВЛЯЕМ логирование - показываем доступные ключи для отладки
            available_keys = list(buyer_lookup.keys())[:5]  # Первые 5 для отладки
            self._logger.warning(f"Не найдена ячейка {entry_type} [{table_idx}, {row_idx}]. Доступные ключи: {available_keys}")
            return False
        
        col_idx = key[2]
        orig_val = buyer_lookup[key]['value']
        
        # Сравниваем значения
        if float(orig_val) == float(value):
            self._logger.debug(f"Значения одинаковы для {entry_type} [{table_idx}, {row_idx}]: {value}")
            return False  # Не заполняем одинаковые значения
        
        # Находим ячейку в таблице
        if table_idx >= len(tables):
            self._logger.warning(f"Индекс таблицы {table_idx} превышает количество {len(tables)}")
            return False
        
        table = tables[table_idx]
        cell = next(
            (c for c in table.cells if c.row == row_idx and c.col == col_idx),
            None
        )
        
        if not cell:
            self._logger.warning(f"Ячейка не найдена [{table_idx}, {row_idx}, {col_idx}]")
            return False
        
        # Определяем страницу
        page_num = getattr(cell, 'original_page_num', None) or getattr(table, 'start_page_num', 0)
        if page_num is None or page_num >= len(render_images):
            self._logger.warning(f"Некорректная страница {page_num}")
            return False
        
        # НОВОЕ: Получаем контекст строки
        row_cells = get_row_context(cell, tables)
        
        # Заполняем ячейку с учетом контекста
        img = render_images[page_num]
        font_size = getattr(table, 'average_blob_height', 24)
        if hasattr(table, 'average_blob_height') and table.average_blob_height:
            font_size = int(table.average_blob_height)
        
        formatted_value = f"{value:,.2f}".replace(',', ' ').replace('.', ',')
        
        # ИЗМЕНЕНО: Используем новую функцию с контекстом
        render_images[page_num] = draw_text_to_cell_with_context(
            img, cell, formatted_value, font_size, row_cells
        )
        
        self._logger.debug(f"Успешно заполнена ячейка {entry_type} [{table_idx}, {row_idx}, {col_idx}] значением {formatted_value} с учетом контекста строки")
        
        return True