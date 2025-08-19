# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class NGLinkType(IntEnum):
    UNDEFINED = 0
    LIST = 1
    GENETIVE = 2
    NAME = 3
    AGENT = 4
    PACIENT = 5
    ACTANT = 6
    PARTICIPLE = 7
    ADVERB = 8
    BE = 9
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)