# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class AddressItemType(IntEnum):
    PREFIX = 0
    STREET = 1
    HOUSE = 2
    BUILDING = 3
    CORPUS = 4
    POTCH = 5
    FLOOR = 6
    FLAT = 7
    CORPUSORFLAT = 8
    OFFICE = 9
    ROOM = 10
    PLOT = 11
    FIELD = 12
    GENPLAN = 13
    PAVILION = 14
    BLOCK = 15
    BOX = 16
    WELL = 17
    CARPLACE = 18
    PART = 19
    SPACE = 20
    CITY = 21
    REGION = 22
    COUNTRY = 23
    NUMBER = 24
    NONUMBER = 25
    KILOMETER = 26
    ZIP = 27
    POSTOFFICEBOX = 28
    DELIVERYAREA = 29
    CSP = 30
    DETAIL = 31
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)