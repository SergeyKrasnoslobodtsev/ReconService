"""
Доменные модели для структуры документа (на основе существующего кода)
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Any
from enum import Enum


class InsertionPosition(str, Enum):
    """Позиции для вставки в ячейку"""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"


class ParagraphType(str, Enum):
    """Типы параграфов"""
    HEADER = "header"
    FOOTER = "footer"
    NONE = "none"


class BBox(BaseModel):
    """Прямоугольная область (bounding box)"""
    x1: float
    y1: float
    x2: float
    y2: float
    
    model_config = {
        "frozen": True
    }
    
    @property
    def width(self) -> float:
        return self.x2 - self.x1
    
    @property
    def height(self) -> float:
        return self.y2 - self.y1
    
    @property
    def area(self) -> float:
        return self.width * self.height


class Cell(BaseModel):
    """Ячейка таблицы"""
    bbox: BBox
    row: int
    col: int
    colspan: int
    rowspan: int
    text: Optional[str] = None
    blobs: List[BBox] = Field(default_factory=list)
    original_page_num: Optional[int] = None
    
    @property
    def has_text(self) -> bool:
        """Проверяет, содержит ли ячейка текст"""
        return self.text is not None and self.text.strip() != ""
    
    @property
    def free_space_ratio(self) -> float:
        """Оценивает долю свободного пространства внутри bbox ячейки"""
        cell_area = self.bbox.area
        if cell_area == 0:
            return 1.0
        
        occupied_area_by_blobs = sum(blob.area for blob in self.blobs)
        occupied_area_by_blobs = min(occupied_area_by_blobs, cell_area)
        
        free_area = cell_area - occupied_area_by_blobs
        return free_area / cell_area
    
    def get_insertion_area(
        self,
        position: InsertionPosition,
        min_height: int = 10,
        padding: int = 2
    ) -> Optional[BBox]:
        """Вычисляет область для вставки нового текста"""
        # Упрощенная версия - возвращаем bbox ячейки с padding
        return BBox(
            x1=self.bbox.x1 + padding,
            y1=self.bbox.y1 + padding,
            x2=self.bbox.x2 - padding,
            y2=self.bbox.y2 - padding
        )


class Table(BaseModel):
    """Таблица документа"""
    bbox: BBox
    cells: List[Cell] = Field(default_factory=list)
    start_page_num: Optional[int] = None
    
    @property
    def average_blob_height(self) -> float:
        """Рассчитывает среднюю высоту всех blobs во всех ячейках таблицы"""
        all_blobs_heights = []
        for cell in self.cells:
            for blob in cell.blobs:
                all_blobs_heights.append(blob.height)
        
        if not all_blobs_heights:
            return 12.0
        return sum(all_blobs_heights) / len(all_blobs_heights) + 6
    
    @property
    def rows(self) -> List[List[Cell]]:
        """Возвращает список строк таблицы"""
        if not self.cells:
            return []
        
        # Группируем ячейки по строкам
        rows_dict = {}
        for cell in self.cells:
            row_key = cell.row
            if row_key not in rows_dict:
                rows_dict[row_key] = []
            rows_dict[row_key].append(cell)
        
        # Сортируем строки по ключу
        sorted_rows = sorted(rows_dict.items())
        return [row_cells for _, row_cells in sorted_rows]
    
    @property
    def column_count(self) -> int:
        """Вычисляет количество столбцов в таблице"""
        if not self.cells:
            return 0
        max_col_idx = 0
        for cell in self.cells:
            max_col_idx = max(max_col_idx, cell.col + cell.colspan - 1)
        return max_col_idx + 1


class Paragraph(BaseModel):
    """Параграф текста"""
    bbox: BBox
    text: str
    paragraph_type: ParagraphType = ParagraphType.NONE
    page_num: Optional[int] = None


class Page(BaseModel):
    """Страница документа"""
    bbox: BBox
    image: Optional[Any] = None  # PIL Image объект
    tables: List[Table] = Field(default_factory=list)
    paragraphs: List[Paragraph] = Field(default_factory=list)
    num_page: int = 0
    
    model_config = {
        "arbitrary_types_allowed": True
    }


class Document(BaseModel):
    """Документ PDF"""
    pdf_bytes: bytes
    pages: List[Page] = Field(default_factory=list)
    page_count: int = 0
    
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    def get_all_text_paragraphs(self) -> str:
        """Получает текст параграфов со всех страниц документа"""
        full_text = []
        for page in self.pages:
            for para in page.paragraphs:
                if para.text:
                    full_text.append(para.text)
        
        return "\n".join(full_text)
    
    def get_tables(self) -> List[Table]:
        """
        Возвращает список логических таблиц из документа.
        Упрощенная версия - возвращает все таблицы со всех страниц.
        """
        all_tables = []
        for page in self.pages:
            all_tables.extend(page.tables)
        return all_tables
