"""
Тесты для доменных моделей документа
"""

import pytest
from src.table_detector.document import (
    BBox, Cell, Table, Paragraph, Page, Document,
    InsertionPosition, ParagraphType
)


class TestBBox:
    """Тесты для BBox"""
    
    def test_bbox_creation(self):
        bbox = BBox(x1=10, y1=20, x2=100, y2=200)
        assert bbox.x1 == 10
        assert bbox.y1 == 20
        assert bbox.x2 == 100
        assert bbox.y2 == 200
    
    def test_bbox_properties(self):
        bbox = BBox(x1=10, y1=20, x2=100, y2=120)
        assert bbox.width == 90
        assert bbox.height == 100
        assert bbox.area == 9000
    
    def test_bbox_immutable(self):
        bbox = BBox(x1=10, y1=20, x2=100, y2=120)
        # Проверяем, что нельзя изменить значения
        with pytest.raises(Exception):
            bbox.x1 = 50


class TestCell:
    """Тесты для Cell"""
    
    def test_cell_creation(self):
        bbox = BBox(x1=10, y1=20, x2=100, y2=120)
        cell = Cell(
            bbox=bbox,
            row=0,
            col=0,
            colspan=1,
            rowspan=1,
            text="Test cell"
        )
        assert cell.row == 0
        assert cell.col == 0
        assert cell.text == "Test cell"
        assert cell.has_text
    
    def test_cell_without_text(self):
        bbox = BBox(x1=10, y1=20, x2=100, y2=120)
        cell = Cell(
            bbox=bbox,
            row=0,
            col=0,
            colspan=1,
            rowspan=1
        )
        assert not cell.has_text
    
    def test_cell_with_empty_text(self):
        bbox = BBox(x1=10, y1=20, x2=100, y2=120)
        cell = Cell(
            bbox=bbox,
            row=0,
            col=0,
            colspan=1,
            rowspan=1,
            text="   "
        )
        assert not cell.has_text
    
    def test_free_space_ratio_no_blobs(self):
        bbox = BBox(x1=0, y1=0, x2=100, y2=100)
        cell = Cell(
            bbox=bbox,
            row=0,
            col=0,
            colspan=1,
            rowspan=1
        )
        assert cell.free_space_ratio == 1.0
    
    def test_free_space_ratio_with_blobs(self):
        bbox = BBox(x1=0, y1=0, x2=100, y2=100)
        blob = BBox(x1=0, y1=0, x2=50, y2=50)  # 2500 area
        cell = Cell(
            bbox=bbox,
            row=0,
            col=0,
            colspan=1,
            rowspan=1,
            blobs=[blob]
        )
        # Cell area = 10000, blob area = 2500, free ratio = 0.75
        assert cell.free_space_ratio == 0.75
    
    def test_get_insertion_area(self):
        bbox = BBox(x1=10, y1=20, x2=100, y2=120)
        cell = Cell(
            bbox=bbox,
            row=0,
            col=0,
            colspan=1,
            rowspan=1
        )
        insertion_area = cell.get_insertion_area(InsertionPosition.TOP)
        assert insertion_area.x1 == 12  # 10 + 2 padding
        assert insertion_area.y1 == 22  # 20 + 2 padding
        assert insertion_area.x2 == 98  # 100 - 2 padding
        assert insertion_area.y2 == 118  # 120 - 2 padding


