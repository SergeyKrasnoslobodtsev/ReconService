import pytest

import common_test

from src.init import ServiceInitialize
from src.NER.ner_service import NERService
from src.PDFExtractor.scan_extractor import ScanExtractor


@pytest.fixture
def extractors():
    ServiceInitialize.initialize()
    pdf_bytes = common_test.get_pdf_scan()
    document = ScanExtractor().extract(pdf_bytes)
    return NERService(document)



def test_find_document_organizations(extractors):
    """
    Тест извлечения организаций из документа.
    """

    organizations = extractors.find_document_organizations()
    assert isinstance(organizations, list), "Результат должен быть списком"
    assert len(organizations) > 0, "Список организаций не должен быть пустым"

def test_extract_seller_reconciliation_details(extractors):
    """
    Тест извлечения данных акта сверки для продавца.
    """
    organizations = extractors.find_document_organizations()

    assert len(organizations) > 0, "Список организаций должен содержать хотя бы одну организацию"
    seller = next((org for org in organizations if org.get('role') == 'продавец'), None)
    assert seller is not None, "Продавец не найден"

    reconciliation_details = extractors.extract_seller_reconciliation_details(seller)
    