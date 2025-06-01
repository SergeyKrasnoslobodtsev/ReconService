# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class DecreeChangeValueKind(IntEnum):
    """ Типы изменяющих структурный элемент значений """
    UNDEFINED = 0
    TEXT = 1
    """ Текстовой фрагмент """
    WORDS = 2
    """ Слова (в точном значении) """
    ROBUSTWORDS = 3
    """ Слова (в неточном значений) """
    NUMBERS = 4
    """ Цифры """
    DEFINITION = 5
    """ Определение """
    BLOCK = 6
    """ Блок со словами """
    EXTAPPENDIX = 7
    """ Текст находится во внешнем приложении (здесь только его номер) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)