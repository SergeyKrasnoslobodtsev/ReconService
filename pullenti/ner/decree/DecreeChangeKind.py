# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class DecreeChangeKind(IntEnum):
    """ Типы изменений структурных элементов (СЭ) """
    UNDEFINED = 0
    CONTAINER = 1
    """ Объединяет в себе другие изменения """
    APPEND = 2
    """ Дополнить другим СЭ-м или текстовыми конструкциями """
    EXPIRE = 3
    """ СЭ утратил силу """
    NEW = 4
    """ Изложить в редакции """
    EXCHANGE = 5
    """ Заменить одни текстовые конструкции другими """
    REMOVE = 6
    """ Удалить текстовые конструкции """
    CONSIDER = 7
    """ Считать как """
    SUSPEND = 8
    """ Приостановить (до какого-то числа) """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)