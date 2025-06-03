
import logging
from typing import Optional

from .reconc_act_extractor import ReconciliationActExtractor
from .organization_processor import OrganizationProcessor
from ..PDFExtractor.base_extractor import Document


class NERService:
    """
    Сервис для извлечения именованных сущностей и обработки специфичных документов.
    """
    def __init__(self, doc_structure: Document):
        self.doc = doc_structure
        self.logger = logging.getLogger('app.' + self.__class__.__name__)
        self.organization_processor = OrganizationProcessor(self.logger)
        self.reconciliation_extractor = ReconciliationActExtractor(self.doc, self.logger)

    def find_document_organizations(self) -> list[dict]:
        """Извлекает организации из всего текста документа."""
        full_text = self.doc.get_all_text_paragraphs()
        if not full_text:
            self.logger.warning("Документ не содержит текста для анализа организаций.")
            return []
        return self.organization_processor.process_text(full_text)

    def extract_seller_reconciliation_details(self, seller_info: dict) -> list[dict]:
        """Извлекает данные акта сверки для указанного продавца."""
        if not seller_info:
            self.logger.warning("Информация о продавце не предоставлена.")
            return []
        return self.reconciliation_extractor.extract_for_seller(seller_info)

    def extract_buyer_reconciliation_details(self, buyer_info: dict) -> dict:
        """Извлекает структурную информацию о таблице покупателя для последующего заполнения."""
        if not buyer_info:
            self.logger.warning("Информация о покупателе не предоставлена для определения структуры таблицы.")
            return []

        return self.reconciliation_extractor.extract_for_buyer(buyer_info)