"""
Доменные модели для структуры документа
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Any
from enum import Enum

from ..LayoutAnalisis.TableDetector.table import BBox, Table


class ParagraphType(str, Enum):
    """Типы параграфов"""
    HEADER = "header"
    FOOTER = "footer"
    NONE = "none"


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
