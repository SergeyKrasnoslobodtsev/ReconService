# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class SingleNumValueType(IntEnum):
    """ Тип значения простого номера """
    DIGIT = 0
    """ Цифровой """
    ROMAN = 1
    """ Латиница """
    LETTER = 2
    """ Символом """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)