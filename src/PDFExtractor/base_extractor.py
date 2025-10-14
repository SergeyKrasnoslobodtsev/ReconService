from abc import ABC, abstractmethod
from typing import Protocol
from dataclasses import dataclass, field
import enum
import logging
from typing import List, Optional, Tuple, Union
from PIL import Image
import pymupdf

from openpyxl import Workbook
from openpyxl.utils import get_column_letter 
from openpyxl.styles import Alignment, Border, Side 


@dataclass
class BBox:
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def coords(self) -> Tuple[int, int, int, int]:
        """Вернуть все координаты как кортеж."""
        return self.x1, self.y1, self.x2, self.y2

    @coords.setter
    def coords(self, vals: Tuple[int, int, int, int]):
        """Установить сразу все координаты из кортежа."""
        self.x1, self.y1, self.x2, self.y2 = vals

    @property
    def width(self) -> int:
        """Ширина bbox."""
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        """Высота bbox."""
        return self.y2 - self.y1

    def padding(self, pix: int = 5) -> "BBox":
        return BBox(
            x1=self.x1 - pix,
            y1=self.y1 - pix,
            x2=self.x2 + pix,
            y2=self.y2 + pix,
        )
    
    def contains(self, other: 'BBox') -> bool:
        return (self.x1 <= other.x1 and
                self.y1 <= other.y1 and
                self.x2 >= other.x2 and
                self.y2 >= other.y2)

    @classmethod
    def from_rect(
        cls,
        rect: Union[
            "pymupdf.Rect",      # если у вас есть real Rect
            Tuple[float, float, float, float]  # или кортеж (x0,y0,x1,y1)
        ],
        sx: float = 1.0,
        sy: float = 1.0
    ) -> "BBox":
        """Создать BBox из pymupdf.Rect или из кортежа (x0, y0, x1, y1) с учётом масштабов."""
        # разбираем вход
        if hasattr(rect, "x0"):
            x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1
        else:
            x0, y0, x1, y1 = rect  # ожидаем кортеж из 4-х чисел

        return cls(
            x1=int(x0 * sx),
            y1=int(y0 * sy),
            x2=int(x1 * sx),
            y2=int(y1 * sy),
        )

class InsertionPosition(enum.Enum):
    TOP = "top"  # Сверху
    BOTTOM = "bottom" # Снизу
    LEFT = "left"
    RIGHT = "right"