class TestTable:
    """Тесты для Table"""
    
    def test_table_creation(self):
        bbox = BBox(x1=0, y1=0, x2=200, y2=300)
        table = Table(bbox=bbox)
        assert table.bbox == bbox
        assert len(table.cells) == 0
        assert table.column_count == 0
    
    def test_table_with_cells(self):
        bbox = BBox(x1=0, y1=0, x2=200, y2=300)
        
        # Создаем ячейки 2x2
        cells = [
            Cell(bbox=BBox(x1=0, y1=0, x2=100, y2=150), row=0, col=0, colspan=1, rowspan=1),
            Cell(bbox=BBox(x1=100, y1=0, x2=200, y2=150), row=0, col=1, colspan=1, rowspan=1),
            Cell(bbox=BBox(x1=0, y1=150, x2=100, y2=300), row=1, col=0, colspan=1, rowspan=1),
            Cell(bbox=BBox(x1=100, y1=150, x2=200, y2=300), row=1, col=1, colspan=1, rowspan=1),
        ]
        
        table = Table(bbox=bbox, cells=cells)
        assert len(table.cells) == 4
        assert table.column_count == 2
        
        rows = table.rows
        assert len(rows) == 2
        assert len(rows[0]) == 2  # Первая строка
        assert len(rows[1]) == 2  # Вторая строка
    
    def test_table_with_colspan(self):
        bbox = BBox(x1=0, y1=0, x2=300, y2=200)
        
        # Ячейка с colspan=2
        cells = [
            Cell(bbox=BBox(x1=0, y1=0, x2=200, y2=100), row=0, col=0, colspan=2, rowspan=1),
            Cell(bbox=BBox(x1=0, y1=100, x2=100, y2=200), row=1, col=0, colspan=1, rowspan=1),
            Cell(bbox=BBox(x1=100, y1=100, x2=300, y2=200), row=1, col=1, colspan=2, rowspan=1),
        ]
        
        table = Table(bbox=bbox, cells=cells)
        assert table.column_count == 3  # col 0 + colspan 2 = max_col 2, so 3 columns
    
    def test_average_blob_height_empty(self):
        bbox = BBox(x1=0, y1=0, x2=200, y2=300)
        table = Table(bbox=bbox)
        assert table.average_blob_height == 12.0
    
    def test_average_blob_height_with_blobs(self):
        bbox = BBox(x1=0, y1=0, x2=200, y2=300)
        
        blob1 = BBox(x1=0, y1=0, x2=50, y2=10)  # height = 10
        blob2 = BBox(x1=0, y1=0, x2=50, y2=20)  # height = 20
        
        cell = Cell(
            bbox=BBox(x1=0, y1=0, x2=100, y2=150),
            row=0, col=0, colspan=1, rowspan=1,
            blobs=[blob1, blob2]
        )
        
        table = Table(bbox=bbox, cells=[cell])
        # Average = (10 + 20) / 2 + 6 = 15 + 6 = 21
        assert table.average_blob_height == 21.0


class TestParagraph:
    """Тесты для Paragraph"""
    
    def test_paragraph_creation(self):
        bbox = BBox(x1=10, y1=20, x2=100, y2=120)
        paragraph = Paragraph(
            bbox=bbox,
            text="Test paragraph",
            paragraph_type=ParagraphType.HEADER
        )
        assert paragraph.text == "Test paragraph"
        assert paragraph.paragraph_type == ParagraphType.HEADER


class TestPage:
    """Тесты для Page"""
    
    def test_page_creation(self):
        bbox = BBox(x1=0, y1=0, x2=595, y2=842)  # A4 size
        page = Page(bbox=bbox, num_page=1)
        assert page.num_page == 1
        assert len(page.tables) == 0
        assert len(page.paragraphs) == 0


class TestDocument:
    """Тесты для Document"""
    
    def test_document_creation(self):
        pdf_bytes = b"fake pdf content"
        doc = Document(pdf_bytes=pdf_bytes, page_count=1)
        assert doc.pdf_bytes == pdf_bytes
        assert doc.page_count == 1
        assert len(doc.pages) == 0
    
    def test_get_all_text_paragraphs_empty(self):
        pdf_bytes = b"fake pdf content"
        doc = Document(pdf_bytes=pdf_bytes)
        assert doc.get_all_text_paragraphs() == ""
    
    def test_get_all_text_paragraphs_with_content(self):
        pdf_bytes = b"fake pdf content"
        
        # Создаем страницу с параграфами
        bbox = BBox(x1=0, y1=0, x2=595, y2=842)
        paragraphs = [
            Paragraph(bbox=BBox(x1=0, y1=0, x2=100, y2=50), text="First paragraph"),
            Paragraph(bbox=BBox(x1=0, y1=50, x2=100, y2=100), text="Second paragraph"),
        ]
        page = Page(bbox=bbox, paragraphs=paragraphs, num_page=1)
        
        doc = Document(pdf_bytes=pdf_bytes, pages=[page])
        text = doc.get_all_text_paragraphs()
        assert text == "First paragraph\nSecond paragraph"
    
    def test_get_tables_empty(self):
        pdf_bytes = b"fake pdf content"
        doc = Document(pdf_bytes=pdf_bytes)
        assert len(doc.get_tables()) == 0
    
    def test_get_tables_with_content(self):
        pdf_bytes = b"fake pdf content"
        
        # Создаем страницу с таблицами
        bbox = BBox(x1=0, y1=0, x2=595, y2=842)
        table1 = Table(bbox=BBox(x1=0, y1=0, x2=200, y2=100))
        table2 = Table(bbox=BBox(x1=0, y1=100, x2=200, y2=200))
        page = Page(bbox=bbox, tables=[table1, table2], num_page=1)
        
        doc = Document(pdf_bytes=pdf_bytes, pages=[page])
        tables = doc.get_tables()
        assert len(tables) == 2
