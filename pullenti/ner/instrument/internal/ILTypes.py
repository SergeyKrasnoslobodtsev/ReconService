# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class ILTypes(IntEnum):
    UNDEFINED = 0
    APPENDIX = 1
    APPROVED = 2
    ORGANIZATION = 3
    REGNUMBER = 4
    DATE = 5
    GEO = 6
    PERSON = 7
    TYP = 8
    VERB = 9
    DIRECTIVE = 10
    QUESTION = 11
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)