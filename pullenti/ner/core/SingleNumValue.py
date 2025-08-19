# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.core.SingleNumValueType import SingleNumValueType

class SingleNumValue:
    """ Возможное значение номера """
    
    def __init__(self) -> None:
        self.typ = SingleNumValueType.DIGIT
        self.val = 0
        self.letter = '\x00'
        self.upper = False
    
    def __str__(self) -> str:
        if (self.typ == SingleNumValueType.DIGIT): 
            return str(self.val)
        if (self.typ == SingleNumValueType.ROMAN): 
            return "rom({0})".format(self.val)
        return "{0}".format(self.letter)
    
    @property
    def is_one(self) -> bool:
        if (self.val == 1): 
            return True
        if ((self.letter == 'A' or self.letter == 'А' or self.letter == 'a') or self.letter == 'а'): 
            return True
        return False
    
    def to_int(self) -> int:
        if (self.typ != SingleNumValueType.LETTER): 
            return self.val
        if (not str.isalpha(self.letter)): 
            return -1
        if ((ord(self.letter)) < 0x80): 
            if (str.isupper(self.letter)): 
                return (((ord(self.letter)) - (ord('A'))) + 1)
            else: 
                return (((ord(self.letter)) - (ord('a'))) + 1)
        else: 
            ch = str.upper(self.letter)
            i = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЫЭЮЯ".find(ch)
            if (i >= 0): 
                return i + 1
            return -1