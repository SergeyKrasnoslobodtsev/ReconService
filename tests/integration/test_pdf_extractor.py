from typing import List, Optional
import pytest 

import common_test


from src.PDFExtractor.scan_extractor import ScanExtractor
from src.PDFExtractor.native_extractor import NativeExtractor
from src.PDFExtractor.base_extractor import BBox, Cell, Page, Table
from src.config import load_config
from src.pdf_renderer import draw_comments_to_bottom_right

def _xyxy(b):
    # всегда int и формат ((x1,y1),(x2,y2)) для PIL
    return (int(b.x1), int(b.y1)), (int(b.x2), int(b.y2))

def _draw_table_visualization(image, page: Page, tables: List[Table]):
    from PIL import ImageDraw
    draw = ImageDraw.Draw(image)
    current_page_idx = page.num_page

    def _union_bbox(cells_on_page: List[Cell]) -> Optional[BBox]:
        if not cells_on_page:
            return None
        x1 = min(c.bbox.x1 for c in cells_on_page)
        y1 = min(c.bbox.y1 for c in cells_on_page)
        x2 = max(c.bbox.x2 for c in cells_on_page)
        y2 = max(c.bbox.y2 for c in cells_on_page)
        return BBox(x1=x1, y1=y1, x2=x2, y2=y2)

    for id_t, logical_table_item in enumerate(tables):
        # Ячейки этой логической таблицы на текущей странице
        table_cells_on_page = [c for c in logical_table_item.cells
                               if getattr(c, 'original_page_num', current_page_idx) == current_page_idx]
        if not table_cells_on_page:
            continue

        # Локальная рамка на текущей странице
        page_bbox = _union_bbox(table_cells_on_page)
        if page_bbox:
            x = logical_table_item.bbox.x1
            y = logical_table_item.bbox.y1
            w = logical_table_item.bbox.x2
            h = logical_table_item.bbox.y2
            draw = common_test.draw_label(draw, f'Table: {id_t} (Pg {logical_table_item.start_page_num})', (x, y))
            draw.rectangle([(x, y), (w, h)], outline='blue', width=3)


        # Отрисовка ячеек и их blob'ов
        for cell in table_cells_on_page:
            cx = cell.bbox.x1
            cy = cell.bbox.y1
            cw = cell.bbox.x2
            ch = cell.bbox.y2
            r = cell.row
            c = cell.col
            draw = common_test.draw_label(draw, f'R{r}:C{c}', (cx, cy + 35))
            draw.rectangle([(cx, cy), (cw, ch)], outline='green', width=2)
            print(f'Page {current_page_idx} - LogicalTable {id_t} - Cell R{r}:C{c} - {cell.text}')

            for line_blob in getattr(cell, 'blobs', []):
                lx = line_blob.x1
                ly = line_blob.y1
                lw = line_blob.x2
                lh = line_blob.y2
                draw.rectangle([(lx, ly), (lw, lh)], outline='red', width=1)


    # Параграфы — без изменений
    for id_p, parag in enumerate(page.paragraphs):
        x = parag.bbox.x1
        y = parag.bbox.y1
        w = parag.bbox.x2
        h = parag.bbox.y2
        draw = common_test.draw_label(draw, f'{parag.type.name}', (x, y + 35))
        draw.rectangle([(x, y), (w, h)], outline='red', width=3)
        print(parag.text)

    image.show()


@pytest.fixture
def extractors():
    load_config()
    extractor_scan = ScanExtractor()
    extractor_native = NativeExtractor()

    return extractor_scan, extractor_native 

comments = """
            По данным АО "РУСАЛ Новокузнецк" на 30.09.2023\n
            задолженность в пользу АО "РУСАЛ Новокузнецк"\n
            составляет 13 755 023,24 руб.\n
            \n
            С разногласиями, протокол разногласий прилагается.\n
            Акт сверки проверен ОУФО ОЦО, ООО "РЦУ".\n
            Исполнитель: Воробьева Оксана Евгеньевна\n
            Дата:29.01.2025
            """

def test_extract_from_scan(extractors): 

    extractor_scan, _ = extractors 
    pdf_bytes = common_test.get_pdf_scan()
    doc = extractor_scan.extract(pdf_bytes)
    images = common_test.convert_to_pil(doc.pdf_bytes) 
    tables = doc.get_tables()
    # получим номер последней страницы с таблицей
    last_page_with_table = doc.get_last_page_number_table()
    print(f'Last page with table: {last_page_with_table} - {doc.page_count}')
    for image, page in zip(images, doc.pages):
        if last_page_with_table == page.num_page:
            image = draw_comments_to_bottom_right(image, page.tables[0].bbox, comments)

        _draw_table_visualization(image, page, tables) 
        


def test_extract_from_native(extractors): 

    _, extractor_native = extractors 
    pdf_bytes = common_test.get_pdf_structure()
    doc =  extractor_native.extract(pdf_bytes)
    images = common_test.convert_to_pil(pdf_bytes)
    tables = doc.get_tables()
    for image, page in zip(images, doc.pages):
        _draw_table_visualization(image, page, tables)