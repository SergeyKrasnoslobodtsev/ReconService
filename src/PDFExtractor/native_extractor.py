from typing import List
from pymupdf import find_tables

from .utils import get_pix_rect_page

from .base_extractor import (BBox, 
                             BaseExtractor, 
                             Cell, 
                             Paragraph, 
                             ParagraphType, 
                             Table)



class NativeExtractor(BaseExtractor):

    def _process(self, page):
        x_scale, y_scale = get_pix_rect_page(page)

        tbls = find_tables(page)
        tables: List[Table] = []
        
        for table in tbls:
            text_ext = table.extract()
            cells: List[Cell] = []
            for r, (row, row_text) in enumerate(zip(table.rows, text_ext)):
                for c, (rect, text) in enumerate(zip(list(row.cells), list(row_text))):
                    
                    if rect is None:
                        continue

                    cells.append(
                        Cell(
                            bbox=BBox.from_rect(rect, x_scale, y_scale),
                            row = r,
                            col = c,
                            text=text
                        )
                    )
            tables.append(Table(
                bbox=BBox.from_rect(table.bbox, x_scale, y_scale),
                cells=cells,
            ))
        paragraphs: List[Paragraph] = []

        blocks = page.get_text("blocks")

        scaled = []
        for x0, y0, x1, y1, txt, _, _ in blocks:
            s = txt.strip()
            
            if not s:
               continue

            bb = BBox.from_rect((x0, y0, x1, y1), x_scale, y_scale)
            scaled.append((bb, s))


        if tables:
            top_table_y = min(t.bbox.y1 for t in tables)
            bot_table_y = max(t.bbox.y2 for t in tables)
        else:
            top_table_y = bot_table_y = None

        for bb, txt in scaled:
      
            if any(not (bb.y2 < t.bbox.y1 or bb.y1 > t.bbox.y2) for t in tables):
                continue

            if top_table_y is not None and bb.y2 < top_table_y:
                ptype = ParagraphType.HEADER
            elif bot_table_y is not None and bb.y1 > bot_table_y:
                ptype = ParagraphType.FOOTER
            else:
                ptype = ParagraphType.NONE

            paragraphs.append(Paragraph(bbox=bb, type=ptype, text=txt))
        return paragraphs, tables 
        
        
        
