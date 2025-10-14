# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing

from pullenti.ner.core.SingleNumValueType import SingleNumValueType
from pullenti.ner.core.ComplexNumCompareType import ComplexNumCompareType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.SingleNumComparer import SingleNumComparer
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.SingleNumToken import SingleNumToken

class ComplexNumToken(MetaToken):
    """ Поддержка сложной нумерации разделов, пунктов, формул и т.п.
    (составная, возможны римские цифры, буквы) """
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.nums = list()
    
    @property
    def normal(self) -> str:
        if (len(self.nums) == 0): 
            return None
        res = self.nums[0].normal
        i = 1
        while i < len(self.nums): 
            res = "{0}.{1}".format(res, self.nums[i].normal)
            i += 1
        return res
    
    @property
    def prefix(self) -> str:
        return (self.nums[0].prefix if len(self.nums) > 0 else None)
    
    @property
    def suffix(self) -> str:
        return (self.nums[len(self.nums) - 1].suffix if len(self.nums) > 0 else None)
    
    @property
    def is_one(self) -> bool:
        if (len(self.nums) == 0): 
            return False
        return self.nums[len(self.nums) - 1].is_one
    
    def __str__(self) -> str:
        return self.to_string_ex(False)
    
    def to_string_ex(self, ignore_suffix : bool) -> str:
        if (len(self.nums) == 0): 
            return ""
        res = self.nums[0].value
        i = 1
        while i < len(self.nums): 
            res += self.nums[i].value
            i += 1
        if (ignore_suffix and self.suffix is not None and res.endswith(self.suffix)): 
            res = res[0:0+len(res) - len(self.suffix)]
        return res
    
    @staticmethod
    def try_parse(t : 'Token', prev : 'ComplexNumToken'=None, force : bool=False, ignore_last_suffix : bool=False) -> 'ComplexNumToken':
        """ Выделить сложный номер с указанного токена
        
        Args:
            t(Token): 
            prev(ComplexNumToken): предыдущий номер (если есть)
            force(bool): обязательно ли выделять
            ignore_last_suffix(bool): суффикс у последнего составного числа игнорировать
        
        Returns:
            ComplexNumToken: номер или null
        """
        if (t is None): 
            return None
        if (isinstance(t, ReferentToken)): 
            r = t.get_referent()
            if (r is not None and r.type_name == "BOOKLINKREF"): 
                t = t.begin_token
        nt = SingleNumToken.try_parse(t, True, force)
        if (nt is None): 
            return None
        res = ComplexNumToken(t, nt.end_token)
        res.nums.append(nt)
        t = nt.end_token.next0_
        while t is not None: 
            if (t.is_whitespace_before): 
                if (t.whitespaces_before_count > 2): 
                    break
                if (force and t.is_char_of("<(")): 
                    pass
                else: 
                    break
            nt = SingleNumToken.try_parse(t, False, force)
            if (nt is None): 
                if (((force and t.is_hiphen and not t.is_newline_before) and not t.is_newline_after and (isinstance(t.next0_, NumberToken))) and res.nums[len(res.nums) - 1].suffix is None): 
                    nt = SingleNumToken.try_parse(t.next0_, False, False)
                    if (nt is not None): 
                        res.nums[len(res.nums) - 1].end_token = t
                        res.nums[len(res.nums) - 1].suffix = "-"
                if (nt is None): 
                    break
            if (nt.vals[0].typ == SingleNumValueType.LETTER): 
                if (res.nums[0].vals[0].typ == SingleNumValueType.LETTER): 
                    return None
                if (res.nums[len(res.nums) - 1].vals[0].typ == SingleNumValueType.LETTER): 
                    return None
            res.nums.append(nt)
            t = nt.end_token
            res.end_token = t
            t = t.next0_
        if (len(res.nums) == 1): 
            if (res.prefix == "<" and res.suffix == ">"): 
                return None
            if (not force and res.is_newline_before and res.is_newline_after): 
                return None
        if ((ignore_last_suffix and res.suffix is not None and len(res.suffix) == 1) and res.end_token.is_char(res.suffix[0])): 
            res.end_token = res.end_token.previous
            n1 = res.nums[len(res.nums) - 1]
            if (n1.value is not None and n1.value.endswith(n1.suffix)): 
                n1.value = n1.value[0:0+len(n1.value) - 1]
            n1.suffix = (None)
            n1.end_token = res.end_token
        return res
    
    @staticmethod
    def correct_seq(seq : typing.List['ComplexNumToken']) -> None:
        if (len(seq) == 0): 
            return
        seq[0].__correct(None)
        i = 1
        while i < len(seq): 
            seq[i].__correct(seq[i - 1])
            i += 1
        lat = 0
        cyr = 0
        for s in seq: 
            for n in s.nums: 
                for v in n.vals: 
                    if (v.typ == SingleNumValueType.LETTER): 
                        if ((ord(v.letter)) < 0x80): 
                            lat += 1
                        else: 
                            cyr += 1
        if (lat > cyr or cyr > lat): 
            for s in seq: 
                for n in s.nums: 
                    for i in range(len(n.vals) - 1, -1, -1):
                        if (n.vals[i].typ == SingleNumValueType.LETTER and len(n.vals) > 1): 
                            if ((ord(n.vals[i].letter)) < 0x80): 
                                if (cyr > lat): 
                                    del n.vals[i]
                            elif (lat > cyr): 
                                del n.vals[i]
    
    def __correct(self, prev : 'ComplexNumToken') -> None:
        if (prev is not None and len(prev.nums) == len(self.nums)): 
            self.nums[len(self.nums) - 1].correct(prev.nums[len(prev.nums) - 1])
        elif (prev is None): 
            self.nums[len(self.nums) - 1].correct(None)
    
    def can_be_psevdo_subseq(self, sub : 'ComplexNumToken') -> bool:
        if (sub is None): 
            return False
        if (self.prefix != sub.prefix or self.suffix != sub.suffix): 
            return False
        if ((len(self.nums) + 1) != len(sub.nums)): 
            return False
        if (not sub.nums[len(sub.nums) - 1].is_one): 
            return False
        comp = SingleNumComparer()
        i = 0
        while i < len(self.nums): 
            comp.process(self.nums[i], sub.nums[i])
            if (comp.typ != ComplexNumCompareType.EQUALS): 
                return False
            i += 1
        return True