@dataclass
class Cell:
    bbox: BBox
    row: int
    col: int
    colspan: int
    rowspan: int
    text: str = None
    blobs: List[BBox] = field(default_factory=list)
    original_page_num: Optional[int] = None

    @property
    def has_text(self) -> bool:
        """Проверяет, содержит ли ячейка текст (на основе атрибута text)."""
        return self.text is not None and self.text.strip() != ""

    @property
    def free_space_ratio(self) -> float:
        """
        Оценивает долю свободного пространства внутри bbox ячейки, не занятого blobs.
        Возвращает 1.0, если bbox ячейки имеет нулевую площадь.
        """
        cell_area = self.bbox.width * self.bbox.height
        if cell_area == 0:
            return 1.0  # Если площадь ячейки 0, считаем ее полностью свободной или полностью занятой в зависимости от контекста. 1.0 означает нет места для нового.
                        # Или можно вернуть 0.0 если blobs тоже нет, что означает "нет контента, нет места"

        occupied_area_by_blobs = 0
        for blob in self.blobs:
            occupied_area_by_blobs += blob.width * blob.height
        
        # Ограничиваем occupied_area, чтобы она не превышала cell_area
        occupied_area_by_blobs = min(occupied_area_by_blobs, float(cell_area))

        free_area = cell_area - occupied_area_by_blobs
        return free_area / cell_area

    def get_insertion_area(
        self,
        position: InsertionPosition,
        min_height: int = 10, # Минимальная высота для области вставки
        padding: int = 2      # Отступ от краев основного bbox ячейки
    ) -> Optional[BBox]:
        """
        Вычисляет прямоугольную область внутри ячейки, подходящую для вставки нового текста.
        Область будет занимать ширину ячейки (за вычетом отступов).

        Args:
            position: Член перечисления InsertionPosition (TOP или BOTTOM).
            min_height: Минимально необходимая высота для области вставки.
            padding: Отступ от краев основного bbox ячейки.

        Returns:
            Объект BBox, представляющий доступную область, или None, если подходящая область не найдена.
        """
        if self.bbox.width <= 2 * padding or self.bbox.height <= 2 * padding:
            return None # Ячейка слишком мала для отступов

        # Эффективные границы ячейки после применения отступов
        eff_cell_x1 = self.bbox.x1 + padding
        eff_cell_y1 = self.bbox.y1 + padding
        eff_cell_x2 = self.bbox.x2 - padding
        eff_cell_y2 = self.bbox.y2 - padding

        if eff_cell_x1 >= eff_cell_x2 or eff_cell_y1 >= eff_cell_y2:
            return None # Нет места после применения отступов

        insert_x1 = eff_cell_x1
        insert_x2 = eff_cell_x2
        insert_y1 = -1
        insert_y2 = -1

        # Фильтруем blobs, которые находятся по горизонтали в пределах эффективной ширины ячейки
        relevant_blobs = [
            b for b in self.blobs if b.x1 < eff_cell_x2 and b.x2 > eff_cell_x1
        ]

        if position == InsertionPosition.TOP:
            insert_y1 = eff_cell_y1 
            limit_y = eff_cell_y2 # По умолчанию, предел - это нижняя граница ячейки с отступом
            if relevant_blobs:
                # Ищем самый верхний край существующих blobs, чтобы вставить текст над ними
                blob_tops = [b.y1 for b in relevant_blobs if b.y1 >= eff_cell_y1] 
                if blob_tops:
                    limit_y = min(min(blob_tops) - 1, eff_cell_y2) # -1 для небольшого зазора
            insert_y2 = limit_y

        elif position == InsertionPosition.BOTTOM:
            insert_y2 = eff_cell_y2
            limit_y = eff_cell_y1 # По умолчанию, предел - это верхняя граница ячейки с отступом
            if relevant_blobs:
                # Ищем самый нижний край существующих blobs, чтобы вставить текст под ними
                blob_bottoms = [b.y2 for b in relevant_blobs if b.y2 <= eff_cell_y2]
                if blob_bottoms:
                    limit_y = max(max(blob_bottoms) + 1, eff_cell_y1) # +1 для небольшого зазора
            insert_y1 = limit_y
        else:
            # Это можно расширить для других позиций, таких как LEFT, RIGHT и т.д.
            raise NotImplementedError(f"Позиция для вставки {position} еще не поддерживается.")

        # Проверяем рассчитанную область
        if insert_y1 != -1 and insert_y2 != -1 and \
        insert_x1 < insert_x2 and insert_y1 < insert_y2 and \
        (insert_y2 - insert_y1) >= min_height:
            return BBox(x1=insert_x1, y1=insert_y1, x2=insert_x2, y2=insert_y2)

        return None

@dataclass
class Table:
    bbox: BBox
    cells: List[Cell] = field(default_factory=list)
    start_page_num: Optional[int] = None
    end_page_num: Optional[int] = None
    
    @property
    def average_blob_height(self) -> float:
        """
        Рассчитывает среднюю высоту всех blobs во всех ячейках таблицы.
        Возвращает 0.0, если blobs отсутствуют в таблице.
        """
        all_blobs_heights = []
        for cell in self.cells:
            for blob in cell.blobs:
                all_blobs_heights.append(blob.height)
        
        if not all_blobs_heights:
            return 12.0
        return sum(all_blobs_heights) / len(all_blobs_heights) + 6

    @property
    def rows(self) -> List[List[Cell]]:
        """
        Возвращает список строк таблицы, где каждая строка - это список ячеек.
        Строки упорядочены по вертикали (от верхней к нижней).
        """
        if not self.cells:
            return []

        # Группируем ячейки по строкам
        rows_dict = {}
        for cell in self.cells:
            row_key = cell.row
            if row_key not in rows_dict:
                rows_dict[row_key] = []
            rows_dict[row_key].append(cell)

        # Сортируем строки по ключу (номеру строки)
        sorted_rows = sorted(rows_dict.items())
        return [row_cells for _, row_cells in sorted_rows]

