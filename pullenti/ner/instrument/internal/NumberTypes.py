# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class NumberTypes(IntEnum):
    UNDEFINED = 0
    DIGIT = 1
    TWODIGITS = 2
    THREEDIGITS = 3
    FOURDIGITS = 4
    ROMAN = 5
    LETTER = 6
    COMBO = 7
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)