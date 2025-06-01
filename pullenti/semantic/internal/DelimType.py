# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class DelimType(IntEnum):
    UNDEFINED = 0
    AND = 1
    BUT = 2
    IF = 4
    THEN = 8
    ELSE = 0x10
    BECAUSE = 0x20
    FOR = 0x40
    WHAT = 0x80
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)