class ParagraphType(enum.Enum):
    HEADER = 0
    FOOTER = 1
    NONE = 2

@dataclass
class Paragraph:
    bbox: BBox
    type: ParagraphType = ParagraphType.NONE
    text: str = None
    blobs: List[BBox] = field(default_factory=list)
    

@dataclass
class Page:
    image: Image.Image = None
    tables: List[Table] = field(default_factory=list)
    paragraphs: List[Paragraph] = field(default_factory=list)
    num_page: int = 0

@dataclass
class Document:
    pdf_bytes: bytes = None
    pages: List[Page] = field(default_factory=list)
    page_count: int = 0

    def get_last_page_number_table(self) -> int:
        '''Получаем номер последней страницы с таблицей'''
        tables = self.get_tables()
        if not tables:
            return -1 
        return max(table.end_page_num for table in tables if table.end_page_num is not None)

    def get_first_row_tables_text(self) -> str:
        '''Получаем текст первой строки всех таблиц в документе'''
        first_row_text = []
        for page in self.pages:
            for table in page.tables:
                if table.cells:
                    first_row = table.rows[0] if table.rows else []
                    first_row_text.append(" ".join(cell.text for cell in first_row if cell.text))
        return "\n".join(first_row_text)

    def get_all_text_paragraphs(self) -> str:
        '''Получем текс параграфов со всех страниц документа и представим его в виде строки'''
        full_text = []
        for page in self.pages:
            for para in page.paragraphs:
                if not para.text:
                    continue
                full_text.append(para.text)
        
        return "\n".join(full_text)

    def _get_table_column_count(self, table_obj: Table) -> int:
        """
        Calculates the number of columns in a table.
        Returns 0 if the table has no cells.
        """
        if not table_obj.cells:
            return 0
        max_col_idx = 0  # 0-indexed
        for cell in table_obj.cells:
            max_col_idx = max(max_col_idx, cell.col + cell.colspan - 1)
        return max_col_idx + 1  # Return 1-indexed count


    def get_tables(self) -> List[Table]:
        """
        Извлекает логические таблицы из документа с учетом новых правил:
        1. Таблицы на одной странице НЕ объединяются
        2. Таблицы на разных страницах объединяются, если:
           - Следующая таблица находится вверху страницы
           - В её первой строке нет слов "дебет" или "кредит"
           - Над ней нет большого текста (кроме номера страницы)
        """
        # Инициализация компонентов
        stream_builder = DocumentStreamBuilder()
        fragment_factory = TableFragmentFactory()
        
        # Создание стратегий объединения
        same_page_strategy = SamePageStrategy()
        cross_page_strategy = CrossPageStrategy(self.pages)
        merge_decider = TableMergeDecider([same_page_strategy, cross_page_strategy])
        
        table_builder = LogicalTableBuilder()
        paragraph_analyzer = ParagraphAnalyzer()
        
        # Построение потока элементов
        all_elements = stream_builder.build(self.pages)
        
        # Обработка потока
        logical_tables: List[Table] = []
        current_fragments: List[TableFragment] = []
        had_semantic_paragraph = False
        
        for el in all_elements:
            if el['type'] == 'paragraph':
                para: Paragraph = el['obj']
                if paragraph_analyzer.is_semantic(para):
                    had_semantic_paragraph = True
            
            else:  # table
                table_obj: Table = el['obj']
                if not table_obj.cells:
                    continue
                
                current_fragment = fragment_factory.create(
                    table=table_obj,
                    page_num=el['page_num'],
                    y1=el['y1']
                )
                
                should_start_new = False
                
                if not current_fragments:
                    # Первый фрагмент
                    should_start_new = False
                else:
                    prev_fragment = current_fragments[-1]
                    
                    # Проверяем условия для начала новой таблицы
                    should_start_new = (
                        had_semantic_paragraph  # Был семантический параграф
                        or "по данным" in current_fragment.first_row_text  # Ключевая фраза
                        or not merge_decider.should_merge(prev_fragment, current_fragment)  # Стратегии запрещают
                    )
                
                if should_start_new:
                    # Завершаем текущую логическую таблицу
                    if current_fragments:
                        logical_table = table_builder.build(current_fragments)
                        if logical_table:
                            logical_tables.append(logical_table)
                    current_fragments = []
                    had_semantic_paragraph = False
                
                # Добавляем фрагмент к текущей логической таблице
                current_fragments.append(current_fragment)
                had_semantic_paragraph = False
        
        # Обработка последнего фрагмента
        if current_fragments:
            logical_table = table_builder.build(current_fragments)
            if logical_table:
                logical_tables.append(logical_table)
        
        return logical_tables
        
