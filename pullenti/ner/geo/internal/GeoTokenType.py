# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class GeoTokenType(IntEnum):
    ANY = 0
    ORG = 1
    STREET = 2
    CITY = 3
    TERR = 4
    STRONG = 5
    HOUSE = 6
    TOSLASH = 7
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)