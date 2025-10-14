# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.SingleNumValueType import SingleNumValueType
from pullenti.ner.core.ComplexNumCompareType import ComplexNumCompareType

class SingleNumComparer:
    
    def __init__(self) -> None:
        self.typ = ComplexNumCompareType.UNCOMPARABLE
        self.rank = 0
        self.delta = 0
        self.first = None;
        self.second = None;
        self.val1 = None;
        self.val2 = None;
    
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
        return Utils.toStringStringIO(res)
    
    def process(self, fir : 'SingleNumToken', sec : 'SingleNumToken') -> None:
        self.first = fir
        self.second = sec
        self.typ = ComplexNumCompareType.UNCOMPARABLE
        self.delta = 0
        self.rank = (0)
        self.val1 = (None)
        self.val2 = (None)
        for v1 in fir.vals: 
            for v2 in sec.vals: 
                if (v1.typ != v2.typ): 
                    continue
                rank_ = 1
                ty = ComplexNumCompareType.UNCOMPARABLE
                delt = 0
                if (v1.typ == SingleNumValueType.LETTER): 
                    ch1 = str.upper(v1.letter)
                    ch2 = str.upper(v2.letter)
                    if (LanguageHelper.is_cyrillic_char(ch1) != LanguageHelper.is_cyrillic_char(ch2)): 
                        if (LanguageHelper.is_cyrillic_char(ch1)): 
                            ch11 = LanguageHelper.get_lat_for_cyr(ch1)
                            if ((ord(ch11)) != 0): 
                                ch1 = ch11
                            else: 
                                ch22 = LanguageHelper.get_cyr_for_lat(ch2)
                                if ((ord(ch22)) != 0): 
                                    ch2 = ch22
                        else: 
                            ch11 = LanguageHelper.get_cyr_for_lat(ch1)
                            if ((ord(ch11)) != 0): 
                                ch1 = ch11
                            else: 
                                ch22 = LanguageHelper.get_lat_for_cyr(ch2)
                                if ((ord(ch22)) != 0): 
                                    ch2 = ch22
                    if ((ord(ch1)) < (ord(ch2))): 
                        ty = ComplexNumCompareType.LESS
                        delt = ((ord(ch2)) - (ord(ch1)))
                        if (ch1 == 'И' and ch2 == 'К'): 
                            delt = 1
                        elif (ch1 == 'Е' and ch2 == 'Ж'): 
                            delt = 1
                    elif ((ord(ch1)) > (ord(ch2))): 
                        ty = ComplexNumCompareType.GREAT
                        delt = ((ord(ch1)) - (ord(ch2)))
                        if (ch2 == 'И' and ch1 == 'К'): 
                            delt = 1
                        elif (ch2 == 'Е' and ch1 == 'Ж'): 
                            delt = 1
                    else: 
                        ty = ComplexNumCompareType.EQUALS
                elif (v1.val < v2.val): 
                    ty = ComplexNumCompareType.LESS
                    delt = (v2.val - v1.val)
                elif (v1.val > v2.val): 
                    ty = ComplexNumCompareType.GREAT
                    delt = (v1.val - v2.val)
                else: 
                    ty = ComplexNumCompareType.EQUALS
                if (ty == ComplexNumCompareType.GREAT): 
                    rank_ /= (2)
                if (rank_ > self.rank): 
                    self.rank = rank_
                    self.typ = ty
                    self.delta = delt
                    self.val1 = v1
                    self.val2 = v2
                    if (self.delta > 1): 
                        self.rank *= 0.98
        if (fir.suffix is not None and sec.suffix is not None): 
            if (fir.suffix != sec.suffix): 
                self.rank *= 0.8
        elif (fir.suffix is not None or sec.suffix is not None): 
            self.rank *= 0.9