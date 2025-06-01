# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class AddressDetailType(IntEnum):
    """ Детализация местоположения """
    UNDEFINED = 0
    CROSS = 1
    """ Пересечение """
    NEAR = 2
    """ Возле """
    HOSTEL = 3
    """ Общежитие """
    NORTH = 4
    """ На север """
    SOUTH = 5
    """ На юг """
    WEST = 6
    """ На запад """
    EAST = 7
    """ На восток """
    NORTHWEST = 8
    """ На сереро-запад """
    NORTHEAST = 9
    """ На северо-восток """
    SOUTHWEST = 10
    """ На юго-запад """
    SOUTHEAST = 11
    """ На юго-восток """
    CENTRAL = 12
    """ Центральный """
    LEFT = 13
    """ Слева """
    RIGHT = 14
    """ Справа """
    RANGE = 15
    """ Это один очень специфический случай """
    ORG = 16
    """ Ссылка на организацию (типа БЦ, магазин и пр.) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)