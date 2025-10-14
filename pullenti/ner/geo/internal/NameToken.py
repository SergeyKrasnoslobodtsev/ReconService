# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.BracketSequenceToken import BracketSequenceToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.geo.internal.GeoTokenType import GeoTokenType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.geo.internal.CityItemToken import CityItemToken
from pullenti.ner.geo.internal.NumToken import NumToken
from pullenti.ner.geo.internal.OrgTypToken import OrgTypToken

class NameToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.name = None;
        self.number = None;
        self.pref = None;
        self.misc_typ = None;
        self.is_doubt = False
        self.is_eponym = False
        self.__m_lev = 0
        self.__m_typ = GeoTokenType.ANY
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.is_doubt): 
            print("? ", end="", file=res)
        if (self.pref is not None): 
            print("{0} ".format(self.pref), end="", file=res, flush=True)
        if (self.name is not None): 
            print("\"{0}\"".format(self.name), end="", file=res, flush=True)
        if (self.number is not None): 
            print(" N{0}".format(self.number), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def try_parse(t : 'Token', ty : 'GeoTokenType', lev : int, after_typ : bool=False) -> 'NameToken':
        res = NameToken.__try_parse(t, ty, lev, after_typ)
        if (res is None): 
            return None
        if (res.name is None and res.pref is not None and (res.whitespaces_after_count < 3)): 
            next0__ = NameToken.__try_parse(res.end_token.next0_, ty, lev, True)
            if (next0__ is not None and next0__.pref is None and next0__.name is not None): 
                res.name = next0__.name
                if (res.number is not None): 
                    res.number = next0__.number
                res.end_token = next0__.end_token
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', ty : 'GeoTokenType', lev : int, after_typ : bool) -> 'NameToken':
        if (t is None or lev > 3): 
            return None
        br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
        if (br is None and BracketHelper.is_bracket(t, True) and MiscLocationHelper.is_user_param_address(t)): 
            tt = t.next0_
            first_pass3978 = True
            while True:
                if first_pass3978: first_pass3978 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (not BracketHelper.is_bracket(tt, True)): 
                    if (tt.is_newline_before): 
                        break
                    if (tt.next0_ is None or tt.next0_.is_comma): 
                        if ((tt.end_char - t.begin_char) > 30): 
                            break
                        br = BracketSequenceToken(t, tt)
                        break
                    continue
                if ((tt.end_char - t.begin_char) > 30): 
                    break
                if (BracketHelper.try_parse(tt, BracketParseAttr.NO, 100) is not None): 
                    break
                br = BracketSequenceToken(t, tt)
                break
        res = None
        ttt = None
        num = None
        ttok = None
        if (br is not None): 
            if (not BracketHelper.is_bracket(t, True)): 
                return None
            ait = AddressItemToken.try_parse_pure_item(t.next0_, None, None)
            if (ait is not None and ait.typ != AddressItemType.NUMBER and ait.end_token.next0_ == br.end_token): 
                return None
            nam = NameToken.try_parse(t.next0_, ty, lev + 1, False)
            if (nam is not None and nam.end_token.next0_ == br.end_token): 
                res = nam
                nam.begin_token = t
                nam.end_token = br.end_token
                res.is_doubt = False
            else: 
                res = NameToken(t, br.end_token)
                tt = br.end_token.previous
                if (not BracketHelper.is_bracket(br.end_token, False)): 
                    tt = br.end_token
                tt3 = t.next0_
                while tt3 is not None and tt3.end_char <= tt.end_char: 
                    nn = NumToken.try_parse(tt3, GeoTokenType.ANY)
                    if (nn is not None and nn.end_token == tt): 
                        res.number = nn.value
                        res.misc_typ = nn.misc_type
                        tt = tt3.previous
                        if (tt is not None and tt.is_hiphen): 
                            tt = tt.previous
                        break
                    tt3 = tt3.next0_
                if (tt is not None and tt.begin_char > br.begin_char): 
                    res.name = MiscHelper.get_text_value(t.next0_, tt, GetTextAttr.NO)
        elif ((isinstance(t, ReferentToken)) and t.begin_token == t.end_token and not t.begin_token.chars.is_all_lower): 
            res = NameToken._new1491(t, t, True)
            res.name = MiscHelper.get_text_value_of_meta_token(Utils.asObjectOrNull(t, ReferentToken), GetTextAttr.NO)
        else: 
            ttt = MiscHelper.check_number_prefix(t)
            if (isinstance((ttt), NumberToken)): 
                res = NameToken._new1492(t, ttt, ttt.value)
                nnn = NumToken.try_parse(t, GeoTokenType.ORG)
                if (nnn is not None): 
                    res.number = nnn.value
                    ttt = nnn.end_token
                    res.end_token = ttt
                if (ttt.whitespaces_after_count < 2): 
                    ttt3 = ttt.next0_
                    if (ttt3 is not None and ttt3.is_hiphen): 
                        ttt3 = ttt3.next0_
                    nam = NameToken.try_parse(ttt3, ty, lev + 1, False)
                    if (nam is not None and nam.name is not None and nam.number is None): 
                        res.name = nam.name
                        res.end_token = nam.end_token
            else: 
                num = NumberHelper.try_parse_age(t)
                if ((num) is not None): 
                    res = NameToken._new1493(t, num.end_token, num.value + " ЛЕТ")
                else: 
                    num = NumberHelper.try_parse_anniversary(t)
                    if ((num) is not None): 
                        res = NameToken._new1493(t, num.end_token, num.value + " ЛЕТ")
                    elif (isinstance(t, NumberToken)): 
                        nn = NumberHelper.try_parse_number_with_postfix(t)
                        if (nn is not None and not MiscLocationHelper.is_user_param_address(t)): 
                            if (nn.ex_typ != NumberExType.UNDEFINED): 
                                return None
                        res = NameToken._new1492(t, t, t.value)
                        if ((t.whitespaces_after_count < 3) and after_typ): 
                            next0__ = NameToken.try_parse(t.next0_, ty, lev + 1, after_typ)
                            if (next0__ is not None and next0__.number is None and next0__.name is not None): 
                                next0__.number = res.number
                                next0__.begin_token = res.begin_token
                                res = next0__
                        if (t.next0_ is not None and t.next0_.is_hiphen and not t.next0_.is_whitespace_after): 
                            next0__ = NameToken.try_parse(t.next0_.next0_, ty, lev + 1, after_typ)
                            if (next0__ is not None and next0__.number is None and next0__.name is not None): 
                                next0__.number = res.number
                                next0__.begin_token = res.begin_token
                                res = next0__
                    elif (t.is_hiphen and (isinstance(t.next0_, NumberToken))): 
                        num = NumberHelper.try_parse_age(t.next0_)
                        if (num is None): 
                            num = NumberHelper.try_parse_anniversary(t.next0_)
                        if (num is not None): 
                            res = NameToken._new1493(t, num.end_token, num.value + " ЛЕТ")
                        else: 
                            res = NameToken._new1497(t, t.next0_, t.next0_.value, True)
                    elif ((isinstance(t, ReferentToken)) and t.get_referent().type_name == "DATE"): 
                        year = t.get_referent().get_string_value("YEAR")
                        if (year is not None): 
                            res = NameToken._new1493(t, t, year + " ГОДА")
                        else: 
                            mon = t.get_referent().get_string_value("MONTH")
                            day = t.get_referent().get_string_value("DAY")
                            if (day is not None and mon is None and t.get_referent().parent_referent is not None): 
                                mon = t.get_referent().parent_referent.get_string_value("MONTH")
                            if (mon is not None): 
                                res = NameToken._new1499(t, t, str(t.get_referent()).upper())
                    elif (not (isinstance(t, TextToken))): 
                        return None
                    elif (t.length_char == 1): 
                        if (not t.chars.is_letter): 
                            return None
                        if ((t.get_morph_class_in_dictionary().is_preposition and t.chars.is_all_upper and t.whitespaces_after_count > 0) and (t.whitespaces_after_count < 3) and (isinstance(t.next0_, TextToken))): 
                            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
                            if (npt is not None and npt.end_token != t): 
                                return NameToken._new1500(t, npt.end_token, True, MiscHelper.get_text_value(t, npt.end_token, GetTextAttr.NO))
                        if ((t.chars.is_all_upper and t.next0_ is not None and t.next0_.is_hiphen) and (isinstance(t.next0_.next0_, TextToken))): 
                            return NameToken._new1500(t, t.next0_.next0_, True, MiscHelper.get_text_value(t, t.next0_.next0_, GetTextAttr.NO))
                        if (((t.chars.is_all_upper or after_typ)) and t.next0_ is not None): 
                            te = None
                            if ((isinstance(t.next0_, NumberToken)) and (t.whitespaces_after_count < 2)): 
                                te = t.next0_
                            elif (t.next0_.is_hiphen and (isinstance(t.next0_.next0_, NumberToken))): 
                                te = t.next0_.next0_
                            if (te is not None): 
                                num1 = NumToken.try_parse(te, ty)
                                if (num1 is not None): 
                                    return NameToken._new1492(t, num1.end_token, "{0}{1}".format(num1.value, t.term))
                        ok = False
                        if (t.is_newline_after or t.next0_ is None): 
                            ok = True
                        elif (t.next0_.is_comma): 
                            ok = True
                        elif (t.previous is not None and t.previous.is_value("СЕКТОР", None)): 
                            ok = True
                        if (ty == GeoTokenType.ORG and ok and t.chars.is_letter): 
                            return NameToken._new1499(t, t, t.term)
                        if ((((ty != GeoTokenType.ORG and ty != GeoTokenType.STRONG)) or not t.chars.is_all_upper or not t.chars.is_letter) or t.is_whitespace_after): 
                            return None
                        next0__ = NameToken.try_parse(t.next0_, ty, lev + 1, False)
                        if (next0__ is not None and next0__.number is not None and next0__.name is None): 
                            res = next0__
                            res.begin_token = t
                            res.name = t.term
                        elif (t.next0_ is not None and t.next0_.is_char('.')): 
                            nam = io.StringIO()
                            print(t.term, end="", file=nam)
                            t1 = t.next0_
                            tt = t1.next0_
                            while tt is not None: 
                                if (not (isinstance(tt, TextToken)) or tt.length_char != 1 or not tt.chars.is_letter): 
                                    break
                                if (tt.next0_ is None or not tt.next0_.is_char('.')): 
                                    break
                                print(tt.term, end="", file=nam)
                                tt = tt.next0_
                                t1 = tt
                                tt = tt.next0_
                            if (nam.tell() >= 3): 
                                res = NameToken._new1499(t, t1, Utils.toStringStringIO(nam))
                            else: 
                                rt = t.kit.process_referent("PERSON", t, None)
                                if (rt is not None): 
                                    res = NameToken._new1499(t, rt.end_token, rt.referent.get_string_value("LASTNAME"))
                                    if (res.name is None): 
                                        res.name = rt.referent.to_string_ex(False, None, 0).upper()
                                    else: 
                                        tt = t
                                        while tt is not None and tt.end_char <= rt.end_char: 
                                            if ((isinstance(tt, TextToken)) and tt.is_value(res.name, None)): 
                                                res.name = tt.term
                                                break
                                            tt = tt.next0_
                    elif (t.term == "ИМЕНИ" or t.term == "ИМ"): 
                        tt = t.next0_
                        if (t.is_value("ИМ", None) and tt is not None and tt.is_char('.')): 
                            tt = tt.next0_
                        nam = NameToken.try_parse(tt, GeoTokenType.STRONG, lev + 1, False)
                        if (nam is not None): 
                            nam.begin_token = t
                            nam.is_doubt = False
                            nam.is_eponym = True
                            res = nam
                        else: 
                            si = StreetItemToken.try_parse(tt, None, False, None)
                            if (si is not None): 
                                res = NameToken._new1506(t, si.end_token, False, True, si.value)
                    else: 
                        ttok = NameToken.M_ONTO.try_parse(t, TerminParseAttr.NO)
                        if ((ttok) is not None): 
                            res = NameToken._new1499(t, ttok.end_token, ttok.termin.canonic_text)
                            tt = ttok.end_token.next0_
                            if (tt is not None and tt.is_value("СССР", None)): 
                                res.end_token = tt
                        elif (t.is_value("ОТДЕЛЕНИЕ", None)): 
                            res = NameToken.try_parse(t.next0_, ty, lev + 1, after_typ)
                            if (res is not None): 
                                res.misc_typ = "отделение"
                                res.begin_token = t
                        else: 
                            if (t.morph.contains_attr("к.ф.", None)): 
                                ptok = NameToken.M_PREF_ONTO.try_parse(t, TerminParseAttr.NO)
                                if (ptok is not None): 
                                    tt = ptok.end_token.next0_
                                    if (tt is not None and tt.is_hiphen): 
                                        tt = tt.next0_
                                    next0__ = NameToken.try_parse(tt, ty, lev + 1, False)
                                    if (next0__ is not None and next0__.name is not None): 
                                        next0__.name = "{0}{1}".format(ptok.termin.canonic_text, next0__.name)
                                        next0__.begin_token = t
                                        return next0__
                            if ((t.morph.class0_.is_proper_surname or t.get_morph_class_in_dictionary().is_proper_name)): 
                                rt = t.kit.process_referent("PERSON", t, None)
                                if (rt is not None): 
                                    res = NameToken(t, rt.end_token)
                                    sur = rt.referent.get_string_value("LASTNAME")
                                    if (sur is not None): 
                                        tt = t
                                        while tt is not None and tt.end_char <= rt.end_char: 
                                            if ((isinstance(tt, TextToken)) and tt.is_value(sur, None)): 
                                                res.name = tt.term
                                            elif (ty == GeoTokenType.CITY and res.name is not None): 
                                                cit = CityItemToken.check_keyword(tt)
                                                if (cit is not None): 
                                                    res = (None)
                                                    break
                                            tt = tt.next0_
                                    if (res is not None and res.name is None): 
                                        res.name = MiscHelper.get_text_value_of_meta_token(rt, GetTextAttr.NO)
                            if (res is None): 
                                npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
                                if (npt is not None and npt.end_token.is_value("КВАРТАЛ", None)): 
                                    if (npt.begin_token == npt.end_token or npt.begin_token.is_value("КАДАСТРОВЫЙ", None)): 
                                        num2 = NumToken.try_parse(npt.end_token.next0_, ty)
                                        if (num2 is not None and num2.is_cadaster_number): 
                                            res = NameToken._new1492(t, num2.end_token, num2.value)
                                            res.misc_typ = "кадастровый квартал"
                                            if ((res.whitespaces_after_count < 2) and not BracketHelper.is_bracket(res.end_token.next0_, False)): 
                                                if (res.end_token.next0_.is_value("ЛЕСНОЙ", None)): 
                                                    res.end_token = res.end_token.next0_
                                                    res.name = "ЛЕСНОЙ"
                                            return res
                                if (npt is not None and npt.begin_token == npt.end_token): 
                                    npt = (None)
                                if (npt is not None): 
                                    ttt2 = OrgTypToken.try_parse(npt.end_token, False, None)
                                    if (ttt2 is not None and ttt2.end_char > npt.end_char): 
                                        npt = (None)
                                    elif (ttt2 is not None and not after_typ and not npt.morph.case_.is_genitive): 
                                        npt = (None)
                                    elif (len(npt.adjectives) > 1 and OrgTypToken.try_parse(npt.end_token.previous, False, None) is not None): 
                                        npt = (None)
                                if (npt is not None and npt.end_token.chars.is_all_lower): 
                                    if (t.chars.is_all_lower): 
                                        npt = (None)
                                    elif (StreetItemToken.check_keyword(npt.end_token)): 
                                        if (npt.morph.number == MorphNumber.PLURAL): 
                                            pass
                                        elif (npt.end_token.is_value("САД", None) or npt.end_token.is_value("ПАРК", None)): 
                                            pass
                                        else: 
                                            npt = (None)
                                if (npt is not None): 
                                    res = NameToken._new1509(t, npt.end_token, npt.morph, MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO).replace("-", " "))
                                elif (not t.chars.is_all_lower or t.is_value("МЕСТНОСТЬ", None) or ((after_typ and MiscLocationHelper.is_user_param_address(t)))): 
                                    if (TerrItemToken.check_keyword(t) is not None): 
                                        if (t.chars.is_capital_upper and after_typ): 
                                            pass
                                        else: 
                                            return None
                                    sit = StreetItemToken.try_parse(t, None, False, None)
                                    if (sit is not None and sit.typ == StreetItemType.NOUN): 
                                        if (sit.end_token.is_char('.')): 
                                            return None
                                        if (sit.termin.canonic_text == "УЛИЦА"): 
                                            return None
                                    if (t.is_value("ФИЛИАЛ", None)): 
                                        return None
                                    ait = AddressItemToken.try_parse_pure_item(t, None, None)
                                    if ((ait is not None and ait.typ != AddressItemType.NUMBER and ait.value is not None) and ait.value != "0"): 
                                        return None
                                    res = NameToken._new1510(t, t, t.term, t.morph)
                                    if (t.chars.is_all_lower): 
                                        res.is_doubt = True
                                    if ((((LanguageHelper.ends_with(res.name, "ОВ") or LanguageHelper.ends_with(res.name, "ВО"))) and (isinstance(t.next0_, TextToken)) and not t.next0_.chars.is_all_lower) and t.next0_.length_char > 1 and not t.next0_.get_morph_class_in_dictionary().is_undefined): 
                                        if (StreetItemToken.check_keyword(t.next0_)): 
                                            pass
                                        elif (OrgTypToken.try_parse(t.next0_, False, None) is not None): 
                                            pass
                                        else: 
                                            res.end_token = t.next0_
                                            res.name = "{0} {1}".format(res.name, t.next0_.term)
                                            res.morph = t.next0_.morph
                                    if (((t.whitespaces_after_count < 2) and (isinstance(t.next0_, TextToken)) and t.next0_.chars.is_letter) and t.next0_.length_char > 1): 
                                        ok = False
                                        if (MiscLocationHelper.check_territory(t.next0_) is not None): 
                                            pass
                                        elif (t.next0_.length_char >= 3 and t.next0_.get_morph_class_in_dictionary().is_undefined): 
                                            ok = True
                                        elif (MiscLocationHelper.check_name_long(res) is not None): 
                                            ok = True
                                        elif (MiscLocationHelper.check_territory(t.next0_) is not None): 
                                            pass
                                        elif (StreetItemToken.check_keyword(t.next0_)): 
                                            pass
                                        else: 
                                            ok1 = False
                                            if ((((t.next0_.length_char < 4) or t.get_morph_class_in_dictionary().is_undefined)) and t.next0_.chars.equals(t.chars)): 
                                                ok1 = True
                                            elif (t.is_value("МЕСТНОСТЬ", None) and not t.next0_.chars.is_all_lower): 
                                                ok = True
                                            elif (not t.next0_.chars.is_all_lower or not AddressItemToken.check_house_after(t.next0_, False, False)): 
                                                if (MiscLocationHelper.check_territory(t.next0_) is None): 
                                                    if (t.next0_.is_newline_after or t.next0_.next0_.is_comma or AddressItemToken.check_house_after(t.next0_.next0_, False, False)): 
                                                        ok = True
                                                if (not ok and t.next0_.next0_ is not None): 
                                                    typ = OrgTypToken.try_parse(t.next0_.next0_, False, None)
                                                    if (typ is not None and typ.not_org): 
                                                        ok = True
                                                    elif (t.next0_.next0_.is_value("МАССИВ", None)): 
                                                        ok = True
                                            if (ok1): 
                                                next0__ = NameToken.try_parse(t.next0_, ty, lev + 1, False)
                                                if (next0__ is None or next0__.begin_token == next0__.end_token): 
                                                    ok = True
                                        if (not ok and t.next0_.get_morph_class_in_dictionary().is_adjective): 
                                            mc = t.get_morph_class_in_dictionary()
                                            if (mc.is_noun or mc.is_proper_geo): 
                                                if (((t.morph.gender) & (t.next0_.morph.gender)) != (MorphGender.UNDEFINED)): 
                                                    tt = t.next0_.next0_
                                                    if (tt is None): 
                                                        ok = True
                                                    elif (tt.is_comma or tt.is_newline_after): 
                                                        ok = True
                                                    elif (AddressItemToken.check_house_after(tt, False, False)): 
                                                        ok = True
                                                    elif (AddressItemToken.check_street_after(tt, False)): 
                                                        ok = True
                                        if (ok): 
                                            if (OrgTypToken.try_parse(t.next0_, False, None) is not None): 
                                                ok = False
                                        if (ok): 
                                            tt = MiscLocationHelper.check_name_long(res)
                                            if (tt is None): 
                                                tt = t.next0_
                                            if (t.previous is not None and t.previous.is_value("УРОЧИЩЕ", None)): 
                                                tt2 = tt.next0_
                                                while tt2 is not None: 
                                                    if (not (isinstance(tt2, TextToken)) or tt2.whitespaces_before_count > 3 or tt2.length_char == 1): 
                                                        break
                                                    ait = AddressItemToken.try_parse_pure_item(tt2, None, None)
                                                    if (ait is not None): 
                                                        break
                                                    tt = tt2
                                                    tt2 = tt2.next0_
                                            res.name = "{0} {1}".format(res.name, MiscHelper.get_text_value(res.end_token.next0_, tt, GetTextAttr.NO))
                                            res.end_token = tt
                                        elif (t.next0_ is not None and not t.next0_.is_value("СХ", None) and not t.next0_.is_value("CX", None)): 
                                            lat = NumberHelper.try_parse_roman(t.next0_)
                                            if (lat is not None and lat.typ == NumberSpellingType.ROMAN): 
                                                res.number = lat.value
                                                res.end_token = lat.end_token
                                if (res is not None and res.end_token.is_value("УСАДЬБА", None) and (res.whitespaces_after_count < 2)): 
                                    res1 = NameToken.try_parse(res.end_token.next0_, ty, lev + 1, False)
                                    if (res1 is not None and res1.name is not None): 
                                        res.end_token = res1.end_token
                                        res.name = "{0} {1}".format(res.name, res1.name)
        if (res is None or res.whitespaces_after_count > 2): 
            return res
        ttt = res.end_token.next0_
        if (ttt is not None and ttt.is_hiphen): 
            num = NumberHelper.try_parse_age(ttt.next0_)
            if (num is None): 
                num = NumberHelper.try_parse_anniversary(ttt.next0_)
            if (num is not None): 
                res.pref = (num.value + " ЛЕТ")
                res.end_token = num.end_token
            elif ((isinstance(ttt.next0_, NumberToken)) and res.number is None): 
                nnn = NumToken.try_parse(ttt.next0_, ty)
                if (nnn is not None): 
                    res.number = nnn.value
                    res.end_token = nnn.end_token
            elif (res.number is None): 
                nt = NumberHelper.try_parse_roman(ttt.next0_)
                if (nt is not None): 
                    res.number = nt.value
                    res.end_token = nt.end_token
            if ((ttt == res.end_token.next0_ and (isinstance(ttt.next0_, TextToken)) and not ttt.is_whitespace_after) and res.name is not None): 
                res.name = "{0} {1}".format(res.name, ttt.next0_.term)
                res.end_token = ttt.next0_
        else: 
            num = NumberHelper.try_parse_age(ttt)
            if ((num) is not None): 
                res.pref = (num.value + " ЛЕТ")
                res.end_token = num.end_token
            else: 
                num = NumberHelper.try_parse_anniversary(ttt)
                if ((num) is not None): 
                    res.pref = (num.value + " ЛЕТ")
                    res.end_token = num.end_token
                elif ((isinstance(ttt, NumberToken)) and res.number is None): 
                    ok = False
                    if (ty == GeoTokenType.ORG and (ttt.whitespaces_before_count < 2)): 
                        ok = True
                    if (ok): 
                        if (StreetItemToken.check_keyword(ttt.next0_)): 
                            ok = False
                        elif (ttt.next0_ is not None): 
                            if (ttt.next0_.is_value("КМ", None) or ttt.next0_.is_value("КИЛОМЕТР", None)): 
                                ok = False
                    if (ok): 
                        nnn = NumToken.try_parse(ttt, GeoTokenType.ANY)
                        if (nnn is not None): 
                            res.number = nnn.value
                            res.misc_typ = nnn.misc_type
                            res.end_token = nnn.end_token
        if (res.number is None and res.end_token.next0_ is not None): 
            nnn = NumToken.try_parse(res.end_token.next0_, ty)
            if (nnn is not None and nnn.has_prefix): 
                res.number = nnn.value
                res.misc_typ = nnn.misc_type
                res.end_token = nnn.end_token
            elif (nnn is None and res.end_token.next0_.is_comma and (res.end_token.next0_.whitespaces_after_count < 3)): 
                nnn = NumToken.try_parse(res.end_token.next0_.next0_, ty)
                if (nnn is not None and nnn.has_spec_word): 
                    res.number = nnn.value
                    res.misc_typ = nnn.misc_type
                    res.end_token = nnn.end_token
        if ((res.whitespaces_after_count < 3) and res.name is None and BracketHelper.can_be_start_of_sequence(res.end_token.next0_, False, False)): 
            nam = NameToken.try_parse(res.end_token.next0_, ty, lev + 1, False)
            if (nam is not None): 
                res.name = nam.name
                res.end_token = nam.end_token
                res.is_doubt = False
        if (res.pref is not None and res.name is None and res.number is None): 
            nam = NameToken.try_parse(res.end_token.next0_, ty, lev + 1, False)
            if (nam is not None and nam.name is not None and nam.pref is None): 
                res.name = nam.name
                res.number = nam.number
                res.misc_typ = nam.misc_typ
                res.end_token = nam.end_token
        res.__m_lev = lev
        res.__m_typ = ty
        if (res.whitespaces_after_count < 3): 
            nn = NameToken.M_ONTO.try_parse(res.end_token.next0_, TerminParseAttr.NO)
            if (nn is not None): 
                res.end_token = nn.end_token
                res.name = "{0} {1}".format(res.name, MiscHelper.get_text_value_of_meta_token(nn, GetTextAttr.NO))
        if (res.name is not None and res.begin_token == res.end_token): 
            end = MiscLocationHelper.check_name_long(res)
            if (end is not None): 
                if (OrgTypToken.try_parse(res.end_token.next0_, False, None) is None): 
                    res.end_token = end
                    res.name = "{0} {1}".format(res.name, MiscHelper.get_text_value(res.begin_token.next0_, end, GetTextAttr.NO))
        res.try_attach_number()
        if ((not res.end_token.is_whitespace_after and res.end_token.next0_.is_hiphen and not res.end_token.next0_.is_whitespace_after) and res.number is not None and res.name is not None): 
            nam2 = NameToken.__try_parse(res.end_token.next0_.next0_, ty, lev + 1, after_typ)
            if (nam2 is not None and nam2.name is not None and nam2.number is None): 
                res.name = "{0} {1}".format(res.name, nam2.name)
                res.end_token = nam2.end_token
        return res
    
    @staticmethod
    def check_initial(t : 'Token') -> 'Token':
        if (not (isinstance(t, TextToken)) or t.length_char > 2 or not t.chars.is_letter): 
            return None
        term = t.term
        t1 = t.next0_
        if (t1 is not None and ((t1.is_char_of(".,") or t1.is_hiphen))): 
            t1 = t1.next0_
        elif (t.chars.is_all_lower): 
            return None
        if (((isinstance(t1, TextToken)) and t1.length_char == 1 and t1.next0_ is not None) and t1.next0_.is_char('.')): 
            t1 = t1.next0_.next0_
        if (t1 is None): 
            return None
        if (NameToken.check_initial_and_surname(term, t1)): 
            return t1
        return None
    
    @staticmethod
    def check_initial_back(t : 'Token') -> bool:
        if (not (isinstance(t, TextToken)) or t.whitespaces_before_count > 2): 
            return False
        if (t.length_char > 2 or not t.chars.is_letter): 
            return False
        if (t.next0_ is not None and t.next0_.is_char('.')): 
            pass
        elif (not t.chars.is_all_upper): 
            return False
        return NameToken.check_initial_and_surname(t.term, t.previous)
    
    @staticmethod
    def check_initial_and_surname(ini : str, sur : 'Token') -> bool:
        if (sur is None or sur is None): 
            return False
        if (ini == "А"): 
            if ((((((((sur.is_value("МАТРОСОВ", None) or sur.is_value("ПУШКИН", None) or sur.is_value("УЛЬЯНОВ", None)) or sur.is_value("СУВОРОВ", None) or sur.is_value("АХМАТОВА", None)) or sur.is_value("КАДЫРОВ", None) or sur.is_value("АБУБАКАРОВ", None)) or sur.is_value("АЛИША", None) or sur.is_value("БЛОК", None)) or sur.is_value("ГАЙДАР", None) or sur.is_value("НЕВСКИЙ", None)) or sur.is_value("НЕВСКИЙ", None) or sur.is_value("СУЛТАН", None)) or sur.is_value("ТОЛСТОЙ", None) or sur.is_value("ШЕРИПОВ", None)) or sur.is_value("ГРИН", None)): 
                return True
        if (ini == "Б"): 
            if (sur.is_value("ХМЕЛЬНИЦКИЙ", None) or sur.is_value("БИКБАЙ", None) or sur.is_value("АКУГИНОВ", None)): 
                return True
        if (ini == "В" or ini == "B"): 
            if (((((((sur.is_value("ЛЕНИН", None) or sur.is_value("ТЕРЕШКОВА", None) or sur.is_value("УЛЬЯНОВ", None)) or sur.is_value("ВЫСОЦКИЙ", None) or sur.is_value("ПАСТЕРНАК", None)) or sur.is_value("ЧАПАЕВ", None) or sur.is_value("ЧКАЛОВ", None)) or sur.is_value("ЭМИРОВ", None) or sur.is_value("ШУКШИН", None)) or sur.is_value("ГЮГО", None) or sur.is_value("МАЯКОВСКИЙ", None)) or sur.is_value("ГРИБ", None) or sur.is_value("КОРОБКОВ", None)) or sur.is_value("ГРОШЕВ", None)): 
                return True
        if (ini == "Г"): 
            if (((sur.is_value("ЖУКОВ", None) or sur.is_value("ИБРАГИМОВ", None) or sur.is_value("ТУКАЙ", None)) or sur.is_value("ЦАДАС", None) or sur.is_value("ТИТОВ", None)) or sur.is_value("УСПЕНСКИЙ", None) or sur.is_value("ГАМИДОВ", None)): 
                return True
        if (ini == "Д"): 
            if (sur.is_value("УЛЬЯНОВ", None) or sur.is_value("ДОНСКОЙ", None)): 
                return True
        if (ini == "Е"): 
            if (sur.is_value("ПУГАЧЕВ", None) or sur.is_value("ЭМИН", None) or sur.is_value("КОТИН", None)): 
                return True
        if (ini == "З"): 
            if (sur.is_value("КОСМОДЕМЬЯНСКАЯ", None)): 
                return True
        if (ini == "И"): 
            if (((sur.is_value("ФРАНКО", None) or sur.is_value("ШАМИЛЬ", None) or sur.is_value("АЙВАЗОВСКИЙ", None)) or sur.is_value("ТУРГЕНЕВ", None) or sur.is_value("АРМАНД", None)) or sur.is_value("КАЗАК", None)): 
                return True
        if (ini == "К"): 
            if (sur.is_value("МАРКС", None) or sur.is_value("ЛИБКНЕХТ", None) or sur.is_value("ЦЕТКИН", None)): 
                return True
        if (ini == "Л"): 
            if ((sur.is_value("ТОЛСТОЙ", None) or sur.is_value("ЧАЙКИНА", None) or sur.is_value("ШЕВЦОВА", None)) or sur.is_value("УКРАИНКА", None)): 
                return True
        if (ini == "М" or ini == "M"): 
            if (((((((((((sur.is_value("ГОРЬКИЙ", None) or sur.is_value("АЛИЕВ", None) or sur.is_value("БУЛГАКОВ", None)) or sur.is_value("ДЖАЛИЛЬ", None) or sur.is_value("КАРИМ", None)) or sur.is_value("КУТУЗОВ", None) or sur.is_value("ЛЕРМОНТОВ", None)) or sur.is_value("ЦВЕТАЕВА", None) or sur.is_value("ГАДЖИЕВ", None)) or sur.is_value("ЯРАГСКИЙ", None) or sur.is_value("ГАФУРИ", None)) or sur.is_value("РАСКОВА", None) or sur.is_value("УЛЬЯНОВА", None)) or sur.is_value("ЛОМОНОСОВА", None) or sur.is_value("ФРУНЗЕ", None)) or sur.is_value("ШОЛОХОВА", None) or sur.is_value("ТОРЕЗ", None)) or sur.is_value("ЖУКОВ", None) or sur.is_value("РОКОССОВСКИЙ", None)) or sur.is_value("ВАСИЛЕВСКИЙ", None) or sur.is_value("ТИМОШЕНКО", None)) or sur.is_value("УМАРОВ", None)): 
                return True
        if (ini == "Н"): 
            if ((sur.is_value("ГОГОЛЬ", None) or sur.is_value("КРУПСКАЯ", None) or sur.is_value("ОСТРОВСКИЙ", None)) or sur.is_value("САМУРСКИЙ", None) or sur.is_value("ХАКИМ", None)): 
                return True
        if (ini == "О"): 
            if (sur.is_value("КОШЕВОЙ", None) or sur.is_value("ДУНДИЧ", None) or sur.is_value("ШМИДТ", None)): 
                return True
        if (ini == "П"): 
            if (isinstance(sur, TextToken)): 
                if (sur.term == "САВЕЛЬЕВОЙ"): 
                    return True
            if ((sur.is_value("МОРОЗОВ", None) or sur.is_value("КОРЧАГИН", None) or sur.is_value("ОСИПЕНКО", None)) or sur.is_value("ЛУМУМБА", None) or sur.is_value("ГАМЗАТОВ", None)): 
                return True
        if (ini == "Р"): 
            if ((sur.is_value("ЛЮКСЕМБУРГ", None) or sur.is_value("КАДЫРОВ", None) or sur.is_value("ЗОРГЕ", None)) or sur.is_value("АЛИМХАНОВ", None) or sur.is_value("АРСАМУРЗАЕВ", None)): 
                return True
        if ((ini == "СТ" or ini == "CT" or ini == "С") or ini == "C"): 
            if ((((((sur.is_value("РАЗИН", None) or sur.is_value("ХАЛТУРИН", None) or sur.is_value("ЕСЕНИН", None)) or sur.is_value("ЛАЗО", None) or sur.is_value("КИРОВ", None)) or sur.is_value("ОРДЖОНИКИДЗЕ", None) or sur.is_value("ПЕТРОВСКАЯ", None)) or sur.is_value("ЮЛАЕВ", None) or sur.is_value("РАДОНЕЖСКИЙ", None)) or sur.is_value("ПЕТРОВСКАЯ", None) or sur.is_value("КОВАЛЕВСКАЯ", None)) or sur.is_value("КУДАШ", None) or sur.is_value("ЛИСИН", None)): 
                return True
        if (ini == "Т"): 
            if (sur.is_value("ШЕВЧЕНКО", None) or sur.is_value("ХАХЛЫНОВА", None) or sur.is_value("ФРУНЗЕ", None)): 
                return True
        if (ini == "У"): 
            if (sur.is_value("ГРОМОВА", None) or sur.is_value("АЛИЕВ", None) or sur.is_value("БУЙНАКСКИЙ", None)): 
                return True
        if (ini == "Ф"): 
            if (sur.is_value("АМИРХАН", None) or sur.is_value("КАРИМ", None)): 
                return True
        if (ini == "Х" or ini == "X"): 
            if (sur.is_value("АХМЕТОВ", None) or sur.is_value("ТАКТАШ", None) or sur.is_value("ДАВЛЕТШИНА", None)): 
                return True
        if (ini == "Ч"): 
            if (sur.is_value("АЙТМАТОВ", None)): 
                return True
        if (ini == "Ш"): 
            if ((((sur.is_value("УСМАНОВ", None) or sur.is_value("БАБИЧ", None) or sur.is_value("РУСТАВЕЛИ", None)) or sur.is_value("АЛИЕВ", None) or sur.is_value("ХУДАЙБЕРДИН", None)) or sur.is_value("БАБИЧ", None) or sur.is_value("ЕШУГАОВА", None)) or sur.is_value("КАМАЛ", None)): 
                return True
        if (ini == "Ю"): 
            if (sur.is_value("ГАГАРИН", None) or sur.is_value("АКАЕВ", None) or sur.is_value("ФУЧИК", None)): 
                return True
        return False
    
    def try_attach_number(self) -> None:
        if (self.whitespaces_after_count > 1): 
            return
        if (self.number is None and self.end_token.next0_ is not None and self.__m_lev == 0): 
            tt = self.end_token.next0_
            pref_ = False
            if (tt.is_value("БРИГАДА", None) or tt.is_value("ОТДЕЛЕНИЕ", None) or tt.is_value("ОЧЕРЕДЬ", None)): 
                self.misc_typ = tt.get_normal_case_text(MorphClass.NOUN, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False).lower()
                tt = tt.next0_
            elif (tt.is_value("ОТД", None)): 
                self.misc_typ = "отделение"
                tt = tt.next0_
                if (tt is not None and tt.is_char('.')): 
                    tt = tt.next0_
            nam2 = NameToken.try_parse(tt, self.__m_typ, self.__m_lev + 1, False)
            if ((nam2 is not None and nam2.number is not None and nam2.name is None) and nam2.pref is None): 
                if (tt == self.end_token.next0_ and StreetItemToken.check_keyword(nam2.end_token.next0_)): 
                    pass
                else: 
                    self.number = nam2.number
                    self.end_token = nam2.end_token
            elif (nam2 is not None and nam2.is_eponym): 
                self.end_token = nam2.end_token
                if (self.name is None): 
                    self.name = nam2.name
                else: 
                    self.name = "{0} {1}".format(self.name, nam2.name)
                if (nam2.number is not None): 
                    self.number = nam2.number
        if ((self.__m_typ == GeoTokenType.ORG and (isinstance(self.end_token, NumberToken)) and self.number == self.end_token.value) and not self.is_whitespace_after): 
            tmp = Utils.newStringIO(self.number)
            delim = None
            tt = self.end_token.next0_
            first_pass3979 = True
            while True:
                if first_pass3979: first_pass3979 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_whitespace_before): 
                    break
                if (tt.is_char_of(",.") or tt.is_table_control_char): 
                    break
                if (tt.is_char_of("\\/")): 
                    delim = "/"
                    continue
                elif (tt.is_hiphen): 
                    delim = "-"
                    continue
                if ((isinstance(tt, NumberToken)) and tt.typ == NumberSpellingType.DIGIT): 
                    if (delim is not None): 
                        print(delim, end="", file=tmp)
                    delim = (None)
                    print(tt.value, end="", file=tmp)
                    self.end_token = tt
                    continue
                if ((isinstance(tt, TextToken)) and tt.length_char == 1 and tt.chars.is_letter): 
                    if (delim is not None and str.isalpha(Utils.getCharAtStringIO(tmp, tmp.tell() - 1))): 
                        print(delim, end="", file=tmp)
                    delim = (None)
                    print(tt.term, end="", file=tmp)
                    self.end_token = tt
                    continue
                break
            self.number = Utils.toStringStringIO(tmp)
        if ((self.__m_typ == GeoTokenType.ORG and (isinstance(self.end_token, NumberToken)) and self.end_token.next0_ is not None) and self.number == self.end_token.value and (self.whitespaces_after_count < 3)): 
            t1 = self.end_token.next0_
            if (t1.is_value("БРИГАДА", None) or t1.is_value("ОЧЕРЕДЬ", None) or t1.is_value("ОТДЕЛЕНИЕ", None)): 
                if (isinstance(t1.next0_, NumberToken)): 
                    return
                if (MiscHelper.check_number_prefix(t1.next0_) is not None): 
                    return
                self.end_token = t1
        if (self.number is not None and (isinstance(self.end_token, NumberToken))): 
            tt = self.end_token.next0_
            if (((isinstance(tt, TextToken)) and tt.chars.is_letter and tt.length_char == 1) and (tt.whitespaces_before_count < 3)): 
                ok = False
                if (not tt.is_whitespace_before): 
                    ok = True
                elif (tt.is_newline_after): 
                    ok = True
                elif (tt.next0_.is_comma): 
                    ok = True
                if (ok): 
                    ch = tt.term[0]
                    ch1 = LanguageHelper.get_cyr_for_lat(ch)
                    if ((ord(ch1)) != 0): 
                        ch = ch1
                    self.number = "{0}{1}".format(self.number, ch)
                    self.end_token = tt
    
    M_ONTO = None
    
    M_PREF_ONTO = None
    
    _standard_names = None
    
    @staticmethod
    def initialize() -> None:
        NameToken.M_ONTO = TerminCollection()
        NameToken.M_PREF_ONTO = TerminCollection()
        t = Termin._new1166("МИНИСТЕРСТВО ОБОРОНЫ", "МО")
        NameToken.M_ONTO.add(t)
        for s in NameToken._standard_names: 
            pp = Utils.splitString(s, ';', False)
            t = Termin._new1456(pp[0], True)
            kk = 1
            while kk < len(pp): 
                if (pp[kk].find('.') > 0 or pp[kk].find('/') > 0): 
                    t.add_abridge(pp[kk].replace('.', ' '))
                elif (t.acronym is None and (len(pp[kk]) < 4)): 
                    t.acronym = pp[kk]
                else: 
                    t.add_variant(pp[kk], False)
                kk += 1
            NameToken.M_ONTO.add(t)
        for s in ["СТАРО", "НОВО", "НИЖНЕ", "ВЕРХНЕ", "СРЕДНЕ", "СЕВЕРО", "ЮГО", "ЮЖНО", "ВОСТОЧНО", "ЗАПАДНО", "КРАСНО", "БЕЛО", "ВЕЛИКО", "МАЛО"]: 
            NameToken.M_PREF_ONTO.add(Termin(s))
    
    @staticmethod
    def _new1491(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.is_doubt = _arg3
        return res
    
    @staticmethod
    def _new1492(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.number = _arg3
        return res
    
    @staticmethod
    def _new1493(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.pref = _arg3
        return res
    
    @staticmethod
    def _new1497(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : bool) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.number = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1499(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.name = _arg3
        return res
    
    @staticmethod
    def _new1500(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool, _arg4 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.is_doubt = _arg3
        res.name = _arg4
        return res
    
    @staticmethod
    def _new1506(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool, _arg4 : bool, _arg5 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.is_doubt = _arg3
        res.is_eponym = _arg4
        res.name = _arg5
        return res
    
    @staticmethod
    def _new1509(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : str) -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.morph = _arg3
        res.name = _arg4
        return res
    
    @staticmethod
    def _new1510(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'MorphCollection') -> 'NameToken':
        res = NameToken(_arg1, _arg2)
        res.name = _arg3
        res.morph = _arg4
        return res
    
    # static constructor for class NameToken
    @staticmethod
    def _static_ctor():
        NameToken._standard_names = ["БЕЗ НАЗВАНИЯ;БЕЗ НАИМЕНОВАНИЯ;БЕЗ ИМЕНИ;Б/Н", "ЭНГЕЛЬСА;ФРИДРИХА ЭНГЕЛЬСА;ФРИД.ЭНГЕЛЬСА;ФР.ЭНГЕЛЬСА;Ф.ЭНГЕЛЬСА", "МАРКСА;КАРЛА МАРКСА;К.МАРКСА", "ЛИБКНЕХТА;КАРЛА ЛИБКНЕХТА;К.ЛИБКНЕХТА", "ЛЮКСЕМБУРГ;РОЗЫ ЛЮКСЕМБУРГ;Р.ЛЮКСЕМБУРГ", "УЧАСТНИКОВ ВОВ;УЧАСТНИКОВ ВЕЛИКОЙ ОТЕЧЕСТВЕННОЙ ВОЙНЫ", "ТРУД И ОТДЫХ", "СЪЕЗДА КПСС;ПАРТСЪЕЗДА КПСС", "МОЛОДОЙ ГВАРДИИ;М.ГВАРДИИ;МОЛ.ГВАРДИИ", "ЛЕНИНСКОГО КОМСОМОЛА;Л.КОМСОМОЛА;ЛЕН.КОМСОМОЛА", "ЮНЫХ ЛЕНИНЦЕВ;ЮН.ЛЕНИНЦЕВ", "ВЕЛИКОЙ ПОБЕДЫ;ВЕЛ.ПОБЕДЫ;В.ПОБЕДЫ", "КРАСНОЙ АРМИИ;КР.АРМИИ", "СОВЕТСКОЙ АРМИИ;СОВ.АРМИИ;СА", "СОВЕТСКОЙ ВЛАСТИ;СОВ.ВЛАСТИ", "СА И ВМФ;СОВЕТСКОЙ АРМИИ И ВОЕННО МОРСКОГО ФЛОТА", "ВОЕННО МОРСКОЙ ФЛОТ;ВМФ", "МОЛОДАЯ ГВАРДИЯ", "ЗАЩИТНИКИ БЕЛОГО ДОМА", "ЗАРЯ ВОСТОКА", "ЗАРЯ КОММУНИЗМА", "ДРУЖБЫ НАРОДОВ", "ВЕТЕРАН ВС;ВЕТЕРАН ВООРУЖЕННЫХ СИЛ", "ВЕТЕРАН МО;ВЕТЕРАН МИНИСТЕРСТВА ОБОРОНЫ", "ВЕТЕРАН РЕВОЛЮЦИИ", "ВЕТЕРАН ВОЙНЫ И ТРУДА", "ВЕТЕРАН СА;ВЕТЕРАН СОВЕТСКОЙ АРМИИ", "ВЕТЕРАН ВОВ;ВЕТЕРАН ВЕЛИКОЙ ОТЕЧЕСТВЕННОЙ ВОЙНЫ", "ГОРКИ ЛЕНИНСКИЕ", "ГОРОДОК ПИСАТЕЛЕЙ ПЕРЕДЕЛКИНО", "СВЕТЛЫЙ ПУТЬ ЛЕНИНА", "ЗАВЕТЫ ИЛЬИЧА", "СЕРП И МОЛОТ", "СОЦТРУДА;СОЦ.ТРУДА;СОЦИАЛИСТИЧЕСКОГО ТРУДА", "ПАРИЖСКОЙ КОММУНЫ;П.КОММУНЫ;ПАР.КОММУНЫ;ПАРИЖ.КОММУНЫ", "КРАСНЫХ ПАРТИЗАН;КР.ПАРТИЗАН;КРАСН.ПАРТИЗАН", "АЛМА-АТИНСКАЯ;А.АТИНСКАЯ;АЛМАТИНСКАЯ", "КИМ ИР СЕНА;КИМ ИРСЕНА", "ХО ШИ МИНА;ХОШИМИНА;ХО ШИМИНА", "ДРУЖБЫ НАРОДОВ;ДР.НАРОДОВ;ДРУЖ.НАРОДОВ", "КИРИЛЛА И МЕФОДИЯ;КИРИЛА И МЕФОДИЯ", "ПАМЯТИ И СЛАВЫ", "ЗА РУЛЕМ", "ЛАТЫШСКИХ СТРЕЛКОВ;ЛАТ.СТРЕЛКОВ;ЛАТЫШ.СТРЕЛКОВ", "ПАРТСЪЕЗДА;П/СЪЕЗДА;ПАРТИЙНОГО СЪЕЗДА;ПАРТ.СЪЕЗДА", "ТОЛЬЯТТИ;ПАЛЬМИРО ТОЛЬЯТТИ;П.ТОЛЬЯТТИ", "БИКБАЯ;БАЯЗИТА БИКБАЯ", "АМИРХАНА;ФАТЫХА АМИРХАНА", "КАРИМА;ФАТЫХА КАРИМА", "САНТЬЯГО ДЕ КУБА", "СУЛТАНА;АМЕТ ХАН СУЛТАНА;АМЕТХАН СУЛТАНА;АХМЕТ ХАН СУЛТАНА", "БАРКЛАЯ ДЕ ТОЛЛИ", "ЛЕОНАРДО ДА ВИНЧИ;ЛЕОНАРДО ДАВИНЧИ;ДА ВИНЧИ;ДАВИНЧИ", "МЕЛИК КАРАМОВА;М.КАРАМОВА;М КАРАМОВА"]

NameToken._static_ctor()