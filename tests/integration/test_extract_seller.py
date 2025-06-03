import pytest

import common_test

from src.service import ServiceInitialize
from src.NER.ner_service import NERService
from src.PDFExtractor.scan_extractor import ScanExtractor


@pytest.fixture
def extractors():
    ServiceInitialize.initialize()
    pdf_bytes = common_test.get_pdf_scan()
    document = ScanExtractor().extract(pdf_bytes)
    return NERService(document)



def test_find_document_organizations(extractors: NERService):
    """
    Тест извлечения организаций из документа.
    """
    organizations = extractors.find_document_organizations()

    assert len(organizations) > 0, "Список организаций не должен быть пустым"
    assert extractors.get_seller_info is not None, "Продавец не найден"
    assert extractors.get_buyer_info is not None, "Покупатель не найден"

    assert extractors.get_seller_name is not None, "Имя продавца не найдено"
    assert extractors.get_buyer_name is not None, "Имя покупателя не найдено"

def test_extract_seller_reconciliation_details(extractors: NERService):
    """
    Тест извлечения данных акта сверки для продавца.
    """
    organizations = extractors.find_document_organizations()

    extractors.extract_seller_reconciliation_details(seller_info)

def test_extract_buyer_reconciliation_details(extractors: NERService):
    """
    Тест извлечения данных акта сверки для покупателя.
    """
    organizations = extractors.find_document_organizations()

    assert len(organizations) > 0, "Список организаций должен содержать хотя бы одну организацию"
    buyer = next((org for org in organizations if org.get('role') == 'покупатель'), None)
    assert buyer is not None, "Покупатель не найден"

    reconciliation_details = extractors.extract_buyer_reconciliation_details(buyer)
    assert isinstance(reconciliation_details, dict), "Результат должен быть словарем"
    print(reconciliation_details)
    