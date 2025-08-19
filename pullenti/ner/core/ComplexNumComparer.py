# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ComplexNumCompareType import ComplexNumCompareType
from pullenti.ner.core.SingleNumComparer import SingleNumComparer

class ComplexNumComparer:
    """ Сравнение номеров (функцией Process) """
    
    def __init__(self) -> None:
        self.typ = ComplexNumCompareType.UNCOMPARABLE
        self.rank = 0
        self.delta = 0
        self.can_follow = False
        self.first = None;
        self.second = None;
        self.__m_comp = SingleNumComparer()
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.rank > 0): 
            print("{0}: ".format(self.rank), end="", file=res, flush=True)
        print(self.first, end="", file=res)
        if (self.typ == ComplexNumCompareType.UNCOMPARABLE): 
            print(" ?? ", end="", file=res)
        elif (self.typ == ComplexNumCompareType.EQUALS): 
            print(" == ", end="", file=res)
        elif (self.typ == ComplexNumCompareType.LESS): 
            print(" < ", end="", file=res)
        elif (self.typ == ComplexNumCompareType.GREAT): 
            print(" > ", end="", file=res)
        print(self.second, end="", file=res)
        if (self.delta > 0): 
            print(", Delt={0}".format(self.delta), end="", file=res, flush=True)
        if (self.can_follow): 
            print(", follow".format(), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def process(self, fir : 'ComplexNumToken', sec : 'ComplexNumToken') -> None:
        """ Сравнить два номера
        
        Args:
            fir(ComplexNumToken): 
            sec(ComplexNumToken): 
        """
        self.first = fir
        self.second = sec
        self.typ = ComplexNumCompareType.EQUALS
        self.delta = 0
        self.rank = (1)
        if (fir.prefix != sec.prefix or fir.suffix != sec.suffix): 
            if (((fir.suffix is None and sec.suffix == ".")) or ((fir.suffix == "." and sec.suffix is None))): 
                self.rank *= 0.98
            else: 
                self.rank *= 0.8
        i = 0
        i = 0
        first_pass3848 = True
        while True:
            if first_pass3848: first_pass3848 = False
            else: i += 1
            if (not ((i < len(fir.nums)) and (i < len(sec.nums)))): break
            n1 = fir.nums[i]
            n2 = sec.nums[i]
            self.__m_comp.process(n1, n2)
            if (self.__m_comp.typ == ComplexNumCompareType.UNCOMPARABLE): 
                self.typ = ComplexNumCompareType.UNCOMPARABLE
                self.rank = (0)
                return
            if (self.__m_comp.typ == ComplexNumCompareType.EQUALS and len(fir.nums) == len(sec.nums)): 
                self.rank *= self.__m_comp.rank
                continue
            if ((i + 1) == len(fir.nums) and (i + 1) == len(sec.nums)): 
                self.typ = self.__m_comp.typ
                self.rank *= self.__m_comp.rank
                self.delta = self.__m_comp.delta
            elif (((i + 1) < len(fir.nums)) and ((i + 1) < len(sec.nums))): 
                self.typ = ComplexNumCompareType.UNCOMPARABLE
                self.rank = (0)
                break
            elif ((i + 1) == len(fir.nums)): 
                if (self.__m_comp.typ == ComplexNumCompareType.EQUALS): 
                    self.typ = ComplexNumCompareType.LESS
                    self.rank *= self.__m_comp.rank
                    if (len(sec.nums) == (len(fir.nums) + 1) and sec.nums[i + 1].is_one): 
                        self.can_follow = True
                        self.rank /= (2)
                    else: 
                        self.rank /= (2)
                    break
                elif (self.__m_comp.typ == ComplexNumCompareType.LESS): 
                    self.typ = ComplexNumCompareType.UNCOMPARABLE
                    self.rank = (0)
                    break
                else: 
                    self.typ = ComplexNumCompareType.GREAT
                    self.rank *= self.__m_comp.rank
                    if (self.__m_comp.delta != 1): 
                        self.rank /= (2)
                    break
            elif ((i + 1) == len(sec.nums)): 
                if (self.__m_comp.typ == ComplexNumCompareType.EQUALS): 
                    self.typ = ComplexNumCompareType.GREAT
                    self.rank *= self.__m_comp.rank
                    if (len(fir.nums) == (len(sec.nums) + 1) and fir.nums[i + 1].is_one): 
                        self.rank /= (2)
                    else: 
                        self.rank /= (2)
                    break
                elif (self.__m_comp.typ == ComplexNumCompareType.LESS): 
                    self.typ = ComplexNumCompareType.LESS
                    self.rank *= self.__m_comp.rank
                    if (self.__m_comp.delta != 1): 
                        self.rank /= (2)
                    else: 
                        self.can_follow = True
                    break
                else: 
                    self.typ = ComplexNumCompareType.UNCOMPARABLE
                    self.rank = (0)
                    break