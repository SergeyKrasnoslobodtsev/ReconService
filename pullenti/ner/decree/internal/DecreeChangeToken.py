# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.decree.DecreeKind import DecreeKind
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.ComplexNumCompareType import ComplexNumCompareType
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.ComplexNumComparer import ComplexNumComparer
from pullenti.ner.core.TerminToken import TerminToken
from pullenti.ner.core.ConjunctionHelper import ConjunctionHelper
from pullenti.ner.core.TableHelper import TableHelper
from pullenti.ner.decree.DecreeChangeValueKind import DecreeChangeValueKind
from pullenti.ner.core.Termin import Termin
from pullenti.ner.Referent import Referent
from pullenti.ner.decree.DecreeChangeKind import DecreeChangeKind
from pullenti.ner.core.ComplexNumToken import ComplexNumToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.decree.internal.DecreeChangeTokenTyp import DecreeChangeTokenTyp
from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
from pullenti.ner.TextToken import TextToken
from pullenti.ner.decree.DecreeReferent import DecreeReferent
from pullenti.ner.decree.DecreeChangeReferent import DecreeChangeReferent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.decree.internal.PartToken import PartToken

class DecreeChangeToken(MetaToken):
    
    @staticmethod
    def attach_referents(dpr : 'Referent', tok0 : 'DecreeChangeToken') -> typing.List['ReferentToken']:
        from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
        if (dpr is None or tok0 is None): 
            return None
        tt0 = tok0.end_token.next0_
        if (tt0 is not None and tt0.is_comma_and and tok0.act_kind == DecreeChangeKind.UNDEFINED): 
            tt0 = tt0.next0_
        if (tt0 is not None and tt0.is_char(':')): 
            tt0 = tt0.next0_
        toks = None
        if (tt0 is None): 
            pass
        elif (tt0.previous is not None and tt0.previous.is_char(':')): 
            if (tok0.act_kind2 == DecreeChangeKind.APPEND): 
                toks = DecreeChangeToken.__try_attach_list(tt0, True, tok0.indent_regime)
        else: 
            if (tt0.is_comma and tok0.decree is not None): 
                tt0 = tt0.next0_
            toks = DecreeChangeToken.__try_attach_list(tt0, False, tok0.indent_regime)
        if (toks is None): 
            toks = list()
        toks.insert(0, tok0)
        kinds = list()
        for tok in toks: 
            if (tok.act_kind != DecreeChangeKind.UNDEFINED and not tok.act_kind in kinds): 
                kinds.append(tok.act_kind)
        res = list()
        dcr = DecreeChangeReferent()
        dcr.add_slot(DecreeChangeReferent.ATTR_OWNER, dpr, False, 0)
        rt = ReferentToken(dcr, tok0.begin_token, tok0.end_token)
        res.append(rt)
        new_items = None
        in_the_end_ = False
        while True:
            i = 0
            first_pass3878 = True
            while True:
                if first_pass3878: first_pass3878 = False
                else: i += 1
                if (not (i < len(toks))): break
                tok = toks[i]
                if (tok.in_the_end): 
                    in_the_end_ = True
                if (i > 0 and tok.begin_token.previous is not None and tok.begin_token.previous.is_char(';')): 
                    break
                rt.end_token = tok.end_token
                if (tok.typ == DecreeChangeTokenTyp.AFTERVALUE): 
                    if (tok.change_val is not None): 
                        dcr.param = tok.change_val
                        if (tok.end_char > rt.end_char): 
                            rt.end_token = tok.end_token
                        res.insert(len(res) - 1, ReferentToken(tok.change_val, tok.begin_token, tok.end_token))
                    continue
                if (tok.act_kind != DecreeChangeKind.UNDEFINED): 
                    dcr.kind = tok.act_kind
                    if (tok.act_kind == DecreeChangeKind.EXPIRE): 
                        break
                if (tok.change_val is None and tok.app_ext_changes is not None): 
                    tok.change_val = DecreeChangeValueReferent()
                    tok.change_val.kind = DecreeChangeValueKind.EXTAPPENDIX
                    tok.change_val.value = ("" if len(tok.app_ext_changes.values) == 0 else str(tok.app_ext_changes.values[0]))
                    res.insert(len(res) - 1, ReferentToken(tok.change_val, tok.app_ext_changes.begin_token, tok.app_ext_changes.end_token))
                    rt.end_token = tok.end_token
                if (tok.change_val is not None): 
                    if (((i + 2) < len(toks)) and ((toks[i + 1].act_kind == DecreeChangeKind.EXCHANGE or toks[i + 1].act_kind == DecreeChangeKind.NEW)) and toks[i + 2].change_val is not None): 
                        dcr.param = tok.change_val
                        rt11 = ReferentToken(tok.change_val, tok.begin_token, tok.end_token)
                        if (tok.parts is not None and len(tok.parts) > 0): 
                            rt11.begin_token = tok.parts[len(tok.parts) - 1].end_token.next0_
                        res.insert(len(res) - 1, rt11)
                        dcr.value = toks[i + 2].change_val
                        dcr.kind = toks[i + 1].act_kind
                        i += 2
                        tok = toks[i]
                    elif (((i + 1) < len(toks)) and toks[i + 1].change_val is not None and dcr.kind == DecreeChangeKind.EXCHANGE): 
                        dcr.param = tok.change_val
                        res.insert(len(res) - 1, ReferentToken(tok.change_val, tok.begin_token, tok.end_token))
                        dcr.value = toks[i + 1].change_val
                        i += 1
                        tok = toks[i]
                    elif (dcr.value is None): 
                        dcr.value = tok.change_val
                        if (dcr.kind == DecreeChangeKind.UNDEFINED and ((i == (len(toks) - 1) or ((i == (len(toks) - 2) and toks[i + 1].typ == DecreeChangeTokenTyp.VALUE))))): 
                            next0__ = list()
                            ttt = toks[len(toks) - 1].end_token.next0_
                            first_pass3879 = True
                            while True:
                                if first_pass3879: first_pass3879 = False
                                else: ttt = ttt.next0_
                                if (not (ttt is not None)): break
                                if (ttt.is_comma_and): 
                                    continue
                                ne = DecreeChangeToken.try_attach(ttt, None, False, None, False, False)
                                if (ne is None): 
                                    break
                                if (ne.typ == DecreeChangeTokenTyp.VALUE and ne.change_val is not None): 
                                    next0__.append(ne)
                                    ttt = ne.end_token
                                    continue
                                if (ne.typ == DecreeChangeTokenTyp.ACTION and ne.act_kind == DecreeChangeKind.REMOVE): 
                                    next0__.append(ne)
                                break
                            if (len(next0__) > 0 and next0__[len(next0__) - 1].typ == DecreeChangeTokenTyp.ACTION): 
                                dcr.kind = DecreeChangeKind.REMOVE
                                res.insert(len(res) - 1, ReferentToken(tok.change_val, tok.begin_token, tok.end_token))
                                if (i < (len(toks) - 1)): 
                                    next0__.insert(0, toks[i + 1])
                                k = 0
                                while k < (len(next0__) - 1): 
                                    ne = next0__[k]
                                    res.append(ReferentToken(ne.change_val, ne.begin_token, ne.end_token))
                                    dcr = DecreeChangeReferent()
                                    dcr.kind = DecreeChangeKind.REMOVE
                                    dcr.value = ne.change_val
                                    dcr.add_slot(DecreeChangeReferent.ATTR_OWNER, dpr, False, 0)
                                    rt = ReferentToken(dcr, ne.begin_token, ne.end_token)
                                    if (k == (len(next0__) - 2)): 
                                        rt.end_token = next0__[len(next0__) - 1].end_token
                                    res.append(rt)
                                    k += 1
                                break
                    elif ((dcr.value.kind != DecreeChangeValueKind.TEXT and tok.change_val.kind == DecreeChangeValueKind.TEXT and tok.change_val.value is not None) and dcr.value.value is None): 
                        dcr.value.value = tok.change_val.value
                    elif (len(kinds) == 1 and kinds[0] == DecreeChangeKind.REMOVE): 
                        dcr.add_slot(DecreeChangeReferent.ATTR_VALUE, tok.change_val, False, 0)
                    elif (len(kinds) == 1 and kinds[0] == DecreeChangeKind.APPEND and dcr.param is None): 
                        dcr.param = dcr.value
                        dcr.value = tok.change_val
                    else: 
                        dcr.value = tok.change_val
                    if (tok.end_char > rt.end_char): 
                        rt.end_token = tok.end_token
                    res.insert(len(res) - 1, ReferentToken(tok.change_val, tok.begin_token, tok.end_token))
                    if (dcr.kind == DecreeChangeKind.NEW): 
                        break
                    if (dcr.kind == DecreeChangeKind.CONSIDER): 
                        if ((i + 2) < len(toks)): 
                            if (toks[i + 2].act_kind != DecreeChangeKind.UNDEFINED or toks[i + 1].act_kind != DecreeChangeKind.UNDEFINED): 
                                break
                            dcr = DecreeChangeReferent()
                            dcr.add_slot(DecreeChangeReferent.ATTR_OWNER, dpr, False, 0)
                            rt = ReferentToken(dcr, toks[i + 1].begin_token, toks[i + 1].end_token)
                            res.append(rt)
                            continue
                        break
                if (dcr.kind == DecreeChangeKind.APPEND and tok.new_parts is not None): 
                    for np in tok.new_parts: 
                        rank = PartToken._get_rank(np.typ)
                        if (rank == 0): 
                            continue
                        eq_lev_val = None
                        if (isinstance(dpr, DecreePartReferent)): 
                            if (not dpr._is_all_items_over_this_level(np.typ)): 
                                eq_lev_val = dpr.get_string_value(PartToken._get_attr_name_by_typ(np.typ))
                                if (eq_lev_val is None): 
                                    continue
                        dcr.kind = DecreeChangeKind.APPEND
                        if (new_items is None): 
                            new_items = list()
                        nam = PartToken._get_attr_name_by_typ(np.typ)
                        if (nam is None): 
                            continue
                        if (len(np.values) == 0): 
                            if (eq_lev_val is None): 
                                new_items.append(nam)
                            else: 
                                n = 0
                                wrapn1030 = RefOutArgWrapper(0)
                                inoutres1031 = Utils.tryParseInt(eq_lev_val, wrapn1030)
                                n = wrapn1030.value
                                if (inoutres1031): 
                                    new_items.append("{0} {1}".format(nam, n + 1))
                                else: 
                                    new_items.append(nam)
                        elif (len(np.values) == 2 and np.values[0].end_token.next0_.is_hiphen): 
                            vv = NumberingHelper.create_diap(np.values[0].value, np.values[1].value)
                            if (vv is not None): 
                                for v in vv: 
                                    new_items.append("{0} {1}".format(nam, v))
                        if (len(new_items) == 0): 
                            for v in np.values: 
                                new_items.append("{0} {1}".format(nam, v.value))
            if (not dcr._check_correct()): 
                return None
            if (new_items is not None and dcr.value is not None and dcr.kind == DecreeChangeKind.APPEND): 
                for v in new_items: 
                    dcr.value.add_slot(DecreeChangeValueReferent.ATTR_NEWITEM, v, False, 0)
            new_items = (None)
            if (rt.end_token.next0_ is None): 
                break
            if (not rt.end_token.next0_.is_comma_and): 
                break
            tt2 = rt.end_token.next0_.next0_
            if (tt2 is None): 
                break
            if (tt2.is_value("А", None)): 
                tt2 = tt2.next0_
            toks = DecreeChangeToken.__try_attach_list(tt2, False, False)
            if (toks is None): 
                break
            dts1 = DecreeChangeReferent()
            for o in dcr.owners: 
                dts1.add_slot(DecreeChangeReferent.ATTR_OWNER, o, False, 0)
            rt = ReferentToken(dts1, toks[0].begin_token, toks[0].end_token)
            res.append(rt)
            dcr = dts1
        return res
    
    @staticmethod
    def split_value(rt_val : 'ReferentToken', own : 'Referent') -> typing.List['ReferentToken']:
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        res = list()
        t = rt_val.begin_token
        while t is not None and (t.end_char < rt_val.end_char): 
            if (rt_val.begin_token == t and BracketHelper.can_be_start_of_sequence(t, False, False)): 
                t = t.next0_
            line = InstrToken1.parse(t, True, None, 0, None, False, 0, False, False)
            if (line is None): 
                break
            t1 = line.end_token
            if ((t1.end_char + 1) >= rt_val.end_char): 
                while t1 is not None: 
                    if (t1.is_char_of(".;")): 
                        pass
                    elif (BracketHelper.can_be_end_of_sequence(t1, False, None, False)): 
                        t1 = t1.previous
                        break
                    else: 
                        break
                    t1 = t1.previous
            v = DecreeChangeValueReferent()
            v.kind = DecreeChangeValueKind.TEXT
            v.value = MiscHelper.get_text_value(t, t1, Utils.valToEnum((GetTextAttr.KEEPQUOTES) | (GetTextAttr.KEEPREGISTER), GetTextAttr))
            v.begin_char = rt_val.referent.begin_char
            v.end_char = rt_val.referent.end_char
            rr = ReferentToken(v, t, line.end_token)
            res.append(rr)
            t = line.end_token
            t = t.next0_
        if (len(res) > 0): 
            rr = res[len(res) - 1]
            if (rr.end_token.is_char_of(";.,")): 
                rr.end_token = rr.end_token.previous
        return res
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.typ = DecreeChangeTokenTyp.UNDEFINED
        self.decree = None;
        self.decree_tok = None;
        self.parts = None;
        self.new_parts = None;
        self.app_ext_changes = None;
        self.real_part = None;
        self.change_val = None;
        self.has_text = False
        self.ignorable = False
        self.in_the_end = False
        self.has_anafor = False
        self.has_change_keyword = False
        self.act_kind = DecreeChangeKind.UNDEFINED
        self.act_kind2 = DecreeChangeKind.UNDEFINED
        self.part_typ = PartToken.ItemType.UNDEFINED
    
    @property
    def indent_regime(self) -> bool:
        if (self.new_parts is not None): 
            if (len(self.new_parts) == 1 and PartToken._get_rank(self.new_parts[0].typ) >= PartToken._get_rank(PartToken.ItemType.ITEM)): 
                if (len(self.new_parts[0].values) > 1): 
                    return False
                return True
            return False
        if ((self.act_kind != DecreeChangeKind.APPEND and self.parts is not None and not self.parts[0].delim_after) and len(self.parts[0].values) <= 1 and PartToken._get_rank(self.parts[0].typ) >= PartToken._get_rank(PartToken.ItemType.ITEM)): 
            return True
        return False
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print(Utils.enumToString(self.typ), end="", file=tmp)
        if (self.act_kind != DecreeChangeKind.UNDEFINED): 
            print(" Kind={0}".format(Utils.enumToString(self.act_kind)), end="", file=tmp, flush=True)
        if (self.act_kind2 != DecreeChangeKind.UNDEFINED): 
            print(" Kind2={0}".format(Utils.enumToString(self.act_kind2)), end="", file=tmp, flush=True)
        if (self.has_text): 
            print(" HasText", end="", file=tmp)
        if (self.ignorable): 
            print(" Ignorable", end="", file=tmp)
        if (self.in_the_end): 
            print(" InTheEnd", end="", file=tmp)
        if (self.has_anafor): 
            print(" HasAnafor", end="", file=tmp)
        if (self.has_change_keyword): 
            print(" HasChangeKeyword", end="", file=tmp)
        if (self.app_ext_changes is not None): 
            print(" ExtChanges={0}".format(self.app_ext_changes), end="", file=tmp, flush=True)
        if (self.parts is not None): 
            for p in self.parts: 
                print(" {0}".format(p), end="", file=tmp, flush=True)
        if (self.real_part is not None): 
            print(" RealPart={0}".format(str(self.real_part)), end="", file=tmp, flush=True)
        if (self.new_parts is not None): 
            for p in self.new_parts: 
                print(" New={0}".format(p), end="", file=tmp, flush=True)
        if (self.part_typ != PartToken.ItemType.UNDEFINED): 
            print(" PTyp={0}".format(Utils.enumToString(self.part_typ)), end="", file=tmp, flush=True)
        if (self.decree_tok is not None): 
            print(" DecTok={0}".format(str(self.decree_tok)), end="", file=tmp, flush=True)
        if (self.decree is not None): 
            print(" Ref={0}".format(self.decree.to_string_ex(True, None, 0)), end="", file=tmp, flush=True)
        if (self.change_val is not None): 
            print(" ChangeVal={0}".format(self.change_val.to_string_ex(True, None, 0)), end="", file=tmp, flush=True)
        if (self.indent_regime): 
            print(" IndentRegime!", end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    @property
    def is_start(self) -> bool:
        return self.typ == DecreeChangeTokenTyp.STARTSINGLE or self.typ == DecreeChangeTokenTyp.STARTMULTU or self.typ == DecreeChangeTokenTyp.SINGLE
    
    def __skip_decree_dummy(self) -> None:
        ignore_decree = False
        tt = self.end_token.next0_
        first_pass3880 = True
        while True:
            if first_pass3880: first_pass3880 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_comma_and): 
                continue
            if (tt.is_value2("С", "ИЗМЕНЕНИЯМИ")): 
                tt = tt.next0_.next0_
                if (tt is None): 
                    break
                if (tt.is_comma): 
                    tt = tt.next0_
                if (tt is not None and tt.is_value("ВНЕСЕННЫЙ", None)): 
                    tt = tt.next0_
                    ignore_decree = True
                if (tt is None): 
                    break
                continue
            li = PartToken.try_attach_list(tt, False, 40)
            if (li is not None and len(li) > 0): 
                if (not ignore_decree): 
                    break
                if (li[0].morph.case_.is_instrumental): 
                    break
                tt = li[len(li) - 1].end_token
                self.end_token = tt
                continue
            if (tt.is_char('(')): 
                br = BracketHelper.try_parse(tt, BracketParseAttr.CANBEMANYLINES, 3000)
                if (br is not None): 
                    tt = br.end_token
                    self.end_token = tt
                    continue
            if (isinstance(tt.get_referent(), DecreeReferent)): 
                if (not ignore_decree): 
                    break
                self.end_token = tt
                continue
            break
    
    @staticmethod
    def try_attach(t : 'Token', main : 'DecreeChangeReferent'=None, ignore_newlines : bool=False, change_stack : typing.List['Referent']=None, is_in_edition : bool=False, abzac_regime : bool=False) -> 'DecreeChangeToken':
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        if (t is None): 
            return None
        tt = t
        is_newline_before_ = t.is_newline_before
        if ((not is_newline_before_ and t.previous is not None and t.previous.is_char(':')) and t.whitespaces_before_count > 0): 
            is_newline_before_ = True
        if ((t.previous is not None and ((t.previous.is_char_of(";.") or t.previous.is_comma_and)) and t.previous.previous is not None) and (isinstance(t.previous.previous.get_referent(), DecreeChangeReferent))): 
            is_newline_before_ = True
        if ((not is_newline_before_ and t.previous is not None and t.previous.is_table_control_char) and t.previous.is_newline_before): 
            is_newline_before_ = True
        if ((is_newline_before_ and t.previous is not None and t.previous.is_value("РЕДАКЦИЯ", None)) and BracketHelper.can_be_start_of_sequence(t, True, False)): 
            is_newline_before_ = False
        if (is_newline_before_ and not ignore_newlines): 
            tt = t
            first_pass3881 = True
            while True:
                if first_pass3881: first_pass3881 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_char('[')): 
                    ii = MiscHelper.check_image(tt)
                    if (ii is not None and not ii.is_newline_after and ii.next0_ is not None): 
                        tt = ii
                        continue
                if ((tt == t and (isinstance(tt, TextToken)) and ((tt.term == "СТАТЬЯ" or tt.term == "СТАТТЯ"))) and (isinstance(tt.next0_, NumberToken))): 
                    tt1 = tt.next0_.next0_
                    if (tt1 is not None and tt1.is_char('.')): 
                        tt1 = tt1.next0_
                        if (tt1 is not None and not tt1.is_newline_before and tt1.is_value("ВНЕСТИ", "УНЕСТИ")): 
                            continue
                        if (tt1 is not None and tt1.is_newline_before): 
                            return None
                        tt = tt1
                    break
                elif (tt == t and PartToken.try_attach(tt, None, False, False) is not None): 
                    break
                elif ((isinstance(tt, NumberToken)) and tt.typ == NumberSpellingType.DIGIT): 
                    pass
                elif (tt.is_hiphen): 
                    pass
                elif ((isinstance(tt, TextToken)) and not tt.chars.is_letter and not tt.is_whitespace_before): 
                    pass
                elif (((isinstance(tt, TextToken)) and tt.length_char == 1 and (isinstance(tt.next0_, TextToken))) and not tt.next0_.chars.is_letter): 
                    pass
                else: 
                    break
        if (tt is None): 
            return None
        res = None
        te1 = None
        has_change = False
        if ((isinstance(tt, TextToken)) and t.is_newline_before and not ignore_newlines): 
            if (tt.is_value("ВНЕСТИ", "УНЕСТИ") and ((((tt.next0_ is not None and tt.next0_.is_value("В", "ДО"))) or tt.term == "ВНЕСТИ" or tt.term == "УНЕСТИ"))): 
                te1 = tt
                if (tt.next0_ is not None and tt.next0_.is_value("В", "ДО")): 
                    te1 = tt.next0_
            elif (tt.is_value("ИЗМЕНЕНИЕ", None) and tt.next0_ is not None and tt.next0_.is_comma): 
                has_change = True
                ttt = tt.next0_.next0_
                first_pass3882 = True
                while True:
                    if first_pass3882: first_pass3882 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None)): break
                    if (ttt.is_value("КОТОРЫЙ", None)): 
                        continue
                    if (ttt.is_value("ВНОСИТЬСЯ", None) or ttt.is_value("ВНОСИМЫЙ", None)): 
                        continue
                    if (ttt.is_value("В", "ДО")): 
                        te1 = ttt
                        break
                    break
        if (te1 is not None): 
            res = DecreeChangeToken._new1032(tt, te1, DecreeChangeTokenTyp.STARTMULTU, True)
            tt = te1.next0_
            first_pass3883 = True
            while True:
                if first_pass3883: first_pass3883 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_newline_before): 
                    if (MiscHelper.can_be_start_of_sentence(tt)): 
                        break
                if (tt.is_char(':') and tt.whitespaces_after_count > 0): 
                    res.end_token = tt
                    break
                if (isinstance(tt.get_referent(), DecreeReferent)): 
                    res.decree = (Utils.asObjectOrNull(tt.get_referent(), DecreeReferent))
                    res.end_token = tt
                    res.__skip_decree_dummy()
                    tt = res.end_token
                    continue
                if (has_change and tt.is_value2("СОГЛАСНО", "ПРИЛОЖЕНИЕ")): 
                    res.app_ext_changes = PartToken.try_attach(tt.next0_, None, False, False)
                    if (res.app_ext_changes is not None and len(res.app_ext_changes.values) == 1): 
                        tt = res.app_ext_changes.end_token
                        res.end_token = tt
                        continue
                li = PartToken.try_attach_list(tt, False, 40)
                if (li is not None and len(li) > 0): 
                    if (res.parts is not None): 
                        break
                    res.parts = li
                    res.end_token = li[len(li) - 1].end_token
                    tt = res.end_token
                    continue
                if (tt.is_char('(')): 
                    br = BracketHelper.try_parse(tt, BracketParseAttr.CANBEMANYLINES, 100)
                    if (br is not None): 
                        tt = br.end_token
                        continue
                if (tt.is_newline_before): 
                    break
                res.end_token = tt
                if (tt.is_char(',') and has_change): 
                    res.typ = DecreeChangeTokenTyp.STARTSINGLE
                    if (res.parts is not None and tt.next0_ is not None and tt.next0_.is_value("ИЗЛОЖИТЬ", None)): 
                        li2 = PartToken.try_attach_list(tt.next0_.next0_, False, 40)
                        if (li2 is not None and len(li2) == 1): 
                            li2[0].begin_token = li2[0].end_token = res.parts[len(res.parts) - 1].end_token
                            res.parts.append(li2[0])
                    break
                if (tt.is_value("ИЗМЕНЕНИЕ", "ЗМІНА") or tt.is_value("ДОПОЛНЕНИЕ", "ДОДАТОК")): 
                    has_change = True
                elif (tt.is_value("СЛЕДУЮЩИЙ", "НАСТУПНИЙ")): 
                    pass
                elif (tt.is_value("ТАКОЙ", "ТАКИЙ")): 
                    pass
                elif (tt.is_value2("С", "ИЗМЕНЕНИЕ")): 
                    tt = tt.next0_
                    if (tt.next0_ is not None and tt.next0_.is_comma): 
                        tt = tt.next0_
            if (not has_change): 
                return None
            if (res.decree is None): 
                return None
            tt = res.end_token.next0_
            res.has_change_keyword = True
            if (res.typ == DecreeChangeTokenTyp.STARTSINGLE and res.parts is None and tt is not None): 
                if ((tt.is_value("ИЗЛОЖИВ", "ВИКЛАВШИ") or tt.is_value("ДОПОЛНИВ", "ДОПОВНИВШИ") or tt.is_value("ИСКЛЮЧИВ", "ВИКЛЮЧИВШИ")) or tt.is_value("ЗАМЕНИВ", "ЗАМІНИВШИ")): 
                    tt = tt.next0_
                    if (tt is not None and tt.morph.class0_.is_preposition): 
                        tt = tt.next0_
                    res.parts = PartToken.try_attach_list(tt, False, 40)
                    if (res.parts is not None): 
                        tt = res.end_token.next0_
                        if (tt.is_value("ДОПОЛНИВ", "ДОПОВНИВШИ")): 
                            res.act_kind = DecreeChangeKind.APPEND
                        elif (tt.is_value("ИСКЛЮЧИВ", "ВИКЛЮЧИВШИ")): 
                            res.act_kind = DecreeChangeKind.REMOVE
                        elif (tt.is_value("ИЗЛОЖИВ", "ВИКЛАВШИ")): 
                            res.act_kind = DecreeChangeKind.NEW
                        elif (tt.is_value("ЗАМЕНИВ", "ЗАМІНИВШИ")): 
                            res.act_kind = DecreeChangeKind.EXCHANGE
                        res.end_token = res.parts[len(res.parts) - 1].end_token
                        if (res.act_kind == DecreeChangeKind.APPEND): 
                            pp = PartToken.try_attach_list(res.end_token.next0_, False, 40)
                            if (pp is not None and len(pp) == 1): 
                                res.new_parts = pp
                                res.end_token = pp[0].end_token
            return res
        tt_expire = None
        is_suspend = False
        if (not ignore_newlines and is_newline_before_): 
            tt2 = tt
            first_pass3884 = True
            while True:
                if first_pass3884: first_pass3884 = False
                else: tt2 = tt2.next0_
                if (not (tt2 is not None)): break
                if (tt2 != tt and tt2.is_newline_before): 
                    break
                if (tt2.get_referent() is not None): 
                    continue
                if (tt2.is_char('(')): 
                    br = BracketHelper.try_parse(tt2, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        tt2 = br.end_token
                        continue
                dt = DecreeToken.try_attach(tt2, None, False)
                if (dt is not None and dt.typ == DecreeToken.ItemType.TYP): 
                    tt2 = dt.end_token
                    continue
                mc = tt2.get_morph_class_in_dictionary()
                if (mc.is_preposition or mc.is_adjective): 
                    continue
                if (tt2.is_value("МОМЕНТ", None) or tt2.is_value("ДЕНЬ", None)): 
                    continue
                if (tt2.is_value3("ВСТУПЛЕНИЕ", "В", "СИЛУ")): 
                    tt2 = tt2.next0_.next0_
                    continue
                if (tt2.is_value("ПРИЗНАТЬ", "ВИЗНАТИ") or tt2.is_value("СЧИТАТЬ", "ВВАЖАТИ") or tt2.is_value("ПЕРЕЧЕНЬ", None)): 
                    tt3 = tt2.next0_
                    if (tt3 is not None and tt3.is_comma): 
                        tt3 = tt3.next0_
                    if (tt3 is None): 
                        continue
                    if (tt3.is_value("УТРАТИТЬ", "ВТРАТИТИ")): 
                        if (tt3.next0_ is not None and tt3.next0_.is_value("СИЛА", "ЧИННІСТЬ")): 
                            tt_expire = tt3.next0_
                            break
                if (tt.is_value("ПРИОСТАНОВИТЬ", None) and tt.next0_ is not None): 
                    if (tt.next0_.is_value("ДЕЙСТВИЕ", None) or tt.next0_.is_value("С", None)): 
                        tt_expire = tt.next0_
                        is_suspend = True
                        break
                break
        if (tt_expire is not None): 
            res = DecreeChangeToken._new1033(tt, tt_expire, DecreeChangeTokenTyp.ACTION, (DecreeChangeKind.SUSPEND if is_suspend else DecreeChangeKind.EXPIRE))
            day_after = False
            first_pass3885 = True
            while True:
                if first_pass3885: first_pass3885 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_char(':') and tt.end_char > tt_expire.end_char): 
                    res.typ = DecreeChangeTokenTyp.STARTMULTU
                    if (tt.end_char > res.end_char): 
                        res.end_token = tt
                    break
                if (tt.is_value2("ДЕНЬ", "ВВЕДЕНИЯ")): 
                    day_after = True
                if (isinstance(tt.get_referent(), DecreeReferent)): 
                    if (not day_after): 
                        if (res.decree is not None): 
                            break
                        if (tt.previous is not None and tt.previous.is_value("СОГЛАСНО", None)): 
                            pass
                        else: 
                            res.typ = DecreeChangeTokenTyp.STARTSINGLE
                            res.decree = (Utils.asObjectOrNull(tt.get_referent(), DecreeReferent))
                    if (tt.end_char > res.end_char): 
                        res.end_token = tt
                    res.__skip_decree_dummy()
                    tt = res.end_token
                    continue
                li = PartToken.try_attach_list(tt, False, 40)
                if (li is not None and len(li) > 0 and not tt.is_value("СИЛА", None)): 
                    if (not day_after): 
                        if (res.parts is not None): 
                            break
                        if (tt.previous is not None and tt.previous.is_value("СОГЛАСНО", None)): 
                            pass
                        elif (tt.is_value("СОГЛАСНО", None)): 
                            pass
                        else: 
                            res.typ = DecreeChangeTokenTyp.STARTSINGLE
                            res.parts = li
                    tt = li[len(li) - 1].end_token
                    if (tt.end_char > res.end_char): 
                        res.end_token = tt
                    continue
                if (tt.is_char('(')): 
                    br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        tt = br.end_token
                        continue
                npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None): 
                    if (npt.end_token.is_value("АКТ", None) or npt.end_token.is_value("ПОЛОЖЕНИЕ", None)): 
                        tt = npt.end_token
                        if (tt.end_char > res.end_char): 
                            res.end_token = tt
                        continue
                r = tt.get_referent()
                if (r is not None and r.type_name == "ORGANIZATION"): 
                    if (tt.end_char > res.end_char): 
                        res.end_token = tt
                    continue
                if (tt.is_newline_before and tt.begin_char > tt_expire.begin_char): 
                    res.typ = DecreeChangeTokenTyp.STARTMULTU
                    break
            return res
        if ((not ignore_newlines and ((is_newline_before_ or tt == t)) and tt.is_value("УТРАТИТЬ", "ВТРАТИТИ")) and tt.next0_ is not None and tt.next0_.is_value("СИЛА", "ЧИННІСТЬ")): 
            res = DecreeChangeToken._new1034(tt, tt.next0_, DecreeChangeTokenTyp.UNDEFINED)
            tt = tt.next0_
            while tt is not None: 
                res.end_token = tt
                if (tt.is_newline_after): 
                    break
                tt = tt.next0_
            return res
        if (not ignore_newlines and is_newline_before_ and not tt.is_value2("В", "КОНЦЕ")): 
            if (tt.is_value("СЛОВО", None)): 
                pass
            res = DecreeChangeToken._new1034(tt, tt, DecreeChangeTokenTyp.STARTSINGLE)
            izlogit = None
            spec_regime = False
            first_pass3886 = True
            while True:
                if first_pass3886: first_pass3886 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt != res.begin_token and tt.is_newline_before): 
                    break
                if (tt.is_value("В", None)): 
                    if (tt != res.begin_token or not (isinstance(tt, TextToken))): 
                        continue
                    prr = PartToken.try_attach(tt.next0_, None, False, False)
                    if (prr is not None): 
                        continue
                    has_keyword = DecreeToken.is_keyword(tt.next0_, False) is not None
                    tt2 = tt.next0_
                    first_pass3887 = True
                    while True:
                        if first_pass3887: first_pass3887 = False
                        else: tt2 = tt2.next0_
                        if (not (tt2 is not None)): break
                        if (tt2.is_char_of(":;") or tt2.is_newline_before): 
                            break
                        br = BracketHelper.try_parse(tt2, BracketParseAttr.NO, 100)
                        if (br is not None): 
                            tt2 = br.end_token
                            continue
                        if (tt2.is_value("УТВЕРЖДЕННЫЙ", None) and (isinstance(tt2.next0_, ReferentToken)) and (isinstance(tt2.next0_.get_referent(), DecreeReferent))): 
                            tt = tt2
                            break
                        if ((isinstance(tt2.get_referent(), DecreeReferent)) and has_keyword): 
                            tt = tt2.previous
                            break
                    continue
                if (tt.is_value("К", None) or tt.is_value("ИЗ", None)): 
                    continue
                if (((tt.is_value("ПЕРЕЧЕНЬ", "ПЕРЕЛІК") or tt.is_value("СПИСОК", None))) and tt.next0_ is not None and tt.next0_.is_value("ИЗМЕНЕНИЕ", "ЗМІНА")): 
                    if (tt == t): 
                        res.end_token = tt.next0_
                    tt = tt.next0_.next0_
                    res.typ = DecreeChangeTokenTyp.STARTMULTU
                    while tt is not None and tt.next0_ is not None: 
                        if ((tt.next0_.is_comma or tt.next0_.is_value("КОТОРЫЙ", None) or tt.next0_.is_value("ВНОСИТЬ", None)) or tt.next0_.is_value("ВНОСИМЫЙ", None)): 
                            res.end_token = tt
                        else: 
                            break
                        tt = tt.next0_
                    continue
                if (tt.is_value("ИЗМЕНЕНИЕ", None) and tt == t): 
                    res.typ = DecreeChangeTokenTyp.STARTMULTU
                    res.has_change_keyword = True
                    while tt is not None and tt.next0_ is not None: 
                        if ((tt.next0_.is_comma or tt.next0_.is_value("КОТОРЫЙ", None) or tt.next0_.is_value("ВНОСИТЬ", None)) or tt.next0_.is_value("ВНОСИМЫЙ", None)): 
                            res.end_token = tt
                        else: 
                            break
                        tt = tt.next0_
                    continue
                if (tt.is_value("ТЕКСТ", None)): 
                    pt = PartToken.try_attach(tt.next0_, None, False, True)
                    if (pt is not None and pt.end_token.next0_ is not None and pt.end_token.next0_.is_value("СЧИТАТЬ", "ВВАЖАТИ")): 
                        res.end_token = pt.end_token
                        if (change_stack is not None and len(change_stack) > 0 and (isinstance(change_stack[0], DecreePartReferent))): 
                            res.real_part = (Utils.asObjectOrNull(change_stack[0], DecreePartReferent))
                        res.act_kind = DecreeChangeKind.CONSIDER
                        res.part_typ = pt.typ
                        res.has_text = True
                        return res
                if (tt.is_value2("И", "ТЕКСТ")): 
                    res.has_text = True
                    tt = tt.next0_
                    res.end_token = tt
                    continue
                if (tt.is_value3("ПО", "ВСЕМУ", "ТЕКСТУ")): 
                    res.has_text = True
                    tt = tt.next0_.next0_
                    res.end_token = tt
                    continue
                if (res.parts is None and tt.is_value("ДОПОЛНИТЬ", "ДОПОВНИТИ") and tt.next0_ is not None): 
                    res.act_kind = DecreeChangeKind.APPEND
                    if (isinstance(tt.next0_.get_referent(), DecreeReferent)): 
                        continue
                    tt = tt.next0_
                    tt1 = DecreeToken.is_keyword(tt, False)
                    if (tt1 is None or tt1.morph.case_.is_instrumental): 
                        tt1 = tt
                    else: 
                        tt1 = tt1.next0_
                    if (tt1 is not None and tt1.is_value("НОВЫЙ", "НОВИЙ")): 
                        tt1 = tt1.next0_
                    if (tt1 is not None and tt1.morph.case_.is_instrumental): 
                        pt = PartToken.try_attach(tt1, None, False, False)
                        if (pt is None): 
                            pt = PartToken.try_attach(tt1, None, False, True)
                        if (pt is not None and pt.typ != PartToken.ItemType.PREFIX): 
                            res.part_typ = pt.typ
                            res.end_token = pt.end_token
                            tt = res.end_token
                            if (res.new_parts is None): 
                                res.new_parts = list()
                            res.new_parts.append(pt)
                            if (tt.next0_ is not None and tt.next0_.is_and): 
                                pt = PartToken.try_attach(tt.next0_.next0_, None, False, False)
                                if (pt is None): 
                                    pt = PartToken.try_attach(tt.next0_.next0_, None, False, True)
                                if (pt is not None): 
                                    res.new_parts.append(pt)
                                    res.end_token = pt.end_token
                                    tt = res.end_token
                        continue
                if (tt.is_value("ДОПОЛНИТЬ", "ДОПОВНИТИ") and tt.next0_ is not None and tt.next0_.is_char(':')): 
                    res.act_kind2 = DecreeChangeKind.APPEND
                    res.end_token = tt.next0_
                    return res
                li = PartToken.try_attach_list(tt, False, 40)
                if (li is None and tt.is_value("ПРИМЕЧАНИЕ", "ПРИМІТКА")): 
                    li = list()
                    li.append(PartToken._new1036(tt, tt, PartToken.ItemType.NOTICE))
                if (li is not None and len(li) > 0 and li[0].typ == PartToken.ItemType.PREFIX): 
                    li = (None)
                if (li is not None and len(li) > 0): 
                    if ((res.parts is not None and len(res.parts) == 1 and res.parts[0].typ == PartToken.ItemType.NAME) and res.has_text): 
                        res.parts.extend(li)
                        tt = li[len(li) - 1].end_token
                        res.end_token = tt
                        continue
                    if ((len(li) == 1 and li[0].morph.case_.is_instrumental and not li[0].morph.case_.is_accusative) and res.new_parts is None): 
                        res.new_parts = list()
                        res.new_parts.append(li[0])
                        tt = li[0].end_token
                        res.end_token = tt
                        continue
                    if (len(li) == 1 and PartToken._get_rank(li[0].typ) > 0 and tt == t): 
                        if (li[0].is_newline_after): 
                            return None
                        if (li[0].end_token.next0_ is not None and li[0].end_token.next0_.is_char('.')): 
                            return None
                    if (res.act_kind != DecreeChangeKind.APPEND): 
                        if (res.parts is not None): 
                            if (len(res.parts) == 1 and ((res.parts[0].typ == PartToken.ItemType.APPENDIX or res.parts[0].typ == PartToken.ItemType.DOCPART))): 
                                if (len(li) > 1 and PartToken._get_rank(li[0].typ) > PartToken._get_rank(li[len(li) - 1].typ)): 
                                    res.parts[0:0] = li
                                else: 
                                    res.parts.extend(li)
                            else: 
                                break
                        else: 
                            res.parts = li
                            ttt1 = li[len(li) - 1].end_token
                            if (ttt1.next0_ is not None and ttt1.next0_.is_value("ПОСЛЕ", None)): 
                                sss = PartToken.try_attach(ttt1.next0_.next0_, li[len(li) - 1], False, False)
                                if (sss is not None): 
                                    li.append(sss)
                                    ttt1 = sss.end_token
                            while ttt1 is not None: 
                                if (ttt1.is_newline_before or ttt1.is_table_control_char): 
                                    break
                                pp = PartToken.try_attach(ttt1, None, False, False)
                                if (pp is not None and pp.typ != PartToken.ItemType.PREFIX): 
                                    break
                                if (ttt1.is_value3("ВСТУПАТЬ", "В", "СИЛУ")): 
                                    res.ignorable = True
                                    break
                                if ((ttt1.is_value3("ИЗЛОЖИТЬ", "В", "СЛЕДУЮЩЕЙ") or ttt1.is_value3("ПРИНЯТЬ", "В", "СЛЕДУЮЩЕЙ") or ttt1.is_value3("ИЗЛОЖИТЬ", "В", "НОВОЙ")) or ttt1.is_value3("В", "СЛЕДУЮЩЕЙ", "РЕДАКЦИИ") or ttt1.is_value3("В", "РЕДАКЦИИ", "ПРИЛОЖЕНИЯ")): 
                                    izlogit = ttt1.previous
                                    break
                                if (DecreeChangeToken.M_TERMS.try_parse(ttt1, TerminParseAttr.NO) is not None): 
                                    break
                                ttt1 = ttt1.next0_
                    elif (len(li) == 1 and li[0].morph is not None and li[0].morph.case_.is_instrumental): 
                        if (res.new_parts is None): 
                            res.new_parts = list()
                        res.new_parts.append(li[0])
                    elif (res.parts is None): 
                        res.parts = li
                    res.end_token = li[len(li) - 1].end_token
                    tt = res.end_token
                    continue
                if ((tt.morph.class0_.is_noun and change_stack is not None and len(change_stack) > 0) and (isinstance(change_stack[0], DecreePartReferent))): 
                    pa = PartToken.try_attach(tt, None, False, True)
                    if (pa is not None): 
                        if (change_stack[0].get_string_value(PartToken._get_attr_name_by_typ(pa.typ)) is not None): 
                            res.real_part = (Utils.asObjectOrNull(change_stack[0], DecreePartReferent))
                            res.end_token = tt
                            continue
                if (res.act_kind == DecreeChangeKind.APPEND): 
                    pa = PartToken.try_attach(tt, None, False, True)
                    if (pa is not None and pa.typ != PartToken.ItemType.PREFIX): 
                        if (res.new_parts is None): 
                            res.new_parts = list()
                        res.new_parts.append(pa)
                        res.end_token = pa.end_token
                        continue
                if (isinstance(tt.get_referent(), DecreeReferent)): 
                    ki = tt.get_referent().kind
                    if (ki == DecreeKind.PUBLISHER): 
                        continue
                    if (tt.morph.case_.is_instrumental): 
                        if (tt.is_newline_before): 
                            return None
                    res.decree = (Utils.asObjectOrNull(tt.get_referent(), DecreeReferent))
                    res.end_token = tt
                    res.__skip_decree_dummy()
                    tt = res.end_token
                    continue
                pt0 = PartToken.try_attach(tt, None, False, True)
                if (pt0 is not None and ((pt0.typ == PartToken.ItemType.APPENDIX)) and pt0.typ != PartToken.ItemType.PREFIX): 
                    res.end_token = pt0.end_token
                    tt = res.end_token
                    res.part_typ = pt0.typ
                    if (pt0.typ == PartToken.ItemType.APPENDIX and res.parts is None): 
                        res.parts = list()
                        res.parts.append(pt0)
                    continue
                if (res.change_val is None and not is_in_edition): 
                    res1 = None
                    if (tt == res.begin_token and BracketHelper.can_be_start_of_sequence(tt, False, False)): 
                        pass
                    else: 
                        res1 = DecreeChangeToken.try_attach(tt, main, True, None, False, False)
                    if (res1 is not None and res1.typ == DecreeChangeTokenTyp.VALUE and res1.change_val is not None): 
                        res.change_val = res1.change_val
                        res.in_the_end = res1.in_the_end
                        if (res.act_kind == DecreeChangeKind.UNDEFINED): 
                            res.act_kind = res1.act_kind
                        res.end_token = res1.end_token
                        tt = res.end_token
                        if (tt.next0_ is not None and tt.next0_.is_value("К", None)): 
                            tt = tt.next0_
                        continue
                    if (res1 is not None and res1.act_kind == DecreeChangeKind.CONSIDER): 
                        izlogit = (None)
                    if (tt.is_value("ПОСЛЕ", "ПІСЛЯ")): 
                        pts0 = PartToken.try_attach_list(tt.next0_, False, 40)
                        if (pts0 is not None and len(pts0) > 0 and pts0[0].typ != PartToken.ItemType.PREFIX): 
                            tt2 = pts0[len(pts0) - 1].end_token.next0_
                            while tt2 is not None and ((tt2.is_value("НОВЫЙ", None) or tt2.is_value("ДОПОЛНИТЬ", None))):
                                tt2 = tt2.next0_
                            pt2 = PartToken.try_attach(tt2, None, True, False)
                            if (pt2 is None): 
                                pt2 = PartToken.try_attach(tt2, None, False, True)
                            if (pt2 is not None and pt2.typ == pts0[0].typ): 
                                if (len(pt2.values) > 0): 
                                    res.parts = pts0
                                    res.new_parts = list()
                                    res.new_parts.append(pt2)
                                    res.act_kind = DecreeChangeKind.APPEND
                                    res.end_token = pt2.end_token
                                    tt = res.end_token
                                    continue
                                pts1 = PartToken.try_attach_list(tt.next0_, False, 40)
                                if (pts1[0].add_value(1)): 
                                    res.parts = pts0
                                    res.new_parts = pts1
                                    res.act_kind = DecreeChangeKind.APPEND
                                    res.end_token = pt2.end_token
                                    tt = res.end_token
                                    continue
                            if (res.parts is None): 
                                res.parts = pts0
                            res.end_token = pts0[len(pts0) - 1].end_token
                            tt = res.end_token
                            continue
                    pt0 = PartToken.try_attach(tt, None, False, True)
                    if ((pt0 is not None and pt0.typ != PartToken.ItemType.PREFIX and res.new_parts is None) and pt0.morph.case_.is_instrumental): 
                        res.new_parts = list()
                        res.new_parts.append(pt0)
                        res.end_token = pt0.end_token
                        tt = res.end_token
                        continue
                    if (tt.is_value("ТЕКСТ", None) and tt.previous is not None and tt.previous.is_value("В", "У")): 
                        continue
                    if (tt.is_value("ИЗМЕНЕНИЕ", "ЗМІНА")): 
                        res.end_token = tt
                        continue
                    if (tt.is_value("УКАЗАННЫЙ", None) or tt.is_value("ВЫШЕУКАЗАННЫЙ", None)): 
                        npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                        if (npt is not None): 
                            tt = npt.end_token
                            res.end_token = tt
                            continue
                    if (tt.is_char(':') and tt.next0_ is not None and tt.next0_.next0_ is not None): 
                        if ((isinstance(tt.next0_, NumberToken)) or ((tt.next0_.length_char == 1))): 
                            if (tt.next0_.next0_.is_char_of(".)")): 
                                break
                if (tt != t and ((res.parts is not None)) and res.decree is None): 
                    dts = DecreeToken.try_attach_list(tt, None, 10, False)
                    if (dts is not None and len(dts) > 0 and dts[0].typ == DecreeToken.ItemType.TYP): 
                        res.end_token = dts[len(dts) - 1].end_token
                        tt = res.end_token
                        if (main is not None and res.decree is None and res.decree_tok is None): 
                            dec = None
                            for v in main.owners: 
                                if (isinstance(v, DecreeReferent)): 
                                    dec = (Utils.asObjectOrNull(v, DecreeReferent))
                                    break
                                elif (isinstance(v, DecreePartReferent)): 
                                    dec = v.owner
                                    if (dec is not None): 
                                        break
                            if (dec is not None and dec.typ0 == dts[0].value): 
                                res.decree = dec
                                res.decree_tok = dts[0]
                        continue
                if (tt == res.begin_token and main is not None): 
                    npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None): 
                        tt1 = npt.end_token.next0_
                        if ((tt1 is not None and ((tt1.is_value("ИЗЛОЖИТЬ", "ВИКЛАСТИ") or tt1.is_value("ПРИНЯТЬ", None))) and tt1.next0_ is not None) and tt1.next0_.is_value("В", None)): 
                            pt = PartToken._new1036(tt, npt.end_token, PartToken.ItemType.APPENDIX)
                            pt.name = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                            res.parts = list()
                            res.parts.append(pt)
                            res.end_token = pt.end_token
                            break
                ttt = DecreeToken.is_keyword(tt, False)
                if (ttt is not None and res.parts is None): 
                    ttt0 = ttt
                    while ttt is not None: 
                        if (MiscHelper.can_be_start_of_sentence(ttt)): 
                            break
                        if (ttt.is_char('(') and ttt.next0_ is not None and ttt.next0_.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
                            if (ttt.is_newline_before): 
                                break
                            br = BracketHelper.try_parse(ttt, BracketParseAttr.NO, 100)
                            if (br is None): 
                                break
                            pt = PartToken.try_attach(ttt.next0_, None, False, False)
                            if (pt is None): 
                                PartToken.try_attach(ttt.next0_, None, False, True)
                            if (pt is not None): 
                                res.parts = list()
                                res.parts.append(pt)
                                res.end_token = br.end_token
                                tt = res.end_token
                                break
                        if (ttt.is_value3("В", "СЛЕДУЮЩЕЙ", "РЕДАКЦИИ") or ttt.is_value3("В", "РЕДАКЦИИ", "ПРИЛОЖЕНИЕ")): 
                            pt = PartToken(tt, ttt.previous)
                            pt.typ = PartToken.ItemType.CHAPTER
                            pt.name = MiscHelper.get_text_value_of_meta_token(pt, GetTextAttr.NO)
                            res.parts = list()
                            res.parts.append(pt)
                            res.end_token = ttt.previous
                            tt = res.end_token
                            break
                        ttt = ttt.next0_
                    if (res.parts is not None): 
                        continue
                    if (res.act_kind == DecreeChangeKind.APPEND): 
                        res.end_token = ttt0
                        tt = res.end_token
                        continue
                    tt = ttt0
                    continue
                if (spec_regime): 
                    res.end_token = tt
                    continue
                if (tt.is_char_of(".-") and not tt.is_newline_after): 
                    res.end_token = tt
                    continue
                if (tt.is_comma and res.decree is not None): 
                    continue
                if (tt.is_value("ИЗЛОЖИТЬ", None) or tt.is_value("ПРИНЯТЬ", None)): 
                    if (res.parts is None): 
                        res.act_kind = DecreeChangeKind.NEW
                        if (tt.next0_ is not None and tt.next0_.get_morph_class_in_dictionary().is_pronoun): 
                            tt = tt.next0_
                            res.has_anafor = True
                        res.end_token = tt
                        continue
                if (tt.next0_ is not None): 
                    tt2 = tt.next0_
                    if (tt.is_value("СОГЛАСНО", None)): 
                        tt2 = tt
                    if (tt2 is not None and tt2.is_value2("В", "РЕДАКЦИИ")): 
                        tt2 = tt2.next0_.next0_
                    if (tt2 is not None and ((tt2.is_value2("СОГЛАСНО", "ПРИЛОЖЕНИЮ") or ((tt2.is_value("ПРИЛОЖЕНИЯ", None) and res.act_kind == DecreeChangeKind.NEW))))): 
                        ppp = PartToken.try_attach(tt2.next0_, None, False, False)
                        if (ppp is None): 
                            ppp = PartToken.try_attach(tt2.next0_, None, True, False)
                        if (ppp is None): 
                            ppp = PartToken.try_attach(tt2, None, True, False)
                        if (ppp is not None and ppp.typ == PartToken.ItemType.APPENDIX): 
                            res.app_ext_changes = ppp
                            if (res.act_kind == DecreeChangeKind.UNDEFINED): 
                                res.act_kind = DecreeChangeKind.NEW
                            tt = ppp.end_token
                            res.end_token = tt
                            if (tt.next0_ is not None and tt.next0_.is_value("К", None)): 
                                npt = NounPhraseHelper.try_parse(tt.next0_.next0_, NounPhraseParseAttr.NO, 0, None)
                                if (npt is not None): 
                                    tt = npt.end_token
                                    res.end_token = tt
                            continue
                if (izlogit is not None and izlogit.end_char > tt.end_char): 
                    tt = izlogit
                    res.end_token = tt
                    izlogit = (None)
                    continue
                break
            if (((res.ignorable or res.parts is not None or res.decree is not None) or res.real_part is not None or res.act_kind != DecreeChangeKind.UNDEFINED) or res.change_val is not None): 
                if (res.end_token.next0_ is not None and res.end_token.next0_.is_char(':')): 
                    nl = res.end_token.next0_.is_newline_after
                    if (not nl): 
                        pl = PartToken.try_attach(res.end_token.next0_.next0_, None, False, False)
                        if (pl is not None): 
                            nl = True
                    if (nl): 
                        res.typ = DecreeChangeTokenTyp.SINGLE
                        res.end_token = res.end_token.next0_
                return res
            if (res.begin_token == tt): 
                tok1 = DecreeChangeToken.M_TERMS.try_parse(tt, TerminParseAttr.NO)
                if (tok1 is not None): 
                    pass
                elif (tt.is_value("ПОСЛЕ", None)): 
                    pass
                else: 
                    return None
            else: 
                return None
        while tt is not None: 
            if (tt.is_value("В", None) and tt.next0_ is not None and tt.next0_.get_morph_class_in_dictionary().is_pronoun): 
                tt = tt.next0_
            else: 
                break
            tt = tt.next0_
        if (tt is None): 
            return None
        tok = DecreeChangeToken.M_TERMS.try_parse(tt, TerminParseAttr.NO)
        if (tt.morph.class0_.is_adjective and (((isinstance(tt, NumberToken)) or tt.is_value("ПОСЛЕДНИЙ", "ОСТАННІЙ") or tt.is_value("ПРЕДПОСЛЕДНИЙ", "ПЕРЕДОСТАННІЙ")))): 
            tt2 = tt.next0_
            while tt2 is not None: 
                if ((isinstance(tt2, NumberToken)) or tt2.is_comma_and): 
                    pass
                else: 
                    break
                tt2 = tt2.next0_
            tok = DecreeChangeToken.M_TERMS.try_parse(tt2, TerminParseAttr.NO)
            if (tok is not None and (isinstance(tok.termin.tag, DecreeChangeValueKind))): 
                pass
            else: 
                tok = (None)
        after_value = False
        if (tok is None and tt.is_value("ПОСЛЕ", None) and BracketHelper.can_be_start_of_sequence(tt.next0_, True, False)): 
            tok = TerminToken(tt, tt)
            tok.termin = Termin._new84("СЛОВО", DecreeChangeValueKind.WORDS)
            after_value = True
        if (tok is None and tt.is_value("ПРЕДЛОЖЕНИЕ", None) and BracketHelper.can_be_start_of_sequence(tt.next0_, True, False)): 
            tok = TerminToken._new562(tt, tt, DecreeChangeToken.__m_words)
        elif ((tok is None and tt.is_value("ПРЕДЛОЖЕНИЕ", None) and tt.next0_ is not None) and tt.next0_.is_char(':') and BracketHelper.can_be_start_of_sequence(tt.next0_.next0_, True, False)): 
            tok = TerminToken._new562(tt, tt.next0_, DecreeChangeToken.__m_words)
        if (tok is not None): 
            if (isinstance(tok.termin.tag, DecreeChangeKind)): 
                res = DecreeChangeToken._new1033(tt, tok.end_token, DecreeChangeTokenTyp.ACTION, Utils.valToEnum(tok.termin.tag, DecreeChangeKind))
                if (((res.act_kind == DecreeChangeKind.APPEND or res.act_kind == DecreeChangeKind.CONSIDER)) and tok.end_token.next0_ is not None and tok.end_token.next0_.morph.case_.is_instrumental): 
                    tt4 = tok.end_token.next0_
                    if (tt4 is not None and tt4.is_value("СЛЕДУЮЩИЙ", None)): 
                        tt4 = tt4.next0_
                    pt = PartToken.try_attach(tt4, None, False, False)
                    if (pt is None): 
                        pt = PartToken.try_attach(tt4, None, False, True)
                    if (pt is not None and pt.typ != PartToken.ItemType.PREFIX): 
                        if (res.act_kind == DecreeChangeKind.APPEND): 
                            res.part_typ = pt.typ
                            if (res.new_parts is None): 
                                res.new_parts = list()
                            res.new_parts.append(pt)
                        elif (res.act_kind == DecreeChangeKind.CONSIDER): 
                            res.change_val = DecreeChangeValueReferent()
                            res.change_val.value = pt.get_source_text()
                        res.end_token = pt.end_token
                        tt = res.end_token
                        if (tt.next0_ is not None and tt.next0_.is_and and res.act_kind == DecreeChangeKind.APPEND): 
                            pt = PartToken.try_attach(tt.next0_.next0_, None, False, False)
                            if (pt is None): 
                                pt = PartToken.try_attach(tt.next0_.next0_, None, False, True)
                            if (pt is not None): 
                                res.new_parts.append(pt)
                                res.end_token = pt.end_token
                                tt = res.end_token
                if (res.act_kind == DecreeChangeKind.CONSIDER and (isinstance(tok.end_token.next0_, NumberToken)) and (tok.whitespaces_after_count < 3)): 
                    tt3 = res.end_token.next0_
                    first_pass3888 = True
                    while True:
                        if first_pass3888: first_pass3888 = False
                        else: tt3 = tt3.next0_
                        if (not (tt3 is not None)): break
                        if (isinstance(tt3, NumberToken)): 
                            res.end_token = tt3
                            continue
                        if (tt3.is_comma_and): 
                            continue
                        break
                    res.change_val = DecreeChangeValueReferent()
                    res.change_val.value = MiscHelper.get_text_value(tok.end_token.next0_, res.end_token, GetTextAttr.KEEPREGISTER)
                if (res.end_token.next0_ is not None and res.end_token.next0_.is_value("СООТВЕТСТВЕННО", None)): 
                    res.end_token = res.end_token.next0_
                return res
            if (isinstance(tok.termin.tag, DecreeChangeValueKind)): 
                res = DecreeChangeToken._new1034(tt, tok.end_token, DecreeChangeTokenTyp.VALUE)
                res.change_val = DecreeChangeValueReferent()
                res.change_val.kind = Utils.valToEnum(tok.termin.tag, DecreeChangeValueKind)
                if (after_value): 
                    res.typ = DecreeChangeTokenTyp.AFTERVALUE
                if (res.change_val.kind == DecreeChangeValueKind.WORDS and (isinstance(tok.termin.tag2, str))): 
                    res.change_val.value = Utils.asObjectOrNull(tok.termin.tag2, str)
                    res.change_val.begin_char = tok.begin_char
                    res.change_val.end_char = tok.end_char
                    return res
                tt = tok.end_token.next0_
                if (tt is None): 
                    return None
                if (tt is not None and ((tt.is_value("ИЗЛОЖИТЬ", "ВИКЛАСТИ") or tt.is_value("ПРИНЯТЬ", None))) and res.act_kind == DecreeChangeKind.UNDEFINED): 
                    res.act_kind = DecreeChangeKind.NEW
                    tt = tt.next0_
                    if (tt is not None and tt.is_value("В", None)): 
                        tt = tt.next0_
                if ((tt is not None and ((tt.is_value("СЛЕДУЮЩИЙ", "НАСТУПНИЙ") or tt.is_value("ТАКОЙ", "ТАКИЙ"))) and tt.next0_ is not None) and ((tt.next0_.is_value("СОДЕРЖАНИЕ", "ЗМІСТ") or tt.next0_.is_value("СОДЕРЖИМОЕ", "ВМІСТ") or tt.next0_.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ")))): 
                    tt = tt.next0_.next0_
                elif (tt is not None and tt.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
                    tt = tt.next0_
                if (tt is not None and tt.is_char(':')): 
                    tt = tt.next0_
                if (tt is not None): 
                    res.change_val.begin_char = tt.begin_char
                can_be_start = False
                if (BracketHelper.can_be_start_of_sequence(tt, True, False)): 
                    can_be_start = True
                elif (BracketHelper.is_bracket(tt, True) and not tt.is_whitespace_after): 
                    can_be_start = True
                elif ((isinstance(tt, MetaToken)) and BracketHelper.can_be_start_of_sequence(tt.begin_token, True, False)): 
                    can_be_start = True
                elif (tt is not None and tt.is_newline_before and tt.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК")): 
                    if ((tt.previous is not None and tt.previous.is_char(':') and tt.previous.previous is not None) and tt.previous.previous.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
                        can_be_start = True
                elif (t.previous is not None and ((t.previous.is_value("ДОПОЛНИТЬ", None) or t.previous.is_value("ПОСЛЕ", None)))): 
                    can_be_start = True
                elif (tt.is_char('«') and tt.next0_ is not None and tt.next0_.is_char('»')): 
                    res.change_val.value = ""
                    res.end_token = tt.next0_
                    res.change_val.begin_char = tt.end_char + 1
                    res.change_val.end_char = tt.next0_.begin_char - 1
                    return res
                elif (tt.next0_ is not None): 
                    cou = 0
                    tt2 = tt.next0_
                    while tt2 is not None and (cou < 10): 
                        if (tt2.is_char('»')): 
                            res.change_val.value = (MetaToken(tt, tt2.previous)).get_source_text()
                            res.end_token = tt2
                            res.change_val.end_char = tt2.begin_char - 1
                            return res
                        tt2 = tt2.next0_; cou += 1
                if (can_be_start): 
                    ttt = tt
                    if (BracketHelper.is_bracket(tt, True)): 
                        ttt = tt.next0_
                        res.change_val.begin_char = ttt.begin_char
                    first_pass3889 = True
                    while True:
                        if first_pass3889: first_pass3889 = False
                        else: ttt = ttt.next0_
                        if (not (ttt is not None)): break
                        if (ttt.is_char_of(".;")): 
                            stop = ttt.is_newline_after
                            if (not stop and BracketHelper.is_bracket(ttt.previous, False)): 
                                num = ComplexNumToken.try_parse(ttt.next0_, None, False, False)
                                if (num is not None): 
                                    stop = True
                            if (stop): 
                                res.change_val.value = (MetaToken(tt.next0_, ttt.previous)).get_source_text()
                                res.end_token = ttt.previous
                                res.change_val.end_char = res.end_token.end_char
                                break
                        if (DecreeChangeToken._check_end_bracket(ttt)): 
                            pass
                        else: 
                            continue
                        if (ttt.next0_ is None or ttt.is_newline_after): 
                            pass
                        elif (ttt.next0_.is_value("СООТВЕТСТВЕННО", None) or ttt.next0_.is_value2("В", "СООТВЕТСТВУЮЩИЙ")): 
                            pass
                        elif (ttt.next0_.is_char_of(".;") and (((ttt.next0_.is_newline_after or DecreeChangeToken.try_attach(ttt.next0_.next0_, main, False, change_stack, True, False) is not None or PartToken.try_attach(ttt.next0_.next0_, None, False, False) is not None) or ttt.next0_.next0_.is_value("В", None)))): 
                            pass
                        elif (ttt.next0_.is_comma_and and DecreeChangeToken.try_attach(ttt.next0_.next0_, main, False, change_stack, True, False) is not None): 
                            pass
                        elif (ttt.next0_.is_comma and ttt.next0_.next0_ is not None and ttt.next0_.next0_.is_value("А", None)): 
                            conj = ConjunctionHelper.try_parse(ttt.next0_.next0_)
                            if (conj is not None and DecreeChangeToken.try_attach(conj.end_token.next0_, main, False, change_stack, True, False) is not None): 
                                pass
                            else: 
                                continue
                        elif (DecreeChangeToken.try_attach(ttt.next0_, main, False, change_stack, True, False) is not None or DecreeChangeToken.M_TERMS.try_parse(ttt.next0_, TerminParseAttr.NO) is not None): 
                            pass
                        elif ((ttt.next0_.is_value("ДОБАВИТЬ", None) or ttt.next0_.is_value("ДОПОЛНИТЬ", None) or ttt.next0_.is_value("ЗАМЕНИТЬ", None)) or ttt.next0_.is_value("УДАЛИТЬ", None)): 
                            pass
                        else: 
                            continue
                        ttt1 = (ttt.previous if BracketHelper.is_bracket(ttt, True) and not ttt.is_char_of("]>") else ttt)
                        val = (MetaToken((tt.next0_ if BracketHelper.is_bracket(tt, True) else tt), ttt1)).get_source_text()
                        res.end_token = ttt
                        res.change_val.end_char = ttt1.end_char
                        if ((ttt == tt and (isinstance(ttt, MetaToken)) and BracketHelper.is_bracket(ttt.begin_token, True)) and BracketHelper.is_bracket(ttt.end_token, True)): 
                            val = val[1:1+len(val) - 2]
                            res.change_val.end_char = res.change_val.end_char - 1
                        elif ((isinstance(tt, MetaToken)) and BracketHelper.is_bracket(tt.begin_token, True)): 
                            val = val[1:1+len(val) - 1]
                        res.change_val.value = val
                        if (res.end_token.next0_ is not None): 
                            if (res.end_token.next0_.is_value("СООТВЕТСТВЕННО", None)): 
                                res.end_token = res.end_token.next0_
                        if (BracketHelper.can_be_start_of_sequence(tt, True, False) and BracketHelper.can_be_end_of_sequence(ttt, True, None, False)): 
                            vals = None
                            pp = None
                            pp0 = tt.next0_
                            pp = tt.next0_
                            while pp is not None and pp.end_char <= ttt.end_char: 
                                if ((BracketHelper.can_be_end_of_sequence(pp, False, None, False) and pp.next0_ is not None and pp.next0_.is_comma_and) and BracketHelper.can_be_start_of_sequence(pp.next0_.next0_, True, False) and (pp.next0_.next0_.end_char < ttt.begin_char)): 
                                    if (vals is None): 
                                        vals = list()
                                    vals.append((MetaToken(pp0, pp.previous)).get_source_text())
                                    pp = pp.next0_.next0_
                                    pp0 = pp.next0_
                                pp = pp.next0_
                            if (vals is not None): 
                                if (pp0 is not None and (pp0.end_char < ttt.begin_char)): 
                                    vals.append((MetaToken(pp0, ttt.previous)).get_source_text())
                                res.change_val.value = vals[0]
                                i = 1
                                while i < len(vals): 
                                    res.change_val.add_slot(DecreeChangeReferent.ATTR_VALUE, vals[i], False, 0)
                                    i += 1
                        break
                    if (res.change_val.value is None): 
                        return None
                    if (res.change_val.kind == DecreeChangeValueKind.WORDS): 
                        tok = DecreeChangeToken.M_TERMS.try_parse(res.end_token.next0_, TerminParseAttr.NO)
                        if (tok is not None and (isinstance(tok.termin.tag, DecreeChangeValueKind)) and (Utils.valToEnum(tok.termin.tag, DecreeChangeValueKind)) == DecreeChangeValueKind.ROBUSTWORDS): 
                            res.change_val.kind = DecreeChangeValueKind.ROBUSTWORDS
                            res.end_token = tok.end_token
                            if (res.end_token.next0_ is not None): 
                                if (res.end_token.next0_.is_value2("И", "ЧИСЛЕ") or res.end_token.next0_.is_value2("И", "ПАДЕЖЕ")): 
                                    res.end_token = res.end_token.next0_.next0_
                if (res.change_val.value is None): 
                    return None
                return res
        is_nex_change = 0
        if (t is not None and t.is_value("В", "У") and t.next0_ is not None): 
            t = t.next0_
            if (t.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ") and t.next0_ is not None): 
                is_nex_change = 1
                t = t.next0_
        if (((t.is_value("СЛЕДУЮЩИЙ", "НАСТУПНИЙ") or tt.is_value("ТАКОЙ", "ТАКИЙ"))) and t.next0_ is not None and ((t.next0_.is_value("СОДЕРЖАНИЕ", "ЗМІСТ") or t.next0_.is_value("СОДЕРЖИМОЕ", "ВМІСТ") or t.next0_.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ")))): 
            is_nex_change = 2
            t = t.next0_.next0_
        if (t is None): 
            return None
        if (t.is_char(':') and t.next0_ is not None): 
            if (t.previous is not None and t.previous.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
                is_nex_change += 1
            t = t.next0_
            tt = t
            if (is_nex_change > 0): 
                is_nex_change += 1
        elif (t.previous is not None and t.previous.is_value("РЕДАКЦИЯ", None) and BracketHelper.can_be_start_of_sequence(t, True, False)): 
            is_nex_change += 1
        if ((t == tt and t.previous is not None and t.previous.is_char(':')) and BracketHelper.is_bracket(t, False) and not t.is_char('(')): 
            is_nex_change = 1
        xx1 = t
        if (xx1 is not None and xx1.is_table_control_char): 
            xx1 = xx1.next0_
        if (((is_nex_change > 0 and ((BracketHelper.is_bracket(xx1, True) or abzac_regime or ComplexNumToken.try_parse(xx1, None, False, False) is not None)))) or ((is_nex_change > 1 and t.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК")))): 
            if (is_in_edition): 
                res = DecreeChangeToken._new1034(t, xx1, DecreeChangeTokenTyp.VALUE)
                res.change_val = DecreeChangeValueReferent._new1044(DecreeChangeValueKind.TEXT)
                return res
            res = DecreeChangeToken._try_parse_text(xx1, abzac_regime, False)
            if (res is None): 
                return None
            res.begin_token = t
            return res
        if (tt.is_value("ПОСЛЕ", "ПІСЛЯ")): 
            pt = PartToken.try_attach_list(tt.next0_, False, 40)
            if (pt is not None and len(pt) > 0): 
                tt2 = pt[len(pt) - 1].end_token.next0_
                while tt2 is not None and ((tt2.is_value("НОВЫЙ", None) or tt2.is_value("ДОПОЛНИТЬ", None))):
                    tt2 = tt2.next0_
                pt2 = PartToken.try_attach(tt2, None, False, True)
                if (pt2 is not None and pt2.typ == pt[0].typ): 
                    if (len(pt2.values) > 0): 
                        res = DecreeChangeToken(tt, pt2.end_token)
                        res.parts = pt
                        res.act_kind = DecreeChangeKind.APPEND
                        res.new_parts = list()
                        res.new_parts.append(pt2)
                        return res
                    pt1 = PartToken.try_attach_list(tt.next0_, False, 40)
                    if (pt1[0].add_value(1)): 
                        res = DecreeChangeToken(tt, pt2.end_token)
                        res.parts = pt
                        res.act_kind = DecreeChangeKind.APPEND
                        res.new_parts = list()
                        res.new_parts.extend(pt1)
                        return res
            res = DecreeChangeToken.try_attach(tt.next0_, None, False, None, False, False)
            if (res is not None and res.typ == DecreeChangeTokenTyp.VALUE): 
                res.typ = DecreeChangeTokenTyp.AFTERVALUE
                res.begin_token = tt
                return res
        if (tt.is_value2("В", "КОНЦЕ")): 
            pts = PartToken.try_attach_list(tt.next0_.next0_, True, 40)
            if (pts is not None and len(pts) > 0): 
                res = DecreeChangeToken.try_attach(pts[len(pts) - 1].end_token.next0_, None, False, None, False, False)
                if (res is not None and res.parts is None): 
                    res.begin_token = tt
                    res.in_the_end = True
                    if (res.change_val is not None): 
                        res.change_val.add_slot("POSITION", "end", False, 0)
                    res.parts = pts
                    return res
        return None
    
    @staticmethod
    def _check_end_bracket(t : 'Token') -> bool:
        if (BracketHelper.is_bracket(t, True)): 
            return not t.is_char_of(">]")
        if (isinstance(t, MetaToken)): 
            if (BracketHelper.is_bracket(t.end_token, True)): 
                return not t.end_token.is_char_of(">]")
            if (isinstance(t.end_token, MetaToken)): 
                if (BracketHelper.is_bracket(t.end_token.end_token, True)): 
                    return not t.end_token.end_token.is_char_of(">]")
        return False
    
    @staticmethod
    def _try_parse_text(xx1 : 'Token', abzac_regime : bool, word_regime : bool=False) -> 'DecreeChangeToken':
        from pullenti.ner.decree.internal.DecreeToken import DecreeToken
        from pullenti.ner.instrument.internal.InstrToken1 import InstrToken1
        from pullenti.ner.instrument.internal.NumberingHelper import NumberingHelper
        res = DecreeChangeToken._new1034(xx1, xx1, DecreeChangeTokenTyp.VALUE)
        res.change_val = DecreeChangeValueReferent._new1044(DecreeChangeValueKind.TEXT)
        t0 = xx1
        if (BracketHelper.is_bracket(xx1, True)): 
            res.change_val.begin_char = xx1.end_char + 1
            t0 = xx1.next0_
        else: 
            res.change_val.begin_char = xx1.begin_char
        doubt1 = None
        clause_last = None
        pstack = dict()
        nls = 0
        last_nums = dict()
        ln = ComplexNumToken.try_parse(xx1.next0_, None, False, False)
        if (ln is not None): 
            last_nums[Utils.ifNotNull(ln.suffix, "")] = ln
        tt = xx1.next0_
        first_pass3890 = True
        while True:
            if first_pass3890: first_pass3890 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            stop = False
            is_doubt = False
            seq_num = -1
            if (not tt.is_newline_after): 
                if (tt == xx1.next0_): 
                    part0 = PartToken.try_attach(tt, None, False, False)
                    if (part0 is not None and len(part0.values) == 1): 
                        pstack[part0.typ] = part0.values[0].value
                        tt = part0.end_token
                        continue
                if (tt.is_char_of(";.") or ((tt.is_value("ИСКЛЮЧИТЬ", None) and word_regime))): 
                    if (DecreeChangeToken._check_end_bracket(tt.previous)): 
                        is_doubt = True
                        if (((isinstance(tt.next0_, TextToken)) and tt.next0_.length_char == 1 and tt.next0_.next0_ is not None) and tt.next0_.next0_.is_char(')')): 
                            stop = True
                        elif ((isinstance(tt.next0_, NumberToken)) and tt.next0_.next0_ is not None and tt.next0_.next0_.is_char_of(").")): 
                            stop = True
                        else: 
                            part0 = PartToken.try_attach(tt.next0_, None, False, False)
                            if (part0 is not None and len(part0.values) == 1): 
                                if (part0.is_newline_after and part0.morph.case_.is_nominative and not tt.next0_.chars.is_all_lower): 
                                    stop = True
                                else: 
                                    tok1 = DecreeChangeToken.M_TERMS.try_parse(part0.end_token.next0_, TerminParseAttr.NO)
                                    if (tok1 is not None): 
                                        stop = True
                        if (tt.is_value("ИСКЛЮЧИТЬ", None)): 
                            tt = tt.previous
                            stop = True
                    else: 
                        continue
                elif ((tt.is_comma_and and BracketHelper.can_be_end_of_sequence(tt.previous, True, None, False) and not xx1.is_newline_before) and nls == 0): 
                    stop = True
                    tt = tt.previous
                elif (BracketHelper.can_be_end_of_sequence(tt, True, None, False) and tt.is_whitespace_after): 
                    num = ComplexNumToken.try_parse(tt.next0_, None, False, False)
                    if (num is not None): 
                        stop = True
                    else: 
                        continue
                else: 
                    continue
            else: 
                if (tt.next0_ is not None and tt.next0_.is_char(chr(0x1E))): 
                    rows = TableHelper.try_parse_rows(tt.next0_, 0, True)
                    if (rows is not None and len(rows) > 1): 
                        tt = rows[len(rows) - 1].end_token.previous
                        continue
                nls += 1
                nnn = ComplexNumToken.try_parse(tt.next0_, None, False, False)
                if (nnn is not None): 
                    if (nnn.get_source_text() == "19."): 
                        pass
                    seq_num = 0
                    nnn0 = None
                    wrapnnn01047 = RefOutArgWrapper(None)
                    inoutres1048 = Utils.tryGetValue(last_nums, Utils.ifNotNull(nnn.suffix, ""), wrapnnn01047)
                    nnn0 = wrapnnn01047.value
                    if (inoutres1048): 
                        cmp = ComplexNumComparer()
                        cmp.process(nnn0, nnn)
                        if (cmp.typ == ComplexNumCompareType.LESS and cmp.delta == 1): 
                            seq_num = 1
                        last_nums[Utils.ifNotNull(nnn.suffix, "")] = nnn
                    else: 
                        last_nums[Utils.ifNotNull(nnn.suffix, "")] = nnn
                    if (tt.is_char_of(".;") and tt.next0_ is not None): 
                        next1 = DecreeChangeToken.try_attach(tt.next0_, None, False, None, False, False)
                        if (next1 is not None): 
                            if (next1.act_kind != DecreeChangeKind.UNDEFINED): 
                                stop = True
                            elif (next1.typ != DecreeChangeTokenTyp.UNDEFINED and next1.parts is not None and seq_num != 1): 
                                stop = True
                            elif (next1.decree is not None and next1.end_token.is_char(':')): 
                                stop = True
                        elif (seq_num != 1): 
                            tt2 = nnn.end_token.next0_
                            if (tt2 is not None and tt2.is_value("В", None) and DecreeToken.is_keyword(tt2.next0_, False) is not None): 
                                stop = True
                if (tt.next0_ is None): 
                    pass
            part = PartToken.try_attach(tt.next0_, None, False, False)
            if ((part is not None and len(part.values) == 1 and tt.is_newline_after) and part.morph.case_.is_nominative and not tt.next0_.chars.is_all_lower): 
                if (tt != tt.next0_ and len(pstack) == 0): 
                    stop = True
                elif (not part.typ in pstack): 
                    pstack[part.typ] = part.values[0].value
                else: 
                    n0 = 0
                    n1 = 0
                    wrapn01049 = RefOutArgWrapper(0)
                    inoutres1050 = Utils.tryParseInt(pstack[part.typ], wrapn01049)
                    wrapn11051 = RefOutArgWrapper(0)
                    inoutres1052 = Utils.tryParseInt(part.values[0].value, wrapn11051)
                    n0 = wrapn01049.value
                    n1 = wrapn11051.value
                    if (inoutres1050 and inoutres1052): 
                        if ((n0 + 1) == n1): 
                            doubt1 = (None)
                    pstack[part.typ] = part.values[0].value
            instr = InstrToken1.parse(tt.next0_, True, None, 0, None, False, 0, False, False)
            if (instr is not None and instr.typ == InstrToken1.Types.APPENDIX): 
                pass
            if (tt.next0_ is None): 
                if (len(pstack) > 0): 
                    stop = True
                elif (DecreeChangeToken._check_end_bracket(tt) or tt.is_char_of(";.")): 
                    stop = True
            elif (instr is not None and len(instr.numbers) > 0 and not stop): 
                if (is_doubt): 
                    stop = True
                elif (abzac_regime and not BracketHelper.is_bracket(xx1, True)): 
                    stop = True
                elif (not tt.is_char_of(":")): 
                    nn = DecreeChangeToken.try_attach(tt.next0_, None, False, None, False, False)
                    if (nn is not None and nn.parts is not None and ((nn.end_token.is_newline_after or nn.act_kind != DecreeChangeKind.UNDEFINED))): 
                        stop = True
            has_next = False
            dc_next = DecreeChangeToken.try_attach(tt.next0_, None, False, None, True, False)
            if (dc_next is None): 
                dc_next = DecreeChangeToken.try_attach(tt.next0_, None, True, None, True, False)
            if (tt.next0_ is None): 
                pass
            elif (tt.next0_.is_value("ПОСЛЕ", None)): 
                pass
            elif (dc_next is not None and ((dc_next.is_start or dc_next.change_val is not None or dc_next.typ == DecreeChangeTokenTyp.UNDEFINED))): 
                has_next = True
            else: 
                is_doubt = True
                pt = PartToken.try_attach(tt.next0_, None, False, False)
                if (pt is not None and pt.typ == PartToken.ItemType.CLAUSE and ((pt.is_newline_after or ((pt.end_token.next0_ is not None and pt.end_token.next0_.is_char('.')))))): 
                    is_doubt = False
                    if (clause_last is not None and instr is not None and NumberingHelper.calc_delta(clause_last, instr, True) == 1): 
                        is_doubt = True
            if (instr is not None and instr.typ == InstrToken1.Types.CLAUSE): 
                clause_last = instr
            if (is_doubt and instr is not None): 
                ttt = tt
                while ttt is not None and ttt.end_char <= instr.end_char: 
                    if (ttt.is_value("УТРАТИТЬ", "ВТРАТИТИ") and ttt.next0_ is not None and ttt.next0_.is_value("СИЛА", "ЧИННІСТЬ")): 
                        is_doubt = False
                        break
                    ttt = ttt.next0_
            if (BracketHelper.is_bracket(tt.next0_, True)): 
                if (tt.next0_.is_newline_after): 
                    tt = tt.next0_
                    stop = True
                elif (tt.next0_.next0_ is not None and tt.next0_.next0_.is_char_of(":.") and tt.next0_.next0_.is_newline_after): 
                    tt = tt.next0_.next0_
                    stop = True
            res.end_token = tt
            tt1 = tt
            hcou = 0
            tt3 = None
            tt3 = tt.next0_
            while tt3 is not None: 
                if (tt3.is_hiphen or tt3.is_char('_')): 
                    hcou += 1
                else: 
                    break
                tt3 = tt3.next0_
            if (hcou > 4): 
                if (tt3 is None): 
                    stop = True
                elif (DecreeToken.is_keyword(tt3, False) is not None): 
                    stop = True
                elif (tt3.get_referent() is not None and ((tt3.get_referent().type_name == "PERSON" or tt3.get_referent().type_name == "PERSONPROPERTY"))): 
                    stop = True
            if (tt1.next0_ is not None and tt1.next0_.is_value("СТАТЬЯ", None) and not tt1.next0_.chars.is_all_lower): 
                pt = PartToken.try_attach(tt1.next0_, None, False, False)
                if (pt is not None and pt.is_newline_after): 
                    chr0_ = DecreeChangeToken.try_attach(pt.end_token.next0_, None, False, None, False, False)
                    if (chr0_ is not None and ((chr0_.typ == DecreeChangeTokenTyp.STARTMULTU or chr0_.typ == DecreeChangeTokenTyp.STARTSINGLE))): 
                        stop = True
            tok = DecreeChangeToken.M_TERMS.try_parse(tt1.next0_, TerminParseAttr.NO)
            if (tok is not None): 
                if (isinstance(tok.termin.tag, DecreeChangeKind)): 
                    stop = True
            else: 
                pass
            if (tt1.next0_ is not None): 
                if (tt1.next0_.get_referent() is not None and ((tt1.next0_.get_referent().type_name == "PERSON" or tt1.next0_.get_referent().type_name == "PERSONPROPERTY"))): 
                    stop = True
            if (tt1.is_char_of(";.") and tt1.is_newline_after and seq_num == 0): 
                if (DecreeChangeToken._check_end_bracket(tt1.previous)): 
                    stop = True
            if (not stop and tt1.is_newline_after): 
                num = ComplexNumToken.try_parse(tt1.next0_, None, False, False)
                if (num is not None and ((num.suffix is not None or ((num.end_token.is_value("В", None) and len(num.nums) > 1))))): 
                    if (((tt1.is_char_of(";.") and BracketHelper.is_bracket(tt1.previous, True))) or ((tt1.previous.is_char_of(";.") and BracketHelper.is_bracket(tt1, True)))): 
                        tt2 = num.end_token.next0_
                        if (tt2 is not None): 
                            if (tt2.is_value("ВНЕСТИ", None) or tt2.is_value("В", None) or tt2.is_value("ДОПОЛНИТЬ", None)): 
                                stop = True
                            else: 
                                pp = PartToken.try_attach(tt2, None, False, False)
                                if (pp is not None and pp.typ != PartToken.ItemType.PREFIX): 
                                    stop = True
                        if (num.end_token.is_value("В", None) and len(num.nums) > 1): 
                            stop = True
                        if (tt1.previous is not None and tt1.previous.previous is not None and tt1.previous.previous.is_char(']')): 
                            stop = True
            if (stop): 
                if (tt1.is_char_of("<>")): 
                    if (tt.next0_ is not None): 
                        tt = tt.next0_
                    continue
                if (tt1.is_char_of(";.") and BracketHelper.is_bracket(tt1.previous, True)): 
                    res.end_token = tt1.previous
                    tt1 = tt.previous.previous
                elif (tt1.is_char_of(";")): 
                    if (tt1.previous.is_char('.')): 
                        tt1 = tt1.previous
                        res.end_token = tt1
                if (BracketHelper.can_be_end_of_sequence(tt1, True, None, False)): 
                    tt1 = tt1.previous
                if (tt1 is None or t0.begin_char > tt1.begin_char): 
                    return None
                res.change_val.value = (MetaToken(t0, tt1)).get_source_text()
                if (tt1.next0_ is None): 
                    res.change_val.end_char = tt1.end_char
                else: 
                    res.change_val.end_char = tt1.next0_.begin_char - 1
                return res
            if (tt.is_char(')')): 
                tt2 = tt.previous
                while tt2 is not None: 
                    if (tt2.is_char('(') and tt2.previous is not None and tt2.previous.end_char > res.begin_char): 
                        tt1 = tt2.previous
                        break
                    elif (tt2.is_newline_after): 
                        break
                    tt2 = tt2.previous
            close_point = False
            if (tt1.is_char_of(";.")): 
                close_point = True
                res.end_token = tt1.previous
                tt1 = res.end_token
            if (tt1.is_char_of(";.")): 
                close_point = True
                res.end_token = tt1.previous
                tt1 = res.end_token
            close_br = False
            if (BracketHelper.is_bracket(tt1, True) and not tt1.is_char_of("]>")): 
                close_br = True
                tt1 = tt1.previous
            elif (DecreeChangeToken._check_end_bracket(tt1)): 
                pass
            elif (tt1.next0_ is None): 
                pass
            elif (has_next and tt1.is_table_control_char): 
                pass
            else: 
                continue
            if (is_doubt): 
                if (tt.is_char_of("<>[]")): 
                    continue
                if (doubt1 is None): 
                    doubt1 = tt1
                if (not close_point or not close_br): 
                    continue
                if (not BracketHelper.can_be_start_of_sequence(t0.previous, True, False)): 
                    continue
                brs = list()
                brs.append(t0.previous)
                ttt = t0
                first_pass3891 = True
                while True:
                    if first_pass3891: first_pass3891 = False
                    else: ttt = ttt.next0_
                    if (not (ttt is not None and ttt.end_char <= tt1.next0_.end_char)): break
                    if (not BracketHelper.is_bracket(ttt, False)): 
                        continue
                    if (len(brs) > 0 and BracketHelper.can_be_end_of_sequence(ttt, False, brs[0], False)): 
                        del brs[0]
                    else: 
                        brs.insert(0, ttt)
                if (len(brs) > 0): 
                    if ((instr is not None and instr.typ == InstrToken1.Types.APPENDIX and close_br) and close_point): 
                        pass
                    else: 
                        continue
            if (tt1.begin_char > xx1.end_char): 
                res.change_val.value = (MetaToken(t0, tt1)).get_source_text()
                if (tt1.next0_ is None): 
                    res.change_val.end_char = tt1.end_char
                else: 
                    res.change_val.end_char = tt1.next0_.begin_char - 1
                return res
            break
        if (doubt1 is not None): 
            res.change_val.value = (MetaToken(t0, doubt1)).get_source_text()
            if (doubt1.next0_ is None): 
                res.change_val.end_char = doubt1.end_char
            else: 
                res.change_val.end_char = doubt1.next0_.begin_char - 1
            res.end_token = doubt1
            if (BracketHelper.is_bracket(doubt1.next0_, True)): 
                res.end_token = doubt1.next0_
            return res
        return None
    
    @staticmethod
    def __try_attach_list(t : 'Token', ignore_newline : bool=False, abzac_regime : bool=False) -> typing.List['DecreeChangeToken']:
        if (t is None): 
            return None
        if (t.is_newline_before and not ignore_newline): 
            return None
        d0 = DecreeChangeToken.try_attach(t, None, False, None, False, abzac_regime)
        if (d0 is None or d0.typ == DecreeChangeTokenTyp.UNDEFINED): 
            cou = 0
            tt2 = t.next0_
            while tt2 is not None and (cou < 20): 
                if (tt2.is_newline_before or MiscHelper.can_be_start_of_sentence(tt2)): 
                    break
                d1 = DecreeChangeToken.try_attach(tt2, None, False, None, False, False)
                if (d1 is not None and d1.typ == DecreeChangeTokenTyp.ACTION and d1.act_kind == DecreeChangeKind.EXPIRE): 
                    d0 = d1
                    break
                tt2 = tt2.next0_; cou += 1
            if (d0 is None): 
                return None
        res = list()
        res.append(d0)
        t = d0.end_token.next0_
        if (d0.indent_regime): 
            abzac_regime = True
        elif (d0.new_parts is not None): 
            abzac_regime = False
        first_pass3892 = True
        while True:
            if first_pass3892: first_pass3892 = False
            else: t = t.next0_
            if (not (t is not None)): break
            d = DecreeChangeToken.try_attach(t, None, False, None, False, abzac_regime)
            if (t.is_newline_before): 
                if ((t.is_value("ПРИЛОЖЕНИЕ", "ДОДАТОК") and t.previous is not None and t.previous.is_char(':')) and t.previous.previous is not None and t.previous.previous.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ")): 
                    pass
                elif (t.previous is not None and ((t.previous.is_char(':') or t.previous.is_value("РЕДАКЦИЯ", "РЕДАКЦІЯ"))) and BracketHelper.can_be_start_of_sequence(t, True, False)): 
                    pass
                elif (d0.act_kind == DecreeChangeKind.EXCHANGE and t.is_value("НА", None)): 
                    pass
                elif ((d is not None and d.typ == DecreeChangeTokenTyp.STARTSINGLE and d.change_val is not None) and t.morph.case_.is_instrumental): 
                    d.typ = DecreeChangeTokenTyp.VALUE
                else: 
                    break
            if (d is None and t.is_char('.') and not t.is_newline_after): 
                if (res[len(res) - 1].change_val is not None): 
                    break
                continue
            if (d is None and t.previous.is_value("НА", None) and BracketHelper.can_be_start_of_sequence(t, True, False)): 
                d = DecreeChangeToken._try_parse_text(t, abzac_regime, False)
            if (d is None): 
                if (t.is_value("НОВЫЙ", "НОВИЙ")): 
                    continue
                if (t.is_value("НА", None)): 
                    continue
                if (t.is_value2("К", "ОН")): 
                    t = t.next0_
                    continue
                if (t.is_char(':') and ((not t.is_newline_after or res[len(res) - 1].act_kind == DecreeChangeKind.NEW))): 
                    continue
                if ((isinstance(t, TextToken)) and t.term == "ТЕКСТОМ"): 
                    continue
                pts = PartToken.try_attach_list(t, False, 40)
                if (pts is not None): 
                    d = DecreeChangeToken._new1034(pts[0].begin_token, pts[len(pts) - 1].end_token, DecreeChangeTokenTyp.UNDEFINED)
                    if (t.previous is not None and t.previous.is_value("НОВЫЙ", "НОВИЙ")): 
                        d.new_parts = pts
                    else: 
                        d.parts = pts
                else: 
                    pt = PartToken.try_attach(t, None, True, False)
                    if (pt is None): 
                        pt = PartToken.try_attach(t, None, True, True)
                    if (pt is not None): 
                        d = DecreeChangeToken(pt.begin_token, pt.end_token)
                        if (t.previous is not None and t.previous.is_value("НОВЫЙ", "НОВИЙ")): 
                            d.new_parts = list()
                            d.new_parts.append(pt)
                        else: 
                            d.part_typ = pt.typ
            if (d is None and res[len(res) - 1].act_kind == DecreeChangeKind.NEW): 
                if (BracketHelper.is_bracket(t, True)): 
                    d = DecreeChangeToken._try_parse_text(t, abzac_regime, False)
                elif (((t.previous.is_char(':') or t.previous.is_value("РЕДАКЦИЯ", None))) and (isinstance(t, NumberToken))): 
                    nn = ComplexNumToken.try_parse(t, None, False, False)
                    if (nn is not None and BracketHelper.can_be_start_of_sequence(nn.end_token.next0_, True, False)): 
                        d = DecreeChangeToken._try_parse_text(nn.end_token.next0_, abzac_regime, False)
                        if (d is not None and d.change_val is not None): 
                            d.begin_token = t
                            d.change_val.value = "{0} {1}".format(nn.get_source_text(), d.change_val.value)
            if (d is None and res[len(res) - 1].act_kind == DecreeChangeKind.EXCHANGE): 
                if (t.is_value("НА", None) and t.next0_ is not None): 
                    t = t.next0_
                if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                    d = DecreeChangeToken._try_parse_text(t, abzac_regime, False)
            if (d is None): 
                break
            if (d.typ == DecreeChangeTokenTyp.SINGLE or d.typ == DecreeChangeTokenTyp.STARTMULTU or d.typ == DecreeChangeTokenTyp.STARTSINGLE): 
                break
            res.append(d)
            t = d.end_token
            if (d.indent_regime): 
                abzac_regime = True
            elif (d.new_parts is not None): 
                abzac_regime = False
        if ((len(res) == 1 and res[0].act_kind == DecreeChangeKind.CONSIDER and res[0].end_token.next0_ is not None) and res[0].end_token.next0_.is_comma_and and res[0].change_val is None): 
            next0__ = DecreeChangeToken.__try_attach_list(res[0].end_token.next0_.next0_, True, abzac_regime)
            if ((next0__ is not None and len(next0__) == 2 and next0__[0].act_kind == DecreeChangeKind.NEW) and next0__[1].typ == DecreeChangeTokenTyp.VALUE): 
                return next0__
        return res
    
    M_TERMS = None
    
    __m_words = None
    
    @staticmethod
    def _initialize() -> None:
        if (DecreeChangeToken.M_TERMS is not None): 
            return
        DecreeChangeToken.M_TERMS = TerminCollection()
        t = None
        t = Termin._new84("ИЗЛОЖИТЬ В СЛЕДУЮЩЕЙ РЕДАКЦИИ", DecreeChangeKind.NEW)
        t.add_variant("ПРИНЯТЬ В СЛЕДУЮЩЕЙ РЕДАКЦИИ", False)
        t.add_variant("ИЗЛОЖИВ ЕГО В СЛЕДУЮЩЕЙ РЕДАКЦИИ", False)
        t.add_variant("ИЗЛОЖИТЬ В РЕДАКЦИИ", False)
        t.add_variant("ИЗЛОЖИТЬ", False)
        t.add_variant("ПРИНЯТЬ", False)
        t.add_variant("ИЗЛОЖИТЬ В НОВОЙ РЕДАКЦИИ", False)
        t.add_variant("ЧИТАТЬ В СЛЕДУЮЩЕЙ РЕДАКЦИИ", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new504("ВИКЛАСТИ В НАСТУПНІЙ РЕДАКЦІЇ", MorphLang.UA, DecreeChangeKind.NEW)
        t.add_variant("ВИКЛАВШИ В ТАКІЙ РЕДАКЦІЇ", False)
        t.add_variant("ВИКЛАВШИ ЙОГО В НАСТУПНІЙ РЕДАКЦІЇ", False)
        t.add_variant("ВИКЛАСТИ В РЕДАКЦІЇ", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new84("ПРИЗНАТЬ УТРАТИВШИМ СИЛУ", DecreeChangeKind.EXPIRE)
        t.add_variant("СЧИТАТЬ УТРАТИВШИМ СИЛУ", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new504("ВИЗНАТИ таким, що ВТРАТИВ ЧИННІСТЬ", MorphLang.UA, DecreeChangeKind.EXPIRE)
        t.add_variant("ВВАЖАТИ таким, що ВТРАТИВ ЧИННІСТЬ", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new84("ИСКЛЮЧИТЬ", DecreeChangeKind.REMOVE)
        t.add_variant("ИСКЛЮЧИВ ИЗ НЕГО", False)
        t.add_variant("УДАЛИТЬ", False)
        t.add_variant("УДАЛИВ ИЗ НЕГО", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new504("ВИКЛЮЧИТИ", MorphLang.UA, DecreeChangeKind.REMOVE)
        t.add_variant("ВИКЛЮЧИВШИ З НЬОГО", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new84("ПРИОСТАНОВИТЬ ДЕЙСТВИЕ", DecreeChangeKind.SUSPEND)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new84("СЧИТАТЬ", DecreeChangeKind.CONSIDER)
        t.add_variant("СЧИТАТЬ СООТВЕТСТВЕННО", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new504("ВВАЖАТИ", MorphLang.UA, DecreeChangeKind.CONSIDER)
        t.add_variant("ВВАЖАТИ ВІДПОВІДНО", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new84("ЗАМЕНИТЬ", DecreeChangeKind.EXCHANGE)
        t.add_variant("ЗАМЕНИВ В НЕМ", False)
        t.add_variant("ИСКЛЮЧИТЬ ЗАМЕНИТЬ", False)
        t.add_variant("ИСКЛЮЧИТЬ И ЗАМЕНИТЬ", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new504("ЗАМІНИТИ", MorphLang.UA, DecreeChangeKind.EXCHANGE)
        t.add_variant("ЗАМІНИВШИ В НЬОМУ", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new84("ДОПОЛНИТЬ", DecreeChangeKind.APPEND)
        t.add_variant("ДОПОЛНИВ ЕГО", False)
        t.add_variant("ДОБАВИТЬ", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new504("ДОПОВНИТИ", MorphLang.UA, DecreeChangeKind.APPEND)
        t.add_variant("ДОПОВНИВШИ ЙОГО", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new84("СЛОВО", DecreeChangeValueKind.WORDS)
        DecreeChangeToken.__m_words = t
        t.add_variant("АББРЕВИАТУРА", False)
        t.add_variant("АБРЕВІАТУРА", False)
        t.add_variant("ЗНАК СНОСКИ", False)
        t.add_variant("ПЕРЕМЕННАЯ", False)
        t.add_variant("МНОЖИТЕЛЬ", False)
        t.add_variant("КОД", False)
        t.add_variant("ТЕКСТ СЛЕДУЮЩЕГО СОДЕРЖАНИЯ", False)
        t.add_variant("ДАТА", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new86("ОПРЕДЕЛЕНИЕ", DecreeChangeValueKind.DEFINITION, ";")
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new86("ТОЧКА С ЗАПЯТОЙ", DecreeChangeValueKind.WORDS, ";")
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new86("ТОЧКА", DecreeChangeValueKind.WORDS, ".")
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new86("ВОПРОСИТЕЛЬНЫЙ ЗНАК", DecreeChangeValueKind.WORDS, "?")
        t.add_variant("ЗНАК ВОПРОСА", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new86("ВОСКЛИЦАТЕЛЬНЫЙ ЗНАК", DecreeChangeValueKind.WORDS, "!")
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new84("ЦИФРА", DecreeChangeValueKind.NUMBERS)
        t.add_variant("ЧИСЛО", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new84("БЛОК", DecreeChangeValueKind.BLOCK)
        t.add_variant("БЛОК СО СЛОВАМИ", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new504("БЛОК", MorphLang.UA, DecreeChangeValueKind.BLOCK)
        t.add_variant("БЛОК ЗІ СЛОВАМИ", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new84("В СООТВЕТСТВУЮЩИХ ЧИСЛЕ И ПАДЕЖЕ", DecreeChangeValueKind.ROBUSTWORDS)
        t.add_variant("В СООТВЕТСТВУЮЩЕМ ПАДЕЖЕ", False)
        t.add_variant("В СООТВЕТСТВУЮЩЕМ ПАДЕЖЕ И ЧИСЛЕ", False)
        t.add_variant("В СООТВЕТСТВУЮЩЕМ ЧИСЛЕ", False)
        DecreeChangeToken.M_TERMS.add(t)
        t = Termin._new504("У ВІДПОВІДНОМУ ЧИСЛІ ТА ВІДМІНКУ", MorphLang.UA, DecreeChangeValueKind.ROBUSTWORDS)
        t.add_variant("У ВІДПОВІДНОМУ ВІДМІНКУ", False)
        t.add_variant("У ВІДПОВІДНОМУ ЧИСЛІ", False)
        DecreeChangeToken.M_TERMS.add(t)
    
    @staticmethod
    def _new1032(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DecreeChangeTokenTyp', _arg4 : bool) -> 'DecreeChangeToken':
        res = DecreeChangeToken(_arg1, _arg2)
        res.typ = _arg3
        res.has_change_keyword = _arg4
        return res
    
    @staticmethod
    def _new1033(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DecreeChangeTokenTyp', _arg4 : 'DecreeChangeKind') -> 'DecreeChangeToken':
        res = DecreeChangeToken(_arg1, _arg2)
        res.typ = _arg3
        res.act_kind = _arg4
        return res
    
    @staticmethod
    def _new1034(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'DecreeChangeTokenTyp') -> 'DecreeChangeToken':
        res = DecreeChangeToken(_arg1, _arg2)
        res.typ = _arg3
        return res