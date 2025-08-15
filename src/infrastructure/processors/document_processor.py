import logging
from datetime import datetime
from typing import Optional

from ...application.interfaces.document_processor import IDocumentProcessor
from ...application.dto.process_dto import DocumentProcessingResultDto
from ...PDFExtractor.scan_extractor import ScanExtractor
from ...NER.ner_service import NERService


class DocumentProcessor(IDocumentProcessor):
    """Инфраструктурная реализация процессора документов"""
    
    def __init__(self):
        self._logger = logging.getLogger(f"app.{self.__class__.__name__}")
    
    async def process(self, pdf_bytes: bytes) -> DocumentProcessingResultDto:
        """Обрабатывает PDF документ и возвращает результат"""
        
        try:
            self._logger.info("Начало обработки PDF документа")
            
            # Извлечение структуры документа
            self._logger.debug("Извлечение структуры документа...")
            extractor = ScanExtractor()
            document_structure = extractor.extract(pdf_bytes)
            
            if not document_structure:
                return DocumentProcessingResultDto(
                    success=False,
                    error_message="Не удалось извлечь структуру документа"
                )
            
            self._logger.debug("Структура документа извлечена успешно")
            
            # NER-анализ
            self._logger.debug("Начало NER-анализа...")
            ner_service = NERService(document_structure)
            ner_service.find_document_organizations()
            
            # Проверка организаций
            if not ner_service.get_seller_info:
                return DocumentProcessingResultDto(
                    success=False,
                    error_message="Информация о продавце не найдена в документе"
                )
            
            if not ner_service.get_buyer_info:
                return DocumentProcessingResultDto(
                    success=False,
                    error_message="Информация о покупателе не найдена в документе"
                )
            
            self._logger.debug(f"Найдены организации - Продавец: {ner_service.get_seller_name}, Покупатель: {ner_service.get_buyer_name}")
            
            # Извлечение деталей сверки
            self._logger.debug("Извлечение деталей сверки...")
            reconciliation_data = ner_service.extract_seller_reconciliation_details(
                ner_service.get_seller_info
            )
            
            if not reconciliation_data:
                return DocumentProcessingResultDto(
                    success=False,
                    error_message="Не удалось извлечь детали сверки продавца"
                )
            
            # Извлечение периода
            period_from = reconciliation_data.get('period_from')
            period_to = reconciliation_data.get('period_to')
            
            # Извлечение записей дебета/кредита
            debit_entries = reconciliation_data.get('debit_entries_data', [])
            credit_entries = reconciliation_data.get('credit_entries_data', [])
            
            if not debit_entries:
                return DocumentProcessingResultDto(
                    success=False,
                    error_message="Не удалось извлечь данные дебета продавца"
                )
            
            if not credit_entries:
                return DocumentProcessingResultDto(
                    success=False,
                    error_message="Не удалось извлечь данные кредита продавца"
                )
            last_page_with_table = document_structure.get_last_page_number_table()
            self._logger.debug(f"Последняя страница с таблицей: {last_page_with_table}")
            document_structure_dict = {
                'tables': document_structure.get_tables(),  # Сохраняем сами объекты таблиц
                'last_page_with_table': last_page_with_table,
                'metadata': {
                    'pages_count': len(getattr(document_structure, 'pages', [])),
                    'extracted_at': str(datetime.now())
                }
            }
            
            self._logger.info("Документ успешно обработан")
            
            return DocumentProcessingResultDto(
                success=True,
                seller_name=ner_service.get_seller_name,
                buyer_name=ner_service.get_buyer_name,
                buyer_raw_data=ner_service.get_buyer_info,
                period_from=period_from,
                period_to=period_to,
                debit_entries=debit_entries,
                credit_entries=credit_entries,
                document_structure=document_structure_dict
            )
            
        except Exception as e:
            self._logger.exception("Ошибка при обработке документа")
            return DocumentProcessingResultDto(
                success=False,
                error_message=f"Внутренняя ошибка обработки: {str(e)}"
            )
    
    def _table_to_dict(self, table) -> dict:
        """Преобразует таблицу в словарь для сериализации"""
        try:
            return {
                'bbox': {
                    'x1': table.bbox.x1,
                    'y1': table.bbox.y1,
                    'x2': table.bbox.x2,
                    'y2': table.bbox.y2
                } if hasattr(table, 'bbox') else None,
                'cells_count': len(table.cells) if hasattr(table, 'cells') else 0,
                'start_page_num': getattr(table, 'start_page_num', None),
                'average_blob_height': getattr(table, 'average_blob_height', None)
            }
        except Exception as e:
            self._logger.warning(f"Ошибка при преобразовании таблицы в словарь: {e}")
            return {'error': str(e)}