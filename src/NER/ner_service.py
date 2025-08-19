
import logging
from typing import Optional

from .reconc_act_extractor import ReconciliationActExtractor
from .organization_processor import OrganizationProcessor
from .org_extractor import Org, Roles, RegexRoleExtractor, to_label
from ..PDFExtractor.base_extractor import Document



class NERService:
    """
    Сервис для извлечения именованных сущностей и обработки специфичных документов.
    """
    def __init__(self, doc_structure: Document):
        self.doc = doc_structure

        self.organization_processor = RegexRoleExtractor()
        self.reconciliation_extractor = ReconciliationActExtractor(self.doc)
        self._organizations: Roles = None
        self._seller_details: Optional[list[dict]] = None
    
    # @property
    # def get_seller_info(self) -> Optional[dict]:
    #     """Возвращает информацию о продавце, если она была извлечена."""
    #     return next((org for org in self._organizations if org.get('role') == 'продавец'), None)

    # @property
    # def get_buyer_info(self) -> Optional[dict]:
    #     """Возвращает информацию о покупателе, если она была извлечена."""
    #     return next((org for org in self._organizations if org.get('role') == 'покупатель'), None)

    @property
    def get_seller_name(self) -> Optional[str]:
        """Возвращает имя продавца, если оно было извлечено."""
        return to_label(self._organizations.seller)
    
    @property
    def get_buyer_name(self) -> Optional[str]:
        """Возвращает имя покупателя, если оно было извлечено."""
        return to_label(self._organizations.buyer)

    def find_document_organizations(self) -> Roles:
        """Извлекает организации из всего текста документа."""
        paragraph_text = self.doc.get_all_text_paragraphs()
        # table_text = self.doc.get_first_row_tables_text()
        # full_text = table_text + "\n" + paragraph_text
        # print(paragraph_text)
        self._organizations = self.organization_processor.assign(paragraph_text)
        return self._organizations

    def extract_seller_reconciliation_details(self, seller_name: str) -> dict:
        """Извлекает данные акта сверки для указанного продавца."""
        return self.reconciliation_extractor.extract_for_seller(seller_name)

    def extract_buyer_reconciliation_details(self, buyer_name: str) -> dict:
        """Извлекает структурную информацию о таблице покупателя для последующего заполнения."""
        return self.reconciliation_extractor.extract_for_buyer(buyer_name)