# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.decree.DecreeChangeValueKind import DecreeChangeValueKind

class MetaDecreeChangeValue(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
        MetaDecreeChangeValue.GLOBAL_META = MetaDecreeChangeValue()
        fi = MetaDecreeChangeValue.GLOBAL_META.add_feature(DecreeChangeValueReferent.ATTR_KIND, "Тип", 1, 1)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.TEXT), "Текст", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.WORDS), "Слова", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.DEFINITION), "Определение", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.ROBUSTWORDS), "Слова (неточно)", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.NUMBERS), "Цифры", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.BLOCK), "Блок", None, None)
        fi.add_value(Utils.enumToString(DecreeChangeValueKind.EXTAPPENDIX), "Внешнее приложение", None, None)
        MetaDecreeChangeValue.KIND_FEATURE = fi
        MetaDecreeChangeValue.GLOBAL_META.add_feature(DecreeChangeValueReferent.ATTR_VALUE, "Значение", 1, 1)
        MetaDecreeChangeValue.GLOBAL_META.add_feature(DecreeChangeValueReferent.ATTR_NEWITEM, "Новый структурный элемент", 0, 0)
        MetaDecreeChangeValue.GLOBAL_META.add_feature(DecreeChangeValueReferent.ATTR_BEGINCHAR, "Начальная позиция текста", 0, 1)
        MetaDecreeChangeValue.GLOBAL_META.add_feature(DecreeChangeValueReferent.ATTR_ENDCHAR, "Конечная позиция текста", 0, 1)
    
    KIND_FEATURE = None
    
    @property
    def name(self) -> str:
        from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
        return DecreeChangeValueReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Значение изменения СЭ НПА"
    
    IMAGE_ID = "decreechangevalue"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaDecreeChangeValue.IMAGE_ID
    
    GLOBAL_META = None