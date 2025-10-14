# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.ComplexNumCompareType import ComplexNumCompareType
from pullenti.ner.core.SingleNumComparer import SingleNumComparer
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.SingleNumValueType import SingleNumValueType
from pullenti.ner.core.SingleNumValue import SingleNumValue
from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NumberHelper import NumberHelper

class SingleNumToken(MetaToken):
    """ Элемент составного номера """
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.vals = list()
        self.value = None;
        self.prefix = None;
        self.suffix = None;
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0}: ".format(self.value), end="", file=res, flush=True)
        i = 0
        while i < len(self.vals): 
            if (i > 0): 
                print("/", end="", file=res)
            print(str(self.vals[i]), end="", file=res)
            i += 1
        return Utils.toStringStringIO(res)
    
    @property
    def normal(self) -> str:
        """ Нормализация значения """
        if (len(self.vals) == 0): 
            return "?"
        if (self.vals[0].typ == SingleNumValueType.LETTER): 
            return "{0}".format(self.vals[0].letter)
        return str(self.vals[0].val)
    
    def __add_num(self, val : int, rom : bool, upper : bool=False) -> None:
        res = SingleNumValue()
        res.val = val
        if (rom): 
            res.typ = SingleNumValueType.ROMAN
        if (rom and upper): 
            self.vals.insert(0, res)
        else: 
            self.vals.append(res)
    
    def __add_char(self, ch : 'char', up : bool) -> None:
        for v in self.vals: 
            if (ch == v.letter): 
                return
        res = SingleNumValue()
        res.typ = SingleNumValueType.LETTER
        res.letter = str.lower(ch)
        res.upper = up
        self.vals.append(res)
    
    @staticmethod
    def try_parse(t : 'Token', first : bool, force : bool=False) -> 'SingleNumToken':
        if (t is None): 
            return None
        if (t.is_value("I", None)): 
            pass
        if (not first and t.is_whitespace_before): 
            if (not force and not t.is_char_of(".(<")): 
                return None
        t0 = t
        res = None
        if (t.is_char('(') and not t.is_whitespace_after): 
            res = SingleNumToken.try_parse(t.next0_, first, False)
            if (res is not None and res.end_token.is_char(')')): 
                res.begin_token = t
                res.prefix = "("
            return res
        if (t.is_char('<') and not t.is_whitespace_after): 
            res = SingleNumToken.try_parse(t.next0_, first, False)
            if (res is not None and res.end_token.is_char('>')): 
                res.begin_token = t
                res.prefix = "<"
                if (not first): 
                    res.suffix = None
                    res.prefix = res.suffix
                    res.value = ("<" + res.value)
                if (not res.end_token.is_whitespace_after): 
                    t = res.end_token.next0_
                    if (t is not None): 
                        if (t.is_char_of(".])\\")): 
                            res.end_token = t
                            res.suffix = t.get_source_text()
                            res.value += res.suffix
            return res
        has_pref = False
        if (first): 
            tt = MiscHelper.check_number_prefix(t)
            if (tt is not None and not tt.is_char_of(".)")): 
                if (t.is_newline_before): 
                    has_pref = True
                    t = tt
                elif ((t.previous is not None and SingleNumToken.__check_keyword(t.previous)) or t.previous.is_newline_before): 
                    has_pref = True
                    t = tt
        nt = Utils.asObjectOrNull(t, NumberToken)
        if (nt is not None and nt.int_value is not None and (nt.int_value < 3000)): 
            if (nt.typ == NumberSpellingType.WORDS and t == t0): 
                if (not first): 
                    return None
                if (force): 
                    pass
                elif (not t.is_newline_before and SingleNumToken.__check_keyword(t.previous)): 
                    pass
                elif (t.next0_ is not None and not t.is_newline_after and SingleNumToken.__check_keyword(t.next0_)): 
                    pass
                else: 
                    return None
            res = SingleNumToken(t0, t)
            res.__add_num(t.int_value, False, False)
        elif ((isinstance(t, TextToken)) and t.chars.is_letter and t.length_char == 1): 
            if (Utils.isNullOrEmpty(t.term)): 
                return None
            if (t.next0_ is not None and t.next0_.is_char_of(")")): 
                pass
            elif (not first or force): 
                pass
            else: 
                if (t.previous is not None and t.previous.is_char_of("(<") and ((t.previous.is_newline_before or SingleNumToken.__check_keyword(t.previous.previous)))): 
                    pass
                elif (SingleNumToken.__check_keyword(t.previous)): 
                    pass
                elif (t.chars.is_all_upper and t.is_char_of("IXХ") and not t.is_whitespace_after): 
                    pass
                elif (t.is_newline_before and not t.is_whitespace_after): 
                    pass
                else: 
                    return None
                if (t.next0_ is not None and t.next0_.is_char_of(".)>")): 
                    pass
                elif (not t.is_whitespace_after and t.next0_.is_char('(')): 
                    pass
                elif (t.is_newline_after): 
                    pass
                else: 
                    return None
            nt = (None)
            if (t.chars.is_all_upper or t.is_value("I", None)): 
                nt = NumberHelper.try_parse_roman(t)
            up = t.chars.is_all_upper
            res = SingleNumToken(t0, t)
            ch = t.term[0]
            res.__add_char(ch, up)
            if ((ord(ch)) < 0x80): 
                cyr = LanguageHelper.get_cyr_for_lat(ch)
                if (cyr != (chr(0))): 
                    res.__add_char(cyr, up)
            else: 
                lat = LanguageHelper.get_lat_for_cyr(ch)
                if (lat != (chr(0))): 
                    res.__add_char(lat, up)
            if (ch == 'I'): 
                res.__add_num(1, True, up)
            if (ch == 'V'): 
                res.__add_num(5, True, up)
            if (ch == 'X' or ch == 'Х'): 
                res.__add_num(10, True, up)
        else: 
            nt = NumberHelper.try_parse_roman(t)
            if (nt is None or nt.int_value is None): 
                return None
            ok = False
            if (not first or force): 
                ok = True
            elif (t.next0_ is not None and t.next0_.is_char_of(".)")): 
                ok = True
            elif (not t.is_newline_before and SingleNumToken.__check_keyword(t.previous)): 
                ok = True
            if (not ok): 
                return None
            res = SingleNumToken(t0, t)
            res.__add_num(nt.int_value, True, nt.chars.is_all_upper)
        if (res is None): 
            return None
        if (not res.end_token.is_whitespace_after): 
            t = res.end_token.next0_
            if (t is not None): 
                if (t.is_char_of(".])>\\")): 
                    res.end_token = t
                    res.suffix = t.get_source_text()
        if (res.value is None): 
            res.value = res.get_source_text()
        if ((not has_pref and first and not force) and res.suffix is None and not res.is_newline_after): 
            tt = res.end_token.next0_
            if ((isinstance(tt, TextToken)) and tt.chars.is_all_lower): 
                return None
        if (len(res.value) == 1 and res.suffix is None and res.prefix is None): 
            if (str.isalpha(res.value[0]) and res.begin_token.chars.is_all_upper): 
                if (res.begin_token.next0_ is not None and res.begin_token.next0_.chars.is_all_lower): 
                    return None
        return res
    
    @staticmethod
    def __check_keyword(t : 'Token') -> bool:
        if (not (isinstance(t, TextToken))): 
            return False
        term = t.term
        if (((term == "СТАТЬЯ" or term == "ГЛАВА" or term == "РАЗДЕЛ") or term == "ЧАСТЬ" or term == "ПОДРАЗДЕЛ") or term == "ПАРАГРАФ" or term == "ПОДПАРАГРАФ"): 
            return True
        return False
    
    @property
    def is_one(self) -> bool:
        """ Признак, что с номер может начинаться нумерация """
        for v in self.vals: 
            if (v.is_one): 
                return True
        return False
    
    def correct(self, prev : 'SingleNumToken') -> None:
        if (prev is None): 
            if (self.is_one): 
                for i in range(len(self.vals) - 1, -1, -1):
                    if (not self.vals[i].is_one): 
                        del self.vals[i]
            return
        comp = SingleNumComparer()
        comp.process(prev, self)
        if (comp.typ != ComplexNumCompareType.LESS): 
            return
        for i in range(len(prev.vals) - 1, -1, -1):
            if (prev.vals[i] != comp.val1): 
                del prev.vals[i]
        for i in range(len(self.vals) - 1, -1, -1):
            if (self.vals[i] != comp.val2): 
                del self.vals[i]