class TableMergeStrategy(Protocol):
    """Протокол для стратегий объединения таблиц."""
    def should_merge(self, prev_fragment: 'TableFragment', curr_fragment: 'TableFragment') -> bool:
        """Определяет, нужно ли объединить два фрагмента таблицы."""
        ...

@dataclass
class TableFragment:
    """Представляет фрагмент таблицы на одной странице."""
    table: Table
    page_num: int
    y1: int
    first_row_text: str
    column_count: int

class ColumnCountAnalyzer:
    """Отвечает за анализ количества колонок в таблице."""
    
    @staticmethod
    def get_column_count(table_obj: Table) -> int:
        """Вычисляет количество колонок в таблице."""
        if not table_obj.cells:
            return 0
        max_col_idx = 0
        for cell in table_obj.cells:
            max_col_idx = max(max_col_idx, cell.col + cell.colspan - 1)
        return max_col_idx + 1

class FirstRowTextExtractor:
    """Извлекает текст первой строки таблицы."""
    
    @staticmethod
    def extract(table_obj: Table) -> str:
        """Возвращает текст первой строки таблицы в нижнем регистре."""
        if not table_obj.cells or not table_obj.rows:
            return ""
        return " ".join((c.text or "").lower() for c in table_obj.rows[0] if c.text)

class ParagraphAnalyzer:
    """Анализирует параграфы для определения семантических границ."""
    
    @staticmethod
    def is_semantic(paragraph: Paragraph) -> bool:
        """Проверяет, является ли параграф семантически значимым (не колонтитул)."""
        return paragraph.type not in (ParagraphType.HEADER, ParagraphType.FOOTER)
    
    @staticmethod
    def is_large_text(paragraph: Paragraph, threshold: int = 100) -> bool:
        """Проверяет, является ли параграф большим текстом."""
        if not paragraph.text:
            return False
        return len(paragraph.text.strip()) > threshold
    
    @staticmethod
    def contains_keywords(paragraph: Paragraph, keywords: List[str]) -> bool:
        """Проверяет наличие ключевых слов в параграфе."""
        if not paragraph.text:
            return False
        text_lower = paragraph.text.lower()
        return any(keyword in text_lower for keyword in keywords)

class SamePageStrategy:
    """таблицы на одной странице НЕ объединяются."""
    
    def should_merge(self, prev_fragment: TableFragment, curr_fragment: TableFragment) -> bool:
        if prev_fragment.page_num == curr_fragment.page_num:
            return False
        return True  # На разных страницах - передаем решение дальше

