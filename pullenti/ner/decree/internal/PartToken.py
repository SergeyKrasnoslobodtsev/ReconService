# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from enum import IntEnum
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.instrument.InstrumentKind import InstrumentKind
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.ComplexNumToken import ComplexNumToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.decree.DecreeReferent import DecreeReferent
from pullenti.ner.Token import Token
from pullenti.ner.decree.DecreeChangeKind import DecreeChangeKind
from pullenti.ner.decree.DecreeAnalyzer import DecreeAnalyzer

class PartToken(MetaToken):
    # Примитив, из которых состоит часть декрета (статья, пункт и часть)
    
    class ItemType(IntEnum):
        UNDEFINED = 0
        PREFIX = 1
        APPENDIX = 2
        DOCPART = 3
        PART = 4
        SECTION = 5
        SUBSECTION = 6
        CHAPTER = 7
        CLAUSE = 8
        PARAGRAPH = 9
        SUBPARAGRAPH = 10
        ITEM = 11
        SUBITEM = 12
        INDENTION = 13
        SUBINDENTION = 14
        PREAMBLE = 15
        NOTICE = 16
        FOOTNOTE = 17
        FORMULA = 18
        FORM = 19
        TABLE = 20
        TABLECOLUMN = 21
        TABLEROW = 22
        SENTENCE = 23
        SUBPROGRAM = 24
        PAGE = 25
        ADDAGREE = 26
        NAME = 27
        
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)
    
    class PartValue(MetaToken):
        
        def __init__(self, begin : 'Token', end : 'Token') -> None:
            super().__init__(begin, end, None)
            self.value = None;
        
        @property
        def source_value(self) -> str:
            from pullenti.ner.MetaToken import MetaToken
            t0 = self.begin_token
            t1 = self.end_token
            if (t1.is_char('.')): 
                t1 = t1.previous
            elif (t1.is_char(')') and not t0.is_char('(')): 
                t1 = t1.previous
            if (t0.begin_char > t1.begin_char): 
                return ""
            return (MetaToken(t0, t1)).get_source_text()
        
        @property
        def int_value(self) -> int:
            if (Utils.isNullOrEmpty(self.value)): 
                return 0
            num = 0
            wrapnum1314 = RefOutArgWrapper(0)
            inoutres1315 = Utils.tryParseInt(self.value, wrapnum1314)
            num = wrapnum1314.value
            if (inoutres1315): 
                return num
            return 0
        
        def __str__(self) -> str:
            return self.value
        
        def correct_value(self) -> None:
            from pullenti.ner.decree.DecreeReferent import DecreeReferent
            from pullenti.ner.TextToken import TextToken
            from pullenti.ner.NumberToken import NumberToken
            from pullenti.ner.core.BracketHelper import BracketHelper
            if ((isinstance(self.end_token.next0_, TextToken)) and self.end_token.next0_.length_char == 1 and self.end_token.next0_.chars.is_letter): 
                if (not self.end_token.is_whitespace_after): 
                    self.value += self.end_token.next0_.term
                    self.end_token = self.end_token.next0_
                elif ((self.end_token.whitespaces_after_count < 2) and self.end_token.next0_.next0_ is not None and self.end_token.next0_.next0_.is_char(')')): 
                    self.value += self.end_token.next0_.term
                    self.end_token = self.end_token.next0_.next0_
            if (((self.end_token.whitespaces_after_count < 3) and BracketHelper.can_be_start_of_sequence(self.end_token.next0_, False, False) and (isinstance(self.end_token.next0_.next0_, TextToken))) and self.end_token.next0_.next0_.length_char == 1 and BracketHelper.can_be_end_of_sequence(self.end_token.next0_.next0_.next0_, False, self.end_token.next0_, False)): 
                self.value = "{0}.{1}".format(self.value, self.end_token.next0_.next0_.term)
                self.end_token = self.end_token.next0_.next0_.next0_
            if (((self.end_token.whitespaces_after_count < 3) and BracketHelper.can_be_start_of_sequence(self.end_token.next0_, False, False) and (isinstance(self.end_token.next0_.next0_, NumberToken))) and BracketHelper.can_be_end_of_sequence(self.end_token.next0_.next0_.next0_, False, self.end_token.next0_, False)): 
                self.value = "{0}.{1}".format(self.value, self.end_token.next0_.next0_.value)
                self.end_token = self.end_token.next0_.next0_.next0_
            if ((isinstance(self.end_token.next0_, NumberToken)) and (self.end_token.whitespaces_after_count < 2) and (self.end_token.next0_.whitespaces_after_count < 2)): 
                ok = False
                tt2 = self.end_token.next0_
                if (isinstance(tt2.get_referent(), DecreeReferent)): 
                    ok = True
                else: 
                    ne = PartToken.try_attach(tt2.next0_, None, False, False)
                    if (ne is not None and len(ne.values) == 1): 
                        ok = True
                if (ok): 
                    self.end_token = self.end_token.next0_
                    self.value = "{0}.{1}".format(self.value, self.end_token.value)
            t = self.end_token.next0_
            first_pass3913 = True
            while True:
                if first_pass3913: first_pass3913 = False
                else: t = t.next0_
                if (not (t is not None)): break
                if (t.is_whitespace_before): 
                    if (t.whitespaces_before_count > 1): 
                        break
                    if (t.is_char('<')): 
                        pass
                    else: 
                        if (((isinstance(t, TextToken)) and t.length_char == 1 and t.next0_ is not None) and t.next0_.is_char(')')): 
                            self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), t.term)
                            t = t.next0_
                            self.end_token = t
                        break
                if (t.is_char_of("_.") and not t.is_whitespace_after): 
                    if (isinstance(t.next0_, NumberToken)): 
                        self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), t.next0_.value)
                        t = t.next0_
                        self.end_token = t
                        continue
                    if (((t.next0_ is not None and t.next0_.is_char('(') and (isinstance(t.next0_.next0_, NumberToken))) and not t.next0_.is_whitespace_after and t.next0_.next0_.next0_ is not None) and t.next0_.next0_.next0_.is_char(')')): 
                        self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), t.next0_.next0_.value)
                        self.end_token = t.next0_.next0_.next0_
                        continue
                if ((t.is_hiphen and not t.is_whitespace_after and (isinstance(t.next0_, NumberToken))) and t.next0_.int_value is not None): 
                    n1 = 0
                    wrapn11316 = RefOutArgWrapper(0)
                    inoutres1317 = Utils.tryParseInt(self.value, wrapn11316)
                    n1 = wrapn11316.value
                    if (inoutres1317): 
                        if (n1 >= t.next0_.int_value): 
                            self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), t.next0_.value)
                            t = t.next0_
                            self.end_token = t
                            continue
                    if (((self.value is not None and self.value.find('.') > 0 and (isinstance(t.previous, NumberToken))) and t.next0_.next0_ is not None and t.next0_.next0_.is_char('.')) and not (isinstance(t.next0_.next0_.next0_, NumberToken))): 
                        self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), t.next0_.value)
                        t = t.next0_.next0_
                        self.end_token = t
                        break
                if (t.is_char_of("(<") and (isinstance(t.next0_, NumberToken)) and t.next0_.next0_ is not None): 
                    if (t.next0_.next0_.is_char_of(")>")): 
                        self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), t.next0_.value)
                        t = t.next0_.next0_
                        self.end_token = t
                    elif ((t.next0_.next0_.is_char_of(".-") and (isinstance(t.next0_.next0_.next0_, NumberToken)) and t.next0_.next0_.next0_.next0_ is not None) and t.next0_.next0_.next0_.next0_.is_char_of(")>")): 
                        self.value = "{0}.{1}.{2}".format(Utils.ifNotNull(self.value, ""), t.next0_.value, t.next0_.next0_.next0_.value)
                        t = t.next0_.next0_.next0_.next0_
                        self.end_token = t
                    if (t.next0_ is not None and t.next0_.is_char('.') and not t.is_whitespace_after): 
                        t = t.next0_
                    continue
                if ((t.is_char('\\') and (isinstance(t.next0_, NumberToken)) and not t.is_whitespace_before) and not t.is_whitespace_after): 
                    self.value = "{0}.{1}".format(Utils.ifNotNull(self.value, ""), t.next0_.value)
                    t = t.next0_
                    self.end_token = t
                    continue
                break
            if (self.end_token.next0_ is not None and self.end_token.next0_.is_char_of(".") and not self.end_token.is_whitespace_after): 
                if (self.end_token.next0_.next0_ is not None and (((isinstance(self.end_token.next0_.next0_.get_referent(), DecreeReferent)) or self.end_token.next0_.next0_.is_hiphen)) and not self.end_token.next0_.is_newline_after): 
                    self.end_token = self.end_token.next0_
            if (self.begin_token == self.end_token and self.end_token.next0_ is not None and self.end_token.next0_.is_char(')')): 
                ok = True
                lev = 0
                ttt = self.begin_token.previous
                while ttt is not None: 
                    if (ttt.is_newline_after): 
                        break
                    if (ttt.is_char(')')): 
                        lev += 1
                    elif (ttt.is_char('(')): 
                        lev -= 1
                        if (lev < 0): 
                            ok = False
                            break
                    ttt = ttt.previous
                if (ok): 
                    tt = self.end_token.next0_.next0_
                    if (tt is not None): 
                        if ((isinstance(tt.get_referent(), DecreeReferent)) or PartToken.try_attach(tt, None, False, False) is not None): 
                            self.end_token = self.end_token.next0_
        
        @staticmethod
        def _new1320(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'PartValue':
            res = PartToken.PartValue(_arg1, _arg2)
            res.value = _arg3
            return res
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = PartToken.ItemType.UNDEFINED
        self.alt_typ = PartToken.ItemType.UNDEFINED
        self.values = list()
        self.name = None;
        self.ind = 0
        self.decree = None;
        self.is_doubt = False
        self.delim_after = False
        self.has_terminator = False
        self.anafor_ref = None;
    
    def __str__(self) -> str:
        res = Utils.newStringIO(Utils.enumToString(self.typ))
        if (self.alt_typ != PartToken.ItemType.UNDEFINED): 
            print("/{0}".format(Utils.enumToString(self.alt_typ)), end="", file=res, flush=True)
        for v in self.values: 
            print(" {0}".format(v), end="", file=res, flush=True)
        if (self.name is not None): 
            print(" \"{0}\"".format(self.name), end="", file=res, flush=True)
        if (self.delim_after): 
            print(", DelimAfter", end="", file=res)
        if (self.is_doubt): 
            print(", Doubt", end="", file=res)
        if (self.has_terminator): 
            print(", Terminator", end="", file=res)
        if (self.anafor_ref is not None): 
            print(", Ref='{0}'".format(self.anafor_ref.term), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def add_value(self, add : int) -> bool:
        if (len(self.values) != 1): 
            return False
        n = 0
        wrapn1318 = RefOutArgWrapper(0)
        inoutres1319 = Utils.tryParseInt(Utils.ifNotNull(self.values[0].value, ""), wrapn1318)
        n = wrapn1318.value
        if (not inoutres1319): 
            return False
        n += add
        self.values[0].value = str(n)
        return True
    
    @staticmethod
    def try_attach(t : 'Token', prev : 'PartToken', in_bracket : bool=False, ignore_number : bool=False) -> 'PartToken':
        from pullenti.ner.decree.internal.DecreeChangeToken import DecreeChangeToken
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        if (t is None): 
            return None
        res = None
        if (t.morph.class0_.is_personal_pronoun and (t.whitespaces_after_count < 2)): 
            res = PartToken.try_attach(t.next0_, prev, False, False)
            if (res is not None): 
                res.anafor_ref = (Utils.asObjectOrNull(t, TextToken))
                res.begin_token = t
                return res
        tt = Utils.asObjectOrNull(t, TextToken)
        if ((isinstance(t, NumberToken)) and t.next0_ is not None and (t.whitespaces_after_count < 3)): 
            nums = list()
            nums.append(Utils.asObjectOrNull(t, NumberToken))
            tt2 = t.next0_
            while tt2 is not None: 
                if (tt2.is_comma_and and (isinstance(tt2.next0_, NumberToken))): 
                    tt2 = tt2.next0_
                    nums.append(Utils.asObjectOrNull(tt2, NumberToken))
                    if (tt2.previous.is_and): 
                        tt2 = tt2.next0_
                        break
                else: 
                    break
                tt2 = tt2.next0_
            re = PartToken.__create_part_typ0(tt2, prev)
            if (re is not None): 
                t11 = re.end_token.next0_
                ok1 = False
                if (t11 is not None and (isinstance(t11.get_referent(), DecreeReferent))): 
                    ok1 = True
                elif (prev is not None and t11 is not None and not (isinstance(t11, NumberToken))): 
                    ok1 = True
                elif (t.previous is not None and t.previous.is_value("В", None)): 
                    ok1 = True
                elif (t11 is not None): 
                    dcc = DecreeChangeToken.try_attach(t11, None, False, None, False, False)
                    if (dcc is not None): 
                        if (dcc.change_val is not None or dcc.act_kind != DecreeChangeKind.UNDEFINED): 
                            ok1 = True
                if (not ok1): 
                    res1 = PartToken.try_attach(t11, None, False, False)
                    if (res1 is not None): 
                        ok1 = True
                if (ok1 or in_bracket): 
                    re.begin_token = t
                    for n in nums: 
                        re.values.append(PartToken.PartValue._new1320(n, n, n.value))
                    return re
        if (t.is_value("ПОСЛЕДНИЙ", None)): 
            re = PartToken.__create_part_typ0(t.next0_, None)
            if (re is not None): 
                re.begin_token = t
                re.values.append(PartToken.PartValue._new1320(t, t, t.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)))
                return re
        if (((isinstance(t, NumberToken)) and t.typ == NumberSpellingType.DIGIT and prev is None) and t.previous is not None): 
            t0 = t.previous
            delim = False
            if (t0.is_char(',') or t0.morph.class0_.is_conjunction): 
                delim = True
                t0 = t0.previous
            if (t0 is None): 
                return None
            dr = Utils.asObjectOrNull(t0.get_referent(), DecreePartReferent)
            if (dr is None): 
                if (t0.is_char('(') and t.next0_ is not None): 
                    if (t.next0_.is_value("ЧАСТЬ", None) or t.next0_.is_value("Ч", None)): 
                        te = t.next0_
                        if (te.next0_ is not None and te.next0_.is_char('.')): 
                            te = te.next0_
                        res = PartToken._new1036(t, te, PartToken.ItemType.PART)
                        res.values.append(PartToken.PartValue._new1320(t, t, str(t.value)))
                        return res
                return None
            if (dr.clause is None): 
                return None
            res = PartToken._new1324(t, t, PartToken.ItemType.CLAUSE, not delim)
            pv = PartToken.PartValue._new1320(t, t, str(t.value))
            res.values.append(pv)
            t = t.next0_
            while t is not None: 
                if (t.is_whitespace_before): 
                    break
                elif (t.is_char_of("._") and (isinstance(t.next0_, NumberToken))): 
                    t = t.next0_
                    pv.end_token = res.end_token = t
                    pv.value = "{0}.{1}".format(pv.value, t.value)
                else: 
                    break
                t = t.next0_
            return res
        if (((isinstance(t, NumberToken)) and t.typ == NumberSpellingType.DIGIT and prev is not None) and prev.typ == PartToken.ItemType.PREFIX and (t.whitespaces_before_count < 3)): 
            pv = PartToken.PartValue._new1320(t, t, str(t.value))
            pv.correct_value()
            ttt1 = pv.end_token.next0_
            ne = DecreeToken.try_attach(ttt1, None, False)
            ok = False
            if (ne is not None and ne.typ == DecreeToken.ItemType.TYP): 
                ok = True
            elif (DecreeAnalyzer._check_other_typ(ttt1, True) is not None): 
                ok = True
            elif (DecreeAnalyzer._get_decree(ttt1) is not None): 
                ok = True
            if (ok): 
                res = PartToken._new1036(t, pv.end_token, PartToken.ItemType.ITEM)
                res.values.append(pv)
                return res
        if (tt is None): 
            return None
        if (tt.length_char == 1 and not tt.chars.is_all_lower): 
            if (not MiscHelper.can_be_start_of_sentence(tt)): 
                if (tt.previous is not None and tt.previous.is_value("ДОГОВОР", None)): 
                    pass
                else: 
                    return None
        t1 = tt
        res = PartToken.__create_part_typ0(t1, prev)
        if (res is not None): 
            t1 = res.end_token
        elif ((t1.is_value("СИЛУ", None) or t1.is_value("СОГЛАСНО", None) or t1.is_value("СООТВЕТСТВИЕ", None)) or t1.is_value("ПОЛОЖЕНИЕ", None)): 
            if (t1.is_value("СИЛУ", None) and t1.previous is not None and t1.previous.morph.class0_.is_verb): 
                return None
            if (t1.is_value("ПОЛОЖЕНИЕ", None) and prev is not None and not t1.chars.is_all_lower): 
                return None
            res = PartToken._new1036(t1, t1, PartToken.ItemType.PREFIX)
            if (t1.next0_ is not None and t1.next0_.is_value("С", None)): 
                res.end_token = t1.next0_
            return res
        elif (((t1.is_value("УГОЛОВНОЕ", None) or t1.is_value("КРИМІНАЛЬНА", None))) and t1.next0_ is not None and ((t1.next0_.is_value("ДЕЛО", None) or t1.next0_.is_value("СПРАВА", None)))): 
            t1 = t1.next0_
            if (t1.next0_ is not None and t1.next0_.is_value("ПО", None)): 
                t1 = t1.next0_
            return PartToken._new1036(t, t1, PartToken.ItemType.PREFIX)
        elif ((((t1.is_value("МОТИВИРОВОЧНЫЙ", None) or t1.is_value("МОТИВУВАЛЬНИЙ", None) or t1.is_value("РЕЗОЛЮТИВНЫЙ", None)) or t1.is_value("РЕЗОЛЮТИВНИЙ", None))) and t1.next0_ is not None and ((t1.next0_.is_value("ЧАСТЬ", None) or t1.next0_.is_value("ЧАСТИНА", None)))): 
            rr = PartToken._new1036(t1, t1.next0_, PartToken.ItemType.PART)
            rr.values.append(PartToken.PartValue._new1320(t1, t1, ("мотивировочная" if t1.is_value("МОТИВИРОВОЧНЫЙ", None) or t1.is_value("МОТИВУВАЛЬНИЙ", None) else "резолютивная")))
            return rr
        if (res is None): 
            if ((isinstance(t, TextToken)) and not t.chars.is_all_lower): 
                ok = False
                if (t.is_newline_before): 
                    ok = True
                elif (t.previous.is_char_of(")") or t.previous.is_value("В", None)): 
                    ok = True
                elif (prev is not None and prev.end_token.next0_ == t): 
                    ok = True
                if (ok and DecreeToken.is_keyword(t, False) is not None): 
                    cou = 100
                    ttt = t.next0_
                    first_pass3914 = True
                    while True:
                        if first_pass3914: first_pass3914 = False
                        else: ttt = ttt.next0_; cou -= 1
                        if (not (ttt is not None and cou > 0)): break
                        if (ttt.is_newline_before): 
                            break
                        if (ttt.is_value("УТВЕРЖДЕННЫЙ", None)): 
                            break
                        r = ttt.get_referent()
                        if (r is not None and r.type_name == "ORGANIZATION"): 
                            break
                        if (ttt.is_char('(')): 
                            res1 = PartToken.try_attach(ttt.next0_, None, False, False)
                            if (res1 is not None and res1.end_token.next0_ is not None and res1.end_token.next0_.is_char(')')): 
                                res1.name = MiscHelper.get_text_value(t, ttt.previous, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                                res1.begin_token = t
                                res1.end_token = res1.end_token.next0_
                                res1.morph = t.morph
                                return res1
                        br = BracketHelper.try_parse(ttt, BracketParseAttr.NO, 100)
                        if (br is not None): 
                            ttt = br.end_token
                            continue
                        if (ttt.is_comma and ttt.next0_ is not None and ttt.next0_.is_value("ЯВЛЯЮЩИЙСЯ", None)): 
                            res1 = PartToken.try_attach(ttt.next0_.next0_, None, False, False)
                            if (res1 is not None and res1.typ == PartToken.ItemType.APPENDIX): 
                                res1.name = MiscHelper.get_text_value(t, ttt.previous, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                                res1.begin_token = t
                                res1.morph = t.morph
                                return res1
                        if ((isinstance(ttt, TextToken)) and ttt.term == "ПРИЛОЖЕНИЯ"): 
                            res1 = PartToken.try_attach(ttt, None, False, False)
                            if (res1 is not None and res1.typ == PartToken.ItemType.APPENDIX): 
                                res1.name = MiscHelper.get_text_value(t, ttt.previous, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
                                res1.begin_token = t
                                res1.morph = t.morph
                                return res1
                        if (isinstance(ttt, TextToken)): 
                            if (ttt.is_pure_verb): 
                                break
            return None
        if (ignore_number or res.typ == PartToken.ItemType.NAME or res.typ == PartToken.ItemType.PREAMBLE): 
            return res
        if (res.is_newline_after): 
            if (res.chars.is_all_upper): 
                return None
        if (t1.next0_ is not None and t1.next0_.is_char('.')): 
            if (not t1.next0_.is_newline_after or (t1.length_char < 3)): 
                t1 = t1.next0_
                if (t1.next0_ is not None and MiscHelper.can_be_start_of_sentence(t1.next0_)): 
                    if (isinstance(t1.next0_, TextToken)): 
                        return None
                    if ((isinstance(t1.next0_, NumberToken)) and t1.next0_.typ == NumberSpellingType.WORDS): 
                        return None
        t1 = t1.next0_
        if (t1 is None): 
            return None
        if (res.typ == PartToken.ItemType.CLAUSE): 
            if (((isinstance(t1, NumberToken)) and t1.value == "3" and not t1.is_whitespace_after) and t1.next0_ is not None and t1.next0_.length_char == 2): 
                return None
        if (res.typ == PartToken.ItemType.CLAUSE and t1.is_value("СТ", None)): 
            t1 = t1.next0_
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0_
        elif (res.typ == PartToken.ItemType.PART and t1.is_value("Ч", None)): 
            t1 = t1.next0_
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0_
        elif (res.typ == PartToken.ItemType.ITEM and t1.is_value("П", None)): 
            t1 = t1.next0_
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0_
            res.alt_typ = PartToken.ItemType.SUBITEM
        elif ((res.typ == PartToken.ItemType.ITEM and t1.is_char_of("\\/") and t1.next0_ is not None) and t1.next0_.is_value("П", None)): 
            t1 = t1.next0_.next0_
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0_
            res.alt_typ = PartToken.ItemType.SUBITEM
        if (t1 is None): 
            return None
        if (res.typ == PartToken.ItemType.CLAUSE and (isinstance(t1.get_referent(), DecreeReferent)) and t1.next0_ is not None): 
            res.decree = (Utils.asObjectOrNull(t1.get_referent(), DecreeReferent))
            t1 = t1.next0_
        ttn = MiscHelper.check_number_prefix(t1)
        first_num_prefix = None
        if (ttn is not None): 
            first_num_prefix = (Utils.asObjectOrNull(t1, TextToken))
            t1 = ttn
        if (t1 is None): 
            return None
        res.end_token = t1
        and0_ = False
        ntyp = NumberSpellingType.DIGIT
        tt1 = t1
        while t1 is not None:
            if (t1.whitespaces_before_count > 15): 
                break
            if (t1 != tt1 and t1.is_newline_before): 
                if (not t1.is_comma_and): 
                    break
            if (t1.is_newline_before): 
                if (t1.previous.is_char_of(";.")): 
                    if ((isinstance(t1, NumberToken)) and t1.next0_ is not None and t1.next0_.is_char_of(",;")): 
                        pass
                    else: 
                        break
                else: 
                    nnn = ComplexNumToken.try_parse(t1, None, False, False)
                    if (nnn is not None and nnn.suffix is not None): 
                        if (nnn.suffix == ")" and t.previous is not None and t.previous.is_char('(')): 
                            pass
                        else: 
                            break
            if (ttn is not None): 
                ttn = MiscHelper.check_number_prefix(t1)
                if (ttn is not None): 
                    t1 = ttn
            if (BracketHelper.can_be_start_of_sequence(t1, False, False)): 
                br = BracketHelper.try_parse(t1, BracketParseAttr.NO, 100)
                if (br is None): 
                    break
                ok = True
                newp = None
                ttt = t1.next0_
                first_pass3915 = True
                while True:
                    if first_pass3915: first_pass3915 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if (ttt.end_char > br.end_token.previous.end_char): 
                        break
                    if (ttt.is_char(',')): 
                        continue
                    if (isinstance(ttt, NumberToken)): 
                        if (ttt.value == "0"): 
                            ok = False
                            break
                        if (newp is None): 
                            newp = list()
                        pv0 = PartToken.PartValue._new1320(ttt, ttt, str(ttt.value))
                        pv0.correct_value()
                        ttt = pv0.end_token
                        newp.append(pv0)
                        continue
                    to = Utils.asObjectOrNull(ttt, TextToken)
                    if (to is None): 
                        ok = False
                        break
                    if ((res.typ != PartToken.ItemType.ITEM and res.typ != PartToken.ItemType.SUBITEM and res.typ != PartToken.ItemType.INDENTION) and res.typ != PartToken.ItemType.SUBINDENTION): 
                        ok = False
                        break
                    if (not to.chars.is_letter or to.length_char != 1): 
                        ok = False
                        break
                    if (newp is None): 
                        newp = list()
                    pv = PartToken.PartValue._new1320(ttt, ttt, to.term)
                    if (BracketHelper.can_be_start_of_sequence(ttt.previous, False, False)): 
                        pv.begin_token = ttt.previous
                    pv.correct_value()
                    ttt = pv.end_token
                    if (BracketHelper.can_be_end_of_sequence(ttt.next0_, False, None, False)): 
                        ttt = ttt.next0_
                        pv.end_token = ttt
                    if (pv.end_token.next0_ == br.end_token): 
                        ttt = br.end_token
                        pv.end_token = ttt
                    newp.append(pv)
                if (newp is None or not ok): 
                    break
                res.values.extend(newp)
                res.end_token = br.end_token
                t1 = br.end_token.next0_
                if (and0_): 
                    break
                if (t1 is not None and t1.is_hiphen and BracketHelper.can_be_start_of_sequence(t1.next0_, False, False)): 
                    br1 = BracketHelper.try_parse(t1.next0_, BracketParseAttr.NO, 100)
                    if (br1 is not None and (isinstance(t1.next0_.next0_, TextToken)) and t1.next0_.next0_.length_char == 1): 
                        pv = PartToken.PartValue._new1320(br1.begin_token, t1.next0_.next0_, t1.next0_.next0_.term)
                        pv.correct_value()
                        if (pv.end_token == br1.end_token.previous): 
                            res.values.append(pv)
                            res.end_token = br1.end_token
                            t1 = br1.end_token.next0_
                continue
            if (((isinstance(t1, TextToken)) and t1.length_char == 1 and t1.chars.is_letter) and len(res.values) == 0): 
                if (t1.chars.is_all_upper and res.typ == PartToken.ItemType.SUBPROGRAM): 
                    res.values.append(PartToken.PartValue._new1320(t1, t1, t1.term))
                    res.end_token = t1
                    return res
                ok = True
                lev = 0
                ttt = t1.previous
                while ttt is not None: 
                    if (ttt.is_newline_after): 
                        break
                    if (ttt.is_char('(')): 
                        lev -= 1
                        if (lev < 0): 
                            ok = False
                            break
                    elif (ttt.is_char(')')): 
                        lev += 1
                    ttt = ttt.previous
                if (ok and t1.next0_ is not None and t1.next0_.is_char(')')): 
                    res.values.append(PartToken.PartValue._new1320(t1, t1.next0_, t1.term))
                    res.end_token = t1.next0_
                    t1 = t1.next0_.next0_
                    continue
                if (((ok and t1.next0_ is not None and t1.next0_.is_char_of("(.[")) and not t1.next0_.is_whitespace_after and (isinstance(t1.next0_.next0_, NumberToken))) and t1.next0_.next0_.next0_ is not None and t1.next0_.next0_.next0_.is_char_of(")]")): 
                    res.values.append(PartToken.PartValue._new1320(t1, t1.next0_.next0_.next0_, "{0}.{1}".format(t1.term, t1.next0_.next0_.value)))
                    res.end_token = t1.next0_.next0_.next0_
                    t1 = res.end_token.next0_
                    continue
                if (ok and PartToken.try_attach(t1.next0_, None, False, False) is not None): 
                    if (((t1.is_and or t1.is_value("К", None) or t1.is_value("В", None))) and t1.chars.is_all_lower): 
                        pass
                    else: 
                        res.values.append(PartToken.PartValue._new1320(t1, t1, t1.term))
                        res.end_token = t1
                        t1 = t1.next0_
                        continue
                if ((t1.is_value("З", None) and t1.chars.is_all_upper and res.typ != PartToken.ItemType.INDENTION) and res.typ != PartToken.ItemType.SUBITEM): 
                    val = PartToken.PartValue._new1320(t1, t1, "3")
                    val.correct_value()
                    res.values.append(val)
                    res.end_token = val.end_token
                    t1 = val.end_token.next0_
                    continue
                if (len(res.values) == 0 and ((res.typ == PartToken.ItemType.ITEM or res.typ == PartToken.ItemType.SUBITEM))): 
                    ok = False
                    if (t1.next0_ is not None and t1.next0_.is_char_of(".,")): 
                        ok = True
                    elif (DecreeChangeToken.M_TERMS.try_parse(t1.next0_, TerminParseAttr.NO) is not None): 
                        ok = True
                    if (ok): 
                        res.values.append(PartToken.PartValue._new1320(t1, t1, t1.term))
                        res.end_token = t1
                        return res
            pref_to = None
            if (len(res.values) > 0 and not (isinstance(t1, NumberToken)) and first_num_prefix is not None): 
                ttn = MiscHelper.check_number_prefix(t1)
                if (ttn is not None): 
                    pref_to = t1
                    t1 = ttn
            if (isinstance(t1, NumberToken)): 
                tt0 = Utils.ifNotNull(pref_to, t1)
                if (len(res.values) > 0): 
                    if (res.values[0].int_value == 0 and not str.isdigit(res.values[0].value[0])): 
                        break
                    if (t1.typ != ntyp): 
                        break
                ntyp = t1.typ
                val = PartToken.PartValue._new1320(tt0, t1, str(t1.value))
                val.correct_value()
                res.values.append(val)
                res.end_token = val.end_token
                t1 = res.end_token.next0_
                if ((res.typ == PartToken.ItemType.FORM and (isinstance(t1, TextToken)) and t1.chars.is_all_upper) and (t1.length_char < 5) and (t1.whitespaces_before_count < 2)): 
                    val.end_token = res.end_token = t1
                    t1 = t1.next0_
                if (and0_): 
                    break
                continue
            nt = NumberHelper.try_parse_roman(t1)
            if (nt is not None): 
                pv = PartToken.PartValue._new1320(t1, nt.end_token, str(nt.value))
                res.values.append(pv)
                pv.correct_value()
                res.end_token = pv.end_token
                t1 = res.end_token.next0_
                continue
            if ((t1 == tt1 and ((res.typ == PartToken.ItemType.APPENDIX or res.typ == PartToken.ItemType.ADDAGREE)) and t1.is_value("К", None)) and t1.next0_ is not None): 
                if ((isinstance(t1.next0_.get_referent(), DecreeReferent)) or DecreeToken.is_keyword(t1.next0_, False) is not None or DecreeToken.is_keyword(t1.next0_.next0_, False) is not None): 
                    res.values.append(PartToken.PartValue._new1320(t1, t1, ""))
                    break
            if (res.typ == PartToken.ItemType.ADDAGREE and first_num_prefix is not None and len(res.values) == 0): 
                ddd = DecreeToken.try_attach(first_num_prefix, None, False)
                if (ddd is not None and ddd.typ == DecreeToken.ItemType.NUMBER and ddd.value is not None): 
                    if (t1.begin_char <= ddd.end_token.begin_char): 
                        res.values.append(PartToken.PartValue._new1320(t1, ddd.end_token, ddd.value))
                        res.end_token = ddd.end_token
                        t1 = res.end_token
                        break
            if (len(res.values) == 0): 
                break
            if (t1.is_char_of(",.")): 
                if (t1.is_newline_after and t1.is_char('.')): 
                    break
                t1 = t1.next0_
                continue
            if (t1.is_hiphen and res.values[len(res.values) - 1].value.find('.') > 0): 
                t1 = t1.next0_
                continue
            if (t1.is_and or t1.is_or): 
                t1 = t1.next0_
                and0_ = True
                continue
            if (t1.is_hiphen): 
                nmax = Utils.asObjectOrNull(t1.next0_, NumberToken)
                if (nmax is None): 
                    nmax = NumberHelper.try_parse_roman(t1.next0_)
                if (nmax is None or nmax.int_value is None): 
                    break
                min0_ = res.values[len(res.values) - 1].int_value
                if (min0_ == 0): 
                    break
                max0_ = nmax.int_value
                if (max0_ < min0_): 
                    break
                if ((max0_ - min0_) > 200): 
                    break
                val = PartToken.PartValue._new1320(t1.next0_, (t1.next0_ if nmax == t1.next0_ else nmax.end_token), str(max0_))
                val.correct_value()
                res.values.append(val)
                res.end_token = val.end_token
                t1 = res.end_token.next0_
                continue
            break
        if (len(res.values) == 0 and not res.is_newline_after and BracketHelper.can_be_start_of_sequence(res.end_token, True, False)): 
            lev = PartToken._get_rank(res.typ)
            if (lev > 0 and (lev < PartToken._get_rank(PartToken.ItemType.CLAUSE))): 
                br = BracketHelper.try_parse(res.end_token, BracketParseAttr.NO, 100)
                if (br is not None): 
                    res.name = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                    res.end_token = br.end_token
        if (len(res.values) == 0 and res.name is None): 
            if ((((not ignore_number and res.typ != PartToken.ItemType.PREAMBLE and res.typ != PartToken.ItemType.NAME) and res.typ != PartToken.ItemType.TABLE and res.typ != PartToken.ItemType.SUBPROGRAM) and res.typ != PartToken.ItemType.NOTICE and res.typ != PartToken.ItemType.FOOTNOTE) and res.typ != PartToken.ItemType.FORMULA): 
                return None
            if (res.begin_token != res.end_token): 
                res.end_token = res.end_token.previous
        return res
    
    @staticmethod
    def __create_part_typ0(t1 : 'Token', prev : 'PartToken') -> 'PartToken':
        is_short = False
        wrapis_short1346 = RefOutArgWrapper(False)
        pt = PartToken.__create_part_typ(t1, prev, wrapis_short1346)
        is_short = wrapis_short1346.value
        if (pt is None): 
            return None
        if (t1.length_char > 4): 
            pt.morph = t1.morph
        if ((is_short and not pt.end_token.is_whitespace_after and pt.end_token.next0_ is not None) and pt.end_token.next0_.is_char('.')): 
            if (not pt.end_token.next0_.is_newline_after): 
                pt.end_token = pt.end_token.next0_
        return pt
    
    @staticmethod
    def __create_part_typ(t1 : 'Token', prev : 'PartToken', is_short : bool) -> 'PartToken':
        is_short.value = False
        if (t1 is None): 
            return None
        if (t1.is_value("ТЕРМИНОЛОГИЧЕСКИЙ", None)): 
            res = PartToken.__create_part_typ(t1.next0_, prev, is_short)
            if (res is not None): 
                res.begin_token = t1
            return res
        if (t1.is_value("ЧАСТЬ", "ЧАСТИНА") or t1.is_value("PART", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.PART)
        if (t1.is_value("Ч", None)): 
            is_short.value = True
            return PartToken._new1036(t1, t1, PartToken.ItemType.PART)
        if (t1.is_value("ГЛАВА", None) or t1.is_value("ГЛ", None) or t1.is_value("CHAPTER", None)): 
            is_short.value = t1.length_char == 2
            return PartToken._new1036(t1, t1, PartToken.ItemType.CHAPTER)
        if (t1.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК") or t1.is_value("ПРИЛ", None) or t1.is_value("APPENDIX", None)): 
            if ((t1.is_newline_before and t1.length_char > 6 and t1.next0_ is not None) and t1.next0_.is_char(':')): 
                return None
            is_short.value = (t1.length_char < 5)
            return PartToken._new1036(t1, t1, PartToken.ItemType.APPENDIX)
        if (t1.is_value("ПРИМЕЧАНИЕ", "ПРИМІТКА") or t1.is_value("ПРИМ", None)): 
            is_short.value = (t1.length_char < 5)
            return PartToken._new1036(t1, t1, PartToken.ItemType.NOTICE)
        if (t1.is_value("ФОРМУЛА", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.FORMULA)
        if (t1.is_value("ФОРМА", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.FORM)
        if (t1.is_value("ТАБЛИЦА", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.TABLE)
        if (t1.is_value("ГРАФА", None) or t1.is_value("СТРОКА", None)): 
            if (t1.next0_ is not None and t1.next0_.is_value("ТАБЛИЦА", None)): 
                return PartToken._new1036(t1, t1.next0_, PartToken.ItemType.TABLEROW)
            return PartToken._new1036(t1, t1, PartToken.ItemType.TABLEROW)
        if (t1.is_value("СТОЛБЕЦ", None)): 
            if (t1.next0_ is not None and t1.next0_.is_value("ТАБЛИЦА", None)): 
                return PartToken._new1036(t1, t1.next0_, PartToken.ItemType.TABLECOLUMN)
            return PartToken._new1036(t1, t1, PartToken.ItemType.TABLECOLUMN)
        if (t1.is_value("ПРЕДЛОЖЕНИЕ", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.SENTENCE)
        if (t1.is_value("СНОСКА", None)): 
            if (t1.previous is not None and t1.previous.is_value("ЗНАК", None)): 
                pass
            else: 
                return PartToken._new1036(t1, t1, PartToken.ItemType.FOOTNOTE)
        if (t1.is_value("СТАТЬЯ", "СТАТТЯ") or t1.is_value("СТ", None) or t1.is_value("ARTICLE", None)): 
            is_short.value = (t1.length_char < 3)
            return PartToken._new1036(t1, t1, PartToken.ItemType.CLAUSE)
        if (t1.is_value("ПУНКТ", None) or t1.is_value("П", None) or t1.is_value("ПП", None)): 
            is_short.value = (t1.length_char < 3)
            return PartToken._new1362(t1, t1, PartToken.ItemType.ITEM, (PartToken.ItemType.SUBITEM if t1.is_value("ПП", None) else PartToken.ItemType.UNDEFINED))
        if (t1.is_value("ПОДПУНКТ", "ПІДПУНКТ") or t1.is_value("ПОЛПУНКТА", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.SUBITEM)
        if (t1.is_value("ПРЕАМБУЛА", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.PREAMBLE)
        if (t1.is_value("НАИМЕНОВАНИЕ", None) or t1.is_value("НАЗВАНИЕ", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.NAME)
        if (t1.is_value("ПОДП", None) or t1.is_value("ПІДП", None)): 
            is_short.value = True
            return PartToken._new1036(t1, t1, PartToken.ItemType.SUBITEM)
        if (t1.is_value("РАЗДЕЛ", "РОЗДІЛ") or t1.is_value("РАЗД", None) or t1.is_value("SECTION", None)): 
            is_short.value = (t1.length_char < 5)
            return PartToken._new1036(t1, t1, PartToken.ItemType.SECTION)
        if (((t1.is_value("Р", None) or t1.is_value("P", None))) and t1.next0_ is not None and t1.next0_.is_char('.')): 
            if (prev is not None): 
                if (prev.typ == PartToken.ItemType.ITEM or prev.typ == PartToken.ItemType.SUBITEM): 
                    is_short.value = True
                    return PartToken._new1036(t1, t1.next0_, PartToken.ItemType.SECTION)
        if (t1.is_value("ПОДРАЗДЕЛ", "ПІДРОЗДІЛ") or t1.is_value("SUBSECTION", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.SUBSECTION)
        if (t1.is_value("ПАРАГРАФ", None) or t1.is_value("§", None) or t1.is_value("PARAGRAPH", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.PARAGRAPH)
        if (t1.is_value("АБЗАЦ", None) or t1.is_value("АБЗ", None)): 
            is_short.value = (t1.length_char < 7)
            return PartToken._new1036(t1, t1, PartToken.ItemType.INDENTION)
        if (t1.is_value("СТРАНИЦА", "СТОРІНКА") or t1.is_value("СТР", "СТОР") or t1.is_value("PAGE", None)): 
            is_short.value = (t1.length_char < 7)
            return PartToken._new1036(t1, t1, PartToken.ItemType.PAGE)
        if (t1.is_value("ПОДАБЗАЦ", "ПІДАБЗАЦ") or t1.is_value("ПОДАБЗ", "ПІДАБЗ")): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.SUBINDENTION)
        if (t1.is_value("ПОДПАРАГРАФ", "ПІДПАРАГРАФ") or t1.is_value("SUBPARAGRAPH", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.SUBPARAGRAPH)
        if (t1.is_value("ПОДПРОГРАММА", "ПІДПРОГРАМА")): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.SUBPROGRAM)
        if (t1.is_value("ДОПСОГЛАШЕНИЕ", None)): 
            return PartToken._new1036(t1, t1, PartToken.ItemType.ADDAGREE)
        if (((t1.is_value("ДОП", None) or t1.is_value("ДОПОЛНИТЕЛЬНЫЙ", "ДОДАТКОВА"))) and t1.next0_ is not None): 
            tt = t1.next0_
            if (tt.is_char('.') and tt.next0_ is not None): 
                tt = tt.next0_
            if (tt.is_value("СОГЛАШЕНИЕ", "УГОДА")): 
                return PartToken._new1036(t1, tt, PartToken.ItemType.ADDAGREE)
        return None
    
    @staticmethod
    def try_attach_list(t : 'Token', in_bracket : bool=False, max_count : int=40) -> typing.List['PartToken']:
        p = PartToken.try_attach(t, None, in_bracket, False)
        if (p is None): 
            return None
        res = list()
        res.append(p)
        if (p.is_newline_after and p.is_newline_before): 
            if (not p.begin_token.chars.is_all_lower): 
                return res
        tt = p.end_token.next0_
        while tt is not None:
            if (tt.whitespaces_before_count > 15): 
                if (tt.previous is not None and tt.previous.is_comma_and): 
                    pass
                else: 
                    break
            if (max_count > 0 and len(res) >= max_count): 
                break
            delim = False
            if (((tt.is_char_of(",;.") or tt.is_and or tt.is_or)) and tt.next0_ is not None): 
                if (tt.is_char_of(";.")): 
                    res[len(res) - 1].has_terminator = True
                else: 
                    res[len(res) - 1].delim_after = True
                    if ((tt.next0_ is not None and tt.next0_.is_value("А", None) and tt.next0_.next0_ is not None) and tt.next0_.next0_.is_value("ТАКЖЕ", "ТАКОЖ")): 
                        tt = tt.next0_.next0_
                tt = tt.next0_
                delim = True
            if (tt is None): 
                break
            if (tt.is_newline_before): 
                if (tt.chars.is_letter and not tt.chars.is_all_lower): 
                    break
            if (tt.is_char('(')): 
                br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                if (br is not None): 
                    li = PartToken.try_attach_list(tt.next0_, True, 40)
                    if (li is not None and len(li) > 0): 
                        if (li[0].typ == PartToken.ItemType.PARAGRAPH or li[0].typ == PartToken.ItemType.PART or li[0].typ == PartToken.ItemType.ITEM): 
                            if (li[len(li) - 1].end_token.next0_ == br.end_token): 
                                if (len(p.values) > 1): 
                                    ii = 1
                                    while ii < len(p.values): 
                                        pp = PartToken._new1036(p.values[ii].begin_token, (p.end_token if ii == (len(p.values) - 1) else p.values[ii].end_token), p.typ)
                                        pp.values.append(p.values[ii])
                                        res.append(pp)
                                        ii += 1
                                    if (p.values[1].begin_token.previous is not None and p.values[1].begin_token.previous.end_char >= p.begin_token.begin_char): 
                                        p.end_token = p.values[1].begin_token.previous
                                    del p.values[1:1+len(p.values) - 1]
                                res.extend(li)
                                li[len(li) - 1].end_token = br.end_token
                                tt = br.end_token.next0_
                                continue
            p0 = PartToken.try_attach(tt, p, in_bracket, False)
            if (p0 is None and ((tt.is_value("В", None) or tt.is_value("К", None) or tt.is_value("ДО", None)))): 
                p0 = PartToken.try_attach(tt.next0_, p, in_bracket, False)
            if (p0 is None): 
                if (BracketHelper.is_bracket(tt, False)): 
                    br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        p0 = PartToken.try_attach(br.end_token.next0_, None, False, False)
                        if (p0 is not None and p0.typ != PartToken.ItemType.PREFIX and len(p0.values) > 0): 
                            res[len(res) - 1].end_token = br.end_token
                            res[len(res) - 1].name = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                            if (p0.is_newline_before): 
                                break
                            p = p0
                            res.append(p)
                            tt = p.end_token.next0_
                            continue
                        if (BracketHelper.is_bracket(tt, True) and (tt.whitespaces_before_count < 3) and res[len(res) - 1].typ == PartToken.ItemType.APPENDIX): 
                            res[len(res) - 1].end_token = br.end_token
                            res[len(res) - 1].name = MiscHelper.get_text_value_of_meta_token(br, GetTextAttr.NO)
                            tt = br.end_token.next0_
                            continue
                if (tt.is_newline_before): 
                    if (len(res) == 1 and res[0].is_newline_before): 
                        break
                    if (tt.previous is not None and tt.previous.is_comma_and): 
                        pass
                    else: 
                        break
                if ((isinstance(tt, NumberToken)) and delim): 
                    p0 = (None)
                    if (p.typ == PartToken.ItemType.CLAUSE or in_bracket): 
                        p0 = PartToken._new1036(tt, tt, PartToken.ItemType.CLAUSE)
                    elif (len(res) > 1 and res[len(res) - 2].typ == PartToken.ItemType.CLAUSE and res[len(res) - 1].typ == PartToken.ItemType.PART): 
                        p0 = PartToken._new1036(tt, tt, PartToken.ItemType.CLAUSE)
                    elif ((len(res) > 2 and res[len(res) - 3].typ == PartToken.ItemType.CLAUSE and res[len(res) - 2].typ == PartToken.ItemType.PART) and res[len(res) - 1].typ == PartToken.ItemType.ITEM): 
                        p0 = PartToken._new1036(tt, tt, PartToken.ItemType.CLAUSE)
                    elif (len(res) > 0 and len(res[len(res) - 1].values) > 0 and "." in res[len(res) - 1].values[0].value): 
                        p0 = PartToken._new1036(tt, tt, res[len(res) - 1].typ)
                    if (p0 is None): 
                        break
                    vv = PartToken.PartValue._new1320(tt, tt, str(tt.value))
                    p0.values.append(vv)
                    vv.correct_value()
                    p0.end_token = vv.end_token
                    tt = p0.end_token.next0_
                    if (tt is not None and tt.is_hiphen and (isinstance(tt.next0_, NumberToken))): 
                        tt = tt.next0_
                        vv = PartToken.PartValue._new1320(tt, tt, str(tt.value))
                        vv.correct_value()
                        p0.values.append(vv)
                        p0.end_token = vv.end_token
                        tt = p0.end_token.next0_
            if (tt is not None and tt.is_char(',') and not tt.is_newline_after): 
                p1 = PartToken.try_attach(tt.next0_, p, False, False)
                if (p1 is not None and PartToken._get_rank(p1.typ) > 0 and PartToken._get_rank(p.typ) > 0): 
                    if (PartToken._get_rank(p1.typ) < PartToken._get_rank(p.typ)): 
                        p0 = p1
            if (p0 is None): 
                break
            if (p0.is_newline_before and len(res) == 1 and res[0].is_newline_before): 
                break
            if (p0.morph is not None and p0.morph.case_.is_instrumental): 
                if ((p.typ != PartToken.ItemType.PREFIX and not p.delim_after and p.morph is not None) and not p.morph.case_.is_instrumental): 
                    break
                elif ((isinstance(p.begin_token, TextToken)) and p.begin_token.term == "СТАТЬЮ"): 
                    break
            if (p0.typ == PartToken.ItemType.ITEM and p.typ == PartToken.ItemType.ITEM): 
                if (p0.alt_typ == PartToken.ItemType.UNDEFINED and p.alt_typ == PartToken.ItemType.SUBITEM): 
                    p.typ = PartToken.ItemType.SUBITEM
                    p.alt_typ = PartToken.ItemType.UNDEFINED
                elif (p.alt_typ == PartToken.ItemType.UNDEFINED and p0.alt_typ == PartToken.ItemType.SUBITEM): 
                    p0.typ = PartToken.ItemType.SUBITEM
                    p0.alt_typ = PartToken.ItemType.UNDEFINED
                elif (p0.alt_typ == PartToken.ItemType.SUBITEM and p.alt_typ == PartToken.ItemType.SUBITEM): 
                    next0__ = PartToken.try_attach(p0.end_token.next0_, None, False, False)
                    if (next0__ is not None and next0__.typ == PartToken.ItemType.ITEM and next0__.alt_typ == PartToken.ItemType.UNDEFINED): 
                        p.typ = PartToken.ItemType.SUBITEM
                        p.alt_typ = PartToken.ItemType.UNDEFINED
                        p0.typ = PartToken.ItemType.SUBITEM
                        p0.alt_typ = PartToken.ItemType.UNDEFINED
            p = p0
            res.append(p)
            tt = p.end_token.next0_
        i = 0
        first_pass3916 = True
        while True:
            if first_pass3916: first_pass3916 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == PartToken.ItemType.PART and res[i + 1].typ == PartToken.ItemType.PART and len(res[i].values) > 1): 
                v1 = res[i].values[len(res[i].values) - 2].int_value
                v2 = res[i].values[len(res[i].values) - 1].int_value
                if (v1 == 0 or v2 == 0): 
                    continue
                if ((v2 - v1) < 10): 
                    continue
                pt = PartToken._new1036(res[i].end_token, res[i].end_token, PartToken.ItemType.CLAUSE)
                pt.values.append(PartToken.PartValue._new1320(res[i].end_token, res[i].end_token, str(v2)))
                del res[i].values[len(res[i].values) - 1]
                if (res[i].end_token != res[i].begin_token): 
                    res[i].end_token = res[i].end_token.previous
                res.insert(i + 1, pt)
        if ((len(res) == 1 and res[0].typ == PartToken.ItemType.SUBPROGRAM and res[0].end_token.next0_ is not None) and res[0].end_token.next0_.is_char('.')): 
            res[0].end_token = res[0].end_token.next0_
        for i in range(len(res) - 1, -1, -1):
            p = res[i]
            if (p.is_newline_after and p.is_newline_before and p.typ != PartToken.ItemType.SUBPROGRAM): 
                del res[i:i+len(res) - i]
                continue
            if (((i == 0 and ((p.is_newline_before or ((p.begin_token.previous is not None and p.begin_token.previous.is_table_control_char)))) and p.has_terminator) and p.end_token.next0_ is not None and p.end_token.next0_.is_char('.')) and MiscHelper.can_be_start_of_sentence(p.end_token.next0_.next0_)): 
                del res[i]
                continue
        if (len(res) == 1 and res[0].typ == PartToken.ItemType.PREFIX): 
            return None
        return (None if len(res) == 0 else res)
    
    def can_be_next_narrow(self, p : 'PartToken') -> bool:
        if (self.typ == PartToken.ItemType.FORMULA): 
            return False
        if (p.typ == PartToken.ItemType.FORMULA): 
            return True
        if (self.typ == PartToken.ItemType.SENTENCE): 
            return False
        if (p.typ == PartToken.ItemType.SENTENCE): 
            if ((self.typ == PartToken.ItemType.PREAMBLE or self.typ == PartToken.ItemType.INDENTION or self.typ == PartToken.ItemType.PART) or self.typ == PartToken.ItemType.ITEM or self.typ == PartToken.ItemType.SUBITEM): 
                return True
            return False
        if (self.typ == PartToken.ItemType.TABLE): 
            if (p.typ == PartToken.ItemType.TABLECOLUMN or p.typ == PartToken.ItemType.TABLEROW or p.typ == PartToken.ItemType.NAME): 
                return True
        if (self.typ == p.typ): 
            if (self.typ != PartToken.ItemType.SUBITEM): 
                return False
            if (p.values is not None and len(p.values) > 0 and p.values[0].int_value == 0): 
                if (self.values is not None and len(self.values) > 0 and self.values[0].int_value > 0): 
                    return True
            return False
        if (self.typ == PartToken.ItemType.PART or p.typ == PartToken.ItemType.PART): 
            return True
        if (self.typ == PartToken.ItemType.NOTICE or self.typ == PartToken.ItemType.FOOTNOTE): 
            if (p.typ == PartToken.ItemType.INDENTION): 
                return True
        i1 = PartToken._get_rank(self.typ)
        i2 = PartToken._get_rank(p.typ)
        if (i1 >= 0 and i2 >= 0): 
            return i1 < i2
        return False
    
    @staticmethod
    def is_part_before(t0 : 'Token') -> bool:
        if (t0 is None): 
            return False
        i = 0
        tt = t0.previous
        while tt is not None: 
            if (tt.is_newline_after or (isinstance(tt, ReferentToken))): 
                break
            else: 
                st = PartToken.try_attach(tt, None, False, False)
                if (st is not None): 
                    if (st.end_token.next0_ == t0): 
                        return True
                    break
                if ((isinstance(tt, TextToken)) and tt.chars.is_letter): 
                    i += 1
                    if (i > 2): 
                        break
            tt = tt.previous
        return False
    
    @staticmethod
    def _get_rank(t : 'ItemType') -> int:
        if (t == PartToken.ItemType.DOCPART): 
            return 1
        if (t == PartToken.ItemType.APPENDIX): 
            return 1
        if (t == PartToken.ItemType.SECTION): 
            return 2
        if (t == PartToken.ItemType.SUBPROGRAM): 
            return 2
        if (t == PartToken.ItemType.SUBSECTION): 
            return 3
        if (t == PartToken.ItemType.CHAPTER): 
            return 4
        if (t == PartToken.ItemType.PREAMBLE): 
            return 5
        if (t == PartToken.ItemType.PARAGRAPH): 
            return 5
        if (t == PartToken.ItemType.SUBPARAGRAPH): 
            return 6
        if (t == PartToken.ItemType.PAGE): 
            return 6
        if (t == PartToken.ItemType.CLAUSE): 
            return 7
        if (t == PartToken.ItemType.PART): 
            return 8
        if (t == PartToken.ItemType.NOTICE): 
            return 8
        if (t == PartToken.ItemType.ITEM): 
            return 9
        if (t == PartToken.ItemType.SUBITEM): 
            return 10
        if (t == PartToken.ItemType.NAME): 
            return 11
        if (t == PartToken.ItemType.INDENTION): 
            return 12
        if (t == PartToken.ItemType.SUBINDENTION): 
            return 13
        if (t == PartToken.ItemType.FORM): 
            return 13
        if (t == PartToken.ItemType.SENTENCE): 
            return 14
        if (t == PartToken.ItemType.TABLE): 
            return 14
        if (t == PartToken.ItemType.TABLECOLUMN): 
            return 15
        if (t == PartToken.ItemType.TABLEROW): 
            return 15
        if (t == PartToken.ItemType.FOOTNOTE): 
            return 15
        if (t == PartToken.ItemType.FORMULA): 
            return 16
        return 0
    
    @staticmethod
    def _get_attr_name_by_typ(typ_ : 'ItemType') -> str:
        if (typ_ == PartToken.ItemType.CHAPTER): 
            return DecreePartReferent.ATTR_CHAPTER
        if (typ_ == PartToken.ItemType.APPENDIX): 
            return DecreePartReferent.ATTR_APPENDIX
        if (typ_ == PartToken.ItemType.CLAUSE): 
            return DecreePartReferent.ATTR_CLAUSE
        if (typ_ == PartToken.ItemType.INDENTION): 
            return DecreePartReferent.ATTR_INDENTION
        if (typ_ == PartToken.ItemType.ITEM): 
            return DecreePartReferent.ATTR_ITEM
        if (typ_ == PartToken.ItemType.PARAGRAPH): 
            return DecreePartReferent.ATTR_PARAGRAPH
        if (typ_ == PartToken.ItemType.SUBPARAGRAPH): 
            return DecreePartReferent.ATTR_SUBPARAGRAPH
        if (typ_ == PartToken.ItemType.PART): 
            return DecreePartReferent.ATTR_PART
        if (typ_ == PartToken.ItemType.SECTION): 
            return DecreePartReferent.ATTR_SECTION
        if (typ_ == PartToken.ItemType.SUBSECTION): 
            return DecreePartReferent.ATTR_SUBSECTION
        if (typ_ == PartToken.ItemType.SUBINDENTION): 
            return DecreePartReferent.ATTR_SUBINDENTION
        if (typ_ == PartToken.ItemType.SUBITEM): 
            return DecreePartReferent.ATTR_SUBITEM
        if (typ_ == PartToken.ItemType.PREAMBLE): 
            return DecreePartReferent.ATTR_PREAMBLE
        if (typ_ == PartToken.ItemType.NOTICE): 
            return DecreePartReferent.ATTR_NOTICE
        if (typ_ == PartToken.ItemType.FOOTNOTE): 
            return DecreePartReferent.ATTR_FOOTNOTE
        if (typ_ == PartToken.ItemType.FORMULA): 
            return DecreePartReferent.ATTR_FORMULA
        if (typ_ == PartToken.ItemType.FORM): 
            return DecreePartReferent.ATTR_FORM
        if (typ_ == PartToken.ItemType.TABLE): 
            return DecreePartReferent.ATTR_TABLE
        if (typ_ == PartToken.ItemType.TABLECOLUMN): 
            return DecreePartReferent.ATTR_TABLECOLUMN
        if (typ_ == PartToken.ItemType.TABLEROW): 
            return DecreePartReferent.ATTR_TABLEROW
        if (typ_ == PartToken.ItemType.SENTENCE): 
            return DecreePartReferent.ATTR_SENTENCE
        if (typ_ == PartToken.ItemType.NAME): 
            return DecreePartReferent.ATTR_NAMEASITEM
        if (typ_ == PartToken.ItemType.SUBPROGRAM): 
            return DecreePartReferent.ATTR_SUBPROGRAM
        if (typ_ == PartToken.ItemType.ADDAGREE): 
            return DecreePartReferent.ATTR_ADDAGREE
        if (typ_ == PartToken.ItemType.DOCPART): 
            return DecreePartReferent.ATTR_DOCPART
        if (typ_ == PartToken.ItemType.PAGE): 
            return DecreePartReferent.ATTR_PAGE
        return None
    
    @staticmethod
    def _get_instr_kind_by_typ(typ_ : 'ItemType') -> 'InstrumentKind':
        if (typ_ == PartToken.ItemType.CHAPTER): 
            return InstrumentKind.CHAPTER
        if (typ_ == PartToken.ItemType.APPENDIX): 
            return InstrumentKind.APPENDIX
        if (typ_ == PartToken.ItemType.CLAUSE): 
            return InstrumentKind.CLAUSE
        if (typ_ == PartToken.ItemType.INDENTION): 
            return InstrumentKind.INDENTION
        if (typ_ == PartToken.ItemType.ITEM): 
            return InstrumentKind.ITEM
        if (typ_ == PartToken.ItemType.PARAGRAPH): 
            return InstrumentKind.PARAGRAPH
        if (typ_ == PartToken.ItemType.SUBPARAGRAPH): 
            return InstrumentKind.SUBPARAGRAPH
        if (typ_ == PartToken.ItemType.PART): 
            return InstrumentKind.CLAUSEPART
        if (typ_ == PartToken.ItemType.SECTION): 
            return InstrumentKind.SECTION
        if (typ_ == PartToken.ItemType.SUBSECTION): 
            return InstrumentKind.SUBSECTION
        if (typ_ == PartToken.ItemType.SUBITEM): 
            return InstrumentKind.SUBITEM
        if (typ_ == PartToken.ItemType.PREAMBLE): 
            return InstrumentKind.PREAMBLE
        if (typ_ == PartToken.ItemType.NOTICE): 
            return InstrumentKind.NOTICE
        if (typ_ == PartToken.ItemType.DOCPART): 
            return InstrumentKind.DOCPART
        if (typ_ == PartToken.ItemType.TABLE): 
            return InstrumentKind.TABLE
        return InstrumentKind.UNDEFINED
    
    @staticmethod
    def _get_type_by_attr_name(name_ : str) -> 'ItemType':
        if (name_ == DecreePartReferent.ATTR_CHAPTER): 
            return PartToken.ItemType.CHAPTER
        if (name_ == DecreePartReferent.ATTR_APPENDIX): 
            return PartToken.ItemType.APPENDIX
        if (name_ == DecreePartReferent.ATTR_CLAUSE): 
            return PartToken.ItemType.CLAUSE
        if (name_ == DecreePartReferent.ATTR_INDENTION): 
            return PartToken.ItemType.INDENTION
        if (name_ == DecreePartReferent.ATTR_ITEM): 
            return PartToken.ItemType.ITEM
        if (name_ == DecreePartReferent.ATTR_PARAGRAPH): 
            return PartToken.ItemType.PARAGRAPH
        if (name_ == DecreePartReferent.ATTR_SUBPARAGRAPH): 
            return PartToken.ItemType.SUBPARAGRAPH
        if (name_ == DecreePartReferent.ATTR_PART): 
            return PartToken.ItemType.PART
        if (name_ == DecreePartReferent.ATTR_SECTION): 
            return PartToken.ItemType.SECTION
        if (name_ == DecreePartReferent.ATTR_SUBSECTION): 
            return PartToken.ItemType.SUBSECTION
        if (name_ == DecreePartReferent.ATTR_SUBINDENTION): 
            return PartToken.ItemType.SUBINDENTION
        if (name_ == DecreePartReferent.ATTR_SUBITEM): 
            return PartToken.ItemType.SUBITEM
        if (name_ == DecreePartReferent.ATTR_NOTICE): 
            return PartToken.ItemType.NOTICE
        if (name_ == DecreePartReferent.ATTR_FOOTNOTE): 
            return PartToken.ItemType.FOOTNOTE
        if (name_ == DecreePartReferent.ATTR_FORMULA): 
            return PartToken.ItemType.FORMULA
        if (name_ == DecreePartReferent.ATTR_FORM): 
            return PartToken.ItemType.FORM
        if (name_ == DecreePartReferent.ATTR_TABLE): 
            return PartToken.ItemType.TABLE
        if (name_ == DecreePartReferent.ATTR_TABLECOLUMN): 
            return PartToken.ItemType.TABLECOLUMN
        if (name_ == DecreePartReferent.ATTR_TABLEROW): 
            return PartToken.ItemType.TABLEROW
        if (name_ == DecreePartReferent.ATTR_SENTENCE): 
            return PartToken.ItemType.SENTENCE
        if (name_ == DecreePartReferent.ATTR_NAMEASITEM): 
            return PartToken.ItemType.NAME
        if (name_ == DecreePartReferent.ATTR_PREAMBLE): 
            return PartToken.ItemType.PREAMBLE
        if (name_ == DecreePartReferent.ATTR_SUBPROGRAM): 
            return PartToken.ItemType.SUBPROGRAM
        if (name_ == DecreePartReferent.ATTR_ADDAGREE): 
            return PartToken.ItemType.ADDAGREE
        if (name_ == DecreePartReferent.ATTR_DOCPART): 
            return PartToken.ItemType.DOCPART
        return PartToken.ItemType.PREFIX
    
    @staticmethod
    def try_create_between(p1 : 'DecreePartReferent', p2 : 'DecreePartReferent') -> typing.List['DecreePartReferent']:
        from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
        not_eq_attr = None
        val1 = None
        val2 = None
        for s1 in p1.slots: 
            if (p2.find_slot(s1.type_name, s1.value, True) is not None): 
                continue
            else: 
                if (not_eq_attr is not None): 
                    return None
                val2 = p2.get_string_value(s1.type_name)
                if (val2 is None): 
                    return None
                not_eq_attr = s1.type_name
                val1 = (Utils.asObjectOrNull(s1.value, str))
        if (val1 is None or val2 is None): 
            return None
        diap = NumberingHelper.create_diap(val1, val2)
        if (diap is None or (len(diap) < 3)): 
            return None
        res = list()
        i = 1
        while i < (len(diap) - 1): 
            dpr = DecreePartReferent()
            for s in p1.slots: 
                val = s.value
                if (s.type_name == not_eq_attr): 
                    val = (diap[i])
                dpr.add_slot(s.type_name, val, False, 0)
            res.append(dpr)
            i += 1
        return res
    
    @staticmethod
    def get_number(str0_ : str) -> int:
        if (Utils.isNullOrEmpty(str0_)): 
            return 0
        i = 0
        wrapi1391 = RefOutArgWrapper(0)
        inoutres1392 = Utils.tryParseInt(str0_, wrapi1391)
        i = wrapi1391.value
        if (inoutres1392): 
            return i
        if (not str.isalpha(str0_[0])): 
            return 0
        ch = str.upper(str0_[0])
        if ((ord(ch)) < 0x80): 
            i = (((ord(ch)) - (ord('A'))) + 1)
            if ((ch == 'Z' and len(str0_) > 2 and str0_[1] == '.') and str.isdigit(str0_[2])): 
                n = 0
                wrapn1387 = RefOutArgWrapper(0)
                inoutres1388 = Utils.tryParseInt(str0_[2:], wrapn1387)
                n = wrapn1387.value
                if (inoutres1388): 
                    i += n
        elif (LanguageHelper.is_cyrillic_char(ch)): 
            i = PartToken.RU_NUMS.find(ch)
            if (i < 0): 
                return 0
            i += 1
            if ((ch == 'Я' and len(str0_) > 2 and str0_[1] == '.') and str.isdigit(str0_[2])): 
                n = 0
                wrapn1389 = RefOutArgWrapper(0)
                inoutres1390 = Utils.tryParseInt(str0_[2:], wrapn1389)
                n = wrapn1389.value
                if (inoutres1390): 
                    i += n
        if (i < 0): 
            return 0
        return i
    
    RU_NUMS = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ"
    
    @staticmethod
    def _new1036(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType') -> 'PartToken':
        res = PartToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new1324(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : bool) -> 'PartToken':
        res = PartToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1362(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ItemType', _arg4 : 'ItemType') -> 'PartToken':
        res = PartToken(_arg1, _arg2)
        res.typ = _arg3
        res.alt_typ = _arg4
        return res