# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphClass import MorphClass
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.ner.core.ProperNameHelper import ProperNameHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.NumberToken import NumberToken
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Token import Token
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.geo.internal.CityItemToken import CityItemToken
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
from pullenti.ner.geo.internal.NameToken import NameToken
from pullenti.ner.geo.internal.CityAttachHelper import CityAttachHelper

class TerrDefineHelper:
    
    @staticmethod
    def __try_attach_moscowao(li : typing.List['TerrItemToken'], ad : 'AnalyzerData') -> 'ReferentToken':
        if (li[0].termin_item is None or not li[0].termin_item.is_moscow_region): 
            return None
        if (li[0].is_doubt): 
            ok = False
            if (CityAttachHelper.check_city_after(li[0].end_token.next0_)): 
                ok = True
            else: 
                ali = AddressItemToken.try_parse_list(li[0].end_token.next0_, 2)
                if (ali is not None and len(ali) > 0 and ali[0].typ == AddressItemType.STREET): 
                    ok = True
            if (not ok): 
                return None
        reg = GeoReferent()
        typ = "АДМИНИСТРАТИВНЫЙ ОКРУГ"
        reg._add_typ(typ)
        name = li[0].termin_item.canonic_text
        if (LanguageHelper.ends_with(name, typ)): 
            name = name[0:0+len(name) - len(typ) - 1].strip()
        reg._add_name(name)
        return ReferentToken(reg, li[0].begin_token, li[0].end_token)
    
    @staticmethod
    def try_define(li : typing.List['TerrItemToken'], ad : 'AnalyzerData', attach_always : bool=False, cits : typing.List['CityItemToken']=None, exists : typing.List['GeoReferent']=None) -> 'ReferentToken':
        if (li is None or len(li) == 0): 
            return None
        ex_obj = None
        new_name = None
        adj_list = list()
        noun = None
        add_noun = None
        number = None
        rt = TerrDefineHelper.__try_attach_moscowao(li, ad)
        if (rt is not None): 
            return rt
        can_be_city_before = False
        adj_terr_before = False
        if (cits is not None): 
            if (cits[0].typ == CityItemToken.ItemType.CITY): 
                can_be_city_before = True
            elif (cits[0].typ == CityItemToken.ItemType.NOUN and len(cits) > 1): 
                can_be_city_before = True
        k = 0
        k = 0
        first_pass3987 = True
        while True:
            if first_pass3987: first_pass3987 = False
            else: k += 1
            if (not (k < len(li))): break
            if (li[k].onto_item is not None): 
                if (ex_obj is not None or new_name is not None): 
                    break
                if (noun is not None): 
                    if (k == 1): 
                        if (noun.termin_item.canonic_text == "РАЙОН" or noun.termin_item.canonic_text == "ОБЛАСТЬ" or noun.termin_item.canonic_text == "СОЮЗ"): 
                            if (isinstance(li[k].onto_item.referent, GeoReferent)): 
                                if (li[k].onto_item.referent.is_state): 
                                    break
                            ok = False
                            tt = li[k].end_token.next0_
                            if (tt is None): 
                                ok = True
                            elif (tt.is_char_of(",.")): 
                                ok = True
                            if ((not ok and len(li) >= 4 and li[2].termin_item is not None) and li[3].termin_item is None): 
                                ok = True
                            if (not ok): 
                                ok = MiscLocationHelper.check_geo_object_before(li[0].begin_token, False)
                            if (not ok): 
                                ok = MiscLocationHelper.check_geo_object_after(li[1].end_token, False, False)
                            if (not ok): 
                                adr = AddressItemToken.try_parse(tt, False, None, None)
                                if (adr is not None): 
                                    if (adr.typ == AddressItemType.STREET): 
                                        ok = True
                            if (not ok and MiscLocationHelper.is_user_param_address(tt) and (isinstance(tt, NumberToken))): 
                                ok = True
                            if (not ok): 
                                break
                        if (li[k].onto_item is not None): 
                            if (noun.begin_token.is_value("МО", None) or noun.begin_token.is_value("ЛО", None)): 
                                return None
                ex_obj = li[k]
            elif (li[k].termin_item is not None): 
                if (noun is not None): 
                    break
                if (li[k].termin_item.is_always_prefix and k > 0): 
                    break
                if (k > 0 and li[k].is_doubt): 
                    if (li[k].begin_token == li[k].end_token and li[k].begin_token.is_value("ЗАО", None)): 
                        break
                if (li[k].termin_item.is_adjective or li[k].is_geo_in_dictionary): 
                    adj_list.append(li[k])
                else: 
                    if (ex_obj is not None): 
                        geo_ = Utils.asObjectOrNull(ex_obj.onto_item.referent, GeoReferent)
                        if (geo_ is None): 
                            break
                        if (ex_obj.is_adjective and ((li[k].termin_item.canonic_text == "СОЮЗ" or li[k].termin_item.canonic_text == "ФЕДЕРАЦИЯ"))): 
                            str0_ = str(ex_obj.onto_item)
                            if (not li[k].termin_item.canonic_text in str0_): 
                                break
                        if (li[k].termin_item.canonic_text == "РАЙОН" or li[k].termin_item.canonic_text == "ОКРУГ" or li[k].termin_item.canonic_text == "КРАЙ"): 
                            tmp = io.StringIO()
                            for s in geo_.slots: 
                                if (s.type_name == GeoReferent.ATTR_TYPE): 
                                    print("{0};".format(s.value), end="", file=tmp, flush=True)
                            if (not li[k].termin_item.canonic_text in Utils.toStringStringIO(tmp).upper()): 
                                if (k != 1 or new_name is not None): 
                                    break
                                new_name = li[0]
                                new_name.is_adjective = True
                                new_name.onto_item = (None)
                                ex_obj = (None)
                    noun = li[k]
                    if (k == 0 and not li[k].is_newline_before): 
                        tt = TerrItemToken.try_parse(li[k].begin_token.previous, None, None)
                        if (tt is not None and tt.morph.class0_.is_adjective): 
                            adj_terr_before = True
            else: 
                if (ex_obj is not None): 
                    break
                if (new_name is not None): 
                    if ((k == 2 and len(li) == 3 and li[0] == new_name) and li[1].termin_item is not None): 
                        if (CityItemToken.check_keyword(li[2].end_token.next0_) is not None): 
                            break
                        if (li[0].begin_token.previous is not None): 
                            cit = CityItemToken.try_parse(li[0].begin_token.previous, None, False, None)
                            if (cit is None): 
                                cit = CityItemToken.try_parse(li[0].begin_token.previous.previous, None, False, None)
                            if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN): 
                                return None
                    if ((k == 1 and len(li) == 3 and li[2].termin_item is not None) and li[1].begin_token.is_char('(')): 
                        continue
                    if ((k == 2 and new_name == li[1] and len(li) == 3) and noun is not None): 
                        cit = CityItemToken.try_parse(new_name.begin_token, None, False, None)
                        if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN and cit.end_token.next0_ == li[k].begin_token): 
                            if ("МУНИЦИПАЛ" in noun.termin_item.canonic_text): 
                                nam = CityItemToken.try_parse(cit.end_token.next0_, None, False, None)
                                if (nam is not None and ((nam.typ == CityItemToken.ItemType.PROPERNAME or nam.typ == CityItemToken.ItemType.CITY))): 
                                    if (nam.end_token.next0_ is not None and nam.end_token.next0_.is_and): 
                                        li2 = TerrItemToken.try_parse_list(nam.end_token.next0_.next0_, 4, None)
                                        if (li2 is not None and len(li2) >= 2 and ((li2[0].termin_item is not None or li2[1].termin_item is not None))): 
                                            geo1 = GeoReferent()
                                            rt1 = ReferentToken(geo1, li[0].begin_token, li2[1].end_token)
                                            geo1._add_typ(noun.termin_item.canonic_text)
                                            geo1.add_slot(GeoReferent.ATTR_NAME, MiscHelper.get_text_value(li[1].begin_token, rt1.end_token, GetTextAttr.NO), False, 0)
                                            return rt1
                        else: 
                            break
                    else: 
                        break
                new_name = li[k]
        name = None
        alt_name = None
        full_name = None
        morph_ = None
        typ_var = None
        end_tok = None
        if (ex_obj is not None and noun is not None): 
            geo_ = Utils.asObjectOrNull(ex_obj.onto_item.referent, GeoReferent)
            if (geo_ is not None and not geo_.is_city and ((geo_.is_state or (len(noun.termin_item.canonic_text) < 3) or geo_._contains_type(noun.termin_item.canonic_text)))): 
                pass
            else: 
                new_name = ex_obj
                ex_obj = (None)
        if (ex_obj is not None): 
            if (ex_obj.is_adjective and not ex_obj.morph.language.is_en and noun is None): 
                if (attach_always and ex_obj.end_token.next0_ is not None): 
                    npt = MiscLocationHelper._try_parse_npt(ex_obj.begin_token)
                    if (ex_obj.end_token.next0_.is_comma_and): 
                        pass
                    elif (npt is None): 
                        pass
                    else: 
                        str0_ = StreetItemToken.try_parse(ex_obj.end_token.next0_, None, False, None)
                        if (str0_ is not None): 
                            if (str0_.typ == StreetItemType.NOUN and str0_.end_token == npt.end_token): 
                                return None
                elif (ex_obj.begin_token.is_value("ПОДНЕБЕСНЫЙ", None)): 
                    pass
                elif (MiscLocationHelper.is_user_param_address(ex_obj) and ex_obj.is_newline_before and not StreetItemToken.check_keyword(ex_obj.end_token.next0_)): 
                    sit = StreetItemToken.try_parse(ex_obj.end_token.next0_, None, False, None)
                    if (sit is not None): 
                        if (sit.typ == StreetItemType.NUMBER or sit.typ == StreetItemType.STDADJECTIVE): 
                            return None
                else: 
                    npt = MiscLocationHelper._try_parse_npt(ex_obj.begin_token)
                    if (npt is not None and npt.end_token != npt.begin_token): 
                        return None
                    ttt = ex_obj.end_token.next0_
                    if (ttt is not None and ttt.is_comma and len(li) == 1): 
                        ttt = ttt.next0_
                    elif (AddressItemToken.check_street_after(ex_obj.begin_token, False)): 
                        return None
                    elif (AddressItemToken.check_street_after(ex_obj.begin_token.previous, False)): 
                        return None
                    cit = CityItemToken.try_parse_list(ttt, 5, None)
                    if (cit is not None and ((cit[0].typ == CityItemToken.ItemType.NOUN or cit[0].typ == CityItemToken.ItemType.CITY))): 
                        if (npt is not None and npt.end_token == cit[0].end_token): 
                            pass
                        elif (not MiscLocationHelper.is_user_param_address(ex_obj)): 
                            return None
                        elif (cit[0].typ == CityItemToken.ItemType.NOUN and ((len(cit) == 2 or len(cit) == 4)) and ((cit[1].typ == CityItemToken.ItemType.CITY or cit[1].typ == CityItemToken.ItemType.PROPERNAME))): 
                            if (AddressItemToken.check_street_after(cit[1].begin_token, False)): 
                                return None
                        elif (cit[0].typ == CityItemToken.ItemType.CITY): 
                            pass
                        else: 
                            return None
                    elif ((cit is not None and cit[0].typ == CityItemToken.ItemType.PROPERNAME and len(cit) == 2) and cit[1].typ == CityItemToken.ItemType.NOUN and ex_obj.end_token.next0_.is_comma): 
                        pass
                    elif (ttt is None or ttt.whitespaces_before_count > 4): 
                        return None
                    elif (MiscLocationHelper.check_geo_object_after(ttt.previous, False, False)): 
                        pass
                    elif (not MiscLocationHelper.is_user_param_address(ex_obj)): 
                        return None
                    elif (AddressItemToken.check_house_after(ex_obj.end_token.next0_, True, False)): 
                        return None
                    elif (ttt.is_hiphen): 
                        return None
                    cnou = CityItemToken.check_keyword_before(ex_obj.begin_token.previous)
                    if (cnou is not None): 
                        return None
            if (noun is None and ((ex_obj.can_be_city or ex_obj.can_be_surname))): 
                cit0 = CityItemToken.try_parse_back(ex_obj.begin_token.previous, False)
                if (cit0 is not None and cit0.typ != CityItemToken.ItemType.PROPERNAME): 
                    return None
            if (ex_obj.is_doubt and noun is None): 
                ok2 = False
                if (TerrDefineHelper.__can_be_geo_after(ex_obj.end_token.next0_)): 
                    ok2 = True
                elif (not ex_obj.can_be_surname and not ex_obj.can_be_city): 
                    if ((ex_obj.end_token.next0_ is not None and ex_obj.end_token.next0_.is_char(')') and ex_obj.begin_token.previous is not None) and ex_obj.begin_token.previous.is_char('(')): 
                        ok2 = True
                    elif (ex_obj.chars.is_latin_letter and ex_obj.begin_token.previous is not None): 
                        if (ex_obj.begin_token.previous.is_value("IN", None)): 
                            ok2 = True
                        elif (ex_obj.begin_token.previous.is_value("THE", None) and ex_obj.begin_token.previous.previous is not None and ex_obj.begin_token.previous.previous.is_value("IN", None)): 
                            ok2 = True
                if (not ok2): 
                    cit0 = CityItemToken.try_parse_back(ex_obj.begin_token.previous, False)
                    if (cit0 is not None and cit0.typ != CityItemToken.ItemType.PROPERNAME): 
                        pass
                    else: 
                        if (MiscLocationHelper.check_geo_object_before(ex_obj.begin_token.previous, False)): 
                            pass
                        if (ex_obj.is_newline_before and MiscLocationHelper.is_user_param_address(ex_obj)): 
                            pass
                        else: 
                            return None
            name = ex_obj.onto_item.canonic_text
            morph_ = ex_obj.morph
        elif (new_name is not None and noun is None): 
            if (not MiscLocationHelper.is_user_param_address(new_name)): 
                return None
            if (not li[0].morph.class0_.is_adjective): 
                return None
            if (StreetItemToken.check_keyword(li[0].begin_token)): 
                return None
            after_org = False
            ttt = li[0].begin_token.previous
            if ((ttt is not None and ttt.is_comma and li[0].end_token.next0_ is not None) and li[0].end_token.next0_.is_comma): 
                cou = 10
                tt0 = ttt.previous
                first_pass3988 = True
                while True:
                    if first_pass3988: first_pass3988 = False
                    else: tt0 = tt0.previous; cou -= 1
                    if (not (tt0 is not None and cou > 0)): break
                    org0_ = OrgItemToken.try_parse(tt0, None)
                    if (org0_ is None): 
                        continue
                    if (org0_.end_token.next0_ == ttt): 
                        after_org = True
                        break
                if (after_org): 
                    after_org = False
                    ttt = li[0].end_token.next0_
                    while ttt is not None:
                        if (ttt.is_comma): 
                            ttt = ttt.next0_
                        else: 
                            break
                    ters = TerrItemToken.try_parse_list(ttt, 4, None)
                    if (ters is not None): 
                        if (((len(ters) == 1 or len(ters) == 2)) and ters[0].onto_item is not None): 
                            after_org = True
                        elif (len(ters) == 2 and ters[0].termin_item is not None): 
                            after_org = True
            if (not after_org): 
                if ((len(li) == 3 and li[1].onto_item is None and li[2].onto_item is None) and li[1].termin_item is None and li[2].termin_item is None): 
                    if (MiscLocationHelper.is_user_param_address(li[0])): 
                        if (AddressItemToken.check_house_after(li[2].end_token.next0_, False, False)): 
                            rr = GeoReferent()
                            rr._add_typ("район")
                            rr.add_slot(GeoReferent.ATTR_NAME, MiscHelper.get_text_value_of_meta_token(li[0], GetTextAttr.NO), False, 0)
                            return ReferentToken._new948(rr, li[0].begin_token, li[0].end_token, li[0].morph)
                if (len(li) != 1 or not MiscLocationHelper.check_geo_object_before(li[0].begin_token, False)): 
                    return None
                str0_ = li[0].get_source_text()
                if (Utils.endsWithString(str0_, "О", True)): 
                    return None
                if (Utils.endsWithString(str0_, "ОЕ", True)): 
                    return None
                if (Utils.endsWithString(str0_, "АЯ", True)): 
                    return None
                tt0 = li[0].begin_token.previous
                while tt0 is not None and tt0.is_comma:
                    tt0 = tt0.previous
                if (not (isinstance(tt0, ReferentToken))): 
                    return None
                geo0 = Utils.asObjectOrNull(tt0.get_referent(), GeoReferent)
                if (geo0 is None): 
                    return None
                if (geo0 is not None and geo0.find_slot(GeoReferent.ATTR_TYPE, "район", True) is not None): 
                    return None
                cit = CityItemToken.try_parse_list(li[0].begin_token, 5, None)
                if (cit is not None and len(cit) > 0): 
                    if ((cit[0].typ == CityItemToken.ItemType.CITY or cit[0].typ == CityItemToken.ItemType.NOUN)): 
                        return None
                    if (len(cit) == 2 and cit[1].typ == CityItemToken.ItemType.NOUN): 
                        return None
                    if (len(cit) > 1 and cit[1].typ == CityItemToken.ItemType.NOUN): 
                        if (AddressItemToken.check_street_after(cit[1].end_token.next0_, False)): 
                            return None
                sits = StreetItemToken.try_parse_list(li[0].begin_token, 3, None)
                if (sits is not None and len(sits) == 2 and sits[1].typ == StreetItemType.NOUN): 
                    return None
            name = MiscHelper.get_text_value_of_meta_token(li[0], GetTextAttr.NO)
            morph_ = li[0].morph
            typ_var = "район"
        elif (new_name is not None): 
            j = 1
            while j < k: 
                if (li[j].is_newline_before and ((not li[0].is_newline_before or not li[j].is_newline_after))): 
                    if (BracketHelper.can_be_start_of_sequence(li[j].begin_token, False, False)): 
                        pass
                    else: 
                        if (j < (k - 1)): 
                            return None
                        if (len(li) == 2 and k == 2): 
                            pass
                        else: 
                            li2 = list(li)
                            del li2[0:0+k]
                            rt2 = TerrDefineHelper.try_define(li2, ad, False, None, None)
                            if (rt2 is not None and rt2.end_token == li2[len(li2) - 1].end_token): 
                                pass
                            else: 
                                return None
                j += 1
            morph_ = noun.morph
            if (noun.termin_item.canonic_text == "МУНИЦИПАЛЬНЫЙ РАЙОН"): 
                if (StreetItemToken.check_keyword(noun.begin_token)): 
                    ok = False
                    tt = li[0].begin_token.previous
                    first_pass3989 = True
                    while True:
                        if first_pass3989: first_pass3989 = False
                        else: tt = tt.previous
                        if (not (tt is not None)): break
                        if (tt.length_char == 1): 
                            continue
                        geo_ = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                        if (geo_ is not None): 
                            if (geo_.is_region or geo_.is_state): 
                                ok = True
                        break
                    if (not ok): 
                        return None
            if (new_name.is_adjective): 
                if (noun.termin_item.acronym == "АО"): 
                    if (noun.begin_token != noun.end_token): 
                        return None
                    if (new_name.morph.gender != MorphGender.FEMINIE): 
                        return None
                geo_before = None
                tt0 = li[0].begin_token.previous
                if (tt0 is not None and tt0.is_comma_and): 
                    tt0 = tt0.previous
                if (not li[0].is_newline_before and tt0 is not None): 
                    geo_before = (Utils.asObjectOrNull(tt0.get_referent(), GeoReferent))
                if (Utils.indexOfList(li, noun, 0) < Utils.indexOfList(li, new_name, 0)): 
                    if (noun.termin_item.is_state): 
                        return None
                    if (new_name.can_be_surname and geo_before is None): 
                        if (((noun.morph.case_) & new_name.morph.case_).is_undefined): 
                            return None
                    dont_check = False
                    if (MiscHelper.is_exists_in_dictionary(new_name.begin_token, new_name.end_token, (MorphClass.ADJECTIVE) | MorphClass.PRONOUN | MorphClass.VERB)): 
                        if (noun.begin_token != new_name.begin_token): 
                            if (geo_before is None): 
                                if (len(li) == 2 and TerrDefineHelper.__can_be_geo_after(li[1].end_token.next0_)): 
                                    pass
                                elif (len(li) == 3 and li[2].termin_item is not None and ((TerrDefineHelper.__can_be_geo_after(li[2].end_token.next0_) or "МУНИЦИП" in noun.termin_item.canonic_text or "ГОРОДСК" in noun.termin_item.canonic_text))): 
                                    add_noun = li[2]
                                elif (len(li) == 4 and li[2].termin_item is not None and li[3].termin_item is None): 
                                    pass
                                elif (new_name.is_geo_in_dictionary): 
                                    pass
                                elif (new_name.end_token.is_newline_after): 
                                    pass
                                elif (AddressItemToken.check_street_after(new_name.end_token.next0_, False)): 
                                    pass
                                elif (new_name.end_token.next0_ is not None and new_name.end_token.next0_.is_value("КИЛОМЕТР", None)): 
                                    pass
                                elif (OrgItemToken.try_parse(new_name.end_token.next0_, None) is not None): 
                                    pass
                                elif (MiscLocationHelper.is_user_param_address(new_name)): 
                                    pass
                                else: 
                                    return None
                                dont_check = True
                    if (not dont_check): 
                        npt = NounPhraseHelper.try_parse(new_name.end_token, NounPhraseParseAttr.PARSEPRONOUNS, 0, None)
                        if (npt is not None and npt.end_token != new_name.end_token): 
                            if (len(li) == 3 and li[2].termin_item is not None and npt.end_token == li[2].end_token): 
                                add_noun = li[2]
                            elif (len(li) == 4 and li[2].termin_item is not None and npt.end_token == li[2].end_token): 
                                pass
                            elif (AddressItemToken.check_street_after(npt.end_token, False)): 
                                pass
                            elif (MiscLocationHelper.check_geo_object_after(new_name.end_token, False, False)): 
                                pass
                            elif (npt.end_token.is_value("КИЛОМЕТР", None)): 
                                pass
                            elif (OrgItemToken.try_parse(new_name.end_token.next0_, None) is not None): 
                                pass
                            elif (len(li) == 2 and new_name == li[1]): 
                                cits0 = CityItemToken.try_parse_list(li[1].end_token.next0_, 2, None)
                                if (cits0 is not None and len(cits0) == 1 and cits0[0].typ == CityItemToken.ItemType.NOUN): 
                                    end_tok = cits0[0].end_token
                                else: 
                                    return None
                            else: 
                                return None
                    rtp = new_name.kit.process_referent("PERSON", new_name.begin_token, None)
                    if (rtp is not None): 
                        return None
                    if (new_name.real_name is not None): 
                        name = ProperNameHelper.get_name_ex(new_name.real_name.begin_token, new_name.real_name.end_token, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False)
                    else: 
                        name = ProperNameHelper.get_name_ex(new_name.begin_token, new_name.end_token, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False)
                    vvv = MiscHelper.get_text_value_of_meta_token(new_name, GetTextAttr.NO)
                    if (vvv.endswith("ВО")): 
                        name = vvv
                else: 
                    ok = False
                    if (((k + 1) < len(li)) and li[k].termin_item is None and li[k + 1].termin_item is not None): 
                        ok = True
                    elif ((k < len(li)) and li[k].onto_item is not None): 
                        ok = True
                    elif (k == len(li) and not new_name.is_adj_in_dictionary): 
                        ok = True
                        if (noun.termin_item.canonic_text == "ТЕРРИТОРИЯ"): 
                            cit1 = CityItemToken.try_parse_back(li[0].begin_token.previous, False)
                            if (cit1 is not None and cit1.typ == CityItemToken.ItemType.NOUN): 
                                return None
                        if (noun.begin_token.length_char == 1 and new_name.begin_token == new_name.end_token): 
                            if (NameToken.check_initial_and_surname(noun.begin_token.term, new_name.begin_token)): 
                                return None
                    elif (MiscLocationHelper.check_geo_object_before(li[0].begin_token, False) or can_be_city_before): 
                        ok = True
                    elif (MiscLocationHelper.check_geo_object_after(li[k - 1].end_token, False, False)): 
                        ok = True
                    elif (len(li) == 3 and k == 2): 
                        cit = CityItemToken.try_parse(li[2].begin_token, None, False, None)
                        if (cit is not None): 
                            if (cit.typ == CityItemToken.ItemType.CITY or cit.typ == CityItemToken.ItemType.NOUN): 
                                ok = True
                    elif (len(li) == 2): 
                        ok = TerrDefineHelper.__can_be_geo_after(li[len(li) - 1].end_token.next0_)
                    if (not ok and not li[0].is_newline_before and not li[0].chars.is_all_lower): 
                        rt00 = li[0].kit.process_referent("PERSONPROPERTY", li[0].begin_token.previous, None)
                        if (rt00 is not None): 
                            ok = True
                    if (noun.termin_item is not None and noun.termin_item.is_strong and new_name.is_adjective): 
                        ok = True
                    if (noun.is_doubt and len(adj_list) == 0 and geo_before is None): 
                        return None
                    if (new_name.real_name is not None): 
                        name = ProperNameHelper.get_name_ex(new_name.real_name.begin_token, new_name.real_name.end_token, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False)
                    else: 
                        name = ProperNameHelper.get_name_ex(new_name.begin_token, new_name.end_token, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False)
                    vvv = MiscHelper.get_text_value_of_meta_token(new_name, GetTextAttr.NO)
                    if (vvv.endswith("ВО")): 
                        name = vvv
                    if (not ok and not attach_always and not MiscLocationHelper.is_user_param_address(new_name)): 
                        if (MiscHelper.is_exists_in_dictionary(new_name.begin_token, new_name.end_token, (MorphClass.ADJECTIVE) | MorphClass.PRONOUN | MorphClass.VERB)): 
                            if (exists is not None): 
                                for e0_ in exists: 
                                    if (e0_.find_slot(GeoReferent.ATTR_NAME, name, True) is not None): 
                                        ok = True
                                        break
                            if (not ok): 
                                return None
                    full_name = "{0} {1}".format(ProperNameHelper.get_name_ex(li[0].begin_token, noun.begin_token.previous, MorphClass.ADJECTIVE, MorphCase.UNDEFINED, noun.termin_item.gender, False, False), noun.termin_item.canonic_text)
            else: 
                if (not attach_always or ((noun.termin_item is not None and noun.termin_item.canonic_text == "ФЕДЕРАЦИЯ"))): 
                    is_latin = noun.chars.is_latin_letter and new_name.chars.is_latin_letter
                    if (Utils.indexOfList(li, noun, 0) > Utils.indexOfList(li, new_name, 0)): 
                        if (not is_latin and new_name.named_by is None): 
                            if (noun.end_token.next0_ is not None and noun.end_token.next0_.is_comma): 
                                pass
                            else: 
                                return None
                    if (not new_name.is_district_name and new_name.named_by is None and not BracketHelper.can_be_start_of_sequence(new_name.begin_token, False, False)): 
                        if (len(adj_list) == 0 and MiscHelper.is_exists_in_dictionary(new_name.begin_token, new_name.end_token, (MorphClass.NOUN) | MorphClass.PRONOUN)): 
                            if (len(li) == 2 and noun.is_city_region and (noun.whitespaces_after_count < 2)): 
                                pass
                            elif (MiscLocationHelper.check_geo_object_after(new_name.end_token, False, False)): 
                                pass
                            elif (len(li) < 3): 
                                if (MiscLocationHelper.is_user_param_address(li[0])): 
                                    pass
                                else: 
                                    return None
                            else: 
                                ii = Utils.indexOfList(li, new_name, 0)
                                li2 = list(li)
                                del li2[0:0+ii + 1]
                                rt2 = TerrDefineHelper.try_define(li2, ad, False, None, None)
                                if (rt2 is None): 
                                    return None
                        if (not is_latin): 
                            if ((noun.termin_item.is_region and not attach_always and ((not adj_terr_before or new_name.is_doubt))) and not noun.is_city_region and not noun.termin_item.is_specific_prefix): 
                                if (not MiscLocationHelper.check_geo_object_before(noun.begin_token, False)): 
                                    if (not noun.is_doubt and noun.begin_token != noun.end_token): 
                                        pass
                                    elif ((noun.termin_item.is_always_prefix and len(li) == 2 and li[0] == noun) and li[1] == new_name): 
                                        pass
                                    elif (MiscLocationHelper.is_user_param_address(li[0])): 
                                        pass
                                    else: 
                                        return None
                            if (noun.is_doubt and len(adj_list) == 0): 
                                if (noun.termin_item.acronym == "МО" or noun.termin_item.acronym == "ЛО"): 
                                    if (k == (len(li) - 1) and li[k].termin_item is not None): 
                                        add_noun = li[k]
                                        k += 1
                                    elif (len(li) == 2 and noun == li[0] and str(new_name).endswith("совет")): 
                                        pass
                                    else: 
                                        return None
                                else: 
                                    return None
                            if (new_name.begin_token.is_value("КОРОЛЕВ", None)): 
                                pass
                            else: 
                                pers = new_name.kit.process_referent("PERSON", new_name.begin_token, None)
                                if (pers is not None): 
                                    return None
                if (new_name.real_name is not None): 
                    name = MiscHelper.get_text_value(new_name.real_name.begin_token, new_name.real_name.end_token, GetTextAttr.NO)
                else: 
                    name = MiscHelper.get_text_value(new_name.begin_token, new_name.end_token, GetTextAttr.NO)
                if (new_name.named_by is not None): 
                    name = MiscHelper.get_text_value_of_meta_token(new_name.named_by, GetTextAttr.NO)
                if (new_name.begin_token != new_name.end_token): 
                    ttt = new_name.begin_token.next0_
                    while ttt is not None and ttt.end_char <= new_name.end_char: 
                        if (ttt.chars.is_letter): 
                            ty = TerrItemToken.try_parse(ttt, None, None)
                            if ((ty is not None and ty.termin_item is not None and noun is not None) and ((noun.termin_item.canonic_text in ty.termin_item.canonic_text or ty.termin_item.canonic_text in noun.termin_item.canonic_text))): 
                                name = MiscHelper.get_text_value(new_name.begin_token, ttt.previous, GetTextAttr.NO)
                                break
                            cit = CityItemToken.try_parse(ttt, None, False, None)
                            if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN): 
                                typ_var = cit.value.lower()
                                name = MiscHelper.get_text_value(new_name.begin_token, ttt.previous, GetTextAttr.NO)
                                if (ttt.previous == new_name.begin_token and BracketHelper.is_bracket(ttt.previous, False) and (cit.end_char < new_name.end_char)): 
                                    name = MiscHelper.get_text_value(cit.end_token.next0_, new_name.end_token, GetTextAttr.NO)
                                break
                        ttt = ttt.next0_
                if (new_name.begin_token != new_name.end_token): 
                    tt2 = new_name.begin_token
                    if (BracketHelper.is_bracket(tt2, False)): 
                        tt2 = tt2.next0_
                    if (tt2.is_value("ГОРОД", None)): 
                        cits2 = CityItemToken.try_parse_list(tt2, 3, None)
                        if (cits2 is not None and len(cits2) == 2 and ((cits2[1].typ == CityItemToken.ItemType.CITY or cits2[1].typ == CityItemToken.ItemType.PROPERNAME))): 
                            rt2 = CityAttachHelper.try_define(cits2, None, False)
                            if (rt2 is not None): 
                                if (new_name.end_char > rt2.end_char): 
                                    rt2.end_token = new_name.end_token
                                if (noun is not None and "ГОРОД" in noun.termin_item.canonic_text): 
                                    if (noun.begin_char < rt2.begin_char): 
                                        rt2.begin_token = noun.begin_token
                                    if (noun.end_char > rt2.end_char): 
                                        rt2.end_token = noun.end_token
                                return rt2
                if (len(adj_list) > 0): 
                    npt = MiscLocationHelper._try_parse_npt(adj_list[0].begin_token)
                    if (npt is not None and npt.end_token == noun.end_token): 
                        alt_name = "{0} {1}".format(npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), name)
        else: 
            if ((len(li) == 1 and noun is not None and noun.end_token.next0_ is not None) and (isinstance(noun.end_token.next0_.get_referent(), GeoReferent))): 
                g = Utils.asObjectOrNull(noun.end_token.next0_.get_referent(), GeoReferent)
                if (noun.termin_item is not None): 
                    tyy = noun.termin_item.canonic_text.lower()
                    ooo = False
                    if (g.find_slot(GeoReferent.ATTR_TYPE, tyy, True) is not None): 
                        ooo = True
                    elif (tyy.endswith("район") and g.find_slot(GeoReferent.ATTR_TYPE, "район", True) is not None): 
                        ooo = True
                    if (ooo): 
                        return ReferentToken._new948(g, noun.begin_token, noun.end_token.next0_, noun.begin_token.morph)
            if ((len(li) == 1 and noun == li[0] and li[0].termin_item is not None) and TerrItemToken.try_parse(li[0].end_token.next0_, None, None) is None and TerrItemToken.try_parse(li[0].begin_token.previous, None, None) is None): 
                if (li[0].morph.number == MorphNumber.PLURAL): 
                    return None
                cou = 0
                str0_ = li[0].termin_item.canonic_text.lower()
                tt = li[0].begin_token.previous
                first_pass3990 = True
                while True:
                    if first_pass3990: first_pass3990 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.is_newline_after): 
                        cou += 10
                    else: 
                        cou += 1
                    if (cou > 500): 
                        break
                    g = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                    if (g is None): 
                        continue
                    ok = True
                    cou = 0
                    tt = li[0].end_token.next0_
                    first_pass3991 = True
                    while True:
                        if first_pass3991: first_pass3991 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        if (tt.is_newline_before): 
                            cou += 10
                        else: 
                            cou += 1
                        if (cou > 500): 
                            break
                        tee = TerrItemToken.try_parse(tt, None, None)
                        if (tee is None): 
                            continue
                        ok = False
                        break
                    if (ok): 
                        ii = 0
                        while g is not None and (ii < 3): 
                            if (g.find_slot(GeoReferent.ATTR_TYPE, str0_, True) is not None): 
                                return ReferentToken._new948(g, li[0].begin_token, li[0].end_token, noun.begin_token.morph)
                            g = g.higher; ii += 1
                    break
            if (len(li) == 1 and li[0].termin_item is not None and li[0].termin_item.canonic_text == "МУНИЦИПАЛЬНЫЙ ОКРУГ"): 
                ait = AddressItemToken.try_parse_pure_item(li[0].end_token.next0_, None, None)
                if (ait is not None and ait.typ == AddressItemType.NUMBER): 
                    number = ait
                    name = number.value
            if (name is None): 
                return None
        ter = None
        if (ex_obj is not None and (isinstance(ex_obj.tag, GeoReferent))): 
            ter = (Utils.asObjectOrNull(ex_obj.tag, GeoReferent))
        else: 
            ter = GeoReferent()
            if (ex_obj is not None): 
                geo_ = Utils.asObjectOrNull(ex_obj.onto_item.referent, GeoReferent)
                if (geo_ is not None and not geo_.is_city and (((geo_.is_state or noun is None or (len(noun.termin_item.canonic_text) < 3)) or geo_._contains_type(noun.termin_item.canonic_text)))): 
                    psevdo = False
                    if (noun is None and ex_obj.begin_token == ex_obj.end_token): 
                        if (ex_obj.begin_token.is_value("ПРИМОРСКИЙ", None)): 
                            cou = 0
                            ttt = ex_obj.end_token.next0_
                            while ttt is not None and (cou < 5): 
                                if (ttt.is_value("АРХАНГЕЛЬСКИЙ", None)): 
                                    psevdo = True
                                    break
                                ttt = ttt.next0_; cou += 1
                    if (psevdo): 
                        ter._add_name(MiscHelper.get_text_value_of_meta_token(ex_obj, GetTextAttr.NO))
                        ter._add_typ("район")
                    else: 
                        ter._merge_slots2(geo_, li[0].kit.base_language)
                else: 
                    ter._add_name(name)
                if (noun is None and ex_obj.can_be_city): 
                    ter._add_typ_city(li[0].kit.base_language, True)
                else: 
                    pass
            elif (name is not None): 
                ter._add_name(name)
                if (alt_name is not None): 
                    ter._add_name(alt_name)
            if (typ_var is not None): 
                ter._add_typ(typ_var)
            if (noun is not None): 
                if (noun.termin_item.canonic_text == "АО"): 
                    ter._add_typ(("АВТОНОМНИЙ ОКРУГ" if li[0].kit.base_language.is_ua else "АВТОНОМНЫЙ ОКРУГ"))
                elif (noun.termin_item.canonic_text == "МУНИЦИПАЛЬНОЕ СОБРАНИЕ" or noun.termin_item.canonic_text == "МУНІЦИПАЛЬНЕ ЗБОРИ"): 
                    ter._add_typ(("МУНІЦИПАЛЬНЕ УТВОРЕННЯ" if li[0].kit.base_language.is_ua else "МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ"))
                elif (noun.termin_item.acronym == "МО" and add_noun is not None): 
                    ter._add_typ(add_noun.termin_item.canonic_text)
                else: 
                    if (noun.termin_item.canonic_text == "СОЮЗ" and ex_obj is not None and ex_obj.end_char > noun.end_char): 
                        return ReferentToken._new948(ter, ex_obj.begin_token, ex_obj.end_token, ex_obj.morph)
                    ter._add_typ(noun.termin_item.canonic_text)
                    if (noun.termin_item.is_region and ter.is_state): 
                        ter._add_typ_reg(li[0].kit.base_language)
                if (noun.termin_item2 is not None): 
                    ter._add_typ(noun.termin_item2.canonic_text)
            if (ter.is_state and ter.is_region): 
                for a in adj_list: 
                    if (a.termin_item.is_region): 
                        ter._add_typ_reg(li[0].kit.base_language)
                        break
            if (ter.is_state): 
                if (full_name is not None): 
                    ter._add_name(full_name)
                if (ter.alpha2 is None and ter.find_slot(GeoReferent.ATTR_NAME, "АБХАЗИЯ", True) is not None): 
                    s = ter.find_slot(GeoReferent.ATTR_TYPE, "государство", True)
                    if (s is not None): 
                        ter.slots.remove(s)
                        ter._add_typ("регион")
        if (noun is None): 
            while k > 1 and li[k - 1] in adj_list:
                k -= 1
        res = ReferentToken(ter, li[0].begin_token, Utils.ifNotNull(end_tok, li[k - 1].end_token))
        if ((k == 2 and len(li) == 3 and noun == li[0]) and li[2].termin_item is not None): 
            if (li[2].termin_item == noun.termin_item or ((li[2].termin_item.canonic_text == "АВТОНОМНЫЙ ОКРУГ" and noun.termin_item.canonic_text == "АО"))): 
                res.end_token = li[2].end_token
                k = 3
        if (noun is not None and noun.morph.class0_.is_noun): 
            res.morph = noun.morph
        else: 
            res.morph = MorphCollection()
            ii = 0
            while ii < k: 
                for v in li[ii].morph.items: 
                    bi = MorphBaseInfo()
                    bi.copy_from(v)
                    if (noun is not None): 
                        if (bi.class0_.is_adjective): 
                            bi.class0_ = MorphClass.NOUN
                    res.morph.add_item(bi)
                ii += 1
        if (li[0].termin_item is not None and li[0].termin_item.is_specific_prefix): 
            res.begin_token = li[0].end_token.next0_
        if (add_noun is not None and add_noun.end_char > res.end_char): 
            res.end_token = add_noun.end_token
        if (number is not None and number.end_char > res.end_char): 
            res.end_token = number.end_token
        if ((isinstance(res.begin_token.previous, TextToken)) and (res.whitespaces_before_count < 2)): 
            tt = Utils.asObjectOrNull(res.begin_token.previous, TextToken)
            if (tt.term == "АР"): 
                for ty in ter.typs: 
                    if ("республика" in ty or "республіка" in ty): 
                        res.begin_token = tt
                        break
        if (len(li) == 3 and li[1] == noun): 
            if (li[2].termin_item == noun.termin_item): 
                res.end_token = li[2].end_token
        if (noun is not None and "МЕЖСЕЛЕН" in noun.termin_item.canonic_text): 
            tt = res.end_token.next0_
            if (tt is not None and tt.is_comma): 
                tt = tt.next0_
            if ((tt is not None and tt.is_value("НАХОДИТЬСЯ", None) and tt.next0_ is not None) and tt.next0_.is_value("ВНЕ", None)): 
                tt = tt.next0_.next0_
                first_pass3992 = True
                while True:
                    if first_pass3992: first_pass3992 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    mc = tt.get_morph_class_in_dictionary()
                    if (not mc.is_noun): 
                        continue
                    if (tt.is_value("ГРАНИЦА", None) or tt.is_value("ПРЕДЕЛ", None) or tt.is_value("ПОСЕЛЕНИЕ", None)): 
                        res.end_token = tt
                    elif (not mc.is_adjective): 
                        break
        if (noun is not None and noun.termin_item.canonic_text == "СЕЛЬСКИЙ ОКРУГ"): 
            t0 = res.begin_token.previous
            if (t0 is not None and ((t0.is_value("ПОСЕЛОК", None) or t0.is_value("ПОСЕЛЕНИЕ", None)))): 
                if (t0.previous is not None and t0.previous.is_value("СЕЛЬСКИЙ", None)): 
                    res.begin_token = t0.previous
        if (noun is not None and noun.termin_item.canonic_text == "АВТОНОМНЫЙ ОКРУГ"): 
            t0 = res.begin_token.previous
            if (t0 is not None and t0.is_char_of(".-")): 
                t0 = t0.previous
            if (t0 is not None and t0.is_value("АО", None)): 
                res.begin_token = t0
        if (noun is not None and noun.termin_item.canonic_text.endswith(" ОКРУГ") and new_name is not None): 
            t0 = res.begin_token.previous
            if (t0 is not None and t0.is_comma): 
                t0 = t0.previous
            if (t0 is not None and t0.previous is not None): 
                ok = False
                if (t0.previous.is_comma): 
                    ok = True
                if (ok): 
                    nnn = TerrItemToken.try_parse(t0, None, None)
                    if (nnn is not None and str(nnn) == str(new_name)): 
                        res.begin_token = t0
                        ter._add_typ("город")
        if (res.end_token.next0_ is not None and res.end_token.next0_.is_hiphen and res.end_token.next0_.next0_ is not None): 
            tt = res.end_token.next0_.next0_
            if (str(ter) == "область Кемеровская"): 
                if (tt.is_value("КУЗБАСС", None)): 
                    res.end_token = tt
            else: 
                next0_ = TerrItemToken.try_parse(tt, None, None)
                if ((next0_ is not None and next0_.onto_item is not None and ex_obj is not None) and next0_.onto_item == ex_obj.onto_item): 
                    res.end_token = tt
            nexts = TerrItemToken.try_parse_list(tt.next0_, 3, None)
            if (nexts is not None and len(nexts) == 1 and nexts[0].termin_item is not None): 
                res.end_token = nexts[0].end_token
        if (res.whitespaces_after_count < 3): 
            tt = res.end_token.next0_
            if (tt is not None and tt.is_value("МУНИЦИПАЛЬНЫЙ", None)): 
                if (NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None) is None): 
                    res.end_token = tt
            if ((isinstance(tt, TextToken)) and tt.term == "МО"): 
                if (str(ter) == "область Московская"): 
                    res.end_token = tt
            if (((isinstance(tt, NumberToken)) and MiscLocationHelper.is_user_param_address(tt) and tt.next0_ is not None) and tt.next0_.is_comma): 
                res.end_token = tt
            tt = res.end_token.next0_
            if (tt is not None and tt.is_char('(')): 
                br = BracketHelper.try_parse(tt, BracketParseAttr.NO, 100)
                if (br is not None and (br.length_char < 100)): 
                    ttt = tt
                    while ttt is not None and (ttt.end_char < br.end_char): 
                        if (ttt.is_value("СОСТАВ", None)): 
                            res.end_token = br.end_token
                            break
                        elif (ttt.get_referent() is not None and ttt.get_referent().type_name == "DATERANGE"): 
                            res.end_token = br.end_token
                            break
                        ttt = ttt.next0_
        return res
    
    @staticmethod
    def __can_be_geo_after(tt : 'Token') -> bool:
        while tt is not None and ((tt.is_comma or BracketHelper.is_bracket(tt, True))):
            tt = tt.next0_
        if (tt is None): 
            return False
        if (isinstance(tt.get_referent(), GeoReferent)): 
            return True
        tli = TerrItemToken.try_parse_list(tt, 2, None)
        if (tli is not None and len(tli) > 1): 
            if (tli[0].termin_item is None and tli[1].termin_item is not None): 
                return True
            elif (tli[0].termin_item is not None and tli[1].termin_item is None): 
                return True
        if (CityAttachHelper.check_city_after(tt)): 
            return True
        if (TerrDefineHelper.try_attach_stateusaterritory(tt) is not None): 
            return True
        return False
    
    @staticmethod
    def try_attach_stateusaterritory(t : 'Token') -> 'ReferentToken':
        if (t is None or not t.chars.is_latin_letter): 
            return None
        tok = TerrItemToken._m_geo_abbrs.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        g = Utils.asObjectOrNull(tok.termin.tag, GeoReferent)
        if (g is None): 
            return None
        if (tok.end_token.next0_ is not None and tok.end_token.next0_.is_char('.')): 
            tok.end_token = tok.end_token.next0_
        gg = g.clone()
        gg.occurrence.clear()
        return ReferentToken(gg, tok.begin_token, tok.end_token)