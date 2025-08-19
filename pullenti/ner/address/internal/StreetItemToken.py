# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.geo.internal.GeoAnalyzerData import GeoAnalyzerData
from pullenti.ner.Referent import Referent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphCase import MorphCase
from pullenti.ner.geo.internal.Condition import Condition
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.geo.internal.GeoTokenType import GeoTokenType
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.GetTextAttr import GetTextAttr

class StreetItemToken(MetaToken):
    
    @staticmethod
    def try_parse_list(t : 'Token', max_count : int=10, ad : 'GeoAnalyzerData'=None) -> typing.List['StreetItemToken']:
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        if (t is None): 
            return None
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (ad.slevel > 2): 
            return None
        ad.slevel += 1
        res = StreetItemToken.__try_parse_list(t, max_count, ad)
        ad.slevel -= 1
        return res
    
    @staticmethod
    def __try_parse_list(t : 'Token', max_count : int, ad : 'GeoAnalyzerData') -> typing.List['StreetItemToken']:
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.NumToken import NumToken
        from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
        res = None
        sit = StreetItemToken.try_parse(t, None, False, ad)
        if (sit is not None): 
            res = list()
            res.append(sit)
            t = sit.end_token.next0_
        else: 
            res = StreetItemToken._try_parse_spec(t, None)
            if (res is None): 
                return None
            sit = res[len(res) - 1]
            t = sit.end_token.next0_
            sit2 = StreetItemToken.try_parse(t, None, False, None)
            if (sit2 is not None and sit2.typ == StreetItemType.NOUN): 
                pass
            elif (AddressItemToken.check_house_after(t, False, True)): 
                pass
            else: 
                return None
        first_pass3786 = True
        while True:
            if first_pass3786: first_pass3786 = False
            else: t = (None if t is None else t.next0_)
            if (not (t is not None)): break
            if (max_count > 0 and len(res) >= max_count): 
                break
            if (t.is_newline_before): 
                if (t.newlines_before_count > 1): 
                    break
                if (((t.whitespaces_after_count < 15) and sit is not None and sit.typ == StreetItemType.NOUN) and t.chars.is_capital_upper): 
                    pass
                else: 
                    ok = False
                    if (len(res) == 1 and res[0].typ == StreetItemType.NAME): 
                        sit1 = StreetItemToken.try_parse(sit.end_token.next0_, sit, False, ad)
                        if (sit1 is not None and sit1.typ == StreetItemType.NOUN): 
                            sit2 = StreetItemToken.try_parse(sit1.end_token.next0_, sit1, False, ad)
                            if (sit2 is None): 
                                ok = True
                    elif (len(res) == 2 and res[0].typ == StreetItemType.NOUN and res[1].typ == StreetItemType.STDADJECTIVE): 
                        sit1 = StreetItemToken.try_parse(sit.end_token.next0_, sit, False, ad)
                        if (sit1 is not None and ((sit1.typ == StreetItemType.STDNAME or sit1.typ == StreetItemType.NAME))): 
                            if (AddressItemToken.check_house_after(sit1.end_token.next0_, False, False)): 
                                ok = True
                    if (not ok): 
                        break
            if (t.is_hiphen and sit is not None and ((sit.typ == StreetItemType.NAME or sit.typ == StreetItemType.STDNAME or ((sit.typ == StreetItemType.STDADJECTIVE))))): 
                sit1 = StreetItemToken.try_parse(t.next0_, sit, False, ad)
                if (sit1 is None): 
                    num = NumberHelper.try_parse_roman(t.next0_)
                    if (num is not None): 
                        sit = StreetItemToken._new294(t, num.end_token, StreetItemType.NUMBER, num.value, True)
                        res.append(sit)
                        t = sit.end_token
                        continue
                    break
                if (sit1.typ == StreetItemType.NUMBER): 
                    tt = sit1.end_token.next0_
                    if (tt is not None and tt.is_comma): 
                        tt = tt.next0_
                    ok = False
                    ait = AddressItemToken.try_parse_pure_item(tt, None, None)
                    if (ait is not None): 
                        if (ait.typ == AddressItemType.HOUSE): 
                            ok = True
                    if (not ok): 
                        if (len(res) == 2 and res[0].typ == StreetItemType.NOUN): 
                            if (res[0].termin.canonic_text == "МИКРОРАЙОН"): 
                                ok = True
                    if (not ok and t.is_hiphen): 
                        ok = True
                    if (ok): 
                        sit = sit1
                        res.append(sit)
                        t = sit.end_token
                        sit.number_has_prefix = True
                        continue
                if (sit1.typ != StreetItemType.NAME and sit1.typ != StreetItemType.NAME): 
                    if (sit1.typ == StreetItemType.NOUN and sit1.noun_can_be_name): 
                        pass
                    elif (sit1.typ == StreetItemType.STDADJECTIVE): 
                        pass
                    else: 
                        break
                if (t.is_whitespace_before and t.is_whitespace_after): 
                    break
                if (res[0].begin_token.previous is not None): 
                    aaa = AddressItemToken.try_parse_pure_item(res[0].begin_token.previous, None, None)
                    if (aaa is not None and aaa.typ == AddressItemType.DETAIL and aaa.detail_type == AddressDetailType.CROSS): 
                        break
                sit = sit1
                res.append(sit)
                t = sit.end_token
                continue
            elif (t.is_hiphen and sit is not None and sit.typ == StreetItemType.NUMBER): 
                sit1 = StreetItemToken.try_parse(t.next0_, None, False, ad)
                if (sit1 is not None and (((sit1.typ == StreetItemType.STDADJECTIVE or sit1.typ == StreetItemType.STDNAME or sit1.typ == StreetItemType.NAME) or sit1.typ == StreetItemType.NOUN))): 
                    sit.number_has_prefix = True
                    sit = sit1
                    res.append(sit)
                    t = sit.end_token
                    continue
            if (t.is_char('.') and sit is not None and sit.typ == StreetItemType.NOUN): 
                if (t.whitespaces_after_count > 1): 
                    break
                sit = StreetItemToken.try_parse(t.next0_, None, False, ad)
                if (sit is None): 
                    break
                if (sit.typ == StreetItemType.NUMBER or sit.typ == StreetItemType.STDADJECTIVE): 
                    sit1 = StreetItemToken.try_parse(sit.end_token.next0_, None, False, ad)
                    if (sit1 is not None and ((sit1.typ == StreetItemType.STDADJECTIVE or sit1.typ == StreetItemType.STDNAME or sit1.typ == StreetItemType.NAME))): 
                        pass
                    elif (not MiscLocationHelper.is_user_param_address(sit)): 
                        break
                    else: 
                        ai = AddressItemToken.try_parse_pure_item(t.next0_, None, None)
                        if (ai is not None and ai.typ != AddressItemType.NUMBER): 
                            break
                elif (sit.typ != StreetItemType.NAME and sit.typ != StreetItemType.STDNAME and sit.typ != StreetItemType.AGE): 
                    break
                if (t.previous.get_morph_class_in_dictionary().is_noun): 
                    if (not sit.is_in_dictionary): 
                        tt = sit.end_token.next0_
                        has_house = False
                        first_pass3787 = True
                        while True:
                            if first_pass3787: first_pass3787 = False
                            else: tt = tt.next0_
                            if (not (tt is not None)): break
                            if (tt.is_newline_before): 
                                break
                            if (tt.is_comma): 
                                continue
                            ai = AddressItemToken.try_parse_pure_item(tt, None, None)
                            if (ai is not None and ((ai.typ == AddressItemType.HOUSE or ai.typ == AddressItemType.BUILDING or ai.typ == AddressItemType.CORPUS))): 
                                has_house = True
                                break
                            if (isinstance(tt, NumberToken)): 
                                has_house = True
                                break
                            vv = StreetItemToken.try_parse(tt, None, False, ad)
                            if (vv is None or vv.typ == StreetItemType.NOUN): 
                                break
                            tt = vv.end_token
                        if (not has_house): 
                            break
                    if (t.previous.previous is not None): 
                        npt11 = MiscLocationHelper._try_parse_npt(t.previous.previous)
                        if (npt11 is not None and npt11.end_token == t.previous): 
                            break
                res.append(sit)
            else: 
                sit = StreetItemToken.try_parse(t, res[len(res) - 1], False, ad)
                if (sit is None): 
                    spli = StreetItemToken._try_parse_spec(t, res[len(res) - 1])
                    if (spli is not None and len(spli) > 0): 
                        res.extend(spli)
                        t = spli[len(spli) - 1].end_token
                        continue
                    if (((isinstance(t, TextToken)) and ((len(res) == 2 or len(res) == 3)) and res[0].typ == StreetItemType.NOUN) and res[1].typ == StreetItemType.NUMBER and (((t.term == "ГОДА" or t.term == "МАЯ" or t.term == "МАРТА") or t.term == "СЪЕЗДА"))): 
                        sit = StreetItemToken._new284(t, t, StreetItemType.STDNAME, t.term)
                        res.append(sit)
                        continue
                    sit = res[len(res) - 1]
                    if (t is None): 
                        break
                    if (sit.typ == StreetItemType.NOUN and ((sit.termin.canonic_text == "МИКРОРАЙОН" or sit.termin.canonic_text == "МІКРОРАЙОН")) and (t.whitespaces_before_count < 2)): 
                        tt1 = t
                        if (tt1.is_hiphen and tt1.next0_ is not None): 
                            tt1 = tt1.next0_
                        if (BracketHelper.is_bracket(tt1, True) and tt1.next0_ is not None): 
                            tt1 = tt1.next0_
                        tt2 = tt1.next0_
                        br = False
                        if (BracketHelper.is_bracket(tt2, True)): 
                            tt2 = tt2.next0_
                            br = True
                        if (((isinstance(tt1, TextToken)) and tt1.length_char == 1 and tt1.chars.is_letter) and ((AddressItemToken.check_house_after(tt2, False, True) or tt2 is None))): 
                            sit = StreetItemToken._new284(t, (tt1.next0_ if br else tt1), StreetItemType.NAME, tt1.term)
                            ch1 = AddressItemToken.correct_char(sit.value[0])
                            if ((ord(ch1)) != 0 and ch1 != sit.value[0]): 
                                sit.alt_value = "{0}".format(ch1)
                            res.append(sit)
                            break
                    if (t.is_comma and (((sit.typ == StreetItemType.NAME or sit.typ == StreetItemType.STDNAME or sit.typ == StreetItemType.STDPARTOFNAME) or sit.typ == StreetItemType.STDADJECTIVE or ((sit.typ == StreetItemType.NUMBER and len(res) > 1 and (((res[len(res) - 2].typ == StreetItemType.NAME or res[len(res) - 2].typ == StreetItemType.STDNAME or res[len(res) - 2].typ == StreetItemType.STDADJECTIVE) or res[len(res) - 2].typ == StreetItemType.STDPARTOFNAME))))))): 
                        sit2 = StreetItemToken.try_parse(t.next0_, None, False, ad)
                        if (sit2 is not None and sit2.typ == StreetItemType.NOUN): 
                            ttt = sit2.end_token.next0_
                            if (ttt is not None and ttt.is_comma): 
                                ttt = ttt.next0_
                            add = AddressItemToken.try_parse_pure_item(ttt, None, None)
                            if (add is not None and ((add.typ == AddressItemType.HOUSE or add.typ == AddressItemType.CORPUS or add.typ == AddressItemType.BUILDING))): 
                                res.append(sit2)
                                t = sit2.end_token
                                continue
                    elif (t.is_comma and sit.typ == StreetItemType.NOUN and "КВАРТАЛ" in sit.termin.canonic_text): 
                        num = NumToken.try_parse(t.next0_, GeoTokenType.STREET)
                        if (num is not None and num.is_cadaster_number): 
                            continue
                    if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                        sit1 = res[len(res) - 1]
                        if (sit1.typ == StreetItemType.NOUN and ((sit1.noun_is_doubt_coef == 0 or (((isinstance(t.next0_, TextToken)) and not t.next0_.chars.is_all_lower))))): 
                            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                            if (br is not None and (br.length_char < 50)): 
                                sit2 = StreetItemToken.try_parse(t.next0_, None, False, ad)
                                if (sit2 is not None and sit2.end_token.next0_ == br.end_token): 
                                    if (sit2.value is None and sit2.typ == StreetItemType.NAME): 
                                        sit2.value = MiscHelper.get_text_value(sit2.begin_token, sit2.end_token, GetTextAttr.NO)
                                    sit2.begin_token = t
                                    sit2.is_in_brackets = True
                                    sit2.end_token = br.end_token
                                    t = sit2.end_token
                                    res.append(sit2)
                                    continue
                                res.append(StreetItemToken._new297(t, br.end_token, StreetItemType.NAME, MiscHelper.get_text_value(t, br.end_token, GetTextAttr.NO), True))
                                t = br.end_token
                                continue
                    if (t.is_hiphen and (isinstance(t.next0_, NumberToken)) and t.next0_.int_value is not None): 
                        sit = res[len(res) - 1]
                        if (sit.typ == StreetItemType.NOUN and (((sit.termin.canonic_text == "КВАРТАЛ" or sit.termin.canonic_text == "МИКРОРАЙОН" or sit.termin.canonic_text == "ГОРОДОК") or sit.termin.canonic_text == "МІКРОРАЙОН"))): 
                            sit = StreetItemToken._new298(t, t.next0_, StreetItemType.NUMBER, t.next0_.value, t.next0_.typ, True)
                            res.append(sit)
                            t = t.next0_
                            continue
                    if ((((t.is_char(':') or t.is_hiphen)) and len(res) == 1 and res[0].typ == StreetItemType.NOUN) and (t.whitespaces_after_count < 3)): 
                        continue
                    if ((t.is_comma and len(res) == 1 and res[0].typ == StreetItemType.NOUN) and MiscLocationHelper.is_user_param_address(t)): 
                        sit = StreetItemToken.try_parse(t.next0_, None, False, None)
                        if (sit is not None and ((sit.typ == StreetItemType.NAME or sit.typ == StreetItemType.STDNAME or sit.typ == StreetItemType.STDADJECTIVE))): 
                            res.append(sit)
                            t = sit.end_token
                            continue
                    if ((t.is_char('(') and t.next0_ is not None and (isinstance(t.next0_.get_referent(), GeoReferent))) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(')')): 
                        sit = StreetItemToken.try_parse(t.next0_.next0_.next0_, None, False, None)
                        if (sit is not None and sit.typ == StreetItemType.NOUN): 
                            res[len(res) - 1]._area = AddressItemToken._new202(AddressItemType.REGION, t, t.next0_.next0_, t.next0_.get_referent())
                            res.append(sit)
                            t = sit.end_token
                            continue
                    break
                res.append(sit)
                if (sit.typ == StreetItemType.NAME): 
                    cou = 0
                    jj = 0
                    for jj in range(len(res) - 1, -1, -1):
                        if (res[jj].typ == StreetItemType.NAME): 
                            cou += 1
                        else: 
                            break
                    else: jj = -1
                    if (cou > 4): 
                        if (jj < 0): 
                            return None
                        del res[jj:jj+len(res) - jj]
                        break
                    if (len(res) > 1 and res[0].typ == StreetItemType.NOUN and res[0].is_road): 
                        tt = sit.end_token.next0_
                        if (tt is not None): 
                            if (tt.is_value("Ш", None) or tt.is_value("ШОССЕ", None) or tt.is_value("ШОС", None)): 
                                sit = sit.clone()
                                res[len(res) - 1] = sit
                                sit.end_token = tt
                                if (tt.next0_ is not None and tt.next0_.is_char('.') and tt.length_char <= 3): 
                                    sit.end_token = sit.end_token.next0_
            t = sit.end_token
        i = 0
        while i < (len(res) - 1): 
            if (res[i].typ == StreetItemType.NAME and ((res[i + 1].alt_typ == StreetItemType.STDPARTOFNAME or res[i + 1].typ == StreetItemType.STDPARTOFNAME))): 
                r = res[i].clone()
                if (r.value is None): 
                    r.value = MiscHelper.get_text_value_of_meta_token(r, GetTextAttr.NO)
                r.misc = (Utils.ifNotNull(res[i + 1].value, MiscHelper.get_text_value_of_meta_token(res[i + 1], GetTextAttr.NO)))
                r.end_token = res[i + 1].end_token
                res[i] = r
                del res[i + 1]
            elif (res[i + 1].typ == StreetItemType.NAME and ((res[i].alt_typ == StreetItemType.STDPARTOFNAME or res[i].typ == StreetItemType.STDPARTOFNAME))): 
                r = res[i + 1].clone()
                if (r.value is None): 
                    r.value = MiscHelper.get_text_value_of_meta_token(r, GetTextAttr.NO)
                r.misc = (Utils.ifNotNull(res[i].value, MiscHelper.get_text_value_of_meta_token(res[i], GetTextAttr.NO)))
                r.begin_token = res[i].begin_token
                res[i] = r
                del res[i + 1]
            i += 1
        i = 0
        first_pass3788 = True
        while True:
            if first_pass3788: first_pass3788 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == StreetItemType.NAME and res[i + 1].typ == StreetItemType.NAME and (res[i].whitespaces_after_count < 3)): 
                is_prop = False
                is_pers = False
                if (res[i].begin_token.morph.class0_.is_noun): 
                    rt = res[i].kit.process_referent("PERSON", res[i].begin_token, None)
                    if (rt is not None): 
                        if (rt.referent.type_name == "PERSONPROPERTY"): 
                            is_prop = True
                        elif (rt.end_token == res[i + 1].end_token): 
                            is_pers = True
                if ((i == 0 and ((not is_prop and not is_pers)) and ((i + 2) < len(res))) and res[i + 2].typ == StreetItemType.NOUN and not res[i].begin_token.morph.class0_.is_adjective): 
                    if (MiscLocationHelper.check_geo_object_before(res[0].begin_token, False) and res[0].end_token.next0_ == res[1].begin_token and (res[0].whitespaces_after_count < 2)): 
                        pass
                    else: 
                        del res[i]
                        i -= 1
                        continue
                if (res[i].morph.class0_.is_adjective and res[i + 1].morph.class0_.is_adjective and not is_pers): 
                    if (res[i].end_token.next0_.is_hiphen): 
                        pass
                    elif (i == 1 and res[0].typ == StreetItemType.NOUN and len(res) == 3): 
                        pass
                    elif (i == 0 and len(res) == 3 and res[2].typ == StreetItemType.NOUN): 
                        pass
                    else: 
                        continue
                if (res[i].chars.value != res[i + 1].chars.value): 
                    rt = res[0].kit.process_referent("ORGANIZATION", res[i + 1].begin_token, None)
                    if (rt is not None): 
                        del res[i + 1:i + 1+len(res) - i - 1]
                        continue
                r = res[i].clone()
                if (r.value is None): 
                    r.value = MiscHelper.get_text_value_of_meta_token(res[i], GetTextAttr.NO)
                tt1 = res[i + 1].end_token
                mc1 = res[i].begin_token.get_morph_class_in_dictionary()
                mc2 = tt1.get_morph_class_in_dictionary()
                if ((tt1.is_value("БОР", None) or tt1.is_value("САД", None) or tt1.is_value("ПАРК", None)) or tt1.previous.is_hiphen): 
                    r.value = MiscHelper.get_text_value(res[i].begin_token, res[i + 1].end_token, GetTextAttr.NO)
                elif (((mc1.is_proper_name and not mc2.is_proper_name)) or ((not mc1.is_proper_surname and mc2.is_proper_surname))): 
                    if (r.misc is None): 
                        r.misc = r.value
                    r.value = (Utils.ifNotNull(res[i + 1].value, MiscHelper.get_text_value_of_meta_token(res[i + 1], GetTextAttr.NO)))
                elif (((mc2.is_proper_name and not mc1.is_proper_name)) or ((not mc2.is_proper_surname and mc1.is_proper_surname))): 
                    if (r.misc is None): 
                        r.misc = MiscHelper.get_text_value_of_meta_token(res[i + 1], GetTextAttr.NO)
                else: 
                    r.value = MiscHelper.get_text_value(res[i].begin_token, res[i + 1].end_token, GetTextAttr.NO)
                if ("-" in r.value): 
                    r.value = r.value.replace('-', ' ')
                r._orto_terr = res[i + 1]._orto_terr
                r.end_token = res[i + 1].end_token
                r.exist_street = (None)
                r.is_in_dictionary = (res[i + 1].is_in_dictionary or res[i].is_in_dictionary)
                res[i] = r
                del res[i + 1]
                i -= 1
        i = 0
        while i < (len(res) - 1): 
            if (res[i].typ == StreetItemType.STDADJECTIVE and res[i].end_token.is_char('.') and res[i + 1].__is_surname()): 
                r = res[i + 1].clone()
                r.value = res[i + 1].begin_token.term
                r.alt_value = MiscHelper.get_text_value(res[i].begin_token, res[i + 1].end_token, GetTextAttr.NO)
                r.begin_token = res[i].begin_token
                r.std_adj_version = res[i]
                res[i + 1] = r
                del res[i]
                break
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if ((res[i + 1].typ == StreetItemType.STDADJECTIVE and res[i + 1].end_token.is_char('.') and res[i + 1].begin_token.length_char == 1) and not res[i].begin_token.chars.is_all_lower): 
                if (res[i].__is_surname()): 
                    if (i == (len(res) - 2) or res[i + 2].typ != StreetItemType.NOUN): 
                        r = res[i].clone()
                        if (r.value is None): 
                            r.value = MiscHelper.get_text_value_of_meta_token(r, GetTextAttr.NO)
                        r.end_token = res[i + 1].end_token
                        r.std_adj_version = res[i + 1]
                        res[i] = r
                        del res[i + 1]
                        break
            i += 1
        i = 0
        first_pass3789 = True
        while True:
            if first_pass3789: first_pass3789 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == StreetItemType.NAME or res[i].typ == StreetItemType.STDNAME or res[i].typ == StreetItemType.STDADJECTIVE): 
                if (res[i + 1].typ == StreetItemType.NOUN and not res[i + 1].is_abridge and res[i + 1].termin.canonic_text != "УЛИЦА"): 
                    res0 = list(res)
                    del res0[0:0+i + 1]
                    rtt = StreetDefineHelper._try_parse_street(res0, False, False, False, None)
                    if (rtt is not None): 
                        continue
                    i0 = -1
                    if (i == 1 and res[0].typ == StreetItemType.NOUN and len(res) == 3): 
                        i0 = 0
                    elif (i == 0 and len(res) == 3 and res[2].typ == StreetItemType.NOUN): 
                        i0 = 2
                    if (i0 < 0): 
                        continue
                    if (res[i0].termin == res[i + 1].termin): 
                        continue
                    r = res[i].clone()
                    r.alt_value = (Utils.ifNotNull(res[i].value, MiscHelper.get_text_value(res[i].begin_token, res[i].end_token, GetTextAttr.NO)))
                    if (res[i].typ == StreetItemType.STDADJECTIVE): 
                        adjs = MiscLocationHelper.get_std_adj_full(res[i].begin_token, res[i + 1].morph.gender, res[i + 1].morph.number, True)
                        if (adjs is not None and len(adjs) > 0): 
                            r.alt_value = adjs[0]
                    r.value = "{0} {1}".format(r.alt_value, res[i + 1].termin.canonic_text)
                    r.typ = StreetItemType.STDNAME
                    r.end_token = res[i + 1].end_token
                    res[i] = r
                    rr = res[i0].clone()
                    rr.alt_termin = res[i + 1].termin
                    res[i0] = rr
                    del res[i + 1]
                    i -= 1
        if ((len(res) >= 3 and res[0].typ == StreetItemType.NOUN and res[0].termin.canonic_text == "КВАРТАЛ") and ((res[1].typ == StreetItemType.NAME or res[1].typ == StreetItemType.STDNAME)) and res[2].typ == StreetItemType.NOUN): 
            if (len(res) == 3 or res[3].typ == StreetItemType.NUMBER): 
                res0 = list(res)
                del res0[0:0+2]
                rtt = StreetDefineHelper._try_parse_street(res0, False, False, False, None)
                if (rtt is None or res0[0].chars.is_capital_upper): 
                    r = res[1].clone()
                    r.value = "{0} {1}".format(MiscHelper.get_text_value_of_meta_token(res[1], GetTextAttr.NO), res[2].termin.canonic_text)
                    r.end_token = res[2].end_token
                    res[1] = r
                    del res[2]
        if ((len(res) >= 3 and res[0].typ == StreetItemType.NOUN and res[0].termin.canonic_text == "КВАРТАЛ") and ((res[2].typ == StreetItemType.NAME or res[2].typ == StreetItemType.STDNAME)) and res[1].typ == StreetItemType.NOUN): 
            if (len(res) == 3 or res[3].typ == StreetItemType.NUMBER): 
                r = res[1].clone()
                r.value = "{0} {1}".format(MiscHelper.get_text_value_of_meta_token(res[2], GetTextAttr.NO), res[1].termin.canonic_text)
                r.end_token = res[2].end_token
                r.typ = StreetItemType.NAME
                res[1] = r
                del res[2]
        if ((len(res) >= 3 and res[0].typ == StreetItemType.NUMBER and not res[0].is_number_km) and res[1].typ == StreetItemType.NOUN): 
            if (not MiscLocationHelper.is_user_param_address(res[0]) and res[2].typ != StreetItemType.STDNAME and res[2].typ != StreetItemType.FIX): 
                nt = Utils.asObjectOrNull(res[0].begin_token, NumberToken)
                if (nt is not None and nt.typ == NumberSpellingType.DIGIT and nt.morph.class0_.is_undefined): 
                    return None
        ii0 = -1
        ii1 = -1
        if (len(res) > 0 and res[0].typ == StreetItemType.NOUN and res[0].is_road): 
            ii1 = 0
            ii0 = ii1
            if (((ii0 + 1) < len(res)) and res[ii0 + 1].typ == StreetItemType.NUMBER and res[ii0 + 1].is_number_km): 
                ii0 += 1
        elif ((len(res) > 1 and res[0].typ == StreetItemType.NUMBER and res[0].is_number_km) and res[1].typ == StreetItemType.NOUN and res[1].is_road): 
            ii1 = 1
            ii0 = ii1
        if (ii0 >= 0): 
            if (len(res) == (ii0 + 1)): 
                tt = res[ii0].end_token.next0_
                num = StreetItemToken.__try_attach_road_num(tt)
                if (num is not None): 
                    res.append(num)
                    tt = num.end_token.next0_
                    res[0].is_abridge = False
                if (tt is not None and (isinstance(tt.get_referent(), GeoReferent))): 
                    g1 = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                    tt = tt.next0_
                    if (tt is not None and tt.is_hiphen): 
                        tt = tt.next0_
                    g2 = (None if tt is None else Utils.asObjectOrNull(tt.get_referent(), GeoReferent))
                    if (g2 is not None): 
                        if (g1.is_city and g2.is_city): 
                            nam = StreetItemToken._new300(res[0].end_token.next0_, tt, StreetItemType.NAME)
                            nam.value = "{0} - {1}".format(g1.to_string_ex(True, tt.kit.base_language, 0), g2.to_string_ex(True, tt.kit.base_language, 0)).upper()
                            nam.alt_value = "{0} - {1}".format(g2.to_string_ex(True, tt.kit.base_language, 0), g1.to_string_ex(True, tt.kit.base_language, 0)).upper()
                            res.append(nam)
                elif (BracketHelper.is_bracket(tt, False)): 
                    br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                    if (br is not None): 
                        nam = StreetItemToken._new301(tt, br.end_token, StreetItemType.NAME, True)
                        nam.value = MiscHelper.get_text_value(tt.next0_, br.end_token, GetTextAttr.NO)
                        res.append(nam)
            elif ((len(res) == (ii0 + 2) and res[ii0 + 1].typ == StreetItemType.NAME and res[ii0 + 1].end_token.next0_ is not None) and res[ii0 + 1].end_token.next0_.is_hiphen): 
                tt = res[ii0 + 1].end_token.next0_.next0_
                g2 = (None if tt is None else Utils.asObjectOrNull(tt.get_referent(), GeoReferent))
                te = None
                name2 = None
                if (g2 is None and tt is not None): 
                    rt = tt.kit.process_referent("GEO", tt, None)
                    if (rt is not None): 
                        te = rt.end_token
                        name2 = rt.referent.to_string_ex(True, te.kit.base_language, 0)
                    else: 
                        cits2 = CityItemToken.try_parse_list(tt, 2, None)
                        if (cits2 is not None): 
                            if (len(cits2) == 1 and ((cits2[0].typ == CityItemToken.ItemType.PROPERNAME or cits2[0].typ == CityItemToken.ItemType.CITY))): 
                                if (cits2[0].onto_item is not None): 
                                    name2 = cits2[0].onto_item.canonic_text
                                else: 
                                    name2 = cits2[0].value
                                te = cits2[0].end_token
                elif (g2 is not None): 
                    te = tt
                    name2 = g2.to_string_ex(True, te.kit.base_language, 0)
                if (((g2 is not None and g2.is_city)) or ((g2 is None and name2 is not None))): 
                    r = res[ii0 + 1].clone()
                    r.alt_value = "{0} - {1}".format(name2, Utils.ifNotNull(res[ii0 + 1].value, res[ii0 + 1].get_source_text())).upper()
                    r.value = "{0} - {1}".format(Utils.ifNotNull(res[ii0 + 1].value, res[ii0 + 1].get_source_text()), name2).upper()
                    r.end_token = te
                    res[ii0 + 1] = r
            nn = StreetItemToken.__try_attach_road_num(res[len(res) - 1].end_token.next0_)
            if (nn is not None): 
                res.append(nn)
                res[ii1].is_abridge = False
            if (len(res) > (ii0 + 1) and res[ii0 + 1].typ == StreetItemType.NAME and res[ii1].termin.canonic_text == "АВТОДОРОГА"): 
                if (res[ii0 + 1].begin_token.is_value("ФЕДЕРАЛЬНЫЙ", None)): 
                    return None
                npt = MiscLocationHelper._try_parse_npt(res[ii0 + 1].begin_token)
                if (npt is not None and len(npt.adjectives) > 0): 
                    if (npt.end_token.is_value("ЗНАЧЕНИЕ", None)): 
                        return None
        while len(res) > 1:
            it = res[len(res) - 1]
            if (it.begin_token == it.end_token and it.length_char == 1 and it.is_value("В", None)): 
                if (isinstance(it.end_token.next0_, ReferentToken)): 
                    res.remove(it)
                    continue
            if (len(res) == 4): 
                if ((res[0].typ == StreetItemType.NOUN and res[1].typ == StreetItemType.NUMBER and res[2].typ == StreetItemType.NOUN) and res[3].typ == StreetItemType.NUMBER): 
                    break
            if (len(res) == 5): 
                if (((res[0].typ == StreetItemType.NOUN and res[0].termin.canonic_text == "УЛИЦА" and res[1].typ == StreetItemType.NOUN) and res[2].typ == StreetItemType.NUMBER and res[3].typ == StreetItemType.NOUN) and res[4].typ == StreetItemType.NUMBER): 
                    break
            it0 = (res[len(res) - 2] if len(res) > 1 else None)
            if (it.typ == StreetItemType.NUMBER and not it.number_has_prefix and not it.is_number_km): 
                if (isinstance(it.begin_token, NumberToken)): 
                    if (len(res) == 2 and res[0].typ == StreetItemType.NOUN): 
                        break
                    if (MiscLocationHelper.is_user_param_gar_address(res[0])): 
                        break
                    if (not it.begin_token.morph.class0_.is_adjective or it.begin_token.morph.class0_.is_noun): 
                        if (AddressItemToken.check_house_after(it.end_token.next0_, False, True)): 
                            it.number_has_prefix = True
                        elif (it0 is not None and it0.typ == StreetItemType.NOUN and (((it0.termin.canonic_text == "МИКРОРАЙОН" or it0.termin.canonic_text == "МІКРОРАЙОН" or it0.termin.canonic_text == "КВАРТАЛ") or it0.termin.canonic_text == "ГОРОДОК"))): 
                            ait = AddressItemToken.try_parse_pure_item(it.begin_token, None, None)
                            if (ait is not None and ait.typ == AddressItemType.NUMBER and ait.end_char > it.end_char): 
                                it.number_type = NumberSpellingType.UNDEFINED
                                it.value = ait.value
                                it.end_token = ait.end_token
                                it.typ = StreetItemType.NAME
                        elif (it0 is not None and it0.termin is not None and it0.termin.canonic_text == "ПОЧТОВОЕ ОТДЕЛЕНИЕ"): 
                            it.number_has_prefix = True
                        elif (it0 is not None and it0.begin_token.is_value("ЛИНИЯ", None)): 
                            it.number_has_prefix = True
                        elif (len(res) == 2 and res[0].typ == StreetItemType.NOUN and (res[0].whitespaces_after_count < 2)): 
                            pass
                        elif (it.begin_token.morph.class0_.is_adjective and it.begin_token.typ == NumberSpellingType.WORDS and it.begin_token.chars.is_capital_upper): 
                            it.number_has_prefix = True
                        elif (it.begin_token.previous.is_hiphen): 
                            it.number_has_prefix = True
                        elif ((len(res) > 1 and res[len(res) - 2].typ == StreetItemType.NAME and res[len(res) - 2].begin_token == res[len(res) - 2].end_token) and it.begin_token.previous.get_morph_class_in_dictionary().is_proper_name): 
                            it.number_has_prefix = True
                        else: 
                            del res[len(res) - 1]
                            continue
                    else: 
                        it.number_has_prefix = True
            break
        if (len(res) == 0): 
            return None
        i = 0
        while i < len(res): 
            if (res[i].next_item is not None): 
                if (res[i].typ == StreetItemType.NUMBER and i > 0 and res[i - 1].typ == StreetItemType.NAME): 
                    pass
                else: 
                    res.insert(i + 1, res[i].next_item)
            i += 1
        i = 0
        while i < len(res): 
            if ((res[i].typ == StreetItemType.NOUN and res[i].chars.is_capital_upper and (((res[i].termin.canonic_text == "НАБЕРЕЖНАЯ" or res[i].termin.canonic_text == "МИКРОРАЙОН" or res[i].termin.canonic_text == "НАБЕРЕЖНА") or res[i].termin.canonic_text == "МІКРОРАЙОН" or res[i].termin.canonic_text == "ГОРОДОК"))) and res[i].begin_token.is_value(res[i].termin.canonic_text, None)): 
                ok = False
                if (i > 0 and ((res[i - 1].typ == StreetItemType.NOUN or res[i - 1].typ == StreetItemType.STDADJECTIVE))): 
                    ok = True
                elif (i > 1 and ((res[i - 1].typ == StreetItemType.STDADJECTIVE or res[i - 1].typ == StreetItemType.NUMBER)) and res[i - 2].typ == StreetItemType.NOUN): 
                    ok = True
                if (ok): 
                    r = res[i].clone()
                    r.typ = StreetItemType.NAME
                    res[i] = r
            i += 1
        last = res[len(res) - 1]
        for kk in range(2):
            ttt = last.end_token.next0_
            if (((last.typ == StreetItemType.NAME and ttt is not None and ttt.length_char == 1) and ttt.chars.is_all_upper and (ttt.whitespaces_before_count < 2)) and ttt.next0_ is not None and ttt.next0_.is_char('.')): 
                if (AddressItemToken.try_parse_pure_item(ttt, None, None) is not None): 
                    break
                last = last.clone()
                last.end_token = ttt.next0_
                res[len(res) - 1] = last
        if (len(res) > 1): 
            if (res[len(res) - 1]._org0_ is not None): 
                if (len(res) == 2 and res[0].typ == StreetItemType.NOUN): 
                    pass
                else: 
                    del res[len(res) - 1]
        if (len(res) == 2 and res[0].typ == StreetItemType.NOUN and res[1].typ == StreetItemType.NOUN): 
            if (not res[1].chars.is_all_lower and not res[1].is_abridge and res[1].begin_token == res[1].end_token): 
                res[1] = res[1].clone()
                res[1].typ = StreetItemType.NAME
                res[1].value = MiscHelper.get_text_value_of_meta_token(res[1], GetTextAttr.NO)
        if (len(res) == 0): 
            return None
        return res
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.geo.internal.NameToken import NameToken
        if (StreetItemToken._m_ontology is not None): 
            return
        StreetItemToken._m_ontology = TerminCollection()
        StreetItemToken._m_ontology_ex = TerminCollection()
        StreetItemToken.__m_std_ont_misc = TerminCollection()
        StreetItemToken.__m_std_adj = TerminCollection()
        t = None
        t = Termin._new302("УЛИЦА", StreetItemType.NOUN, MorphGender.FEMINIE)
        t.add_abridge("УЛ.")
        t.add_abridge("УЛЮ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new303("ВУЛИЦЯ", StreetItemType.NOUN, MorphLang.UA, MorphGender.FEMINIE)
        t.add_abridge("ВУЛ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("STREET", StreetItemType.NOUN)
        t.add_abridge("ST.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ПЛОЩАДЬ", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_abridge("ПЛ.")
        t.add_abridge("ПЛОЩ.")
        t.add_abridge("ПЛ-ДЬ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new306("ПЛОЩА", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.FEMINIE)
        t.add_abridge("ПЛ.")
        t.add_abridge("ПЛОЩ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("МАЙДАН", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("SQUARE", StreetItemType.NOUN)
        t.add_abridge("SQ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ПРОЕЗД", StreetItemType.NOUN, 1, MorphGender.MASCULINE)
        t.add_abridge("ПР.")
        t.add_abridge("П-Д")
        t.add_abridge("ПР-Д")
        t.add_abridge("ПР-ЗД")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new306("ПРОЕЗД", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.MASCULINE)
        t.add_abridge("ПР.")
        t.add_abridge("П-Д")
        t.add_abridge("ПР-Д")
        t.add_abridge("ПР-ЗД")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ЛИНИЯ", StreetItemType.NOUN, 2, MorphGender.FEMINIE)
        t.add_abridge("ЛИН.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new306("ЛІНІЯ", StreetItemType.NOUN, MorphLang.UA, 2, MorphGender.FEMINIE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("РЯД", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("БЛОК", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        StreetItemToken.__m_block = t
        t.add_abridge("БЛ.")
        t.add_variant("БЛОК ГАРАЖЕЙ", False)
        t.add_variant("ГАРАЖНЫЙ БЛОК", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ПАНЕЛЬ", StreetItemType.NOUN, 2, MorphGender.FEMINIE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("КУСТ", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        t.add_variant("КУСТ ГАЗОВЫХ СКВАЖИН", False)
        t.add_variant("КУСТОВАЯ ПЛОЩАДКА СКВАЖИН", False)
        t.add_variant("КУСТ СКВАЖИН", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ПРОСПЕКТ", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        StreetItemToken.__m_prospect = t
        t.add_abridge("ПРОС.")
        t.add_abridge("ПРКТ")
        t.add_abridge("ПРОСП.")
        t.add_abridge("ПР-Т")
        t.add_abridge("ПР-КТ")
        t.add_abridge("П-Т")
        t.add_abridge("П-КТ")
        t.add_abridge("ПР Т")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ПЕРЕУЛОК", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.add_abridge("ПЕР.")
        t.add_abridge("ПЕР-К")
        t.add_abridge("П-К")
        t.add_variant("ПРЕУЛОК", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ПРОУЛОК", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.add_abridge("ПРОУЛ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new306("ПРОВУЛОК", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.MASCULINE)
        t.add_abridge("ПРОВ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new86("LANE", StreetItemType.NOUN, 0)
        t.add_abridge("LN.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ТУПИК", StreetItemType.NOUN, 1, MorphGender.MASCULINE)
        t.add_abridge("ТУП.")
        t.add_abridge("Т.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("БУЛЬВАР", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.add_abridge("БУЛЬВ.")
        t.add_abridge("БУЛ.")
        t.add_abridge("Б-Р")
        t.add_abridge("Б-РЕ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new86("BOULEVARD", StreetItemType.NOUN, 0)
        t.add_abridge("BLVD")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new86("СКВЕР", StreetItemType.NOUN, 1)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("НАБЕРЕЖНАЯ", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        t.add_abridge("НАБ.")
        t.add_abridge("НАБЕР.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new306("НАБЕРЕЖНА", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.FEMINIE)
        t.add_abridge("НАБ.")
        t.add_abridge("НАБЕР.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("АЛЛЕЯ", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        t.add_abridge("АЛ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new306("АЛЕЯ", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.FEMINIE)
        t.add_abridge("АЛ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new86("ALLEY", StreetItemType.NOUN, 0)
        t.add_abridge("ALY.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("АВЕНЮ", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        t.add_variant("АВЕНЬЮ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ПРОСЕКА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_variant("ПРОСЕК", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ПЛОЩАДКА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_abridge("ПЛ-КА")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new306("ПРОСІКА", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.FEMINIE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ТРАКТ", StreetItemType.NOUN, 1, MorphGender.NEUTER)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ШОССЕ", StreetItemType.NOUN, 1, MorphGender.NEUTER)
        t.add_abridge("Ш.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new306("ШОСЕ", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.NEUTER)
        t.add_abridge("Ш.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new86("ROAD", StreetItemType.NOUN, 1)
        t.add_abridge("RD.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("МИКРОРАЙОН", StreetItemType.NOUN, 0, MorphGender.MASCULINE)
        t.add_abridge("МКР.")
        t.add_abridge("МКН.")
        t.add_abridge("МИКР-Н")
        t.add_abridge("МИКР.")
        t.add_abridge("МКР-Н")
        t.add_abridge("МКР-ОН")
        t.add_abridge("МКРН.")
        t.add_abridge("М-Н")
        t.add_abridge("М-ОН")
        t.add_abridge("М.Р-Н")
        t.add_abridge("МИКР-ОН")
        t.add_variant("МИКРОН", False)
        t.add_abridge("М/Р")
        t.add_variant("МІКРОРАЙОН", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("КВАРТАЛ", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        t.add_abridge("КВАРТ.")
        t.add_abridge("КВ-Л")
        t.add_abridge("КВ.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("КАДАСТРОВЫЙ КВАРТАЛ", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        t.add_abridge("КАД.КВАРТ.")
        t.add_abridge("КАД.КВ-Л")
        t.add_abridge("КАД.КВ.")
        t.add_abridge("КАД.КВАРТАЛ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("ТОРФЯНОЙ УЧАСТОК", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        t.add_variant("ТОРФУЧАСТОК", False)
        t.add_variant("ТОРФОУЧАСТОК", False)
        t.add_abridge("ТОРФ.УЧАСТОК")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new305("МОСТ", StreetItemType.NOUN, 2, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new306("МІСТ", StreetItemType.NOUN, MorphLang.UA, 2, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new86("PLAZA", StreetItemType.NOUN, 1)
        t.add_abridge("PLZ")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new346("СТАНЦИЯ МЕТРО", "МЕТРО", StreetItemType.NOUN, 0, MorphGender.FEMINIE)
        StreetItemToken.__m_metro = t
        t.add_variant("СТАНЦІЯ МЕТРО", False)
        t.add_abridge("СТ.МЕТРО")
        t.add_abridge("СТ.М.")
        t.add_abridge("МЕТРО")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new347("АВТОДОРОГА", StreetItemType.NOUN, "ФАД", 0, MorphGender.FEMINIE)
        StreetItemToken.__m_road = t
        t.add_variant("ФЕДЕРАЛЬНАЯ АВТОДОРОГА", False)
        t.add_variant("АВТОМОБИЛЬНАЯ ДОРОГА", False)
        t.add_variant("АВТОТРАССА", False)
        t.add_variant("ФЕДЕРАЛЬНАЯ ТРАССА", False)
        t.add_variant("ФЕДЕР ТРАССА", False)
        t.add_variant("АВТОМАГИСТРАЛЬ", False)
        t.add_abridge("А/Д")
        t.add_abridge("ФЕДЕР.ТРАССА")
        t.add_abridge("ФЕД.ТРАССА")
        t.add_variant("ГОСТРАССА", False)
        t.add_variant("ГОС.ТРАССА", False)
        t.add_variant("АВТОМАГ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new346("ДОРОГА", "АВТОДОРОГА", StreetItemType.NOUN, 1, MorphGender.FEMINIE)
        t.add_variant("ТРАССА", False)
        t.add_variant("МАГИСТРАЛЬ", False)
        t.add_abridge("ДОР.")
        t.add_variant("ДОР", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new306("АВТОДОРОГА", StreetItemType.NOUN, MorphLang.UA, 0, MorphGender.FEMINIE)
        t.add_variant("ФЕДЕРАЛЬНА АВТОДОРОГА", False)
        t.add_variant("АВТОМОБІЛЬНА ДОРОГА", False)
        t.add_variant("АВТОТРАСА", False)
        t.add_variant("ФЕДЕРАЛЬНА ТРАСА", False)
        t.add_variant("АВТОМАГІСТРАЛЬ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new350("ДОРОГА", "АВТОДОРОГА", StreetItemType.NOUN, MorphLang.UA, 1, MorphGender.FEMINIE)
        t.add_variant("ТРАСА", False)
        t.add_variant("МАГІСТРАЛЬ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new351("МОСКОВСКАЯ КОЛЬЦЕВАЯ АВТОМОБИЛЬНАЯ ДОРОГА", "МКАД", StreetItemType.FIX, MorphGender.FEMINIE)
        t.add_variant("МОСКОВСКАЯ КОЛЬЦЕВАЯ АВТОДОРОГА", False)
        StreetItemToken._m_ontology.add(t)
        StreetItemToken._m_ontology.add(Termin._new84("САДОВОЕ КОЛЬЦО", StreetItemType.FIX))
        StreetItemToken._m_ontology.add(Termin._new84("БУЛЬВАРНОЕ КОЛЬЦО", StreetItemType.FIX))
        StreetItemToken._m_ontology.add(Termin._new84("ТРАНСПОРТНОЕ КОЛЬЦО", StreetItemType.FIX))
        t = Termin._new355("ПОЧТОВОЕ ОТДЕЛЕНИЕ", StreetItemType.NOUN, "ОПС", MorphGender.NEUTER)
        t.add_abridge("П.О.")
        t.add_abridge("ПОЧТ.ОТД.")
        t.add_abridge("ПОЧТОВ.ОТД.")
        t.add_abridge("ПОЧТОВОЕ ОТД.")
        t.add_abridge("П/О")
        t.add_variant("ОТДЕЛЕНИЕ ПОЧТОВОЙ СВЯЗИ", False)
        t.add_variant("ПОЧТАМТ", False)
        t.add_variant("ГЛАВПОЧТАМТ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new302("БУДКА", StreetItemType.NOUN, MorphGender.FEMINIE)
        t.add_variant("ЖЕЛЕЗНОДОРОЖНАЯ БУДКА", False)
        t.add_abridge("Ж/Д БУДКА")
        t.add_abridge("ЖЕЛ.ДОР.БУДКА")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new302("КАЗАРМА", StreetItemType.NOUN, MorphGender.FEMINIE)
        t.add_variant("ЖЕЛЕЗНОДОРОЖНАЯ КАЗАРМА", False)
        t.add_abridge("Ж/Д КАЗАРМА")
        t.add_abridge("ЖЕЛ.ДОР.КАЗАРМА")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new302("СТОЯНКА", StreetItemType.NOUN, MorphGender.FEMINIE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new302("ПУНКТ", StreetItemType.NOUN, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new302("РАЗЪЕЗД", StreetItemType.NOUN, MorphGender.MASCULINE)
        t.add_abridge("РЗД")
        t.add_abridge("Ж/Д РАЗЪЕЗД")
        t.add_variant("ЖЕЛЕЗНОДОРОЖНЫЙ РАЗЪЕЗД", False)
        t.add_abridge("ЖЕЛ.ДОР.РАЗЪЕЗД")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new302("ЗАЕЗД", StreetItemType.NOUN, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new302("ПЕРЕЕЗД", StreetItemType.NOUN, MorphGender.MASCULINE)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("БОЛЬШОЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("БОЛ.")
        t.add_abridge("Б.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("ВЕЛИКИЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("ВЕЛ.")
        t.add_abridge("В.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("МАЛЫЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("МАЛ.")
        t.add_abridge("М.")
        t.add_variant("МАЛИЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("СРЕДНИЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("СРЕД.")
        t.add_abridge("СР.")
        t.add_abridge("С.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new85("СЕРЕДНІЙ", StreetItemType.STDADJECTIVE, MorphLang.UA)
        t.add_abridge("СЕРЕД.")
        t.add_abridge("СЕР.")
        t.add_abridge("С.")
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("ВЕРХНИЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("ВЕРХН.")
        t.add_abridge("ВЕРХ.")
        t.add_abridge("ВЕР.")
        t.add_abridge("В.")
        t.add_variant("ВЕРХНІЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("НИЖНИЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("НИЖН.")
        t.add_abridge("НИЖ.")
        t.add_abridge("Н.")
        t.add_variant("НИЖНІЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("СТАРЫЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("СТАР.")
        t.add_abridge("СТ.")
        t.add_variant("СТАРИЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("НОВЫЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("НОВ.")
        t.add_abridge("Н.")
        t.add_variant("НОВИЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("КРАСНЫЙ", StreetItemType.STDADJECTIVE)
        t.add_abridge("КРАСН.")
        t.add_abridge("КР.")
        t.add_abridge("КРАС.")
        t.add_variant("ЧЕРВОНИЙ", False)
        StreetItemToken._m_ontology.add(t)
        t = Termin._new84("НОМЕР", StreetItemType.STDADJECTIVE)
        t.add_abridge("N")
        t.add_abridge("№")
        t.add_abridge("НОМ.")
        StreetItemToken._m_ontology.add(t)
        for s in ["ПРОЕКТИРУЕМЫЙ", "ЮНЫХ ЛЕНИНЦЕВ;ЮН. ЛЕНИНЦЕВ", "МАРКСА И ЭНГЕЛЬСА;КАРЛА МАРКСА И ФРИДРИХА ЭНГЕЛЬСА", "БАКИНСКИХ КОМИССАРОВ;БАК.КОМИССАРОВ;Б.КОМИССАРОВ", "САККО И ВАНЦЕТТИ", "СЕРП И МОЛОТ", "ЗАВОДА СЕРП И МОЛОТ", "ШАРЛЯ ДЕ ГОЛЛЯ;ДЕ ГОЛЛЯ", "МИНИНА И ПОЖАРСКОГО", "ХО ШИ МИНА;ХОШИМИНА", "ЗОИ И АЛЕКСАНДРА КОСМОДЕМЬЯНСКИХ;З.И А.КОСМОДЕМЬЯНСКИХ;З.А.КОСМОДЕМЬЯНСКИХ", "АРМАНД;ИНЕССЫ АРМАНД", "МИРА", "СВОБОДЫ", "РИМСКОГО-КОРСАКОВА", "ПЕТРА И ПАВЛА"]: 
            pp = Utils.splitString(s, ';', False)
            t = Termin._new136(pp[0], StreetItemType.STDNAME, True)
            kk = 1
            while kk < len(pp): 
                if (pp[kk].find('.') > 0): 
                    t.add_abridge(pp[kk])
                else: 
                    t.add_variant(pp[kk], False)
                kk += 1
            StreetItemToken._m_ontology.add(t)
        for s in NameToken._standard_names: 
            pp = Utils.splitString(s, ';', False)
            t = Termin._new136(pp[0], StreetItemType.STDNAME, True)
            kk = 1
            while kk < len(pp): 
                if (pp[kk].find('.') > 0 or pp[kk].find('/') > 0): 
                    t.add_abridge(pp[kk])
                elif (t.acronym is None and (len(pp[kk]) < 4)): 
                    t.acronym = pp[kk]
                else: 
                    t.add_variant(pp[kk], False)
                kk += 1
            StreetItemToken._m_ontology.add(t)
        for s in ["МАРТА", "МАЯ", "ОКТЯБРЯ", "НОЯБРЯ", "БЕРЕЗНЯ", "ТРАВНЯ", "ЖОВТНЯ", "ЛИСТОПАДА", "ДОРОЖКА", "ЛУЧ", "НАДЕЛ", "ПОЛЕ", "СКЛОН"]: 
            StreetItemToken._m_ontology.add(Termin._new84(s, StreetItemType.STDNAME))
        for s in ["МАРШАЛА", "ГЕНЕРАЛА", "ГЕНЕРАЛ-МАЙОРА", "ГЕНЕРАЛ-ЛЕЙТЕНАНТА", "ГЕНЕРАЛ-ПОЛКОВНИКА", "АДМИРАЛА", "КОНТРАДМИРАЛА", "КОСМОНАВТА", "ЛЕТЧИКА", "ЛЕТЧИКА-ИСПЫТАТЕЛЯ", "ПИЛОТА", "ПОГРАНИЧНИКА", "ПУТЕШЕСТВЕННИКА", "ПАРТИЗАНА", "АТАМАНА", "ВОЕВОДЫ", "ТАНКИСТА", "ОРУЖЕЙНИКА", "ПОЛЯРНИКА", "АВИАКОНСТРУКТОРА", "АРХИТЕКТОРА", "ГЛАВНОГО АРХИТЕКТОРА", "СКУЛЬПТОРА", "ХУДОЖНИКА", "КОНСТРУКТОРА", "ГЛАВНОГО КОНСТРУКТОРА", "АКАДЕМИКА", "ПРОФЕССОРА", "КОМПОЗИТОРА", "ПИСАТЕЛЯ", "ПОЭТА", "ДИРИЖЕРА", "ГЕРОЯ", "БРАТЬЕВ", "ЛЕЙТЕНАНТА", "СТАРШЕГО ЛЕЙТЕНАНТА", "КАПИТАНА", "КАПИТАНА-ЛЕЙТЕНАНТА", "МАЙОРА", "ПОДПОЛКОВНИКА", "ПОЛКОВНИКА", "СЕРЖАНТА", "МЛАДШЕГО СЕРЖАНТА", "СТАРШЕГО СЕРЖАНТА", "ЕФРЕЙТОРА", "СТАРШИНЫ", "ПРАПОРЩИКА", "СТАРШЕГО ПРАПОРЩИКА", "ПОЛИТРУКА", "МИТРОПОЛИТА", "ПАТРИАРХА", "ИЕРЕЯ", "ПРОТОИЕРЕЯ", "МОНАХА", "СВЯТОГО", "СВЯТИТЕЛЯ", "ШЕЙХА", "БАЛЕРИНЫ", "ПЕВИЦЫ", "ХИРУРГА", "НАРОДНОГО АРТИСТА"]: 
            StreetItemToken.__m_std_ont_misc.add(Termin(s))
            t = Termin._new84(s, StreetItemType.STDPARTOFNAME)
            if (s == "СВЯТОГО" or s == "СВЯТИТЕЛЯ"): 
                t.add_abridge("СВ.")
                t.add_abridge("СВЯТ.")
            else: 
                t.add_all_abridges(0, 0, 2)
                t.add_all_abridges(2, 5, 0)
                if (s == "ПРОФЕССОРА"): 
                    t.add_variant("ПРОФЕСОРА", False)
            StreetItemToken._m_ontology.add(t)
        for s in ["МАРШАЛА", "ГЕНЕРАЛА", "ГЕНЕРАЛ-МАЙОРА", "ГЕНЕРАЛ-ЛЕЙТЕНАНТА", "ГЕНЕРАЛ-ПОЛКОВНИКА", "АДМІРАЛА", "КОНТРАДМІРАЛА", "КОСМОНАВТА", "ЛЬОТЧИКА", " ПРИКОРДОННИКА", " МАНДРІВНИКА", "ПАРТИЗАНА", "ОТАМАНА", "ТАНКІСТА", "АВІАКОНСТРУКТОРА", "АРХІТЕКТОРА", "СКУЛЬПТОРА", "ХУДОЖНИКА", "КОНСТРУКТОРА", "АКАДЕМІКА", "ПРОФЕСОРА", "КОМПОЗИТОРА", "ПИСЬМЕННИКА", "ПОЕТА", "ДИРИГЕНТА", "ГЕРОЯ", "ЛЕЙТЕНАНТА", "КАПІТАНА", "КАПІТАНА-ЛЕЙТЕНАНТА", "МАЙОРА", "ПІДПОЛКОВНИКА", "ПОЛКОВНИКА", "СЕРЖАНТА", "ЄФРЕЙТОРА", " СТАРШИНИ", " ПРАПОРЩИКА", "ПОЛІТРУКА", "ПОЛІЦІЇ", "МІЛІЦІЇ", "ГВАРДІЇ", "АРМІЇ", "МИТРОПОЛИТА", "ПАТРІАРХА", "ІЄРЕЯ", "ПРОТОІЄРЕЯ", "ЧЕНЦЯ", "СВЯТОГО", "СВЯТИТЕЛЯ"]: 
            StreetItemToken.__m_std_ont_misc.add(Termin(s))
            t = Termin._new85(s, StreetItemType.STDPARTOFNAME, MorphLang.UA)
            if (s == "СВЯТОГО" or s == "СВЯТИТЕЛЯ"): 
                t.add_abridge("СВ.")
                t.add_abridge("СВЯТ.")
            else: 
                t.add_all_abridges(0, 0, 2)
                t.add_all_abridges(2, 5, 0)
                t.add_abridge("ГЛ." + s)
                t.add_abridge("ГЛАВ." + s)
            StreetItemToken._m_ontology.add(t)
        t = Termin._new84("ЛЕНИНСКИЕ ГОРЫ", StreetItemType.FIX)
        StreetItemToken._m_ontology.add(t)
        for s in ["КРАСНЫЙ", "СОВЕТСТКИЙ", "ЛЕНИНСКИЙ"]: 
            StreetItemToken.__m_std_adj.add(Termin(s))
        for s in ["НЕТ", "НЕ УКАЗАНА", "НЕ ЗАДАНА", "ОТСУТСТВУЕТ"]: 
            StreetItemToken._m_ontology.add(Termin._new84(s, StreetItemType.ABSENT))
        StreetItemToken.__m_misc_nouns = TerminCollection()
        for s in ["ВАЛ", "ПОЛЕ", "МАГИСТРАЛЬ", "СПУСК", "ВЗВОЗ", "РЯД", "СЛОБОДА", "РОЩА", "ПРУД", "СЪЕЗД", "КОЛЬЦО", "МАГІСТРАЛЬ", "УЗВІЗ", "УЗВІЗ", "ГАЙ", "СТАВОК", "ЗЇЗД", "КІЛЬЦЕ"]: 
            StreetItemToken.__m_misc_nouns.add(Termin(s))
    
    @staticmethod
    def check_std_name(t : 'Token') -> 'Token':
        if (t is None): 
            return None
        if (StreetItemToken.__m_std_adj.try_parse(t, TerminParseAttr.NO) is not None): 
            return t
        tok = StreetItemToken._m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        if ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.STDNAME): 
            return tok.end_token
        return None
    
    @staticmethod
    def check_keyword(t : 'Token') -> bool:
        if (t is None): 
            return False
        tok = StreetItemToken._m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return False
        return (Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.NOUN
    
    @staticmethod
    def check_onto(t : 'Token') -> bool:
        if (t is None): 
            return False
        tok = StreetItemToken._m_ontology_ex.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return False
        return True
    
    _m_ontology = None
    
    _m_ontology_ex = None
    
    __m_std_ont_misc = None
    
    __m_std_adj = None
    
    __m_misc_nouns = None
    
    __m_prospect = None
    
    __m_metro = None
    
    __m_road = None
    
    __m_block = None
    
    __m_reg_tails = None
    
    @staticmethod
    def _is_region(txt : str) -> bool:
        txt = txt.upper()
        for v in StreetItemToken.__m_reg_tails: 
            if (LanguageHelper.ends_with(txt, v)): 
                return True
        return False
    
    __m_spec_tails = None
    
    @staticmethod
    def _is_spec(txt : str) -> bool:
        txt = txt.upper()
        for v in StreetItemToken.__m_spec_tails: 
            if (LanguageHelper.ends_with(txt, v)): 
                return True
        return False
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.typ = StreetItemType.NOUN
        self.alt_typ = StreetItemType.NOUN
        self.termin = None;
        self.alt_termin = None;
        self.exist_street = None;
        self.number_type = NumberSpellingType.UNDEFINED
        self.number_has_prefix = False
        self.is_number_km = False
        self.value = None;
        self.alt_value = None;
        self.alt_value2 = None;
        self.misc = None;
        self.is_abridge = False
        self.is_in_dictionary = False
        self.is_in_brackets = False
        self.has_std_suffix = False
        self.noun_is_doubt_coef = 0
        self.noun_can_be_name = False
        self.is_road_name = False
        self.std_adj_version = None;
        self.next_item = None;
        self.is_railway = False
        self._cond = None;
        self._no_geo_in_this_token = False
        self._org0_ = None;
        self._orto_terr = None;
        self._area = None;
        self._city = None;
    
    @property
    def is_road(self) -> bool:
        if (self.termin is None): 
            return False
        if ((self.termin.canonic_text == "АВТОДОРОГА" or self.termin.canonic_text == "ШОССЕ" or self.termin.canonic_text == "ТРАКТ") or self.termin.canonic_text == "АВТОШЛЯХ" or self.termin.canonic_text == "ШОСЕ"): 
            return True
        return False
    
    def clone(self) -> 'StreetItemToken':
        res = StreetItemToken(self.begin_token, self.end_token)
        res.morph = self.morph
        res.typ = self.typ
        res.alt_typ = self.alt_typ
        res.termin = self.termin
        res.alt_termin = self.alt_termin
        res.value = self.value
        res.alt_value = self.alt_value
        res.alt_value2 = self.alt_value2
        res.is_railway = self.is_railway
        res.is_road_name = self.is_road_name
        res.noun_can_be_name = self.noun_can_be_name
        res.noun_is_doubt_coef = self.noun_is_doubt_coef
        res.has_std_suffix = self.has_std_suffix
        res.is_in_brackets = self.is_in_brackets
        res.is_abridge = self.is_abridge
        res.is_in_dictionary = self.is_in_dictionary
        res.exist_street = self.exist_street
        res.misc = self.misc
        res.number_type = self.number_type
        res.number_has_prefix = self.number_has_prefix
        res.is_number_km = self.is_number_km
        res._cond = self._cond
        res._org0_ = self._org0_
        if (self._orto_terr is not None): 
            res._orto_terr = self._orto_terr.clone()
        res._city = self._city
        res._area = self._area
        if (self.std_adj_version is not None): 
            res.std_adj_version = self.std_adj_version.clone()
        if (self.next_item is not None): 
            res.next_item = self.next_item.clone()
        return res
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0}".format(Utils.enumToString(self.typ)), end="", file=res, flush=True)
        if (self.value is not None): 
            print(" {0}".format(self.value), end="", file=res, flush=True)
            if (self.alt_value is not None): 
                print("/{0}".format(self.alt_value), end="", file=res, flush=True)
            if (self.is_number_km): 
                print("км", end="", file=res)
        if (self.misc is not None): 
            print(" <{0}>".format(self.misc), end="", file=res, flush=True)
        if (self.exist_street is not None): 
            print(" {0}".format(str(self.exist_street)), end="", file=res, flush=True)
        if (self.termin is not None): 
            print(" {0}".format(str(self.termin)), end="", file=res, flush=True)
            if (self.alt_termin is not None): 
                print("/{0}".format(str(self.alt_termin)), end="", file=res, flush=True)
        else: 
            print(" {0}".format(super().__str__()), end="", file=res, flush=True)
        if (self._org0_ is not None): 
            print(" Org: {0}".format(self._org0_), end="", file=res, flush=True)
        if (self.is_abridge): 
            print(" (?)", end="", file=res)
        if (self._orto_terr is not None): 
            print(" TERR: {0}".format(self._orto_terr), end="", file=res, flush=True)
        if (self._area is not None): 
            print(" AREA: {0}".format(self._area), end="", file=res, flush=True)
        if (self.std_adj_version is not None): 
            print(" + (?) {0}".format(str(self.std_adj_version)), end="", file=res, flush=True)
        if (self.next_item is not None): 
            print(" + {0}".format(str(self.next_item)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def __is_surname(self) -> bool:
        if (self.typ != StreetItemType.NAME): 
            return False
        if (not (isinstance(self.end_token, TextToken))): 
            return False
        nam = self.end_token.term
        if (len(nam) > 4): 
            if (LanguageHelper.ends_with_ex(nam, "А", "Я", "КО", "ЧУКА")): 
                if (not LanguageHelper.ends_with_ex(nam, "АЯ", "ЯЯ", None, None)): 
                    mc = self.end_token.get_morph_class_in_dictionary()
                    if (not mc.is_noun): 
                        return True
        return False
    
    SPEED_REGIME = False
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        if (not StreetItemToken.SPEED_REGIME): 
            return
        ad = GeoAnalyzer._get_data(t0)
        if (ad is None): 
            return
        ad.sregime = False
        t = t0
        while t is not None: 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            prev = None
            kk = 0
            tt = t.previous
            first_pass3790 = True
            while True:
                if first_pass3790: first_pass3790 = False
                else: tt = tt.previous; kk += 1
                if (not (tt is not None and (kk < 10))): break
                dd = Utils.asObjectOrNull(tt.tag, GeoTokenData)
                if (dd is None or dd.street is None): 
                    continue
                if (dd.street.end_token.next0_ == t): 
                    prev = dd.street
                if (t.previous is not None and t.previous.is_hiphen and dd.street.end_token.next0_ == t.previous): 
                    prev = dd.street
            str0_ = StreetItemToken.try_parse(t, prev, False, ad)
            if (str0_ is not None): 
                if (d is None): 
                    d = GeoTokenData(t)
                d.street = str0_
                if (str0_._no_geo_in_this_token): 
                    if (((prev is not None and prev.typ == StreetItemType.NOUN)) or StreetItemToken.check_keyword(str0_.end_token.next0_)): 
                        tt = str0_.begin_token
                        while tt is not None and tt.end_char <= str0_.end_char: 
                            dd = Utils.asObjectOrNull(tt.tag, GeoTokenData)
                            if (dd is None): 
                                dd = GeoTokenData(tt)
                            dd.no_geo = True
                            tt = tt.next0_
            t = t.next0_
        ad.sregime = True
    
    @staticmethod
    def try_parse(t : 'Token', prev : 'StreetItemToken'=None, in_search : bool=False, ad : 'GeoAnalyzerData'=None) -> 'StreetItemToken':
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.internal.OrgTypToken import OrgTypToken
        if (t is None): 
            return None
        if ((isinstance(t, TextToken)) and t.length_char == 1 and t.is_char_of(",.:")): 
            return None
        if (ad is None): 
            ad = (Utils.asObjectOrNull(GeoAnalyzer._get_data(t), GeoAnalyzerData))
        if (ad is None): 
            return None
        if ((StreetItemToken.SPEED_REGIME and ((ad.sregime or ad.all_regime)) and not in_search) and not (isinstance(t, ReferentToken))): 
            if ((isinstance(t, TextToken)) and t.is_char('м')): 
                pass
            else: 
                d = Utils.asObjectOrNull(t.tag, GeoTokenData)
                if (d is None): 
                    return None
                if (d.street is not None): 
                    if (d.street._cond is None): 
                        return d.street
                    if (d.street._cond.check()): 
                        return d.street
                    return None
                if (d.org0_ is not None): 
                    return StreetItemToken._new262(t, d.org0_.end_token, StreetItemType.FIX, d.org0_)
                return None
        if (ad.slevel > 3): 
            return None
        ad.slevel += 1
        res = StreetItemToken._try_parse(t, False, prev, in_search)
        if (res is not None and res.typ != StreetItemType.NOUN): 
            if (res.typ == StreetItemType.NAME and res.begin_token == res.end_token and (isinstance(res.begin_token, TextToken))): 
                tt2 = Utils.asObjectOrNull(res.begin_token, TextToken)
                if (tt2.term == "ИЖС" or tt2.term == "ЛПХ" or tt2.term == "ДУБЛЬ"): 
                    ad.slevel -= 1
                    return None
                ait = AddressItemToken.try_parse_pure_item(t, None, None)
                if ((ait is not None and ait.typ == AddressItemType.HOUSE and ait.value is not None) and ait.value != "0"): 
                    ad.slevel -= 1
                    return None
            tt = Utils.asObjectOrNull(res.end_token.next0_, TextToken)
            if (tt is not None and res.typ == StreetItemType.NUMBER and tt.is_value("ОТДЕЛЕНИЕ", None)): 
                res.end_token = tt
                res.number_has_prefix = True
            elif (tt is not None and res.typ == StreetItemType.NUMBER and tt.is_char('+')): 
                res2 = StreetItemToken._try_parse(tt.next0_, False, prev, in_search)
                if (res2 is not None and res2.typ == StreetItemType.NUMBER): 
                    res.end_token = res2.end_token
                    res.value = "{0}+{1}".format(res.value, res2.value)
            elif (tt is not None and tt.is_char('(')): 
                if (res.value is None): 
                    res.value = MiscHelper.get_text_value(res.begin_token, res.end_token, GetTextAttr.NO)
                ait = AddressItemToken.try_parse(tt.next0_, False, None, None)
                if ((ait is not None and ait.typ == AddressItemType.STREET and ait.end_token.next0_ is not None) and ait.end_token.next0_.is_char(')')): 
                    res._orto_terr = ait.clone()
                    res._orto_terr.end_token = ait.end_token.next0_
                    res.end_token = res._orto_terr.end_token
                else: 
                    sit = StreetItemToken.try_parse(tt.next0_, None, False, None)
                    if ((sit is not None and ((sit.typ == StreetItemType.NAME or sit.typ == StreetItemType.STDNAME)) and sit.end_token.next0_ is not None) and sit.end_token.next0_.is_char(')')): 
                        oty = OrgTypToken.try_parse(tt.next0_, False, None)
                        if (oty is not None and oty.end_token == sit.end_token): 
                            res.end_token = sit.end_token.next0_
                        else: 
                            ait = AddressItemToken(AddressItemType.STREET, tt.next0_, sit.end_token)
                            stre = StreetReferent()
                            stre.kind = StreetKind.AREA
                            stre._add_typ("территория")
                            stre._add_name(sit)
                            ait.referent = (stre)
                            res._orto_terr = ait
                            res.end_token = sit.end_token.next0_
            if (res.begin_token == res.end_token and ((res.typ == StreetItemType.NAME or res.typ == StreetItemType.STDNAME or res.typ == StreetItemType.STDPARTOFNAME))): 
                end = MiscLocationHelper.check_name_long(res)
                if ((isinstance(end, ReferentToken)) and (isinstance(end.get_referent(), DateReferent))): 
                    end = (None)
                if (end is not None): 
                    tok = StreetItemToken._m_ontology.try_parse(end, TerminParseAttr.NO)
                    if (tok is not None): 
                        if ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.NOUN or (Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.STDPARTOFNAME): 
                            end = (None)
                if (end is not None): 
                    res.end_token = end
                    if (res.value is None): 
                        res.value = MiscHelper.get_text_value(res.begin_token, end, GetTextAttr.NO)
                    else: 
                        res.value = "{0} {1}".format(res.value, MiscHelper.get_text_value(res.begin_token.next0_, end, GetTextAttr.NO))
                        if (res.alt_value is not None): 
                            res.alt_value = "{0} {1}".format(res.alt_value, MiscHelper.get_text_value(res.begin_token.next0_, end, GetTextAttr.NO))
                    if (res.begin_token.next0_ == res.end_token): 
                        mc = res.begin_token.get_morph_class_in_dictionary()
                        mc1 = res.end_token.get_morph_class_in_dictionary()
                        if (((mc.is_proper_name and not res.begin_token.is_value("СЛАВА", None))) or mc1.is_proper_surname): 
                            res.alt_value2 = res.alt_value
                            res.alt_value = MiscHelper.get_text_value(end, end, GetTextAttr.NO)
                        elif (mc.is_proper_surname and mc1.is_proper_name): 
                            res.alt_value2 = res.alt_value
                            res.alt_value = MiscHelper.get_text_value(res.begin_token, res.begin_token, GetTextAttr.NO)
        if (res is not None and res.is_road): 
            tt = res.end_token.next0_
            first_pass3791 = True
            while True:
                if first_pass3791: first_pass3791 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None): 
                    if (npt.end_token.is_value("ПОЛЬЗОВАНИЕ", None) or npt.end_token.is_value("ЗНАЧЕНИЕ", None)): 
                        tt = npt.end_token
                        res.end_token = tt
                        continue
                break
        if ((res is None and t.is_char('(') and MiscLocationHelper.is_user_param_address(t)) and StreetItemToken._m_ontology.try_parse(t.next0_, TerminParseAttr.NO) is not None): 
            next0__ = StreetItemToken.try_parse(t.next0_, None, False, None)
            if ((next0__ is not None and next0__.typ == StreetItemType.NOUN and next0__.end_token.next0_ is not None) and next0__.end_token.next0_.is_char(')')): 
                next0__.begin_token = t
                next0__.end_token = next0__.end_token.next0_
                res = next0__
        ad.slevel -= 1
        return res
    
    @staticmethod
    def _try_parse(t : 'Token', ignore_onto : bool, prev : 'StreetItemToken', in_search : bool) -> 'StreetItemToken':
        from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.geo.internal.NumToken import NumToken
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        from pullenti.ner.geo.internal.NameToken import NameToken
        if (t is None): 
            return None
        res1 = StreetItemToken._try_parse_spec(t, prev)
        if (res1 is not None and ((res1[0].typ == StreetItemType.NAME or res1[0].typ == StreetItemType.STDNAME))): 
            return res1[0]
        if ((prev is None and t.next0_ is not None and t.next0_.is_hiphen) and MiscLocationHelper.is_user_param_address(t)): 
            res1 = StreetItemToken._try_parse_spec(t, prev)
            if (res1 is not None and res1[0].typ == StreetItemType.NAME): 
                return res1[0]
        if (t.is_value("ТЕР", None)): 
            pass
        if ((t.is_value("А", None) or t.is_value("АД", None) or t.is_value("АВТ", None)) or t.is_value("АВТОДОР", None)): 
            tt1 = t
            if (t.is_value("А", None)): 
                tt1 = t.next0_
                if (tt1 is not None and tt1.is_char_of("\\/")): 
                    tt1 = tt1.next0_
                elif ((tt1 is not None and not tt1.is_whitespace_after and tt1.is_char_of(",.")) and MiscLocationHelper.is_user_param_address(tt1)): 
                    tt1 = tt1.next0_
                if (tt1 is not None and ((tt1.is_value("Д", None) or tt1.is_value("М", None)))): 
                    if (tt1.next0_ is not None and tt1.next0_.is_char('.')): 
                        tt1 = tt1.next0_
                else: 
                    tt1 = (None)
            elif (tt1.next0_ is not None and tt1.next0_.is_char('.')): 
                tt1 = tt1.next0_
            if (tt1 is not None): 
                if (t == tt1 and (t.length_char < 5) and not MiscLocationHelper.is_user_param_address(t)): 
                    pass
                else: 
                    res = StreetItemToken._new382(t, tt1, StreetItemType.NOUN, StreetItemToken.__m_road)
                    if (res.length_char >= 4): 
                        return res
                    if (prev is not None and ((prev.is_road_name or prev.is_road))): 
                        return res
                    next0__ = StreetItemToken.try_parse(tt1.next0_, res, False, None)
                    if (next0__ is not None and next0__.is_road_name): 
                        return res
                    if (t.previous is not None): 
                        if (t.previous.is_value("КМ", None) or t.previous.is_value("КИЛОМЕТР", None)): 
                            return res
        if ((((t.is_value("Ж", None) or t.is_value("ЖЕЛ", None))) and t.next0_ is not None and t.next0_.is_char_of("\\/")) and (isinstance(t.next0_.next0_, TextToken)) and t.next0_.next0_.is_value("ДОРОЖНЫЙ", None)): 
            return StreetItemToken._new284(t, t.next0_.next0_, StreetItemType.NAME, "ЖЕЛЕЗНО" + t.next0_.next0_.term)
        if ((((t.is_value("ФЕДЕРАЛЬНЫЙ", None) or t.is_value("ГОСУДАРСТВЕННЫЙ", None) or t.is_value("АВТОМОБИЛЬНЫЙ", None)) or t.is_value("ФЕД", None) or t.is_value("ФЕДЕРАЛ", None)) or t.is_value("ГОС", None) or t.is_value("АВТО", None)) or t.is_value("АВТОМОБ", None)): 
            tt2 = t.next0_
            if (tt2 is not None and tt2.is_char('.')): 
                tt2 = tt2.next0_
            tok2 = StreetItemToken._m_ontology.try_parse(tt2, TerminParseAttr.NO)
            if (tok2 is not None and tok2.termin.canonic_text == "АВТОДОРОГА"): 
                return StreetItemToken._new382(t, tok2.end_token, StreetItemType.NOUN, tok2.termin)
        if (t.is_hiphen and prev is not None and prev.typ == StreetItemType.NAME): 
            num = NumberHelper.try_parse_roman(t.next0_)
            if (num is not None): 
                return StreetItemToken._new294(t, num.end_token, StreetItemType.NUMBER, num.value, True)
        if (t.is_value("НОЛЬ", None) or t.is_value("НУЛЬ", None)): 
            if (isinstance(t.next0_, NumberToken)): 
                return StreetItemToken._new284(t, t.next0_, StreetItemType.NUMBER, "0" + t.next0_.value)
        if (t.is_newline_before): 
            if (t.is_value("ТАБЛИЦА", None) or t.is_value("РИСУНОК", None) or t.is_value("ФОРМУЛА", None)): 
                return None
        t0 = t
        tn = None
        org1 = OrgItemToken.try_parse(t, None)
        if (org1 is not None): 
            if (org1.is_building): 
                return None
            if (org1.is_gsk or not org1.is_doubt or org1.has_terr_keyword): 
                return StreetItemToken._new262(t0, org1.end_token, StreetItemType.FIX, org1)
            if (BracketHelper.is_bracket(t, True)): 
                next0__ = StreetItemToken.try_parse(t.next0_, prev, False, None)
                if (next0__ is not None): 
                    if (BracketHelper.is_bracket(next0__.end_token.next0_, True)): 
                        if (next0__.typ == StreetItemType.NAME and next0__.value is None): 
                            next0__.value = MiscHelper.get_text_value_of_meta_token(next0__, GetTextAttr.NO)
                        next0__.begin_token = t0
                        next0__.end_token = next0__.end_token.next0_
                    return next0__
        geo1 = Utils.asObjectOrNull(t.get_referent(), GeoReferent)
        if (geo1 is not None and geo1.is_city and MiscLocationHelper.is_user_param_address(t)): 
            for ty in geo1.typs: 
                if ((ty == "поселок" or ty == "станция" or ty == "слобода") or ty == "хутор"): 
                    return StreetItemToken._new388(t0, t, StreetItemType.FIX, geo1)
        if (isinstance(t, TextToken)): 
            if (t.is_value("ТЕРРИТОРИЯ", None) or t.term == "ТЕР" or t.term == "ТЕРР"): 
                return None
        nnn2 = NumToken.try_parse(t, GeoTokenType.STREET)
        if (nnn2 is not None and ((nnn2.has_prefix or nnn2.is_cadaster_number))): 
            return StreetItemToken._new389(t, nnn2.end_token, nnn2.value, StreetItemType.NUMBER, True)
        if (prev is not None): 
            pass
        has_named = False
        if (t.is_value("ИМЕНИ", "ІМЕНІ")): 
            tn = t
        elif (t.is_value("ПАМЯТИ", "ПАМЯТІ")): 
            nam = NameToken.try_parse(t, GeoTokenType.STREET, 0, False)
            if (nam is not None and nam.end_token != t and nam.number is None): 
                pass
            elif (t.is_newline_after or ((t.next0_ is not None and t.next0_.is_comma))): 
                pass
            else: 
                tn = t
        elif (t.is_value("ИМ", None) or t.is_value("ІМ", None)): 
            tn = t
            if (tn.next0_ is not None and tn.next0_.is_char('.')): 
                tn = tn.next0_
        if (tn is not None): 
            if (tn.next0_ is None or tn.newlines_after_count > 1): 
                return None
            t = tn.next0_
            tn = t
            has_named = True
        if (t.is_value("ДВАЖДЫ", None) or t.is_value("ТРИЖДЫ", None) or t.is_value("ЧЕТЫРЕЖДЫ", None)): 
            if (t.next0_ is not None): 
                t = t.next0_
        if (t.is_value("ГЕРОЙ", None)): 
            if ((isinstance(t, TextToken)) and t.term == "ГЕРОЕВ"): 
                pass
            else: 
                ters = TerrItemToken.try_parse_list(t.next0_, 3, None)
                if (ters is not None and len(ters) > 0): 
                    tt1 = None
                    if (ters[0].onto_item is not None): 
                        tt1 = ters[0].end_token.next0_
                    elif (ters[0].termin_item is not None and len(ters) > 1 and ters[1].onto_item is not None): 
                        tt1 = ters[1].end_token.next0_
                    nnn = StreetItemToken.try_parse(tt1, prev, in_search, None)
                    if (nnn is not None and nnn.typ == StreetItemType.NAME): 
                        return nnn
        if (t.is_value("БОЙЦОВ", None)): 
            if ((isinstance(t.next0_, NumberToken)) and (isinstance(t.next0_.next0_, TextToken)) and t.next0_.next0_.morph.case_.is_genitive): 
                return StreetItemToken._new284(t, t.next0_, StreetItemType.NUMBER, t.next0_.value)
        if (t.is_value("НЕЗАВИСИМОСТЬ", None)): 
            ters = TerrItemToken.try_parse_list(t.next0_, 3, None)
            if (ters is not None and len(ters) > 0): 
                tok2 = None
                if (ters[0].onto_item is not None): 
                    tok2 = ters[0]
                elif (ters[0].termin_item is not None and len(ters) > 1 and ters[1].onto_item is not None): 
                    tok2 = ters[1]
                if (tok2 is not None): 
                    res = StreetItemToken._new300(t, tok2.end_token, StreetItemType.NAME)
                    res.value = "НЕЗАВИСИМОСТИ {0}".format(tok2.onto_item.canonic_text)
                    return res
        if (t.is_value("ЖУКОВА", None)): 
            pass
        if (isinstance(t, ReferentToken)): 
            res1 = StreetItemToken._try_parse_spec(t, prev)
            if (res1 is not None and ((len(res1) == 1 or res1[0].typ == StreetItemType.NAME))): 
                return res1[0]
            if ((res1 is not None and len(res1) == 2 and res1[0].typ == StreetItemType.NUMBER) and ((res1[1].typ == StreetItemType.NAME or res1[1].typ == StreetItemType.STDNAME))): 
                res1[0].next_item = res1[1]
                return res1[0]
        nt = NumberHelper.try_parse_age(t)
        if (nt is not None and nt.int_value is not None): 
            return StreetItemToken._new392(nt.begin_token, nt.end_token, StreetItemType.AGE, nt.value, NumberSpellingType.AGE)
        nt = Utils.asObjectOrNull(t, NumberToken)
        if ((nt) is not None): 
            if (nt.int_value is None): 
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    pass
                else: 
                    return None
            elif (nt.int_value == 0): 
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    pass
                else: 
                    next0__ = StreetItemToken.try_parse(nt.next0_, None, False, None)
                    if (next0__ is not None and next0__.typ == StreetItemType.NOUN): 
                        pass
                    else: 
                        return None
            res = StreetItemToken._new393(nt, nt, StreetItemType.NUMBER, nt.value, nt.typ, nt.morph)
            res.value = nt.value
            nnn = NumToken.try_parse(t, GeoTokenType.STREET)
            if (nnn is not None): 
                res.value = nnn.value
                res.end_token = nnn.end_token
                t = res.end_token
                if ((nnn.value.find('-') > 0 and prev is not None and prev.typ == StreetItemType.NOUN) and prev.termin.canonic_text == "МИКРОРАЙОН"): 
                    jj = nnn.value.find('-')
                    tt2 = nnn.begin_token.next0_
                    while tt2 is not None and (tt2.end_char < nnn.end_char): 
                        if (tt2.is_hiphen): 
                            res.end_token = tt2.previous
                            t = res.end_token
                            res.value = res.value[0:0+jj]
                            return res
                        tt2 = tt2.next0_
            nex = NumberHelper.try_parse_number_with_postfix(t)
            if (nex is not None): 
                if (nex.ex_typ == NumberExType.KILOMETER): 
                    res.is_number_km = True
                    res.end_token = nex.end_token
                    if (res.value.startswith("0") and len(res.value) > 1): 
                        res.value = res.value[1:]
                    tt2 = res.end_token.next0_
                    has_br = False
                    while tt2 is not None:
                        if (tt2.is_hiphen or tt2.is_char('+')): 
                            tt2 = tt2.next0_
                        elif (tt2.is_char('(')): 
                            has_br = True
                            tt2 = tt2.next0_
                        else: 
                            break
                    nex2 = NumberHelper.try_parse_number_with_postfix(tt2)
                    if (nex2 is not None and nex2.ex_typ == NumberExType.METER): 
                        res.end_token = nex2.end_token
                        if (has_br and res.end_token.next0_ is not None and res.end_token.next0_.is_char(')')): 
                            res.end_token = res.end_token.next0_
                        mm = NumberHelper.double_to_string(nex2.real_value / (1000))
                        if (mm.startswith("0.")): 
                            res.value += mm[1:]
                    ait = AddressItemToken.try_parse_pure_item(t, None, None)
                    if (ait is not None and ait.typ == AddressItemType.DETAIL): 
                        return None
                else: 
                    nex2 = StreetItemToken.try_parse(res.end_token.next0_, None, False, None)
                    if (nex2 is not None and nex2.typ == StreetItemType.NOUN and nex2.end_char > nex.end_char): 
                        pass
                    else: 
                        return None
            if (t.next0_ is not None and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, NumberToken))): 
                nex = NumberHelper.try_parse_number_with_postfix(t.next0_.next0_)
                if (nex is not None): 
                    if (nex.ex_typ == NumberExType.KILOMETER): 
                        res.is_number_km = True
                        res.end_token = nex.end_token
                        res.value = "{0}-{1}".format(res.value, nex.value)
                    else: 
                        return None
            aaa = AddressItemToken.try_parse_pure_item(t, None, None)
            if (aaa is not None and aaa.typ == AddressItemType.NUMBER and aaa.end_char > (t.end_char + 1)): 
                next0__ = StreetItemToken.try_parse(res.end_token.next0_, None, False, None)
                if (next0__ is not None and ((next0__.typ == StreetItemType.NAME or next0__.typ == StreetItemType.STDNAME))): 
                    pass
                elif (prev is not None and prev.typ == StreetItemType.NOUN and (((t.next0_.is_hiphen or prev.termin.canonic_text == "КВАРТАЛ" or prev.termin.canonic_text == "ЛИНИЯ") or prev.termin.canonic_text == "АЛЛЕЯ" or prev.termin.canonic_text == "ДОРОГА"))): 
                    if (StreetItemToken._m_ontology.try_parse(aaa.end_token, TerminParseAttr.NO) is not None): 
                        pass
                    else: 
                        res.end_token = aaa.end_token
                        res.value = aaa.value
                        res.number_type = NumberSpellingType.UNDEFINED
                else: 
                    return None
            if (nt.typ == NumberSpellingType.WORDS and nt.morph.class0_.is_adjective): 
                npt2 = MiscLocationHelper._try_parse_npt(t)
                if (npt2 is not None and npt2.end_char > t.end_char and npt2.morph.number != MorphNumber.SINGULAR): 
                    if (t.next0_ is not None and not t.next0_.chars.is_all_lower): 
                        pass
                    elif (StreetItemToken.check_keyword(t.next0_)): 
                        pass
                    else: 
                        return None
            if (not res.is_number_km and prev is not None and prev.begin_token.is_value("КИЛОМЕТР", None)): 
                res.is_number_km = True
            elif (prev is not None and prev.typ == StreetItemType.NOUN and not res.is_whitespace_after): 
                tt1 = res.end_token.next0_
                while tt1 is not None: 
                    if (tt1.is_whitespace_before): 
                        break
                    if (isinstance(tt1, NumberToken)): 
                        res.value += tt1.value
                        res.end_token = tt1
                    elif (tt1.is_hiphen): 
                        res.value += "-"
                        res.end_token = tt1
                    elif ((isinstance(tt1, TextToken)) and tt1.chars.is_letter and tt1.length_char == 1): 
                        ch = tt1.term[0]
                        ch1 = LanguageHelper.get_cyr_for_lat(ch)
                        if ((ord(ch1)) != 0): 
                            ch = ch1
                        res.value = "{0}{1}".format(res.value, ch)
                        res.end_token = tt1
                    else: 
                        break
                    tt1 = tt1.next0_
            if (res.value.endswith("-")): 
                res.value = res.value[0:0+len(res.value) - 1]
            if (res.end_token.next0_ is not None and ((res.end_token.next0_.is_value("СЕКТОР", None) or res.end_token.next0_.is_value("ЗОНА", None)))): 
                tt1 = res.end_token.next0_.next0_
                if ((isinstance(tt1, TextToken)) and tt1.length_char == 1 and tt1.chars.is_letter): 
                    ch = tt1.term[0]
                    ch1 = LanguageHelper.get_cyr_for_lat(ch)
                    if ((ord(ch1)) != 0): 
                        ch = ch1
                    res.value = "{0}{1}".format(res.value, ch)
                    res.end_token = tt1
                elif (isinstance(tt1, NumberToken)): 
                    res.value = "{0}-{1}".format(res.value, tt1.value)
                    res.end_token = tt1
            return res
        ntt = MiscHelper.check_number_prefix(t)
        if ((ntt is not None and (isinstance(ntt, NumberToken)) and prev is not None) and ntt.int_value is not None): 
            return StreetItemToken._new298(t, ntt, StreetItemType.NUMBER, ntt.value, ntt.typ, True)
        rrr = OrgItemToken.try_parse_railway(t)
        if (rrr is not None): 
            return rrr
        if ((isinstance(t, ReferentToken)) and t.begin_token == t.end_token and not t.chars.is_all_lower): 
            if (prev is not None and prev.typ == StreetItemType.NOUN): 
                if (((prev.morph.number) & (MorphNumber.PLURAL)) == (MorphNumber.UNDEFINED)): 
                    res = StreetItemToken._new284(t, t, StreetItemType.NAME, MiscHelper.get_text_value_of_meta_token(Utils.asObjectOrNull(t, ReferentToken), GetTextAttr.NO))
                    if ((t.next0_ is not None and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, TextToken))) and not t.is_whitespace_after and not t.next0_.is_whitespace_after): 
                        res.end_token = t.next0_.next0_
                        res.value = "{0} {1}".format(res.value, res.end_token.term)
                    return res
        if (t.is_value("ЧАСТЬ", None)): 
            return None
        if (t.is_value("УГОЛ", None)): 
            if (prev is not None and ((prev.typ == StreetItemType.NOUN or prev.typ == StreetItemType.STDADJECTIVE))): 
                pass
            else: 
                return None
        tt = Utils.asObjectOrNull(t, TextToken)
        npt = None
        if (tt is not None and tt.morph.class0_.is_adjective): 
            if (tt.chars.is_capital_upper or MiscLocationHelper.is_user_param_address(tt) or ((prev is not None and prev.typ == StreetItemType.NUMBER and tt.is_value("ТРАНСПОРТНЫЙ", None)))): 
                npt = MiscLocationHelper._try_parse_npt(tt)
                if (npt is not None and "-" in MiscHelper.get_text_value_of_meta_token(npt.noun, GetTextAttr.NO)): 
                    npt = (None)
                elif (npt is not None and len(npt.adjectives) > 0 and ((npt.adjectives[0].is_newline_after or npt.noun.is_newline_before))): 
                    npt = (None)
                if (npt is not None and AddressItemToken.try_parse_pure_item(npt.end_token, None, None) is not None): 
                    npt = (None)
                tte = tt.next0_
                if (npt is not None and len(npt.adjectives) == 1): 
                    tte = npt.end_token
                if (StreetItemToken.__m_misc_nouns.try_parse(tte, TerminParseAttr.NO) is not None): 
                    sit = StreetItemToken._new396(tt, tte, True)
                    sit.typ = StreetItemType.NAME
                    if (npt is None or len(npt.adjectives) == 0): 
                        sit.value = MiscHelper.get_text_value(tt, tte, GetTextAttr.NO)
                    elif (npt.morph.case_.is_genitive): 
                        sit.value = MiscHelper.get_text_value(tt, tte, GetTextAttr.NO)
                        sit.alt_value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                    else: 
                        sit.value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                    tok2 = StreetItemToken._m_ontology.try_parse(tt, TerminParseAttr.NO)
                    if (tok2 is not None and tok2.termin is not None and tok2.end_token == tte): 
                        sit.termin = tok2.termin
                    return sit
                if (npt is not None and npt.begin_token != npt.end_token and len(npt.adjectives) <= 1): 
                    oo = StreetItemToken._m_ontology.try_parse(t, TerminParseAttr.NO)
                    if (oo is not None): 
                        if ((Utils.valToEnum(oo.termin.tag, StreetItemType)) == StreetItemType.NOUN or (Utils.valToEnum(oo.termin.tag, StreetItemType)) == StreetItemType.STDPARTOFNAME): 
                            npt = (None)
                if (npt is not None and npt.end_token.is_value("ВЕРХ", None)): 
                    npt = (None)
                if (npt is not None): 
                    ait = AddressItemToken.try_parse_pure_item(t, None, None)
                    if (ait is not None and ait.detail_type != AddressDetailType.UNDEFINED): 
                        npt = (None)
                if (npt is not None and npt.begin_token != npt.end_token and len(npt.adjectives) <= 1): 
                    tt1 = npt.end_token.next0_
                    ok = MiscLocationHelper.is_user_param_address(npt)
                    if (npt.is_newline_after): 
                        ok = True
                    elif (tt1 is not None and tt1.is_comma): 
                        ok = True
                        tt1 = tt1.next0_
                    sti1 = StreetItemToken.try_parse(tt1, None, False, None)
                    if (sti1 is not None and sti1.typ == StreetItemType.NOUN): 
                        ok = True
                    elif (tt1 is not None and tt1.is_hiphen and (isinstance(tt1.next0_, NumberToken))): 
                        ok = True
                    else: 
                        ait = AddressItemToken.try_parse_pure_item(tt1, None, None)
                        if (ait is not None): 
                            if (ait.typ == AddressItemType.HOUSE): 
                                ok = True
                            elif (ait.typ == AddressItemType.NUMBER): 
                                ait2 = AddressItemToken.try_parse_pure_item(npt.end_token, None, None)
                                if (ait2 is None): 
                                    ok = True
                    if (ok): 
                        sti1 = StreetItemToken.try_parse(npt.end_token, None, False, None)
                        if (sti1 is not None and sti1.typ == StreetItemType.NOUN): 
                            ok = (sti1.noun_is_doubt_coef >= 2 and sti1.termin.canonic_text != "КВАРТАЛ")
                        else: 
                            tok2 = StreetItemToken._m_ontology.try_parse(npt.end_token, TerminParseAttr.NO)
                            if (tok2 is not None): 
                                typ_ = Utils.valToEnum(tok2.termin.tag, StreetItemType)
                                if (typ_ == StreetItemType.NOUN or typ_ == StreetItemType.STDPARTOFNAME or typ_ == StreetItemType.STDADJECTIVE): 
                                    ok = False
                    if (ok): 
                        sit = StreetItemToken(tt, npt.end_token)
                        sit.typ = StreetItemType.NAME
                        sit.value = MiscHelper.get_text_value(tt, npt.end_token, GetTextAttr.NO)
                        sit.alt_value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                        if (sit.alt_value.endswith("ПОЛОК")): 
                            sit.alt_value = (sit.alt_value[0:0+len(sit.alt_value) - 5] + "ПОЛК")
                        return sit
        if (tt is not None and (isinstance(tt.next0_, TextToken)) and ((not tt.next0_.chars.is_all_lower or MiscLocationHelper.is_user_param_address(tt)))): 
            if (StreetItemToken.__m_misc_nouns.try_parse(tt, TerminParseAttr.NO) is not None): 
                sit = StreetItemToken.try_parse(tt.next0_, None, False, None)
                if (sit is not None and sit.typ == StreetItemType.NAME): 
                    if (sit.value is not None): 
                        sit.value = "{0} {1}".format(sit.value, tt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
                    else: 
                        sit.value = "{0} {1}".format(sit.get_source_text().upper(), tt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
                    if (sit.alt_value is not None): 
                        sit.alt_value = "{0} {1}".format(sit.alt_value, tt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False))
                    sit.begin_token = tt
                    sit.has_std_suffix = True
                    return sit
        if (((tt is not None and tt.length_char == 1 and tt.chars.is_all_lower) and tt.next0_ is not None and tt.next0_.is_char('.')) and tt.kit.base_language.is_ru): 
            if (tt.is_value("М", None) or tt.is_value("M", None)): 
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    pass
                elif (not in_search): 
                    tok1 = StreetItemToken._m_ontology.try_parse(tt, TerminParseAttr.NO)
                    if (tok1 is not None and tok1.termin.canonic_text == "МИКРОРАЙОН"): 
                        return StreetItemToken._new397(tt, tok1.end_token, tok1.termin, StreetItemType.NOUN)
                    if (NameToken.check_initial(tt) is not None or MiscLocationHelper.is_user_param_address(tt)): 
                        pass
                    else: 
                        return StreetItemToken._new398(tt, tt.next0_, StreetItemToken.__m_metro, StreetItemType.NOUN, True)
        ot = None
        if (not MiscLocationHelper.is_user_param_address(t)): 
            if (t.kit.ontology is not None and ot is None): 
                ots = t.kit.ontology.attach_token(AddressReferent.OBJ_TYPENAME, t)
                if (ots is not None): 
                    ot = ots[0]
            if (ot is not None and ot.begin_token == ot.end_token and ot.morph.class0_.is_adjective): 
                tok0 = StreetItemToken._m_ontology.try_parse(t, TerminParseAttr.NO)
                if (tok0 is not None): 
                    if ((Utils.valToEnum(tok0.termin.tag, StreetItemType)) == StreetItemType.STDADJECTIVE): 
                        ot = (None)
        if (ot is not None): 
            res0 = StreetItemToken._new399(ot.begin_token, ot.end_token, StreetItemType.NAME, Utils.asObjectOrNull(ot.item.referent, StreetReferent), ot.morph, True)
            return res0
        if (prev is not None and prev.typ == StreetItemType.NOUN and prev.termin.canonic_text == "ПРОЕЗД"): 
            if (t.is_value("ПР", None)): 
                res1 = StreetItemToken._new284(t, t, StreetItemType.NAME, "ПРОЕКТИРУЕМЫЙ")
                if (t.next0_ is not None and t.next0_.is_char('.')): 
                    res1.end_token = t.next0_
                return res1
        tok = (None if ignore_onto else StreetItemToken._m_ontology.try_parse(t, TerminParseAttr.NO))
        tok_ex = (None if ignore_onto else StreetItemToken._m_ontology_ex.try_parse(t, TerminParseAttr.NO))
        if (tok is None): 
            tok = tok_ex
        elif (tok_ex is not None and tok_ex.end_char > tok.end_char): 
            tok = tok_ex
        if (tok is not None and (isinstance(t, TextToken)) and ((t.term == "ДОРОГАЯ" or t.term == "ДОРОГОЙ"))): 
            tok = (None)
        if ((tok is not None and t.length_char == 1 and t.is_value("Б", None)) and (isinstance(t.previous, NumberToken)) and t.previous.value == "26"): 
            tok = (None)
        if ((tok is not None and tok.termin.canonic_text == "БЛОК" and (isinstance(t, TextToken))) and tok.end_token == t): 
            if (t.term == "БЛОКА"): 
                tok = (None)
            elif (t.chars.is_all_lower): 
                pass
            elif (prev is not None and prev.typ == StreetItemType.NOUN and prev.termin.canonic_text == "РЯД"): 
                pass
            else: 
                ait = AddressItemToken.try_parse_pure_item(t.next0_, None, None)
                if (ait is not None and ait.typ == AddressItemType.NUMBER): 
                    pass
                else: 
                    tok = (None)
        if (tok is not None and tok.termin.canonic_text == "СЕКЦИЯ"): 
            if (prev is not None): 
                tok = (None)
        if (tok is not None and tok.begin_token == tok.end_token): 
            if (((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.NAME or t.is_value("ГАРАЖНО", None) or t.length_char == 1) or t.is_value("СТ", None)): 
                org0_ = OrgItemToken.try_parse(t, None)
                if (org0_ is not None): 
                    tok = (None)
                    if (t.length_char < 3): 
                        return StreetItemToken._new262(t, org0_.end_token, StreetItemType.FIX, org0_)
            elif ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.STDADJECTIVE and (isinstance(t, TextToken)) and t.term.endswith("О")): 
                tok = (None)
            elif (t.is_value("АК", None) and t.next0_ is not None and t.next0_.is_hiphen): 
                tok = (None)
            elif ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.NOUN and t.is_value("САД", None) and t.previous is not None): 
                if (t.previous.is_value("ДЕТСКИЙ", None)): 
                    tok = (None)
                elif (t.previous.is_hiphen and t.previous.previous is not None and t.previous.previous.is_value("ЯСЛИ", None)): 
                    tok = (None)
        if (tok is not None and not ignore_onto): 
            if ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.NUMBER): 
                if ((isinstance(tok.end_token.next0_, NumberToken)) and tok.end_token.next0_.int_value is not None): 
                    return StreetItemToken._new402(t, tok.end_token.next0_, StreetItemType.NUMBER, tok.end_token.next0_.value, tok.end_token.next0_.typ, True, tok.morph)
                return None
            if ((Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.ABSENT): 
                return StreetItemToken._new300(t, tok.end_token, StreetItemType.ABSENT)
            if (tt is None): 
                return None
            abr = True
            swichVal = Utils.valToEnum(tok.termin.tag, StreetItemType)
            if (swichVal == StreetItemType.STDADJECTIVE): 
                while True:
                    tt3 = NameToken.check_initial(tok.begin_token)
                    if (tt3 is not None): 
                        next0__ = StreetItemToken.try_parse(tt3, prev, in_search, None)
                        if (next0__ is not None and next0__.typ != StreetItemType.NOUN): 
                            if (next0__.value is None): 
                                next0__.value = MiscHelper.get_text_value_of_meta_token(next0__, GetTextAttr.NO)
                            next0__.begin_token = t0
                            return next0__
                    if (tt.chars.is_all_lower and prev is None and not in_search): 
                        if (not MiscLocationHelper.is_user_param_address(tok)): 
                            return None
                    if (tt.is_value(tok.termin.canonic_text, None)): 
                        abr = False
                    elif (tt.length_char == 1): 
                        if (not tt.is_whitespace_before and not tt.previous.is_char_of(":,.")): 
                            break
                        if (not tok.end_token.is_char('.')): 
                            oo2 = False
                            if (not tt.chars.is_all_upper and not in_search): 
                                if ((tt.is_char_of("мб") and (isinstance(tt.previous, TextToken)) and tt.previous.chars.is_capital_upper) and AddressItemToken.check_house_after(tt.next0_, False, False)): 
                                    oo2 = True
                                else: 
                                    break
                            if (tok.end_token.is_newline_after and prev is not None and prev.typ != StreetItemType.NOUN): 
                                oo2 = True
                            elif (in_search): 
                                oo2 = True
                            else: 
                                next0__ = StreetItemToken.try_parse(tok.end_token.next0_, None, False, None)
                                if (next0__ is not None and ((next0__.typ == StreetItemType.NAME or next0__.typ == StreetItemType.NOUN))): 
                                    oo2 = True
                                elif (AddressItemToken.check_house_after(tok.end_token.next0_, False, True) and prev is not None): 
                                    oo2 = True
                            if (oo2): 
                                return StreetItemToken._new404(tok.begin_token, tok.end_token, StreetItemType.STDADJECTIVE, tok.termin, abr, tok.morph)
                            break
                        tt2 = tok.end_token.next0_
                        if (tt2 is not None and tt2.is_hiphen): 
                            tt2 = tt2.next0_
                        if (isinstance(tt2, TextToken)): 
                            if (tt2.length_char == 1 and tt2.chars.is_all_upper): 
                                break
                            if (tt2.chars.is_capital_upper): 
                                is_sur = False
                                txt = tt2.term
                                if (LanguageHelper.ends_with(txt, "ОГО")): 
                                    is_sur = True
                                else: 
                                    for wf in tt2.morph.items: 
                                        if (wf.class0_.is_proper_surname and wf.is_in_dictionary): 
                                            if (wf.case_.is_genitive): 
                                                is_sur = True
                                                break
                                if (is_sur): 
                                    break
                    res1 = StreetItemToken._new404(tok.begin_token, tok.end_token, StreetItemType.STDADJECTIVE, tok.termin, abr, tok.morph)
                    toks = StreetItemToken._m_ontology.try_parse_all(tok.begin_token, TerminParseAttr.NO)
                    if (toks is not None and len(toks) > 1): 
                        res1.alt_termin = toks[1].termin
                    return res1
            elif (swichVal == StreetItemType.NOUN): 
                while True:
                    if ((tt.is_value(tok.termin.canonic_text, None) or tok.end_token.is_value(tok.termin.canonic_text, None) or tt.is_value("УЛ", None)) or tok.termin.canonic_text == "НАБЕРЕЖНАЯ"): 
                        abr = False
                    elif (tok.begin_token != tok.end_token and ((tok.begin_token.next0_.is_hiphen or tok.begin_token.next0_.is_char_of("/\\")))): 
                        pass
                    elif (not tt.chars.is_all_lower and tt.length_char == 1 and not tt.is_value("Ш", None)): 
                        break
                    elif (tt.length_char == 1): 
                        if (not tt.is_whitespace_before): 
                            if (tt.previous is not None and tt.previous.is_char_of(",")): 
                                pass
                            else: 
                                return None
                        if (NameToken.check_initial(tt) is not None): 
                            break
                        if (tok.end_token.is_char('.')): 
                            pass
                        elif (tok.begin_token != tok.end_token and tok.begin_token.next0_ is not None and ((tok.begin_token.next0_.is_hiphen or tok.begin_token.next0_.is_char_of("/\\")))): 
                            pass
                        elif (tok.length_char > 5): 
                            pass
                        elif (tok.begin_token == tok.end_token and tt.is_value("Ш", None) and ((tt.chars.is_all_lower or MiscLocationHelper.is_user_param_address(tt)))): 
                            if (prev is not None and ((prev.typ == StreetItemType.NAME or prev.typ == StreetItemType.STDNAME or prev.typ == StreetItemType.STDPARTOFNAME))): 
                                pass
                            else: 
                                sii = StreetItemToken.try_parse(tt.next0_, None, False, None)
                                if (sii is not None and (((sii.typ == StreetItemType.NAME or sii.typ == StreetItemType.STDNAME or sii.typ == StreetItemType.STDPARTOFNAME) or sii.typ == StreetItemType.AGE))): 
                                    pass
                                else: 
                                    return None
                        else: 
                            return None
                    elif (tt.term == "КВ" and not tok.end_token.is_value("Л", None)): 
                        if (prev is not None and prev.typ == StreetItemType.NUMBER): 
                            return None
                        ait = AddressItemToken.try_parse_pure_item(tok.end_token.next0_, None, None)
                        if (ait is not None and ait.typ == AddressItemType.NUMBER): 
                            if (AddressItemToken.check_house_after(ait.end_token.next0_, False, False)): 
                                pass
                            elif (AddressItemToken.check_street_after(ait.end_token.next0_, False)): 
                                pass
                            else: 
                                return None
                        elif (tok.end_token.next0_ is not None and tok.end_token.next0_.is_value("НЕТ", None)): 
                            return None
                    if ((tok.end_token == tok.begin_token and not t.chars.is_all_lower and t.morph.class0_.is_proper_surname) and t.chars.is_cyrillic_letter): 
                        if (((t.morph.number) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED) and not MiscLocationHelper.is_user_param_address(t)): 
                            if (not t.is_value("НАБЕРЕЖНЫЙ", None)): 
                                return None
                    if (tt.term == "ДОРОГОЙ" or tt.term == "РЯДОМ"): 
                        return None
                    if (tt.is_value("ЗАЕЗД", None) or tt.is_value("ВЫЕЗД", None)): 
                        if (not MiscLocationHelper.is_user_param_address(tt)): 
                            return None
                    if (tt.is_value("НАБЕРЕЖНЫЙ", None) and (isinstance(tt, TextToken))): 
                        is_name = False
                        next0__ = StreetItemToken._try_parse(tt.next0_, ignore_onto, None, in_search)
                        if (prev is not None): 
                            if (next0__ is not None and next0__.typ == StreetItemType.NAME): 
                                pass
                            elif (prev.typ == StreetItemType.NOUN or prev.typ == StreetItemType.NUMBER): 
                                is_name = True
                        elif (next0__ is None): 
                            is_name = True
                        elif (next0__.typ == StreetItemType.NOUN or next0__.typ == StreetItemType.NUMBER): 
                            is_name = True
                        if (is_name): 
                            return StreetItemToken._new284(tt, tt, StreetItemType.NAME, tt.term)
                    alt = None
                    if (tok.begin_token.is_value("ПР", None) and ((tok.begin_token == tok.end_token or tok.begin_token.next0_.is_char('.')))): 
                        alt = StreetItemToken.__m_prospect
                    res = StreetItemToken._new407(tok.begin_token, tok.end_token, StreetItemType.NOUN, tok.termin, alt, abr, tok.morph, (tok.termin.tag2 if isinstance(tok.termin.tag2, int) else 0))
                    mc = tok.begin_token.get_morph_class_in_dictionary()
                    if ((not abr and tok.begin_token == tok.end_token and not tok.begin_token.chars.is_all_lower) and ((mc.is_noun or mc.is_adjective))): 
                        if (tok.morph.case_.is_nominative and not tok.morph.case_.is_genitive): 
                            res.noun_can_be_name = True
                        elif ((t.next0_ is not None and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, NumberToken))) and not t.chars.is_all_lower): 
                            res.noun_can_be_name = True
                    if (res.is_road): 
                        next0__ = StreetItemToken._try_parse(res.end_token.next0_, False, None, False)
                        if (next0__ is not None and next0__.is_road): 
                            res.end_token = next0__.end_token
                            res.noun_is_doubt_coef = 0
                            res.is_abridge = False
                    if (not res.is_whitespace_after and res.end_token.next0_.is_char('(')): 
                        br = BracketHelper.try_parse(res.end_token.next0_, BracketParseAttr.NO, 100)
                        if (br is not None and (br.length_char < 5) and (isinstance(br.begin_token.next0_, TextToken))): 
                            res.end_token = br.end_token
                    return res
            elif (swichVal == StreetItemType.STDNAME): 
                is_post_off = tok.termin.canonic_text == "ПОЧТОВОЕ ОТДЕЛЕНИЕ" or tok.termin.canonic_text == "ПРОЕКТИРУЕМЫЙ"
                if (((t.length_char == 1 and t.next0_ is not None and t.next0_.is_char('.')) and t.next0_.next0_ is not None and t.next0_.next0_.length_char == 1) and t.next0_.next0_.end_char <= tok.end_char): 
                    next0__ = StreetItemToken._try_parse(tok.end_token.next0_, ignore_onto, prev, in_search)
                    if (next0__ is not None and ((next0__.typ == StreetItemType.NAME or next0__.typ == StreetItemType.STDNAME))): 
                        next0__.value = MiscHelper.get_text_value_of_meta_token(next0__, GetTextAttr.NO)
                        next0__.begin_token = t
                        return next0__
                if (tok.begin_token.chars.is_all_lower and not is_post_off and tok.end_token.chars.is_all_lower): 
                    if (StreetItemToken.check_keyword(tok.end_token.next0_)): 
                        pass
                    elif (prev is not None and ((prev.typ == StreetItemType.NUMBER or prev.typ == StreetItemType.NOUN or prev.typ == StreetItemType.AGE))): 
                        pass
                    elif (MiscLocationHelper.is_user_param_address(tok)): 
                        pass
                    else: 
                        return None
                sits = StreetItemToken._new408(tok.begin_token, tok.end_token, StreetItemType.STDNAME, tok.morph, tok.termin.canonic_text)
                if (tok.termin.additional_vars is not None and len(tok.termin.additional_vars) > 0 and not tok.termin.additional_vars[0].canonic_text.startswith("ПАРТ")): 
                    if (tok.termin.additional_vars[0].canonic_text.find(' ') < 0): 
                        sits.alt_value = sits.value
                        sits.value = tok.termin.additional_vars[0].canonic_text
                    else: 
                        sits.alt_value = tok.termin.additional_vars[0].canonic_text
                    ii = sits.alt_value.find(sits.value)
                    if (ii >= 0): 
                        if (ii > 0): 
                            sits.misc = sits.alt_value[0:0+ii].strip()
                        else: 
                            sits.misc = sits.alt_value[len(sits.value):].strip()
                        sits.alt_value = (None)
                if (tok.begin_token != tok.end_token and not is_post_off): 
                    if (tok.begin_token.next0_ == tok.end_token): 
                        if (tok.end_token.get_morph_class_in_dictionary().is_noun and tok.begin_token.get_morph_class_in_dictionary().is_adjective): 
                            pass
                        elif (((StreetItemToken.__m_std_ont_misc.try_parse(tok.begin_token, TerminParseAttr.NO) is not None or tok.begin_token.get_morph_class_in_dictionary().is_proper_name or (tok.begin_token.length_char < 4))) and tok.end_token.length_char > 2 and ((tok.end_token.morph.class0_.is_proper_surname or not tok.end_token.get_morph_class_in_dictionary().is_proper_name))): 
                            sits.alt_value2 = MiscHelper.get_text_value(tok.end_token, tok.end_token, GetTextAttr.NO)
                        elif (((tok.end_token.get_morph_class_in_dictionary().is_proper_name or StreetItemToken.__m_std_ont_misc.try_parse(tok.end_token, TerminParseAttr.NO) is not None)) and ((tok.begin_token.morph.class0_.is_proper_surname))): 
                            sits.alt_value2 = MiscHelper.get_text_value(tok.begin_token, tok.begin_token, GetTextAttr.NO)
                return sits
            elif (swichVal == StreetItemType.STDPARTOFNAME): 
                tt1 = tok.end_token
                vvv = tok.termin.canonic_text
                if ((isinstance(tt1.next0_, NumberToken)) and tt1.next0_.next0_ is not None and tt1.next0_.next0_.is_value("РАНГ", None)): 
                    tt1 = tt1.next0_.next0_
                tok2 = StreetItemToken._m_ontology.try_parse(tt1.next0_, TerminParseAttr.NO)
                if (tok2 is not None and (Utils.valToEnum(tok2.termin.tag, StreetItemType)) == StreetItemType.STDPARTOFNAME): 
                    tt1 = tok2.end_token
                    vvv = "{0} {1}".format(vvv, tok2.termin.canonic_text)
                no_geo = False
                if (tt1.next0_ is not None): 
                    if ((tt1.next0_.is_value("ПОЛИЦИИ", None) or tt1.next0_.is_value("МИЛИЦИИ", None) or tt1.next0_.is_value("ГВАРДИИ", None)) or tt1.next0_.is_value("АРМИИ", None)): 
                        tt1 = tt1.next0_
                    if (tt1.next0_ is not None and (isinstance(tt1.next0_.get_referent(), GeoReferent))): 
                        tt1 = tt1.next0_
                    else: 
                        ter = TerrItemToken.try_parse(tt1.next0_, None, None)
                        if (ter is not None and ter.onto_item is not None): 
                            tt1 = ter.end_token
                            no_geo = True
                sit = StreetItemToken.try_parse(tt1.next0_, None, False, None)
                if ((sit is None and tt1.next0_ is not None and vvv is not None) and tt1.next0_.is_hiphen): 
                    sit = StreetItemToken.try_parse(tt1.next0_.next0_, None, False, None)
                if (sit is not None and sit.typ == StreetItemType.STDADJECTIVE and tt1.next0_.length_char == 1): 
                    sit = StreetItemToken.try_parse(sit.end_token.next0_, None, False, None)
                if (sit is None or tt1.whitespaces_after_count > 3): 
                    for m in tok.morph.items: 
                        if (m.number == MorphNumber.PLURAL and m.case_.is_genitive): 
                            return StreetItemToken._new408(tok.begin_token, tt1, StreetItemType.NAME, tok.morph, MiscHelper.get_text_value_of_meta_token(tok, GetTextAttr.NO))
                    return StreetItemToken._new410(tok.begin_token, tt1, StreetItemType.STDPARTOFNAME, tok.morph, tok.termin)
                if (sit.typ == StreetItemType.NUMBER or sit.typ == StreetItemType.STDADJECTIVE): 
                    return StreetItemToken._new408(tok.begin_token, tt1, StreetItemType.NAME, tok.morph, MiscHelper.get_text_value_of_meta_token(tok, GetTextAttr.NO))
                if (sit.typ != StreetItemType.NAME and sit.typ != StreetItemType.NOUN and sit.typ != StreetItemType.STDNAME): 
                    return None
                if (sit.typ == StreetItemType.NOUN): 
                    if (tok.morph.number == MorphNumber.PLURAL): 
                        return StreetItemToken._new412(tok.begin_token, tt1, StreetItemType.NAME, StreetItemType.STDPARTOFNAME, tok.morph, MiscHelper.get_text_value_of_meta_token(tok, GetTextAttr.NO))
                    else: 
                        return StreetItemToken._new413(tok.begin_token, tt1, StreetItemType.NAME, StreetItemType.STDPARTOFNAME, tok.morph, tok.termin)
                if (sit.value is not None): 
                    sit.misc = vvv
                elif (sit.exist_street is None): 
                    if (vvv == "ГЕРОЯ"): 
                        if (tt1.term != "ГЕРОЕВ" and sit.begin_token.morph.class0_.is_proper_surname): 
                            sit.value = MiscHelper.get_text_value_of_meta_token(sit, GetTextAttr.NO)
                        else: 
                            sit.value = ("ГЕРОЕВ " + MiscHelper.get_text_value_of_meta_token(sit, GetTextAttr.NO))
                        sit._no_geo_in_this_token = True
                    else: 
                        sit.misc = vvv
                        sit.value = MiscHelper.get_text_value_of_meta_token(sit, GetTextAttr.NO)
                sit.begin_token = tok.begin_token
                if (no_geo): 
                    sit._no_geo_in_this_token = True
                return sit
            elif (swichVal == StreetItemType.NAME): 
                if (tok.begin_token.chars.is_all_lower): 
                    if (prev is not None and prev.typ == StreetItemType.STDADJECTIVE): 
                        pass
                    elif (prev is not None and prev.typ == StreetItemType.NOUN and AddressItemToken.check_house_after(tok.end_token.next0_, True, False)): 
                        pass
                    elif (t.is_value("ПРОЕКТИРУЕМЫЙ", None) or t.is_value("МИРА", None)): 
                        pass
                    else: 
                        nex = StreetItemToken.try_parse(tok.end_token.next0_, None, False, None)
                        if (nex is not None and nex.typ == StreetItemType.NOUN): 
                            tt2 = nex.end_token.next0_
                            while tt2 is not None and tt2.is_char_of(",."):
                                tt2 = tt2.next0_
                            if (tt2 is None or tt2.whitespaces_before_count > 1): 
                                return None
                            if (AddressItemToken.check_house_after(tt2, False, True)): 
                                pass
                            else: 
                                return None
                        else: 
                            return None
                sit0 = StreetItemToken.try_parse(tok.begin_token, prev, True, None)
                if (sit0 is not None and sit0.typ == StreetItemType.NAME and sit0.end_char > tok.end_char): 
                    sit0.is_in_dictionary = True
                    return sit0
                sit1 = StreetItemToken._new414(tok.begin_token, tok.end_token, StreetItemType.NAME, tok.morph, True)
                if ((not tok.is_whitespace_after and tok.end_token.next0_ is not None and tok.end_token.next0_.is_hiphen) and not tok.end_token.next0_.is_whitespace_after): 
                    sit2 = StreetItemToken.try_parse(tok.end_token.next0_.next0_, None, False, None)
                    if (sit2 is not None and ((sit2.typ == StreetItemType.NAME or sit2.typ == StreetItemType.STDPARTOFNAME or sit2.typ == StreetItemType.STDNAME))): 
                        sit1.end_token = sit2.end_token
                if (npt is not None and (sit1.end_char < npt.end_char) and StreetItemToken._m_ontology.try_parse(npt.end_token, TerminParseAttr.NO) is None): 
                    sit2 = StreetItemToken._try_parse(t, True, prev, in_search)
                    if (sit2 is not None and sit2.end_char > sit1.end_char): 
                        return sit2
                return sit1
            elif (swichVal == StreetItemType.FIX): 
                return StreetItemToken._new415(tok.begin_token, tok.end_token, StreetItemType.FIX, tok.morph, True, tok.termin)
        if (tt is not None and ((tt.is_value("КИЛОМЕТР", None) or tt.is_value("КМ", None)))): 
            tt1 = tt
            if (tt1.next0_ is not None and tt1.next0_.is_char('.')): 
                tt1 = tt1.next0_
            if ((tt1.whitespaces_after_count < 3) and (isinstance(tt1.next0_, NumberToken))): 
                sit = StreetItemToken._new300(tt, tt1.next0_, StreetItemType.NUMBER)
                sit.value = tt1.next0_.value
                sit.number_type = tt1.next0_.typ
                sit.is_number_km = True
                is_plus = False
                tt2 = sit.end_token.next0_
                if (tt2 is not None and ((tt2.is_hiphen or tt2.is_char('+')))): 
                    is_plus = tt2.is_char('+')
                    tt2 = tt2.next0_
                nex2 = NumberHelper.try_parse_number_with_postfix(tt2)
                if (nex2 is not None and nex2.ex_typ == NumberExType.METER): 
                    sit.end_token = nex2.end_token
                    mm = NumberHelper.double_to_string(nex2.real_value / (1000))
                    if (mm.startswith("0.")): 
                        sit.value += mm[1:]
                elif ((isinstance(tt2, NumberToken)) and is_plus): 
                    dw = tt2.real_value
                    if (dw > 0 and (dw < 1000)): 
                        sit.end_token = tt2
                        mm = NumberHelper.double_to_string(dw / (1000))
                        if (mm.startswith("0.")): 
                            sit.value += mm[1:]
                return sit
            next0__ = StreetItemToken.try_parse(tt.next0_, None, in_search, None)
            if (next0__ is not None and ((next0__.is_railway or next0__.is_road))): 
                next0__.begin_token = tt
                return next0__
        tokn = NameToken.M_ONTO.try_parse(tt, TerminParseAttr.NO)
        if (tokn is not None): 
            return StreetItemToken._new284(tt, tokn.end_token, StreetItemType.NAME, tokn.termin.canonic_text)
        if (tt is not None): 
            if (((tt.is_value("РЕКА", None) or tt.is_value("РЕЧКА", "РІЧКА"))) and tt.next0_ is not None and ((not tt.next0_.chars.is_all_lower or MiscLocationHelper.is_user_param_address(tt)))): 
                nam = NameToken.try_parse(tt.next0_, GeoTokenType.CITY, 0, False)
                if (nam is not None and nam.name is not None and nam.number is None): 
                    return StreetItemToken._new418(tt, nam.end_token, StreetItemType.NAME, tt.morph, "реки", nam.name)
            if ((tt.is_value("Р", None) and prev is not None and prev.termin is not None) and prev.termin.canonic_text == "НАБЕРЕЖНАЯ"): 
                tt2 = tt.next0_
                if (tt2 is not None and tt2.is_char('.')): 
                    tt2 = tt2.next0_
                nam = NameToken.try_parse(tt2, GeoTokenType.CITY, 0, False)
                if (nam is not None and nam.name is not None and nam.number is None): 
                    return StreetItemToken._new418(tt, nam.end_token, StreetItemType.NAME, tt.morph, "реки", nam.name)
            if (tt.is_value("КАДАСТРОВЫЙ", None)): 
                next0__ = StreetItemToken.try_parse(tt.next0_, prev, in_search, None)
                if (next0__ is not None and next0__.typ == StreetItemType.NOUN and next0__.termin.canonic_text == "КВАРТАЛ"): 
                    next0__.begin_token = tt
                    return next0__
            if ((isinstance(t.previous, NumberToken)) and t.previous.value == "26"): 
                if (tt.is_value("БАКИНСКИЙ", None) or "БАКИНСК".startswith(tt.term)): 
                    tt2 = tt
                    if (tt2.next0_ is not None and tt2.next0_.is_char('.')): 
                        tt2 = tt2.next0_
                    if (isinstance(tt2.next0_, TextToken)): 
                        tt2 = tt2.next0_
                        if (tt2.is_value("КОМИССАР", None) or tt2.is_value("КОММИССАР", None) or "КОМИС".startswith(tt2.term)): 
                            if (tt2.next0_ is not None and tt2.next0_.is_char('.')): 
                                tt2 = tt2.next0_
                            sit = StreetItemToken._new420(tt, tt2, StreetItemType.STDNAME, True, "БАКИНСКИХ КОМИССАРОВ", tt2.morph)
                            return sit
            if ((tt.next0_ is not None and ((tt.next0_.is_char('.') or ((tt.next0_.is_hiphen and tt.length_char == 1)))) and ((not tt.chars.is_all_lower or MiscLocationHelper.is_user_param_address(tt)))) and (tt.next0_.whitespaces_after_count < 3) and (isinstance(tt.next0_.next0_, TextToken))): 
                tt1 = tt.next0_.next0_
                if (tt1 is not None and tt1.is_hiphen and tt1.next0_ is not None): 
                    tt1 = tt1.next0_
                if (tt.length_char == 1 and tt1.length_char == 1 and (isinstance(tt1.next0_, TextToken))): 
                    if (tt1.is_and and tt1.next0_.chars.is_all_upper and tt1.next0_.length_char == 1): 
                        tt1 = tt1.next0_
                    if ((tt1.chars.is_all_upper and tt1.next0_ is not None and tt1.next0_.is_char('.')) and (tt1.next0_.whitespaces_after_count < 3) and (isinstance(tt1.next0_.next0_, TextToken))): 
                        tt1 = tt1.next0_.next0_
                    elif ((tt1.chars.is_all_upper and (tt1.whitespaces_after_count < 3) and (isinstance(tt1.next0_, TextToken))) and not tt1.next0_.chars.is_all_lower): 
                        tt1 = tt1.next0_
                sit = StreetItemToken.try_parse(tt1, None, False, None)
                if (sit is not None): 
                    ait = AddressItemToken.try_parse_pure_item(tt, None, None)
                    if (ait is not None): 
                        if (not Utils.isNullOrEmpty(ait.value) and ait.value != "0" and str.isdigit(ait.value[0])): 
                            sit = (None)
                if (sit is not None and (isinstance(tt1, TextToken))): 
                    str0_ = tt1.term
                    ok = False
                    mc = tt1.get_morph_class_in_dictionary()
                    cla = tt.next0_.next0_.get_morph_class_in_dictionary()
                    if (sit.is_in_dictionary): 
                        ok = True
                    elif (sit.__is_surname() or cla.is_proper_surname): 
                        ok = True
                    elif (LanguageHelper.ends_with(str0_, "ОЙ") and ((cla.is_proper_surname or ((sit.typ == StreetItemType.NAME and sit.is_in_dictionary))))): 
                        ok = True
                    elif (LanguageHelper.ends_with_ex(str0_, "ГО", "ИХ", "ЫХ", None)): 
                        ok = True
                    elif ((tt1.is_whitespace_before and not mc.is_undefined and not mc.is_proper_surname) and not mc.is_proper_name): 
                        if (AddressItemToken.check_house_after(sit.end_token.next0_, False, True)): 
                            ok = True
                    elif (prev is not None and prev.typ == StreetItemType.NOUN and ((not prev.is_abridge or prev.length_char > 2))): 
                        ok = True
                    elif ((prev is not None and prev.typ == StreetItemType.NAME and sit.typ == StreetItemType.NOUN) and AddressItemToken.check_house_after(sit.end_token.next0_, False, True)): 
                        ok = True
                    elif (sit.typ == StreetItemType.NAME and AddressItemToken.check_house_after(sit.end_token.next0_, False, True)): 
                        if (MiscLocationHelper.check_geo_object_before(tt, False)): 
                            ok = True
                        else: 
                            ad = GeoAnalyzer._get_data(t)
                            if (not ad.sregime and StreetItemToken.SPEED_REGIME): 
                                ok = True
                                sit._cond = Condition._new421(tt, True)
                    if (not ok and MiscLocationHelper.is_user_param_address(tt) and ((sit.typ == StreetItemType.NAME or sit.typ == StreetItemType.STDADJECTIVE))): 
                        sit1 = StreetItemToken.try_parse(sit.end_token.next0_, None, False, None)
                        if (sit1 is not None and sit1.typ == StreetItemType.NOUN): 
                            ok = True
                        elif (AddressItemToken.check_house_after(sit.end_token.next0_, True, False)): 
                            ok = True
                        elif (sit.end_token.is_newline_after): 
                            ok = True
                    if (ok): 
                        sit.begin_token = tt
                        if (sit.value is None): 
                            sit.value = str0_
                        if (tok is not None and (Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.STDADJECTIVE and not has_named): 
                            if ((isinstance(tok.end_token.next0_, TextToken)) and tok.end_token.next0_.length_char == 1 and tok.end_token.next0_.chars.is_letter): 
                                pass
                            else: 
                                sit.std_adj_version = StreetItemToken._new422(tok.begin_token, tok.end_token, StreetItemType.STDADJECTIVE, tok.termin, True)
                                toks2 = StreetItemToken._m_ontology.try_parse_all(tok.begin_token, TerminParseAttr.NO)
                                if (toks2 is not None and len(toks2) > 1): 
                                    sit.std_adj_version.alt_termin = toks2[1].termin
                        return sit
            if (tt.chars.is_cyrillic_letter and tt.length_char > 1 and not tt.morph.class0_.is_preposition): 
                if (((tt.is_value("ОБЪЕЗД", None) or tt.is_value("ОБХОД", None))) and tt.next0_ is not None): 
                    if (prev is None): 
                        return None
                    if (prev.is_road): 
                        cits = CityItemToken.try_parse_list(tt.next0_, 3, None)
                        if (cits is not None and (len(cits) < 3)): 
                            resr = StreetItemToken._new423(tt, cits[len(cits) - 1].end_token, StreetItemType.NAME, True)
                            for ci in cits: 
                                if (ci.typ == CityItemToken.ItemType.CITY or ci.typ == CityItemToken.ItemType.PROPERNAME): 
                                    resr.value = ("ОБЪЕЗД " + MiscHelper.get_text_value_of_meta_token(ci, GetTextAttr.NO))
                                    break
                            if (resr.value is not None): 
                                return resr
                if ((tt.is_value("ГЕРОЙ", None) or tt.is_value("ЗАЩИТНИК", "ЗАХИСНИК") or tt.is_value("ОБРАЗОВАНИЕ", None)) or tt.is_value("ОСВОБОДИТЕЛЬ", "ВИЗВОЛИТЕЛЬ") or tt.is_value("КОНСТИТУЦИЯ", None)): 
                    tt2 = None
                    if ((isinstance(tt.next0_, ReferentToken)) and (isinstance(tt.next0_.get_referent(), GeoReferent))): 
                        tt2 = tt.next0_
                    else: 
                        npt2 = MiscLocationHelper._try_parse_npt(tt.next0_)
                        if (npt2 is not None and npt2.morph.case_.is_genitive): 
                            tt2 = npt2.end_token
                        else: 
                            tee = TerrItemToken.check_onto_item(tt.next0_)
                            if (tee is not None): 
                                tt2 = tee.end_token
                            else: 
                                tee = CityItemToken.check_onto_item(tt.next0_)
                                if ((tee) is not None): 
                                    tt2 = tee.end_token
                    if (tt2 is not None): 
                        re = StreetItemToken._new424(tt, tt2, StreetItemType.STDPARTOFNAME, MiscHelper.get_text_value(tt, tt2, GetTextAttr.NO), True)
                        sit = StreetItemToken.try_parse(tt2.next0_, None, False, None)
                        if (sit is None or sit.typ != StreetItemType.NAME): 
                            ok2 = False
                            if (sit is not None and ((sit.typ == StreetItemType.STDADJECTIVE or sit.typ == StreetItemType.NOUN))): 
                                ok2 = True
                            elif (AddressItemToken.check_house_after(tt2.next0_, False, True)): 
                                ok2 = True
                            elif (tt2.is_newline_after): 
                                ok2 = True
                            if (ok2): 
                                sit = StreetItemToken._new300(tt, tt2, StreetItemType.NAME)
                                sit.value = MiscHelper.get_text_value(tt, tt2, GetTextAttr.NO)
                                if (not tt.is_value("ОБРАЗОВАНИЕ", None)): 
                                    sit._no_geo_in_this_token = True
                                return sit
                            return re
                        if (sit.value is None): 
                            sit.value = MiscHelper.get_text_value_of_meta_token(sit, GetTextAttr.NO)
                        if (sit.alt_value is None): 
                            sit.alt_value = sit.value
                            sit.value = "{0} {1}".format(re.value, sit.value)
                        else: 
                            sit.value = "{0} {1}".format(re.value, sit.value)
                        sit.begin_token = tt
                        return sit
                ani = NumberHelper.try_parse_anniversary(t)
                if (ani is not None): 
                    return StreetItemToken._new426(t, ani.end_token, StreetItemType.AGE, NumberSpellingType.AGE, ani.value)
                num1 = NumToken.try_parse(t, GeoTokenType.STREET)
                if (num1 is not None): 
                    return StreetItemToken._new426(t, num1.end_token, StreetItemType.NUMBER, NumberSpellingType.ROMAN, num1.value)
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    pass
                else: 
                    org0_ = OrgItemToken.try_parse(t, None)
                    if (org0_ is not None): 
                        if (org0_.is_gsk or org0_.has_terr_keyword): 
                            return StreetItemToken._new262(t, org0_.end_token, StreetItemType.FIX, org0_)
                ok1 = False
                cond = None
                if (not tt.chars.is_all_lower): 
                    ait = AddressItemToken.try_parse_pure_item(tt, None, None)
                    if (ait is not None): 
                        if (tt.next0_ is not None and tt.next0_.is_hiphen): 
                            ok1 = True
                        elif (tt.is_value("БЛОК", None) or tt.is_value("ДОС", None) or ait.end_token.is_value("БЛОК", None)): 
                            ok1 = True
                        elif (ait.typ == AddressItemType.SPACE and ait.detail_param is not None): 
                            ok1 = True
                        elif ((ait.typ != AddressItemType.NUMBER and ait.typ != AddressItemType.POTCH and ait.typ != AddressItemType.NONUMBER) and ait.begin_token == ait.end_token and not ait.chars.is_all_lower): 
                            ok1 = True
                    else: 
                        ok1 = True
                elif (prev is not None and ((prev.typ == StreetItemType.NOUN or ((prev.typ == StreetItemType.STDADJECTIVE and t.previous.is_hiphen)) or ((prev.typ == StreetItemType.NUMBER and MiscLocationHelper.is_user_param_address(prev)))))): 
                    if (AddressItemToken.check_house_after(tt.next0_, False, False)): 
                        if (not AddressItemToken.check_house_after(tt, False, False)): 
                            ok1 = True
                    if (not ok1): 
                        tt1 = prev.begin_token.previous
                        if (tt1 is not None and tt1.is_comma): 
                            tt1 = tt1.previous
                        if (tt1 is not None and (isinstance(tt1.get_referent(), GeoReferent))): 
                            ok1 = True
                        elif (MiscLocationHelper.is_user_param_address(prev) and not AddressItemToken.check_house_after(tt, False, False)): 
                            ok1 = True
                        elif (t.previous is not None and t.previous.is_hiphen): 
                            ok1 = True
                        else: 
                            ad = GeoAnalyzer._get_data(t)
                            if (not ad.sregime and StreetItemToken.SPEED_REGIME): 
                                ok1 = True
                                cond = Condition._new421(prev.begin_token, True)
                elif (tt.whitespaces_after_count < 2): 
                    nex = StreetItemToken._m_ontology.try_parse(tt.next0_, TerminParseAttr.NO)
                    if (nex is not None and nex.termin is not None): 
                        if (nex.termin.canonic_text == "ПЛОЩАДЬ"): 
                            if (tt.is_value("ОБЩИЙ", None)): 
                                return None
                        tt1 = tt.previous
                        if (tt1 is not None and tt1.is_comma): 
                            tt1 = tt1.previous
                        if (tt1 is not None and (isinstance(tt1.get_referent(), GeoReferent))): 
                            ok1 = True
                        elif (AddressItemToken.check_house_after(nex.end_token.next0_, False, False)): 
                            ok1 = True
                        elif (MiscLocationHelper.is_user_param_address(tt)): 
                            ok1 = True
                    elif (MiscLocationHelper.is_user_param_address(tt) and tt.length_char > 3): 
                        aaa = AddressItemToken.try_parse_pure_item(tt, None, None)
                        if (aaa is None): 
                            ok1 = True
                        elif (tt.is_value("УГОЛ", None)): 
                            ok1 = True
                elif (tt.is_newline_after and tt.length_char > 2 and MiscLocationHelper.is_user_param_address(tt)): 
                    ok1 = True
                if (ok1): 
                    dc = tt.get_morph_class_in_dictionary()
                    if (dc.is_adverb and not MiscLocationHelper.is_user_param_address(tt)): 
                        if (not ((dc.is_proper))): 
                            if (tt.next0_ is not None and tt.next0_.is_hiphen): 
                                pass
                            else: 
                                return None
                    res = StreetItemToken._new430(tt, tt, StreetItemType.NAME, tt.morph, cond)
                    if ((tt.next0_ is not None and ((tt.next0_.is_hiphen)) and (isinstance(tt.next0_.next0_, TextToken))) and not tt.is_whitespace_after and not tt.next0_.is_whitespace_after): 
                        ok2 = AddressItemToken.check_house_after(tt.next0_.next0_.next0_, False, False) or tt.next0_.next0_.is_newline_after
                        if (not ok2): 
                            te2 = StreetItemToken.try_parse(tt.next0_.next0_.next0_, None, False, None)
                            if (te2 is not None and te2.typ == StreetItemType.NOUN): 
                                ok2 = True
                        if (not ok2 and (isinstance(tt.next0_.next0_.next0_, NumberToken))): 
                            ok2 = True
                        if (((not ok2 and tt.next0_.is_hiphen and not tt.is_whitespace_after) and not tt.next0_.is_whitespace_after and (isinstance(tt.next0_.next0_, TextToken))) and tt.next0_.next0_.length_char > 3): 
                            ok2 = True
                        if (ok2): 
                            res.end_token = tt.next0_.next0_
                            if (tt.get_morph_class_in_dictionary().is_proper_name and not tt.term.endswith("О") and res.end_token.morph.class0_.is_proper_surname): 
                                res.misc = MiscHelper.get_text_value(tt, tt, GetTextAttr.NO)
                                res.value = MiscHelper.get_text_value(res.end_token, res.end_token, GetTextAttr.NO)
                            else: 
                                res.value = "{0} {1}".format(MiscHelper.get_text_value(tt, tt, GetTextAttr.NO), MiscHelper.get_text_value(res.end_token, res.end_token, GetTextAttr.NO))
                    elif ((tt.whitespaces_after_count < 2) and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_letter): 
                        if (tt.next0_.is_value("БИ", None) or tt.next0_.is_value("АТА", None) or tt.next0_.is_value("СУ", None)): 
                            if (res.value is None): 
                                res.value = MiscHelper.get_text_value(tt, tt, GetTextAttr.NO)
                            res.end_token = tt.next0_
                            res.value = "{0} {1}".format(res.value, tt.next0_.term)
                            if (res.alt_value is not None): 
                                res.alt_value = "{0} {1}".format(res.alt_value, tt.next0_.term)
                        elif (not AddressItemToken.check_house_after(tt.next0_, False, False) or tt.next0_.is_newline_after): 
                            tt1 = tt.next0_
                            is_pref = False
                            if (isinstance(tt1, TextToken)): 
                                if (tt1.is_value("ДЕ", None) or tt1.is_value("ЛА", None)): 
                                    tt1 = tt1.next0_
                                    is_pref = True
                            nn = StreetItemToken.try_parse(tt1, None, False, None)
                            if (nn is None or nn.typ == StreetItemType.NAME): 
                                npt = MiscLocationHelper._try_parse_npt(tt)
                                if (npt is not None): 
                                    if (npt.begin_token == npt.end_token): 
                                        npt = (None)
                                    elif (StreetItemToken._m_ontology.try_parse(npt.end_token, TerminParseAttr.NO) is not None): 
                                        npt = (None)
                                if (npt is not None and ((npt.is_newline_after or AddressItemToken.check_house_after(npt.end_token.next0_, False, False) or ((npt.end_token.next0_ is not None and npt.end_token.next0_.is_comma_and))))): 
                                    res.end_token = npt.end_token
                                    if (npt.morph.case_.is_genitive): 
                                        res.value = MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO)
                                        res.alt_value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                                    else: 
                                        res.value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                                        res.alt_value = MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO)
                                elif ((tt1 is not None and tt1.length_char > 2 and AddressItemToken.check_house_after(tt1.next0_, False, False)) and tt1.chars.is_cyrillic_letter == tt.chars.is_cyrillic_letter and (t.whitespaces_after_count < 2)): 
                                    if (tt1.morph.class0_.is_verb and not tt1.is_value("ДАЛИ", None)): 
                                        pass
                                    elif (npt is None and ((not tt1.chars.is_all_lower or MiscLocationHelper.is_user_param_address(tt1))) and not is_pref): 
                                        pass
                                    else: 
                                        res.end_token = tt1
                                        res.value = "{0} {1}".format(MiscHelper.get_text_value(res.begin_token, res.begin_token, GetTextAttr.NO), MiscHelper.get_text_value(res.end_token, res.end_token, GetTextAttr.NO))
                                elif ((nn is not None and t.length_char > 3 and t.get_morph_class_in_dictionary().is_proper_name) and ((nn.begin_token.morph.class0_.is_proper_surname or nn.end_token.morph.class0_.is_proper_surname or nn.begin_token.morph.class0_.is_proper_secname))): 
                                    res.end_token = nn.end_token
                                    if (nn.begin_token.next0_ == nn.end_token and nn.begin_token.morph.class0_.is_proper_secname): 
                                        res.value = MiscHelper.get_text_value(nn.begin_token.next0_, nn.end_token, GetTextAttr.NO)
                                    elif (nn._orto_terr is not None): 
                                        res.value = MiscHelper.get_text_value(nn.begin_token, nn.begin_token, GetTextAttr.NO)
                                        res._orto_terr = nn._orto_terr
                                    else: 
                                        res.value = MiscHelper.get_text_value_of_meta_token(nn, GetTextAttr.NO)
                                    res.misc = MiscHelper.get_text_value(t, t, GetTextAttr.NO)
                                    if (nn.begin_token.morph.class0_.is_proper_secname and nn.end_token.next0_ is not None and nn.end_token.next0_.morph.class0_.is_proper_surname): 
                                        res.end_token = nn.end_token.next0_
                                        res.value = MiscHelper.get_text_value(res.end_token, res.end_token, GetTextAttr.NO)
                                elif (nn is not None and nn.begin_token.next0_ == nn.end_token and nn.end_token.morph.class0_.is_proper_surname): 
                                    res.end_token = nn.end_token
                                    if (nn.misc is not None and nn.end_token.morph.class0_.is_proper_secname): 
                                        res.value = MiscHelper.get_text_value(t, t, GetTextAttr.NO)
                                        res.misc = nn.misc
                                    else: 
                                        res.value = MiscHelper.get_text_value(nn.end_token, nn.end_token, GetTextAttr.NO)
                                        res.misc = MiscHelper.get_text_value(t, t, GetTextAttr.NO)
                            elif (nn.typ == StreetItemType.NOUN): 
                                gen = nn.termin.gender
                                if (gen == MorphGender.UNDEFINED): 
                                    npt = MiscLocationHelper._try_parse_npt(tt)
                                    if (npt is not None and npt.end_token == nn.end_token): 
                                        gen = npt.morph.gender
                                    elif (prev is not None and prev.typ == StreetItemType.NOUN): 
                                        gen = prev.termin.gender
                                else: 
                                    for ii in tt.morph.items: 
                                        if (((ii.class0_.is_proper_surname or ii.class0_.is_noun)) and ii.case_.is_genitive and (isinstance(ii, MorphWordForm))): 
                                            if (ii.is_in_dictionary): 
                                                gen = MorphGender.UNDEFINED
                                                break
                                if (gen != MorphGender.UNDEFINED and ((not nn.morph.case_.is_nominative or nn.morph.number != MorphNumber.SINGULAR))): 
                                    res.value = MiscHelper.get_text_value(res.begin_token, res.end_token, GetTextAttr.NO)
                                    var = None
                                    try: 
                                        var = MorphologyService.get_wordform(res.value, MorphBaseInfo._new431(MorphCase.NOMINATIVE, MorphClass.ADJECTIVE, MorphNumber.SINGULAR, gen))
                                    except Exception as ex: 
                                        pass
                                    if (var is not None and var.endswith("ОЙ") and not res.begin_token.get_morph_class_in_dictionary().is_adjective): 
                                        if (gen == MorphGender.MASCULINE): 
                                            var = (var[0:0+len(var) - 2] + "ЫЙ")
                                        elif (gen == MorphGender.NEUTER): 
                                            var = (var[0:0+len(var) - 2] + "ОЕ")
                                        elif (gen == MorphGender.FEMINIE): 
                                            var = (var[0:0+len(var) - 2] + "АЯ")
                                    if (var is not None and var != res.value): 
                                        res.alt_value = res.value
                                        res.value = var
                    if (res is not None and res.typ == StreetItemType.NAME and (res.whitespaces_after_count < 2)): 
                        tt = (Utils.asObjectOrNull(res.end_token.next0_, TextToken))
                        if (MiscLocationHelper.is_user_param_address(tt) and tt.is_char('.')): 
                            tt = (Utils.asObjectOrNull(tt.next0_, TextToken))
                        if (NameToken.check_initial_back(tt)): 
                            if (res.value is None): 
                                res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO)
                            if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                                tt = (Utils.asObjectOrNull(tt.next0_, TextToken))
                            res.end_token = tt
                            tt = (Utils.asObjectOrNull(res.end_token.next0_, TextToken))
                            if ((((res.whitespaces_after_count < 2) and tt is not None and tt.length_char == 1) and tt.chars.is_all_upper and tt.next0_ is not None) and tt.next0_.is_char('.')): 
                                res.end_token = tt.next0_
                            tt = (Utils.asObjectOrNull(res.end_token.next0_, TextToken))
                        elif ((tt is not None and tt.length_char == 1 and tt.next0_ is not None) and ((tt.chars.is_all_upper or ((MiscLocationHelper.is_user_param_address(tt) and tt.next0_.is_char('.'))))) and tt.next0_.is_char_of(".,")): 
                            if (StreetItemToken.try_parse(tt, None, False, None) is not None or ((not tt.next0_.is_comma and AddressItemToken.check_house_after(tt, False, False)))): 
                                pass
                            elif (AddressItemToken.check_house_after(tt.next0_.next0_, False, False)): 
                                if (res.value is None): 
                                    res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO)
                                res.end_token = tt
                                if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                                    res.end_token = tt.next0_
                            else: 
                                rt = tt.kit.process_referent("PERSON", tt, None)
                                if (rt is None): 
                                    if (res.value is None): 
                                        res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO)
                                    res.end_token = tt.next0_
                                    tt = (Utils.asObjectOrNull(res.end_token.next0_, TextToken))
                                    if (((res.whitespaces_after_count < 2) and tt is not None and tt.length_char == 1) and ((tt.chars.is_all_upper or MiscLocationHelper.is_user_param_address(tt)))): 
                                        if (AddressItemToken.try_parse_pure_item(tt, None, None) is None): 
                                            if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                                                res.end_token = tt.next0_
                                            elif (tt.next0_ is None or tt.next0_.is_comma): 
                                                res.end_token = tt
                        if (tt is not None and tt.get_morph_class_in_dictionary().is_proper_name): 
                            rt = tt.kit.process_referent("PERSON", res.begin_token, None)
                            if (rt is not None): 
                                ok2 = False
                                if (rt.end_token == tt): 
                                    ok2 = True
                                elif (rt.end_token == tt.next0_ and tt.next0_.get_morph_class_in_dictionary().is_proper_secname): 
                                    ok2 = True
                                if (ok2): 
                                    if (res.value is None): 
                                        res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO)
                                    res.end_token = rt.end_token
                                    if (res.begin_token != res.end_token): 
                                        mc1 = res.begin_token.get_morph_class_in_dictionary()
                                        mc2 = res.end_token.get_morph_class_in_dictionary()
                                        if (((mc1.is_proper_name and not mc2.is_proper_name)) or ((not mc1.is_proper_surname and mc2.is_proper_surname))): 
                                            res.misc = res.value
                                            res.value = MiscHelper.get_text_value(res.end_token, res.end_token, GetTextAttr.NO)
                                        elif (mc1.is_proper_name and ((mc2.is_proper_surname or mc2.is_proper_name or mc2.is_undefined))): 
                                            res.misc = res.value
                                            res.value = MiscHelper.get_text_value(res.end_token, res.end_token, GetTextAttr.NO)
                                        else: 
                                            pp = res.kit.process_referent("PERSONPROPERTY", res.begin_token, None)
                                            if (pp is not None and pp.end_token == res.end_token.previous and not mc1.is_proper_surname): 
                                                res.misc = res.value
                                                res.value = MiscHelper.get_text_value(res.end_token, res.end_token, GetTextAttr.NO)
                                            elif ((res.begin_token.morph.class0_.is_proper_surname and res.begin_token.next0_.morph.class0_.is_proper_name and res.begin_token.next0_.next0_ == res.end_token) and res.end_token.morph.class0_.is_proper_secname): 
                                                res.misc = MiscHelper.get_text_value(res.end_token.previous, res.end_token.previous, GetTextAttr.NO)
                                            else: 
                                                res.misc = MiscHelper.get_text_value(res.end_token, res.end_token, GetTextAttr.NO)
                    if (res.begin_token == res.end_token): 
                        nn = MiscLocationHelper.try_attach_nord_west(res.begin_token)
                        if (nn is not None and nn.end_char > res.end_char): 
                            res.end_token = nn.end_token
                            res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO).replace(" - ", " ")
                        elif (res.typ == StreetItemType.NAME): 
                            cou = 0
                            ttt = res.end_token.next0_
                            while ttt is not None and (cou < 2): 
                                if (not ttt.is_hiphen): 
                                    break
                                if (ttt.is_whitespace_before or ttt.is_whitespace_after): 
                                    break
                                if (not (isinstance(ttt.next0_, TextToken)) or (ttt.next0_.length_char < 2) or ttt.next0_.chars.is_latin_letter): 
                                    break
                                if (StreetItemToken._m_ontology.try_parse(ttt.next0_, TerminParseAttr.NO) is not None): 
                                    break
                                ttt = ttt.next0_
                                if (res.value is None): 
                                    res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO)
                                res.value = "{0} {1}".format(res.value, ttt.term)
                                if (res.alt_value is not None): 
                                    res.alt_value = "{0} {1}".format(res.alt_value, ttt.term)
                                res.end_token = ttt
                                ttt = ttt.next0_; cou += 1
                    return res
            if (tt.is_value("№", None) or tt.is_value("НОМЕР", None) or tt.is_value("НОМ", None)): 
                tt1 = tt.next0_
                if (tt1 is not None and tt1.is_char('.')): 
                    tt1 = tt1.next0_
                if ((isinstance(tt1, NumberToken)) and tt1.int_value is not None): 
                    return StreetItemToken._new432(tt, tt1, StreetItemType.NUMBER, tt1.typ, tt1.value, True)
            if (tt.is_hiphen and (isinstance(tt.next0_, NumberToken)) and tt.next0_.int_value is not None): 
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    if ((prev.noun_can_be_name or prev.termin.canonic_text == "МИКРОРАЙОН" or prev.termin.canonic_text == "КВАРТАЛ") or LanguageHelper.ends_with(prev.termin.canonic_text, "ГОРОДОК")): 
                        return StreetItemToken._new432(tt, tt.next0_, StreetItemType.NUMBER, tt.next0_.typ, tt.next0_.value, True)
            if (((isinstance(tt, TextToken)) and tt.length_char == 1 and (tt.whitespaces_before_count < 2)) and tt.chars.is_letter and tt.chars.is_all_upper): 
                if (prev is not None and prev.typ == StreetItemType.NOUN): 
                    nn = NumToken.try_parse(tt, GeoTokenType.STRONG)
                    if (nn is not None): 
                        if (nn.end_token != tt): 
                            return StreetItemToken._new284(tt, nn.end_token, StreetItemType.NUMBER, nn.value)
                        if (prev.termin.canonic_text == "МИКРОРАЙОН" or prev.termin.canonic_text == "КВАРТАЛ" or LanguageHelper.ends_with(prev.termin.canonic_text, "ГОРОДОК")): 
                            return StreetItemToken._new284(tt, nn.end_token, StreetItemType.NUMBER, nn.value)
                        if ((prev.termin.canonic_text == "РЯД" or prev.termin.canonic_text == "БЛОК" or prev.termin.canonic_text == "ЛИНИЯ") or prev.termin.canonic_text == "ПАНЕЛЬ"): 
                            return StreetItemToken._new284(tt, nn.end_token, StreetItemType.NUMBER, nn.value)
                    if (MiscLocationHelper.is_user_param_address(tt)): 
                        next0__ = StreetItemToken.try_parse(tt.next0_, prev, in_search, None)
                        if (next0__ is not None and next0__.typ == StreetItemType.NAME): 
                            next0__ = next0__.clone()
                            next0__.value = MiscHelper.get_text_value_of_meta_token(next0__, GetTextAttr.NO)
                            next0__.begin_token = tt
                            return next0__
                        if (prev is not None and prev.typ == StreetItemType.NOUN): 
                            return StreetItemToken._new284(tt, tt, StreetItemType.NAME, tt.term)
        r = (None if t is None else t.get_referent())
        if (isinstance(r, GeoReferent)): 
            geo = Utils.asObjectOrNull(r, GeoReferent)
            if (prev is not None and prev.typ == StreetItemType.NOUN): 
                if (AddressItemToken.check_house_after(t.next0_, False, False)): 
                    res1 = StreetItemToken.try_parse(t.begin_token, prev, False, None)
                    if (res1 is not None and res1.end_char == t.end_char): 
                        res1 = res1.clone()
                        res1.begin_token = res1.end_token = t
                        return res1
                    res = StreetItemToken._new284(t, t, StreetItemType.NAME, MiscHelper.get_text_value(t, t, GetTextAttr.NO))
                    return res
        if (((isinstance(tt, TextToken)) and tt.chars.is_capital_upper and tt.chars.is_latin_letter) and (tt.whitespaces_after_count < 2)): 
            if (MiscHelper.is_eng_article(tt)): 
                return None
            tt2 = tt.next0_
            if (MiscHelper.is_eng_adj_suffix(tt2)): 
                tt2 = tt2.next0_.next0_
            tok1 = StreetItemToken._m_ontology.try_parse(tt2, TerminParseAttr.NO)
            if (tok1 is not None): 
                return StreetItemToken._new408(tt, tt2.previous, StreetItemType.NAME, tt.morph, tt.term)
        if (((prev is not None and prev.typ == StreetItemType.NAME and prev.begin_token == prev.end_token) and (isinstance(tt, TextToken)) and tt.chars.is_latin_letter) and tt.previous is not None and tt.previous.get_morph_class_in_dictionary().is_proper_name): 
            num = NumberHelper.try_parse_roman(tt)
            if (num is not None): 
                return StreetItemToken._new284(tt, num.end_token, StreetItemType.NUMBER, num.value)
        if (((tt is not None and tt.is_value("ПОДЪЕЗД", None) and prev is not None) and prev.is_road and tt.next0_ is not None) and tt.next0_.is_value("К", None) and tt.next0_.next0_ is not None): 
            sit = StreetItemToken._new300(tt, tt.next0_, StreetItemType.NAME)
            sit.is_road_name = True
            t1 = tt.next0_.next0_
            g1 = None
            first_pass3792 = True
            while True:
                if first_pass3792: first_pass3792 = False
                else: t1 = t1.next0_
                if (not (t1 is not None)): break
                if (t1.whitespaces_before_count > 3): 
                    break
                g1 = Utils.asObjectOrNull(t1.get_referent(), GeoReferent)
                if ((g1) is not None): 
                    break
                if (t1.is_char('.') or (t1.length_char < 3)): 
                    continue
                if ((t1.length_char < 4) and t1.chars.is_all_lower): 
                    continue
                break
            if (g1 is not None): 
                sit.end_token = t1
                nams = g1.get_string_values(GeoReferent.ATTR_NAME)
                if (nams is None or len(nams) == 0): 
                    return None
                sit.value = ("ПОДЪЕЗД - " + nams[0])
                if (len(nams) > 1): 
                    sit.alt_value = ("ПОДЪЕЗД - " + nams[1])
                return sit
            if ((isinstance(t1, TextToken)) and (t1.whitespaces_before_count < 2) and t1.chars.is_capital_upper): 
                cit = CityItemToken.try_parse(t1, None, True, None)
                if (cit is not None and ((cit.typ == CityItemToken.ItemType.PROPERNAME or cit.typ == CityItemToken.ItemType.CITY))): 
                    sit.end_token = cit.end_token
                    sit.value = ("ПОДЪЕЗД - " + cit.value)
                    return sit
        if (tt is not None and tt.length_char == 1): 
            t1 = NameToken.check_initial(tt)
            if (t1 is not None): 
                res = StreetItemToken.try_parse(t1, None, False, None)
                if (res is not None): 
                    if (res.value is None): 
                        res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO)
                    res.begin_token = tt
                    return res
        return None
    
    @staticmethod
    def _try_parse_spec(t : 'Token', prev : 'StreetItemToken') -> typing.List['StreetItemToken']:
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.NumToken import NumToken
        if (t is None): 
            return None
        res = None
        sit = None
        if (t.is_value2("ЗА", "ЛИНИЕЙ")): 
            next0__ = AddressItemToken.try_parse(t.next0_.next0_, False, None, None)
            if (next0__ is not None): 
                sit = StreetItemToken._new300(t, next0__.end_token, StreetItemType.STDNAME)
                nnn = (str(next0__.referent).upper() if next0__.referent is not None else str(next0__).upper())
                if (nnn.startswith("ТЕРРИТОРИЯ ")): 
                    nnn = nnn[11:]
                sit.value = ("ЗА ЛИНИЕЙ " + nnn)
                res = list()
                res.append(sit)
                return res
        if (isinstance(t.get_referent(), DateReferent)): 
            dr = Utils.asObjectOrNull(t.get_referent(), DateReferent)
            if (not (isinstance(t.begin_token, NumberToken))): 
                if (dr.month > 0 and t.begin_token == t.end_token): 
                    res = list()
                    sit = StreetItemToken._new284(t, t, StreetItemType.STDNAME, MiscHelper.get_text_value_of_meta_token(Utils.asObjectOrNull(t, ReferentToken), GetTextAttr.NO))
                    res.append(sit)
                    return res
                return None
            if (dr.year == 0 and dr.day > 0 and dr.month > 0): 
                res = list()
                res.append(StreetItemToken._new444(t, t, StreetItemType.NUMBER, True, NumberSpellingType.DIGIT, str(dr.day)))
                tmp = dr.to_string_ex(False, t.morph.language, 0)
                i = tmp.find(' ')
                sit = StreetItemToken._new284(t, t, StreetItemType.STDNAME, tmp[i + 1:].upper())
                res.append(sit)
                sit.chars.is_capital_upper = True
                return res
            if (dr.year > 0 and dr.month == 0): 
                res = list()
                res.append(StreetItemToken._new444(t, t, StreetItemType.NUMBER, True, NumberSpellingType.DIGIT, str(dr.year)))
                sit = StreetItemToken._new284(t, t, StreetItemType.STDNAME, ("РОКУ" if t.morph.language.is_ua else "ГОДА"))
                res.append(sit)
                sit.chars.is_capital_upper = True
                return res
            return None
        if (prev is not None and prev.typ == StreetItemType.AGE): 
            res = list()
            if (isinstance(t.get_referent(), GeoReferent)): 
                sit = StreetItemToken._new448(t, t, StreetItemType.NAME, t.get_source_text().upper(), t.get_referent().to_string_ex(True, t.kit.base_language, 0).upper())
                res.append(sit)
            elif (t.is_value("ГОРОД", None) or t.is_value("МІСТО", None)): 
                sit = StreetItemToken._new284(t, t, StreetItemType.NAME, "ГОРОДА")
                res.append(sit)
            else: 
                return None
            return res
        if (prev is not None and prev.typ == StreetItemType.NOUN): 
            num = NumToken.try_parse(t, GeoTokenType.STREET)
            if (num is not None): 
                res = list()
                sit = StreetItemToken._new284(num.begin_token, num.end_token, StreetItemType.NUMBER, num.value)
                res.append(sit)
                return res
        can_be_road = False
        if (prev is not None and prev.is_road and (t.whitespaces_before_count < 3)): 
            can_be_road = True
        elif (((prev is None and t.next0_ is not None and t.next0_.is_hiphen) and MiscLocationHelper.is_user_param_address(t) and t.next0_.next0_ is not None) and t.next0_.next0_.length_char > 1): 
            cou = 5
            tt = t.next0_
            while tt is not None and cou > 0: 
                if (tt.whitespaces_before_count > 3): 
                    break
                if ((isinstance(tt, NumberToken)) or tt.is_comma): 
                    break
                sit1 = StreetItemToken.try_parse(tt, None, False, None)
                if (sit1 is not None and sit1.typ == StreetItemType.NOUN): 
                    if (sit1.is_road): 
                        can_be_road = True
                    break
                tt = tt.next0_; cou -= 1
        if (can_be_road): 
            vals = None
            t1 = None
            br = False
            tt = t
            first_pass3793 = True
            while True:
                if first_pass3793: first_pass3793 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.whitespaces_before_count > 3 and tt != t): 
                    break
                if (BracketHelper.is_bracket(tt, False)): 
                    if (tt == t): 
                        br = True
                        continue
                    break
                val = None
                if (isinstance(tt.get_referent(), GeoReferent)): 
                    rt = Utils.asObjectOrNull(tt, ReferentToken)
                    if (rt.begin_token == rt.end_token and (isinstance(rt.end_token, TextToken))): 
                        val = rt.end_token.term
                    else: 
                        val = tt.get_referent().to_string_ex(True, tt.kit.base_language, 0).upper()
                    t1 = tt
                elif ((isinstance(tt, TextToken)) and tt.chars.is_capital_upper): 
                    cit = CityItemToken.try_parse(tt, None, True, None)
                    if (cit is not None and cit.org_ref is None and ((cit.typ == CityItemToken.ItemType.PROPERNAME or cit.typ == CityItemToken.ItemType.CITY))): 
                        val = (Utils.ifNotNull(cit.value, (cit.onto_item.canonic_text if cit is not None and cit.onto_item is not None else None)))
                        tt = cit.end_token
                        t1 = tt
                    else: 
                        break
                else: 
                    break
                if (vals is None): 
                    vals = list()
                if (val.find('-') > 0 and (isinstance(tt, TextToken))): 
                    vals.extend(Utils.splitString(val, '-', False))
                else: 
                    vals.append(val)
                if (tt.next0_ is not None and tt.next0_.is_hiphen): 
                    tt = tt.next0_
                elif (tt.next0_ is not None and tt.next0_.is_comma and br): 
                    tt = tt.next0_
                else: 
                    break
            if (vals is not None): 
                ok = False
                if (len(vals) > 1): 
                    ok = True
                elif (MiscLocationHelper.check_geo_object_before(t, False)): 
                    ok = True
                else: 
                    sit1 = StreetItemToken.try_parse(t1.next0_, None, False, None)
                    if (sit1 is not None and sit1.typ == StreetItemType.NUMBER and sit1.is_number_km): 
                        ok = True
                if (ok): 
                    if (br): 
                        if (BracketHelper.is_bracket(t1.next0_, False)): 
                            t1 = t1.next0_
                    res = list()
                    if (prev is not None): 
                        prev.noun_is_doubt_coef = 0
                        prev.is_abridge = False
                    sit = StreetItemToken._new300(t, t1, StreetItemType.NAME)
                    res.append(sit)
                    if (len(vals) == 1): 
                        sit.value = vals[0]
                    elif (len(vals) == 2): 
                        sit.value = "{0} - {1}".format(vals[0], vals[1])
                        sit.alt_value = "{0} - {1}".format(vals[1], vals[0])
                    elif (len(vals) == 3): 
                        sit.value = "{0} - {1} - {2}".format(vals[0], vals[1], vals[2])
                        sit.alt_value = "{0} - {1} - {2}".format(vals[2], vals[1], vals[0])
                    elif (len(vals) == 4): 
                        sit.value = "{0} - {1} - {2} - {3}".format(vals[0], vals[1], vals[2], vals[3])
                        sit.alt_value = "{0} - {1} - {2} - {3}".format(vals[3], vals[2], vals[1], vals[0])
                    else: 
                        return None
                    return res
            if (((isinstance(t, TextToken)) and t.length_char == 1 and t.chars.is_letter) and t.next0_ is not None): 
                if (t.is_value("К", None) or t.is_value("Д", None)): 
                    return None
                tt = t.next0_
                if (tt.is_hiphen and tt.next0_ is not None): 
                    tt = tt.next0_
                if (isinstance(tt, NumberToken)): 
                    res = list()
                    prev.noun_is_doubt_coef = 0
                    sit = StreetItemToken._new300(t, tt, StreetItemType.NAME)
                    res.append(sit)
                    ch = t.term[0]
                    ch0 = LanguageHelper.get_cyr_for_lat(ch)
                    if ((ord(ch0)) != 0): 
                        ch = ch0
                    sit.value = "{0}{1}".format(ch, tt.value)
                    sit.is_road_name = True
                    tt = tt.next0_
                    if (tt is not None and tt.is_hiphen and (isinstance(tt.next0_, NumberToken))): 
                        sit.end_token = tt.next0_
                        tt = tt.next0_.next0_
                    br1 = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                    if (br1 is not None and (br1.length_char < 15)): 
                        sit.end_token = br1.end_token
                        sit.alt_value = MiscHelper.get_text_value(tt.next0_, sit.end_token.previous, GetTextAttr.NO)
                    elif (tt is not None and tt.length_char > 2 and not tt.chars.is_all_lower): 
                        if ((((((tt.is_value("ДОН", None) or tt.is_value("КАВКАЗ", None) or tt.is_value("УРАЛ", None)) or tt.is_value("БЕЛАРУСЬ", None) or tt.is_value("УКРАИНА", None)) or tt.is_value("КРЫМ", None) or tt.is_value("ВОЛГА", None)) or tt.is_value("ХОЛМОГОРЫ", None) or tt.is_value("БАЛТИЯ", None)) or tt.is_value("РОССИЯ", None) or tt.is_value("НЕВА", None)) or tt.is_value("КОЛА", None) or tt.is_value("КАСПИЙ", None)): 
                            sit.end_token = tt
                            sit.alt_value = MiscHelper.get_text_value(tt, tt, GetTextAttr.NO)
                        else: 
                            nnn = StreetItemToken._try_parse_spec(tt, prev)
                            if (nnn is not None and len(nnn) == 1 and nnn[0].typ == StreetItemType.NAME): 
                                sit.end_token = nnn[0].end_token
                                sit.alt_value = nnn[0].value
                                sit.alt_value2 = nnn[0].alt_value
                    return res
        return None
    
    @staticmethod
    def __try_attach_road_num(t : 'Token') -> 'StreetItemToken':
        if (t is None): 
            return None
        if (not t.chars.is_letter or t.length_char != 1): 
            return None
        tt = t.next0_
        if (tt is not None and tt.is_hiphen): 
            tt = tt.next0_
        if (not (isinstance(tt, NumberToken))): 
            return None
        res = StreetItemToken._new300(t, tt, StreetItemType.NAME)
        res.value = "{0}{1}".format(t.get_source_text().upper(), tt.value)
        return res
    
    @staticmethod
    def _new262(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'OrgItemToken') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res._org0_ = _arg4
        return res
    
    @staticmethod
    def _new284(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        return res
    
    @staticmethod
    def _new294(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.number_has_prefix = _arg5
        return res
    
    @staticmethod
    def _new297(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.is_in_brackets = _arg5
        return res
    
    @staticmethod
    def _new298(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : 'NumberSpellingType', _arg6 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.number_type = _arg5
        res.number_has_prefix = _arg6
        return res
    
    @staticmethod
    def _new300(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new301(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_in_brackets = _arg4
        return res
    
    @staticmethod
    def _new382(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'Termin') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.termin = _arg4
        return res
    
    @staticmethod
    def _new388(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'GeoReferent') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res._city = _arg4
        return res
    
    @staticmethod
    def _new389(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'StreetItemType', _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.value = _arg3
        res.typ = _arg4
        res.number_has_prefix = _arg5
        return res
    
    @staticmethod
    def _new392(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : 'NumberSpellingType') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.number_type = _arg5
        return res
    
    @staticmethod
    def _new393(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : 'NumberSpellingType', _arg6 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.number_type = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new396(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.has_std_suffix = _arg3
        return res
    
    @staticmethod
    def _new397(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Termin', _arg4 : 'StreetItemType') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.termin = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new398(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Termin', _arg4 : 'StreetItemType', _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.termin = _arg3
        res.typ = _arg4
        res.is_abridge = _arg5
        return res
    
    @staticmethod
    def _new399(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'StreetReferent', _arg5 : 'MorphCollection', _arg6 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.exist_street = _arg4
        res.morph = _arg5
        res.is_in_dictionary = _arg6
        return res
    
    @staticmethod
    def _new402(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : 'NumberSpellingType', _arg6 : bool, _arg7 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.number_type = _arg5
        res.number_has_prefix = _arg6
        res.morph = _arg7
        return res
    
    @staticmethod
    def _new404(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'Termin', _arg5 : bool, _arg6 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.termin = _arg4
        res.is_abridge = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new407(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'Termin', _arg5 : 'Termin', _arg6 : bool, _arg7 : 'MorphCollection', _arg8 : int) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.termin = _arg4
        res.alt_termin = _arg5
        res.is_abridge = _arg6
        res.morph = _arg7
        res.noun_is_doubt_coef = _arg8
        return res
    
    @staticmethod
    def _new408(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new410(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : 'Termin') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.termin = _arg5
        return res
    
    @staticmethod
    def _new412(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'StreetItemType', _arg5 : 'MorphCollection', _arg6 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.alt_typ = _arg4
        res.morph = _arg5
        res.value = _arg6
        return res
    
    @staticmethod
    def _new413(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'StreetItemType', _arg5 : 'MorphCollection', _arg6 : 'Termin') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.alt_typ = _arg4
        res.morph = _arg5
        res.termin = _arg6
        return res
    
    @staticmethod
    def _new414(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.is_in_dictionary = _arg5
        return res
    
    @staticmethod
    def _new415(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : bool, _arg6 : 'Termin') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.is_in_dictionary = _arg5
        res.termin = _arg6
        return res
    
    @staticmethod
    def _new418(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : str, _arg6 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res.misc = _arg5
        res.value = _arg6
        return res
    
    @staticmethod
    def _new420(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool, _arg5 : str, _arg6 : 'MorphCollection') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_in_dictionary = _arg4
        res.value = _arg5
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new422(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'Termin', _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.termin = _arg4
        res.is_abridge = _arg5
        return res
    
    @staticmethod
    def _new423(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_road_name = _arg4
        return res
    
    @staticmethod
    def _new424(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res._no_geo_in_this_token = _arg5
        return res
    
    @staticmethod
    def _new426(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberSpellingType', _arg5 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number_type = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new430(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'MorphCollection', _arg5 : 'Condition') -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.morph = _arg4
        res._cond = _arg5
        return res
    
    @staticmethod
    def _new432(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : 'NumberSpellingType', _arg5 : str, _arg6 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number_type = _arg4
        res.value = _arg5
        res.number_has_prefix = _arg6
        return res
    
    @staticmethod
    def _new444(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool, _arg5 : 'NumberSpellingType', _arg6 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.number_has_prefix = _arg4
        res.number_type = _arg5
        res.value = _arg6
        return res
    
    @staticmethod
    def _new448(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : str, _arg5 : str) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.value = _arg4
        res.alt_value = _arg5
        return res
    
    @staticmethod
    def _new1522(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_railway = _arg4
        return res
    
    @staticmethod
    def _new1523(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemType', _arg4 : bool, _arg5 : int) -> 'StreetItemToken':
        res = StreetItemToken(_arg1, _arg2)
        res.typ = _arg3
        res.is_railway = _arg4
        res.noun_is_doubt_coef = _arg5
        return res
    
    # static constructor for class StreetItemToken
    @staticmethod
    def _static_ctor():
        StreetItemToken.__m_reg_tails = ["ГОРОДОК", "РАЙОН", "МАССИВ", "МАСИВ", "КОМПЛЕКС", "ЗОНА", "КВАРТАЛ", "ОТДЕЛЕНИЕ", "ПАРК", "МЕСТНОСТЬ", "РАЗЪЕЗД", "УРОЧИЩЕ", "САД", "МЕСТОРОЖДЕНИЕ"]
        StreetItemToken.__m_spec_tails = ["БУДКА", "КАЗАРМА"]

StreetItemToken._static_ctor()