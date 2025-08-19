import sys
import os
from pathlib import Path
from typing import Optional


project_root = Path(__file__).parent.parent.parent.resolve()


if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print(f"Добавлен в PYTHONPATH: {project_root}")
import pytest
import conftest
from src.NER.org_extractor import RegexRoleExtractor, to_label
from test_data_ext_organization import TEST_TEXT_LIST
from pullenti.Sdk import Sdk

Sdk.initialize_all() 


@pytest.fixture(scope="module")
def extractor():
    """Provides a single instance of the OrganizationExtractor for all tests."""
    return RegexRoleExtractor()

@pytest.mark.parametrize("test_case", TEST_TEXT_LIST)
def test_extract_organizations(extractor, test_case):
    """
    Tests the extraction and role assignment for each test case.
    """
    roles = extractor.assign(test_case.text_raw)
    pred_s, pred_b = to_label(roles.seller), to_label(roles.buyer)
    print(f"Extracted Seller: {pred_s}, Buyer: {pred_b}")
    print(f"Expected test Seller: {test_case.seller}, Buyer: {test_case.buyer}")
    print(f"Role extracted {roles.seller.name} as {roles.seller.otype}, {roles.buyer.name} as {roles.buyer.otype}")