class CrossPageStrategy:
    """таблицы на разных страницах объединяются при выполнении условий."""
    
    def __init__(self, document_pages: List[Page]):
        self.document_pages = document_pages
        self.paragraph_analyzer = ParagraphAnalyzer()
    
    def should_merge(self, prev_fragment: TableFragment, curr_fragment: TableFragment) -> bool:
        # Если на одной странице - не наша зона ответственности
        if prev_fragment.page_num == curr_fragment.page_num:
            return True  # Пропускаем
        
        # Текущая таблица должна быть в верхней части страницы
        current_page = self.document_pages[curr_fragment.page_num]
        if not self._is_table_at_top(curr_fragment, current_page):
            return False
        
        #В первой строке текущей таблицы НЕ должно быть "дебет" или "кредит"
        if self._has_debet_kredit_in_first_row(curr_fragment.first_row_text):
            return False
        
        # Над таблицей НЕ должно быть большого текста (кроме номера страницы)
        if self._has_large_text_above(curr_fragment, current_page):
            return False
        
        # Количество колонок должно совпадать
        # if prev_fragment.column_count != curr_fragment.column_count:
        #     return False
        
        return True
    
    def _is_table_at_top(self, fragment: TableFragment, page: Page, threshold: float = 0.3) -> bool:
        """Проверяет, находится ли таблица в верхней части страницы."""
        if not page.tables:
            return False
        
        # Находим высоту страницы через первую таблицу или параграф
        page_height = 0
        if page.tables:
            page_height = max(t.bbox.y2 for t in page.tables)
        if page.paragraphs:
            page_height = max(page_height, max(p.bbox.y2 for p in page.paragraphs))
        
        if page_height == 0:
            return True  # Нет данных о высоте, считаем что вверху
        
        # Таблица считается вверху, если её Y1 в пределах верхних 30% страницы
        return fragment.y1 / page_height < threshold
    
    def _has_debet_kredit_in_first_row(self, first_row_text: str) -> bool:
        """Проверяет наличие слов 'дебет' или 'кредит' в первой строке."""
        keywords = ['дебет', 'кредит', 'debet', 'kredit']
        return any(keyword in first_row_text for keyword in keywords)
    
    def _has_large_text_above(self, fragment: TableFragment, page: Page, 
                             min_length: int = 100) -> bool:
        """Проверяет наличие большого текста над таблицей (игнорируя номера страниц)."""
        table_y1 = fragment.y1
        
        for para in page.paragraphs:
            # Параграф должен быть выше таблицы
            if para.bbox.y2 > table_y1:
                continue
            
            # Игнорируем колонтитулы
            if not self.paragraph_analyzer.is_semantic(para):
                continue
            
            # Игнорируем короткие тексты (номера страниц)
            if not para.text or len(para.text.strip()) < min_length:
                continue
            
            # Проверяем, не является ли это просто номером страницы
            text_stripped = para.text.strip()
            if text_stripped.isdigit() and len(text_stripped) < 5:
                continue
            
            # Найден большой текст над таблицей
            return True
        
        return False

class TableMergeDecider:
    """(SRP) Принимает решение об объединении на основе цепочки стратегий."""
    
    def __init__(self, strategies: List[TableMergeStrategy]):
        self.strategies = strategies
    
    def should_merge(self, prev_fragment: TableFragment, curr_fragment: TableFragment) -> bool:
        """Применяет все стратегии последовательно."""
        for strategy in self.strategies:
            if not strategy.should_merge(prev_fragment, curr_fragment):
                return False
        return True

