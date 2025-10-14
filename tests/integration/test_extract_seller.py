import pytest

import common_test


from src.NER.ner_service import NERService
from src.PDFExtractor.scan_extractor import ScanExtractor


@pytest.fixture
def extractors():

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
    print("Извлеченные организации:"
          f"\nПродавец: {extractors.get_seller_name}"
          f"\nПокупатель: {extractors.get_buyer_name}")


    