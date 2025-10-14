# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.decree.DecreeReferent import DecreeReferent

class MetaDecreePart(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        MetaDecreePart.GLOBAL_META = MetaDecreePart()
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_NAME, "Наименование", 0, 0)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_OWNER, "Владелец", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_LOCALTYP, "Локальный тип", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_SECTION, "Раздел", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_SUBSECTION, "Подраздел", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_APPENDIX, "Приложение", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_CHAPTER, "Глава", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_PREAMBLE, "Преамбула", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_CLAUSE, "Статья", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_PART, "Часть", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_DOCPART, "Часть документа", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_PARAGRAPH, "Параграф", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_SUBPARAGRAPH, "Подпараграф", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_ITEM, "Пункт", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_SUBITEM, "Подпункт", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_INDENTION, "Абзац", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_SUBINDENTION, "Подабзац", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_FORMULA, "Формула", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_FORM, "Форма", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_TABLE, "Таблица", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_TABLECOLUMN, "Столбец таблицы", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_TABLEROW, "Строка таблицы", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_SENTENCE, "Предложение", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_FOOTNOTE, "Сноска", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_SUBPROGRAM, "Подпрограмма", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_ADDAGREE, "Допсоглашение", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_NOTICE, "Примечание", 0, 1)
        MetaDecreePart.GLOBAL_META.add_feature(DecreePartReferent.ATTR_NAMEASITEM, "Наименование (как элемент структуры)", 0, 1)
    
    @property
    def name(self) -> str:
        return DecreeReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Ссылка на часть НПА"
    
    PART_IMAGE_ID = "part"
    
    PART_LOC_IMAGE_ID = "partloc"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        dpr = Utils.asObjectOrNull(obj, DecreePartReferent)
        if (dpr is not None): 
            if (dpr.owner is None): 
                return MetaDecreePart.PART_LOC_IMAGE_ID
        return MetaDecreePart.PART_IMAGE_ID
    
    GLOBAL_META = None