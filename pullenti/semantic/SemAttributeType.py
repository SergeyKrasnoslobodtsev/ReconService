# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class SemAttributeType(IntEnum):
    """ Типы семантических атрибутов """
    UNDEFINED = 0
    VERY = 1
    """ Очень """
    ALREADY = 2
    """ Уже """
    STILL = 3
    """ Ещё """
    ALL = 4
    """ Все """
    ANY = 5
    """ Любой, каждый """
    SOME = 6
    """ Некоторый """
    ONE = 7
    """ Один """
    ONEOF = 8
    """ Один из """
    OTHER = 9
    """ Другой """
    EACHOTHER = 10
    """ друг друга, один другого """
    HIMELF = 11
    """ Сам себя """
    WHOLE = 12
    """ Целиком, весь """
    LESS = 13
    """ Меньше """
    GREAT = 14
    """ Больше """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)