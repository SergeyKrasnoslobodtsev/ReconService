from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class InsertionPosition(str, Enum):
    """Позиции для вставки в ячейку"""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"

class BBox(BaseModel):
    """Прямоугольная область (bounding box)"""
    x: int
    y: int
    width: int
    height: int
    
    model_config = {
        "frozen": True
    }
        
    @property
    def area(self) -> int:
        return self.width * self.height
    
    @property
    def roi(self) -> tuple[slice, slice]:
        """Возвращает регион bbox"""
        return (slice(self.y, self.y2), slice(self.x, self.x2))

    @property
    def x2(self) -> int:
        """Возвращает координату правого края."""
        return self.x + self.width

    @property
    def y2(self) -> int:
        """Возвращает координату нижнего края."""
        return self.y + self.height

    @property
    def pillow_bbox(self) -> list[tuple[int, int]]:
        """Возвращает координаты в формате, готовом для Pillow."""
        return [(self.x, self.y), (self.x2, self.y2)]

    @property
    def to_string(self) -> str:
        return f'{self.x} {self.y} {self.width} {self.height}'


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
            x1=self.bbox.x + padding,
            y1=self.bbox.y + padding,
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