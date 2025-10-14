# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

class CharsInfo:
    """ Информация о символах токена
    
    Символьная информация
    """
    
    def __init__(self) -> None:
        self.value = 0
    
    def __get_value(self, i : int) -> bool:
        return (((((self.value) >> i)) & 1)) != 0
    
    def __set_value(self, i : int, val : bool) -> None:
        if (val): 
            self.value |= ((1 << i))
        else: 
            self.value &= (~ ((1 << i)))
    
    @property
    def is_all_upper(self) -> bool:
        """ Все символы в верхнем регистре """
        return self.__get_value(0)
    @is_all_upper.setter
    def is_all_upper(self, value_) -> bool:
        self.__set_value(0, value_)
        return value_
    
    @property
    def is_all_lower(self) -> bool:
        """ Все символы в нижнем регистре """
        return self.__get_value(1)
    @is_all_lower.setter
    def is_all_lower(self, value_) -> bool:
        self.__set_value(1, value_)
        return value_
    
    @property
    def is_capital_upper(self) -> bool:
        """ Первый символ в верхнем регистре, остальные в нижнем.
        Для однобуквенной комбинации false. """
        return self.__get_value(2)
    @is_capital_upper.setter
    def is_capital_upper(self, value_) -> bool:
        self.__set_value(2, value_)
        return value_
    
    @property
    def is_last_lower(self) -> bool:
        """ Все символы в верхнем регистре, кроме последнего (длина >= 3) """
        return self.__get_value(3)
    @is_last_lower.setter
    def is_last_lower(self, value_) -> bool:
        self.__set_value(3, value_)
        return value_
    
    @property
    def is_letter(self) -> bool:
        """ Это буквы """
        return self.__get_value(4)
    @is_letter.setter
    def is_letter(self, value_) -> bool:
        self.__set_value(4, value_)
        return value_
    
    @property
    def is_latin_letter(self) -> bool:
        """ Это латиница """
        return self.__get_value(5)
    @is_latin_letter.setter
    def is_latin_letter(self, value_) -> bool:
        self.__set_value(5, value_)
        return value_
    
    @property
    def is_cyrillic_letter(self) -> bool:
        """ Это кириллица """
        return self.__get_value(6)
    @is_cyrillic_letter.setter
    def is_cyrillic_letter(self, value_) -> bool:
        self.__set_value(6, value_)
        return value_
    
    def __str__(self) -> str:
        if (not self.is_letter): 
            return "Nonletter"
        tmp_str = io.StringIO()
        if (self.is_all_upper): 
            print("AllUpper", end="", file=tmp_str)
        elif (self.is_all_lower): 
            print("AllLower", end="", file=tmp_str)
        elif (self.is_capital_upper): 
            print("CapitalUpper", end="", file=tmp_str)
        elif (self.is_last_lower): 
            print("LastLower", end="", file=tmp_str)
        else: 
            print("Nonstandard", end="", file=tmp_str)
        if (self.is_latin_letter): 
            print(" Latin", end="", file=tmp_str)
        elif (self.is_cyrillic_letter): 
            print(" Cyrillic", end="", file=tmp_str)
        elif (self.is_letter): 
            print(" Letter", end="", file=tmp_str)
        return Utils.toStringStringIO(tmp_str)
    
    def equals(self, obj : object) -> bool:
        """ Сравнение на совпадение значений всех полей
        
        Args:
            obj(object): сравниваемый объект
        
        """
        if (not (isinstance(obj, CharsInfo))): 
            return False
        return self.value == obj.value
    
    def convert_word(self, word : str) -> str:
        if (Utils.isNullOrEmpty(word)): 
            return word
        if (self.is_all_lower): 
            return word.lower()
        if (self.is_all_upper): 
            return word.upper()
        if (self.is_capital_upper and len(word) > 0): 
            tmp = Utils.newStringIO(word)
            i = 0
            while i < tmp.tell(): 
                if (i == 0): 
                    Utils.setCharAtStringIO(tmp, 0, str.upper(Utils.getCharAtStringIO(tmp, 0)))
                elif (Utils.getCharAtStringIO(tmp, i - 1) == '-' or Utils.getCharAtStringIO(tmp, i - 1) == ' '): 
                    Utils.setCharAtStringIO(tmp, 0, str.upper(Utils.getCharAtStringIO(tmp, 0)))
                else: 
                    Utils.setCharAtStringIO(tmp, i, str.lower(Utils.getCharAtStringIO(tmp, i)))
                i += 1
            return Utils.toStringStringIO(tmp)
        return word
    
    @staticmethod
    def _new3089(_arg1 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_capital_upper = _arg1
        return res
    
    @staticmethod
    def _new3282(_arg1 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_cyrillic_letter = _arg1
        return res
    
    @staticmethod
    def _new3288(_arg1 : bool, _arg2 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_cyrillic_letter = _arg1
        res.is_capital_upper = _arg2
        return res
    
    @staticmethod
    def _new3293(_arg1 : bool, _arg2 : bool, _arg3 : bool, _arg4 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_capital_upper = _arg1
        res.is_cyrillic_letter = _arg2
        res.is_latin_letter = _arg3
        res.is_letter = _arg4
        return res
    
    @staticmethod
    def _new3301(_arg1 : int) -> 'CharsInfo':
        res = CharsInfo()
        res.value = _arg1
        return res
    
    @staticmethod
    def _new3322(_arg1 : bool) -> 'CharsInfo':
        res = CharsInfo()
        res.is_latin_letter = _arg1
        return res