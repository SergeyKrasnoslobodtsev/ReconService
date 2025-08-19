# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from enum import IntEnum

class SemObjectType(IntEnum):
    """ Тип семантического объекта """
    UNDEFINED = 0
    NOUN = 1
    """ Существительное (в широком смысле, например, сущности) """
    ADJECTIVE = 2
    """ Прилагательное """
    VERB = 3
    """ Предикат (глагол) """
    PARTICIPLE = 4
    """ Причастие или деепричастие """
    ADVERB = 5
    """ Наречие """
    PRONOUN = 6
    """ Местоимение """
    PERSONALPRONOUN = 7
    """ Личное местоимение """
    QUESTION = 8
    """ Вопрос """
    
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)