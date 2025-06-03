
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
        self._organizations: Optional[list[dict]] = None
        self._seller_details: Optional[list[dict]] = None
    
    @property
    def get_seller_info(self) -> Optional[dict]:
        """Возвращает информацию о продавце, если она была извлечена."""
        return next((org for org in self._organizations if org.get('role') == 'продавец'), None)

    @property
    def get_buyer_info(self) -> Optional[dict]:
        """Возвращает информацию о покупателе, если она была извлечена."""
        return next((org for org in self._organizations if org.get('role') == 'покупатель'), None)

    @property
    def get_seller_name(self) -> Optional[str]:
        """Возвращает имя продавца, если оно было извлечено."""
        info = next((org for org in self._organizations if org.get('role') == 'продавец'), None)
        return info.get('str_repr') if info else None
    
    @property
    def get_buyer_name(self) -> Optional[str]:
        """Возвращает имя покупателя, если оно было извлечено."""
        info = next((org for org in self._organizations if org.get('role') == 'покупатель'), None)
        return info.get('str_repr') if info else None

    def find_document_organizations(self) -> list[dict]:
        """Извлекает организации из всего текста документа."""
        full_text = self.doc.get_all_text_paragraphs()
        self._organizations = self.organization_processor.process_text(full_text)
        return self._organizations

    def extract_seller_reconciliation_details(self, seller_info: dict) -> dict:
        """Извлекает данные акта сверки для указанного продавца."""
        return self.reconciliation_extractor.extract_for_seller(seller_info)

    def extract_buyer_reconciliation_details(self, buyer_info: dict) -> dict:
        """Извлекает структурную информацию о таблице покупателя для последующего заполнения."""
        return self.reconciliation_extractor.extract_for_buyer(buyer_info)