class LogicalTableBuilder:
    """Строит логические таблицы из фрагментов."""
    
    @staticmethod
    def build(fragments: List[TableFragment]) -> Table:
        """Объединяет фрагменты в одну логическую таблицу."""
        if not fragments:
            return None
        
        acc_cells = []
        row_offset = 0
        first_bbox = fragments[0].table.bbox
        start_page = fragments[0].page_num
        last_page = fragments[-1].page_num
        
        max_columns = max(fragment.column_count for fragment in fragments)

        for fragment in fragments:
            max_row_end = 0
            col_offset = max_columns - fragment.column_count
            for cell in fragment.table.cells:
                acc_cells.append(Cell(
                    bbox=cell.bbox,
                    row=cell.row + row_offset,
                    col=cell.col + col_offset,
                    colspan=cell.colspan,
                    rowspan=cell.rowspan,
                    text=cell.text,
                    blobs=list(cell.blobs),
                    original_page_num=fragment.page_num
                ))
                max_row_end = max(max_row_end, cell.row + cell.rowspan)

            row_offset += max_row_end
  
        
        return Table(
            bbox=first_bbox,
            cells=acc_cells,
            start_page_num=start_page,
            end_page_num=last_page
        )

class DocumentStreamBuilder:
    """(SRP) Строит поток элементов документа (параграфы + таблицы)."""
    
    @staticmethod
    def build(pages: List[Page]) -> List[dict]:
        """Создает отсортированный поток всех элементов документа."""
        all_elements = []
        for page_data in pages:
            for p_obj in page_data.paragraphs:
                all_elements.append({
                    'type': 'paragraph',
                    'obj': p_obj,
                    'page_num': page_data.num_page,
                    'y1': p_obj.bbox.y1
                })
            for t_obj in page_data.tables:
                if t_obj.cells:
                    all_elements.append({
                        'type': 'table',
                        'obj': t_obj,
                        'page_num': page_data.num_page,
                        'y1': t_obj.bbox.y1
                    })
        all_elements.sort(key=lambda x: (x['page_num'], x['y1']))
        return all_elements

class TableFragmentFactory:
    """(SRP) Создает TableFragment из данных таблицы."""
    
    def __init__(self):
        self.column_analyzer = ColumnCountAnalyzer()
        self.text_extractor = FirstRowTextExtractor()
    
    def create(self, table: Table, page_num: int, y1: int) -> TableFragment:
        """Создает фрагмент таблицы с предварительно вычисленными метаданными."""
        return TableFragment(
            table=table,
            page_num=page_num,
            y1=y1,
            first_row_text=self.text_extractor.extract(table),
            column_count=self.column_analyzer.get_column_count(table)
        )


class BaseExtractor(ABC):
    def __init__(self):
        self.logger = logging.getLogger('app.' + __class__.__name__)

    def extract(self, pdf_bytes: bytes) -> Document:
        self.logger.info("Начало процесса извлечения данных из PDF.")
        if not pdf_bytes:
            self.logger.error("Получены пустые байты PDF. Прерывание операции.")
            raise ValueError("pdf_bytes не могут быть пустыми.")

        try:
            doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
        except Exception as e:
            self.logger.error(f"Ошибка при открытии PDF документа: {e}", exc_info=True)
            raise 

        page_count = len(doc)
        self.logger.info(f"Документ успешно открыт. Количество страниц: {page_count}.")
        
        pages_data: List[Page] = []
        for i in range(page_count):
            self.logger.info(f"Обработка страницы {i + 1}/{page_count}.")
            page_content = doc[i]
            try:
                paragraphs, tables = self._process(page_content)
                self.logger.debug(f"Страница {i + 1}: найдено {len(paragraphs)} параграфов и {len(tables)} таблиц.")
                
                pages_data.append(
                    Page(
                        tables=tables,
                        paragraphs=paragraphs,
                        num_page=i
                    )
                )
            except Exception as e:
                self.logger.error(f"Ошибка при обработке страницы {i + 1}: {e}", exc_info=True)

                pages_data.append(
                    Page(num_page=i) 
                )
                continue 

        self.logger.info("Все страницы обработаны. Формирование итогового документа.")
        final_document = Document(
                            pdf_bytes=pdf_bytes,
                            pages=pages_data,
                            page_count=len(pages_data)
                        )
        self.logger.info("Процесс извлечения данных из PDF завершен.")
        return final_document
    
    def _process(self, page)-> Tuple[List[Paragraph], List[Table]]:
        ...

