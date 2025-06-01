# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class DecreeKind(IntEnum):
    """ Классы нормативных актов """
    UNDEFINED = 0
    KODEX = 1
    """ Кодекс """
    USTAV = 2
    """ Устав """
    LAW = 3
    """ Закон """
    ORDER = 4
    """ Приказ, указ, директива, распоряжение """
    KONVENTION = 5
    """ Конвенция """
    CONTRACT = 6
    """ Договор, контракт """
    PROJECT = 7
    """ Проект """
    PUBLISHER = 8
    """ Источники опубликований """
    PROGRAM = 9
    """ Госпрограммы """
    STANDARD = 10
    """ Стандарт (ГОСТ, ТУ, ANSI и пр.) """
    CLASSIFIER = 11
    """ Общероссийский классификатор (типа ОГРН) """
    LICENSE = 12
    """ Лицензия """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)