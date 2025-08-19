# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.morph.MorphCase import MorphCase
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphBaseInfo import MorphBaseInfo
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.Termin import Termin
from pullenti.morph.MorphologyService import MorphologyService
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.Token import Token
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.geo.internal.OrgTypToken import OrgTypToken
from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken

class StreetDefineHelper:
    
    @staticmethod
    def check_street_after(t : 'Token') -> bool:
        if (t is None): 
            return False
        while t is not None and ((t.is_char_of(",;") or t.morph.class0_.is_preposition)):
            t = t.next0_
        li = StreetItemToken.try_parse_list(t, 10, None)
        if (li is None): 
            return False
        rt = StreetDefineHelper._try_parse_street(li, False, False, False, None)
        if (rt is not None and rt.begin_token == t): 
            return True
        else: 
            return False
    
    @staticmethod
    def try_parse_ext_street(sli : typing.List['StreetItemToken']) -> 'ReferentToken':
        a = StreetDefineHelper._try_parse_street(sli, True, False, False, None)
        if (a is not None): 
            return ReferentToken(a.referent, a.begin_token, a.end_token)
        return None
    
    @staticmethod
    def _try_parse_street(sli : typing.List['StreetItemToken'], ext_onto_regim : bool=False, for_metro : bool=False, street_before : bool=False, cross_street : 'StreetReferent'=None) -> 'AddressItemToken':
        if (sli is None or len(sli) == 0): 
            return None
        if ((len(sli) == 2 and sli[0].typ == StreetItemType.NUMBER and sli[1].typ == StreetItemType.NOUN) and sli[1].is_abridge): 
            if (MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                pass
            elif (StreetItemToken._is_region(sli[1].termin.canonic_text) and MiscLocationHelper.is_user_param_address(sli[1])): 
                pass
            else: 
                return None
        if ((len(sli) == 2 and sli[0].typ == StreetItemType.NOUN and sli[0].noun_is_doubt_coef > 1) and sli[0].begin_token.is_value("КВ", None) and sli[1].typ == StreetItemType.NUMBER): 
            at = AddressItemToken.try_parse_pure_item(sli[0].begin_token, None, None)
            if (at is not None and at.value is not None): 
                ttt = at.end_token.next0_
                if (ttt is not None and ttt.is_comma): 
                    ttt = ttt.next0_
                next0_ = AddressItemToken.try_parse_pure_item(ttt, None, None)
                if (next0_ is not None and next0_.typ == AddressItemType.PLOT): 
                    pass
                else: 
                    return None
        if (((len(sli) == 5 and sli[0].typ == StreetItemType.NOUN and sli[0].termin.canonic_text == "УЛИЦА") and sli[2].typ == StreetItemType.NUMBER and sli[3].typ == StreetItemType.NOUN) and sli[4].typ == StreetItemType.NUMBER): 
            sli[1] = sli[1].clone()
            sli[1].begin_token = sli[0].begin_token
            del sli[0]
        if (((len(sli) == 4 and sli[0].typ == StreetItemType.NOUN and sli[1].typ == StreetItemType.NUMBER) and sli[2].typ == StreetItemType.NOUN and sli[0].termin == sli[2].termin) and ((sli[3].typ == StreetItemType.NAME or sli[3].typ == StreetItemType.STDNAME or sli[3].typ == StreetItemType.STDADJECTIVE))): 
            del sli[2]
        if (len(sli) == 4 and sli[0].typ == StreetItemType.NOUN and sli[1].typ == StreetItemType.NUMBER): 
            if (((sli[2].typ == StreetItemType.NUMBER and sli[3].typ == StreetItemType.NOUN)) or ((sli[3].typ == StreetItemType.NUMBER and sli[2].typ == StreetItemType.NOUN))): 
                del sli[2:2+2]
        if (len(sli) == 2 and sli[0].typ == StreetItemType.NOUN and sli[1].typ == StreetItemType.FIX): 
            return StreetDefineHelper.__try_parse_fix(sli)
        if ((len(sli) == 3 and sli[1].typ == StreetItemType.FIX and sli[2].typ == StreetItemType.NOUN) and (((sli[0].typ == StreetItemType.NUMBER or sli[0].typ == StreetItemType.NAME or sli[0].typ == StreetItemType.STDADJECTIVE) or sli[0].typ == StreetItemType.STDNAME))): 
            tmp = list()
            tmp.append(sli[0])
            tmp.append(sli[2])
            res1 = StreetDefineHelper._try_parse_street(tmp, ext_onto_regim, for_metro, street_before, cross_street)
            if (res1 is None): 
                return None
            tmp.clear()
            tmp.append(sli[1])
            res2 = StreetDefineHelper._try_parse_street(tmp, ext_onto_regim, for_metro, street_before, cross_street)
            if (res2 is not None): 
                res1.orto_terr = res2
            return res1
        if (len(sli) == 1 and sli[0].typ == StreetItemType.ABSENT): 
            if (MiscLocationHelper.is_user_param_address(sli[0])): 
                return AddressItemToken._new202(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, StreetReferent())
            return None
        if (len(sli) == 2): 
            if (((sli[0].typ == StreetItemType.ABSENT and sli[1].typ == StreetItemType.NOUN)) or ((sli[1].typ == StreetItemType.ABSENT and sli[0].typ == StreetItemType.NOUN))): 
                return AddressItemToken._new202(AddressItemType.STREET, sli[0].begin_token, sli[1].end_token, StreetReferent())
        i = 0
        j = 0
        not_doubt = False
        is_terr = False
        i = 0
        first_pass3780 = True
        while True:
            if first_pass3780: first_pass3780 = False
            else: i += 1
            if (not (i < len(sli))): break
            if (i == 0 and sli[i].typ == StreetItemType.FIX and ((len(sli) == 1 or sli[1].typ != StreetItemType.NOUN or sli[0]._org0_ is not None))): 
                return StreetDefineHelper.__try_parse_fix(sli)
            elif (sli[i].typ == StreetItemType.NAME and sli[i].termin is not None and sli[i].termin.canonic_text == "НАБЕРЕЖНАЯ"): 
                if (((i + 1) < len(sli)) and sli[i + 1].typ == StreetItemType.NOUN): 
                    i += 1
                break
            elif (sli[i].typ == StreetItemType.NOUN): 
                if (len(sli) == 1 and sli[0].noun_can_be_name and MiscLocationHelper.is_user_param_address(sli[0])): 
                    continue
                if (sli[i].termin.canonic_text == "МЕТРО"): 
                    if ((i + 1) < len(sli)): 
                        sli1 = list()
                        ii = i + 1
                        while ii < len(sli): 
                            sli1.append(sli[ii])
                            ii += 1
                        str1 = StreetDefineHelper._try_parse_street(sli1, ext_onto_regim, True, False, None)
                        if (str1 is not None): 
                            str1.begin_token = sli[i].begin_token
                            str1.is_doubt = sli[i].is_abridge
                            if (sli[i + 1].is_in_brackets): 
                                str1.is_doubt = False
                            return str1
                    elif (i == 1 and sli[0].typ == StreetItemType.NAME): 
                        for_metro = True
                        break
                    if (i == 0 and len(sli) > 0): 
                        for_metro = True
                        break
                    return None
                if (i == 0 and (i + 1) >= len(sli) and ((sli[i].termin.canonic_text == "ВОЕННЫЙ ГОРОДОК" or sli[i].termin.canonic_text == "ПРОМЗОНА"))): 
                    stri0 = StreetReferent()
                    stri0._add_typ("микрорайон")
                    stri0.add_slot(StreetReferent.ATTR_NAME, sli[i].termin.canonic_text, False, 0)
                    return AddressItemToken._new269(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, stri0, True)
                if (i == 0 and (i + 1) >= len(sli) and sli[i].termin.canonic_text == "МИКРОРАЙОН"): 
                    stri0 = StreetReferent()
                    stri0.kind = StreetKind.AREA
                    stri0.add_slot(StreetReferent.ATTR_TYPE, sli[i].termin.canonic_text.lower(), False, 0)
                    return AddressItemToken._new269(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, stri0, True)
                if (sli[i].termin.canonic_text == "ПЛОЩАДЬ" or sli[i].termin.canonic_text == "ПЛОЩА"): 
                    tt = sli[i].end_token.next0_
                    if (tt is not None and ((tt.is_hiphen or tt.is_char(':')))): 
                        tt = tt.next0_
                    nex = NumberHelper.try_parse_number_with_postfix(tt)
                    if (nex is not None): 
                        return None
                    if (i > 0 and sli[i - 1].value == "ПРОЕКТИРУЕМЫЙ"): 
                        return None
                break
        if (i >= len(sli)): 
            return StreetDefineHelper.__try_detect_non_noun(sli, ext_onto_regim, for_metro, street_before, cross_street)
        name = None
        number = None
        age = None
        adj = None
        noun = sli[i]
        alt_noun = None
        is_micro_raion = StreetItemToken._is_region(noun.termin.canonic_text)
        is_proezd = False
        before = 0
        after = 0
        j = 0
        while j < i: 
            if (((sli[j].typ == StreetItemType.NAME or sli[j].typ == StreetItemType.STDNAME or sli[j].typ == StreetItemType.FIX) or sli[j].typ == StreetItemType.STDADJECTIVE or sli[j].typ == StreetItemType.STDPARTOFNAME) or sli[j].typ == StreetItemType.AGE): 
                before += 1
            elif (sli[j].typ == StreetItemType.NUMBER): 
                if (sli[j].is_newline_after): 
                    return None
                if (sli[j].number_type != NumberSpellingType.UNDEFINED and sli[j].begin_token.morph.class0_.is_adjective): 
                    before += 1
                elif (is_micro_raion or not_doubt): 
                    before += 1
                elif (sli[i].number_has_prefix or sli[i].is_number_km): 
                    before += 1
                elif (MiscLocationHelper.is_user_param_address(sli[i])): 
                    before += 1
            else: 
                before += 1
            j += 1
        j = (i + 1)
        while j < len(sli): 
            if (before > 0 and sli[j].is_newline_before): 
                break
            elif (((sli[j].typ == StreetItemType.NAME or sli[j].typ == StreetItemType.STDNAME or sli[j].typ == StreetItemType.FIX) or sli[j].typ == StreetItemType.STDADJECTIVE or sli[j].typ == StreetItemType.STDPARTOFNAME) or sli[j].typ == StreetItemType.AGE): 
                after += 1
            elif (sli[j].typ == StreetItemType.NUMBER): 
                if (sli[j].number_type != NumberSpellingType.UNDEFINED and sli[j].begin_token.morph.class0_.is_adjective): 
                    after += 1
                elif (is_micro_raion or not_doubt): 
                    after += 1
                elif (sli[j].number_has_prefix or sli[j].is_number_km): 
                    after += 1
                elif (ext_onto_regim or MiscLocationHelper.is_user_param_gar_address(sli[j])): 
                    after += 1
                elif (len(sli) == 2 and sli[0].typ == StreetItemType.NOUN and j == 1): 
                    after += 1
                elif ((len(sli) > 2 and sli[0].typ == StreetItemType.NOUN and sli[1].typ == StreetItemType.NOUN) and j == 2): 
                    after += 1
                elif ((len(sli) == 3 and sli[0].typ == StreetItemType.NOUN and sli[2].typ == StreetItemType.NOUN) and j == 1): 
                    after += 1
                elif (((j + 1) < len(sli)) and sli[j + 1].typ == StreetItemType.NOUN): 
                    after += 1
            elif (sli[j].typ == StreetItemType.NOUN): 
                is_reg = StreetItemToken._is_region(sli[j].termin.canonic_text)
                if (((j == (i + 1) or j == (len(sli) - 1))) and alt_noun is None and not is_reg): 
                    alt_noun = sli[j]
                elif (alt_noun is None and ((sli[i].termin.canonic_text == "ПРОЕЗД" or ((sli[j].termin.canonic_text == "ПРОЕЗД" or sli[j].termin.canonic_text == "НАБЕРЕЖНАЯ")))) and not is_micro_raion): 
                    alt_noun = sli[j]
                    is_proezd = True
                elif (j == 1 and len(sli) == 3 and sli[2].typ == StreetItemType.NUMBER): 
                    alt_noun = sli[j]
                elif (((j + 1) < len(sli)) and not sli[j].is_newline_after): 
                    break
                else: 
                    alt_noun = sli[j]
            else: 
                after += 1
            j += 1
        rli = list()
        n0 = 0
        n1 = 0
        if (before > after): 
            if (noun.termin.canonic_text == "МЕТРО"): 
                return None
            if (noun.termin.canonic_text == "КВАРТАЛ" and not ext_onto_regim and not street_before): 
                if (sli[0].typ == StreetItemType.NUMBER and len(sli) == 2): 
                    if (not AddressItemToken.check_house_after(sli[1].end_token.next0_, False, False)): 
                        if (not MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                            return None
                        if (sli[0].begin_token.previous is not None and sli[0].begin_token.previous.get_morph_class_in_dictionary().is_preposition): 
                            return None
            tt = sli[0].begin_token
            if (tt == sli[0].end_token and noun.begin_token == sli[0].end_token.next0_ and not MiscLocationHelper.is_user_param_address(sli[0])): 
                if (not tt.morph.class0_.is_adjective and not (isinstance(tt, NumberToken))): 
                    if ((sli[0].is_newline_before or not MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False) or noun.morph.case_.is_genitive) or noun.morph.case_.is_instrumental): 
                        ok = False
                        if (AddressItemToken.check_house_after(noun.end_token.next0_, False, True)): 
                            ok = True
                        elif (noun.end_token.next0_ is None): 
                            ok = True
                        elif (noun.is_newline_after and MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                            ok = True
                        if (not ok): 
                            if ((noun.chars.is_latin_letter and noun.chars.is_capital_upper and sli[0].chars.is_latin_letter) and sli[0].chars.is_capital_upper): 
                                ok = True
                        if (not ok): 
                            return None
            n0 = 0
            n1 = (i - 1)
        elif (i == 1 and sli[0].typ == StreetItemType.NUMBER): 
            if (not sli[0].is_whitespace_after): 
                return None
            number = sli[0].value
            if (sli[0].is_number_km): 
                number += "км"
            n0 = (i + 1)
            n1 = (len(sli) - 1)
            rli.append(sli[0])
            rli.append(sli[i])
        elif (after > before): 
            n0 = (i + 1)
            n1 = (len(sli) - 1)
            rli.append(sli[i])
            if (alt_noun is not None and alt_noun == sli[i + 1]): 
                rli.append(sli[i + 1])
                n0 += 1
        elif (after == 0): 
            if (alt_noun is None or len(sli) != 2): 
                return None
            n0 = 1
            n1 = 0
        elif ((len(sli) > 2 and ((sli[0].typ == StreetItemType.NAME or sli[0].typ == StreetItemType.STDADJECTIVE or sli[0].typ == StreetItemType.STDNAME)) and sli[1].typ == StreetItemType.NOUN) and sli[2].typ == StreetItemType.NUMBER): 
            n0 = 0
            n1 = 0
            num = False
            tt2 = sli[2].end_token.next0_
            if (sli[2].is_number_km): 
                num = True
            elif (sli[0].begin_token.previous is not None and sli[0].begin_token.previous.is_value("КИЛОМЕТР", None)): 
                sli[2].is_number_km = True
                num = True
            elif (sli[2].begin_token.previous.is_comma): 
                pass
            elif (sli[2].begin_token != sli[2].end_token): 
                num = True
            elif (AddressItemToken.check_house_after(sli[2].end_token.next0_, False, True)): 
                num = True
            elif (sli[2].morph.class0_.is_adjective and (sli[2].whitespaces_before_count < 2)): 
                if (sli[2].end_token.next0_ is None or sli[2].end_token.is_comma or sli[2].is_newline_after): 
                    num = True
            if (num): 
                number = sli[2].value
                if (sli[2].is_number_km): 
                    number += "км"
                rli.append(sli[2])
            else: 
                del sli[2:2+len(sli) - 2]
        elif ((len(sli) > 2 and sli[0].typ == StreetItemType.STDADJECTIVE and sli[1].typ == StreetItemType.NOUN) and sli[2].typ == StreetItemType.STDNAME): 
            n0 = 0
            n1 = -1
            rli.append(sli[0])
            rli.append(sli[2])
            adj = sli[0]
            name = sli[2]
        else: 
            return None
        sec_number = None
        j = n0
        first_pass3781 = True
        while True:
            if first_pass3781: first_pass3781 = False
            else: j += 1
            if (not (j <= n1)): break
            if (sli[j].typ == StreetItemType.NUMBER): 
                if (sli[j].is_newline_before and j > 0): 
                    break
                if (number is not None): 
                    if (name is not None and name.typ == StreetItemType.STDNAME): 
                        sec_number = sli[j].value
                        if (sli[j].is_number_km): 
                            sec_number += "км"
                        rli.append(sli[j])
                        continue
                    if (((j + 1) < len(sli)) and sli[j + 1].typ == StreetItemType.STDNAME): 
                        sec_number = sli[j].value
                        if (sli[j].is_number_km): 
                            sec_number += "км"
                        rli.append(sli[j])
                        continue
                    break
                if (sli[j].number_type == NumberSpellingType.DIGIT and not sli[j].begin_token.morph.class0_.is_adjective and not sli[j].end_token.morph.class0_.is_adjective): 
                    if (sli[j].whitespaces_before_count > 2 and j > 0): 
                        break
                    nval = 0
                    wrapnval271 = RefOutArgWrapper(0)
                    Utils.tryParseInt(sli[j].value, wrapnval271)
                    nval = wrapnval271.value
                    if (nval > 20): 
                        if (j > n0): 
                            if (((j + 1) < len(sli)) and ((sli[j + 1].typ == StreetItemType.NOUN or sli[j + 1].value == "ГОДА"))): 
                                pass
                            elif (sli[j].next_item is not None): 
                                pass
                            elif ((j + 1) == len(sli) and sli[j].begin_token.previous.is_hiphen): 
                                tt = sli[j].end_token.next0_
                                if (tt is not None and tt.is_comma): 
                                    tt = tt.next0_
                                ait = AddressItemToken.try_parse_pure_item(tt, None, None)
                                if (ait is not None and ait.typ == AddressItemType.HOUSE): 
                                    pass
                                elif (MiscLocationHelper.is_user_param_gar_address(sli[j])): 
                                    pass
                                else: 
                                    break
                            else: 
                                break
                    if (j == n0 and n0 > 0): 
                        pass
                    elif (j == n0 and n0 == 0 and sli[j].whitespaces_after_count == 1): 
                        pass
                    elif (sli[j].number_has_prefix or sli[j].is_number_km): 
                        pass
                    elif (j == n1 and ((n1 + 1) < len(sli)) and sli[n1 + 1].typ == StreetItemType.NOUN): 
                        pass
                    elif (not sli[j].is_whitespace_before): 
                        pass
                    elif (MiscLocationHelper.is_user_param_gar_address(sli[j])): 
                        pass
                    else: 
                        break
                number = sli[j].value
                if (sli[j].is_number_km): 
                    number += "км"
                rli.append(sli[j])
            elif (sli[j].typ == StreetItemType.AGE): 
                if (age is not None): 
                    break
                age = sli[j].value
                rli.append(sli[j])
            elif (sli[j].typ == StreetItemType.STDADJECTIVE): 
                if (adj is not None): 
                    if (j == (len(sli) - 1) and not sli[j].is_abridge and name is None): 
                        name = sli[j]
                        rli.append(sli[j])
                        continue
                    else: 
                        return None
                adj = sli[j]
                rli.append(sli[j])
            elif (sli[j].typ == StreetItemType.NAME or sli[j].typ == StreetItemType.STDNAME or sli[j].typ == StreetItemType.FIX): 
                if (sli[j].typ == StreetItemType.NAME and sli[j].termin is not None and sli[j].termin.canonic_text == "НАБЕРЕЖНАЯ"): 
                    alt_noun = sli[j]
                else: 
                    if (name is not None): 
                        if (j > 1 and sli[j - 2].typ == StreetItemType.NOUN): 
                            if (name.noun_can_be_name and sli[j - 2].termin.canonic_text == "УЛИЦА" and j == (len(sli) - 1)): 
                                noun = name
                            elif ((is_micro_raion and sli[j - 1].termin is not None and StreetItemToken._is_region(sli[j - 1].termin.canonic_text)) and j == (len(sli) - 1)): 
                                noun = name
                            else: 
                                break
                        elif (i < j): 
                            break
                        else: 
                            return None
                    name = sli[j]
                rli.append(sli[j])
            elif (sli[j].typ == StreetItemType.STDPARTOFNAME and j == n1): 
                if (name is not None): 
                    break
                name = sli[j]
                rli.append(sli[j])
            elif (sli[j].typ == StreetItemType.NOUN): 
                if ((sli[0] == noun and ((noun.termin.canonic_text == "УЛИЦА" or noun.termin.canonic_text == "ВУЛИЦЯ")) and j > 0) and name is None): 
                    alt_noun = noun
                    noun = sli[j]
                    rli.append(sli[j])
                elif (sli[j] == alt_noun or j == (len(sli) - 1)): 
                    rli.append(sli[j])
                elif ((noun is not None and noun.is_road and sli[j].typ == StreetItemType.NOUN) and sli[j].is_road): 
                    alt_noun = sli[j]
                    rli.append(sli[j])
                else: 
                    break
        if (((n1 < i) and number is None and ((i + 1) < len(sli))) and sli[i + 1].typ == StreetItemType.NUMBER and sli[i + 1].number_has_prefix): 
            number = sli[i + 1].value
            rli.append(sli[i + 1])
        elif ((((i < n0) and ((name is not None or adj is not None)) and (j < len(sli))) and sli[j].typ == StreetItemType.NOUN and ((noun.termin.canonic_text == "УЛИЦА" or noun.termin.canonic_text == "ВУЛИЦЯ"))) and (((sli[j].termin.canonic_text == "ПЛОЩАДЬ" or sli[j].termin.canonic_text == "БУЛЬВАР" or sli[j].termin.canonic_text == "ПЛОЩА") or sli[j].termin.canonic_text == "МАЙДАН" or (j + 1) == len(sli)))): 
            alt_noun = noun
            noun = sli[j]
            rli.append(sli[j])
        if ((alt_noun is not None and name is None and number is None) and age is None and adj is None): 
            if (noun.termin.canonic_text == "УЛИЦА"): 
                name = alt_noun
                alt_noun = (None)
            elif (alt_noun.termin.canonic_text == "УЛИЦА"): 
                name = noun
                noun = alt_noun
                alt_noun = (None)
            elif (alt_noun.noun_can_be_name): 
                name = alt_noun
                alt_noun = (None)
            if (name is not None): 
                rli.append(name)
        if (not noun in rli): 
            rli.append(noun)
        if (alt_noun is not None and not alt_noun in rli): 
            rli.append(alt_noun)
        if (name is None): 
            if (number is None and age is None and adj is None): 
                return None
            if (noun.is_abridge and not MiscLocationHelper.is_user_param_address(noun)): 
                if (is_micro_raion or not_doubt): 
                    pass
                elif (noun.termin is not None and ((noun.termin.canonic_text == "ПРОЕЗД" or noun.termin.canonic_text == "ПРОЇЗД"))): 
                    pass
                elif (adj is None or adj.is_abridge): 
                    return None
            if (adj is not None and adj.is_abridge): 
                if (not noun.is_abridge and MiscLocationHelper.is_user_param_address(adj)): 
                    pass
                elif (alt_noun is not None): 
                    pass
                else: 
                    return None
        if (alt_noun is not None and alt_noun.termin.canonic_text == "УЛИЦА"): 
            alt_noun = (None)
            is_micro_raion = StreetItemToken._is_region(noun.termin.canonic_text)
        if (alt_noun is not None and noun.termin.canonic_text == "УЛИЦА" and alt_noun.termin.canonic_text != "МЕТРО"): 
            noun = alt_noun
            alt_noun = (None)
        street = StreetReferent()
        if (not for_metro): 
            street._add_typ(noun.termin.canonic_text.lower())
            if (noun.alt_termin is not None): 
                if (noun.alt_termin.canonic_text == "ПРОСПЕКТ" and number is not None): 
                    pass
                else: 
                    street.add_slot(StreetReferent.ATTR_TYPE, noun.alt_termin.canonic_text.lower(), False, 0)
            if (alt_noun is not None): 
                street._add_typ(alt_noun.termin.canonic_text.lower())
                if (alt_noun.alt_termin is not None): 
                    street._add_typ(alt_noun.alt_termin.canonic_text.lower())
        else: 
            street._add_typ("метро")
        street.tag = (noun)
        res = AddressItemToken._new202(AddressItemType.STREET, rli[0].begin_token, rli[0].end_token, street)
        if (noun.termin.canonic_text == "ЛИНИЯ"): 
            if (number is None): 
                if (MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                    pass
                elif (MiscLocationHelper.is_user_param_address(sli[0])): 
                    pass
                else: 
                    return None
            res.is_doubt = True
        elif (noun.termin.canonic_text == "ПУНКТ"): 
            if (not MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                return None
            if (name is None or number is not None): 
                return None
        for r in rli: 
            if (res.begin_char > r.begin_char): 
                res.begin_token = r.begin_token
            if (res.end_char < r.end_char): 
                res.end_token = r.end_token
        if (for_metro and noun in rli and noun.termin.canonic_text == "МЕТРО"): 
            rli.remove(noun)
        if (noun.is_abridge and (noun.length_char < 4)): 
            res.is_doubt = True
        elif (noun.noun_is_doubt_coef > 0 and not not_doubt and not MiscLocationHelper.is_user_param_address(noun)): 
            res.is_doubt = True
            if ((name is not None and name.end_char > noun.end_char and noun.chars.is_all_lower) and not name.chars.is_all_lower and not (isinstance(name.begin_token, ReferentToken))): 
                npt2 = MiscLocationHelper._try_parse_npt(name.begin_token)
                if (npt2 is not None and npt2.end_char > name.end_char): 
                    pass
                elif (AddressItemToken.check_house_after(res.end_token.next0_, False, False)): 
                    res.is_doubt = False
                elif (name.chars.is_capital_upper and noun.noun_is_doubt_coef == 1): 
                    res.is_doubt = False
        name_base = io.StringIO()
        name_alt = io.StringIO()
        name_alt2 = None
        gen = noun.termin.gender
        adj_gen = MorphGender.UNDEFINED
        if (number is not None): 
            street.numbers = number
            if (sec_number is not None): 
                street.numbers = sec_number
        if (age is not None): 
            street.numbers = age
        miscs = None
        if (name is not None and name.value is not None): 
            if (name.value.find(' ') > 0 and name.begin_token.next0_ == name.end_token and not name.end_token.is_value("СУ", None)): 
                ty = OrgTypToken.try_parse(name.end_token, False, None)
                if (ty is not None and len(ty.vals) > 0 and not ty.is_doubt): 
                    name = name.clone()
                    name.alt_value = (None)
                    name.end_token = name.end_token.previous
                    miscs = ty.vals
                    name.value = name.value[0:0+name.value.find(' ')]
                else: 
                    nn = StreetItemToken.try_parse(name.end_token, None, False, None)
                    if (nn is not None and nn.typ == StreetItemType.NOUN and nn.termin.canonic_text != "МОСТ"): 
                        name = name.clone()
                        name.alt_value = (None)
                        name.value = name.value[0:0+name.value.find(' ')]
                        name.end_token = name.end_token.previous
                        street._add_typ(nn.termin.canonic_text.lower())
                        ss = street.find_slot(StreetReferent.ATTR_TYPE, "улица", True)
                        if (ss is not None): 
                            street.slots.remove(ss)
            if (name.alt_value is not None and name_alt.tell() == 0): 
                print("{0} {1}".format(Utils.toStringStringIO(name_base), name.alt_value), end="", file=name_alt, flush=True)
            if (name.value.startswith("НАБЕРЕЖНАЯ ")): 
                street._add_typ("набережная")
                print(" {0}".format(name.value[11:]), end="", file=name_base, flush=True)
            else: 
                print(" {0}".format(name.value), end="", file=name_base, flush=True)
        elif ((name is not None and name.termin is not None and number is not None) and (Utils.valToEnum(name.termin.tag, StreetItemType)) == StreetItemType.NOUN): 
            street._add_typ(name.termin.canonic_text.lower())
        elif (name is not None): 
            is_adj = False
            if (isinstance(name.end_token, TextToken)): 
                for wf in name.end_token.morph.items: 
                    if ((isinstance(wf, MorphWordForm)) and wf.is_in_dictionary): 
                        is_adj = (wf.class0_.is_adjective | wf.class0_.is_proper_geo)
                        adj_gen = wf.gender
                        break
                    elif (wf.class0_.is_adjective | wf.class0_.is_proper_geo): 
                        is_adj = True
            if (is_adj): 
                tmp = io.StringIO()
                vars0_ = list()
                t = name.begin_token
                while t is not None: 
                    tt = Utils.asObjectOrNull(t, TextToken)
                    if (tt is None): 
                        break
                    if (tmp.tell() > 0 and Utils.getCharAtStringIO(tmp, tmp.tell() - 1) != ' '): 
                        print(' ', end="", file=tmp)
                    if (t == name.end_token): 
                        is_padez = False
                        if (not noun.is_abridge): 
                            if (not noun.morph.case_.is_undefined and not noun.morph.case_.is_nominative): 
                                is_padez = True
                            elif (noun.termin.canonic_text == "ШОССЕ" or noun.termin.canonic_text == "ШОСЕ"): 
                                is_padez = True
                        if (res.begin_token.previous is not None and res.begin_token.previous.morph.class0_.is_preposition): 
                            is_padez = True
                        if (is_proezd): 
                            is_padez = True
                        if (not is_padez): 
                            print(tt.term, end="", file=tmp)
                            break
                        for wf in tt.morph.items: 
                            if (((wf.class0_.is_adjective or wf.class0_.is_proper_geo)) and ((wf.gender) & (gen)) != (MorphGender.UNDEFINED)): 
                                if (noun.morph.case_.is_undefined or not ((wf.case_) & noun.morph.case_).is_undefined): 
                                    wff = Utils.asObjectOrNull(wf, MorphWordForm)
                                    if (wff is None): 
                                        continue
                                    if (gen == MorphGender.MASCULINE and wff.normal_case.endswith("ОЙ")): 
                                        continue
                                    if (wff.normal_case.endswith("СКИ")): 
                                        continue
                                    if (not wff.normal_case in vars0_): 
                                        vars0_.append(wff.normal_case)
                        if (not tt.term in vars0_ and Utils.indexOfList(sli, name, 0) > Utils.indexOfList(sli, noun, 0)): 
                            vars0_.append(tt.term)
                        if (len(vars0_) == 0): 
                            vars0_.append(tt.term)
                        if (is_proezd): 
                            nnn = tt.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                            if (nnn is None): 
                                nnn = tt.lemma
                            if (not nnn in vars0_): 
                                vars0_.append(nnn)
                        break
                    if (not tt.is_hiphen): 
                        print(tt.term, end="", file=tmp)
                    t = t.next0_
                if (len(vars0_) == 0): 
                    print(" {0}".format(Utils.toStringStringIO(tmp)), end="", file=name_base, flush=True)
                else: 
                    head = Utils.toStringStringIO(name_base)
                    print(" {0}{1}".format(Utils.toStringStringIO(tmp), vars0_[0]), end="", file=name_base, flush=True)
                    src = MiscHelper.get_text_value_of_meta_token(name, GetTextAttr.NO)
                    ii = Utils.indexOfList(vars0_, src, 0)
                    if (ii > 1): 
                        del vars0_[ii]
                        vars0_.insert(1, src)
                    elif (ii < 0): 
                        vars0_.insert(1, src)
                    if (len(vars0_) > 1): 
                        Utils.setLengthStringIO(name_alt, 0)
                        print("{0} {1}{2}".format(head, Utils.toStringStringIO(tmp), vars0_[1]), end="", file=name_alt, flush=True)
                    if (len(vars0_) > 2): 
                        name_alt2 = "{0} {1}{2}".format(head, Utils.toStringStringIO(tmp), vars0_[2])
            else: 
                str_nam = None
                nits = list()
                has_adj = False
                has_proper_name = False
                t = name.begin_token
                while t is not None and t.end_char <= name.end_char: 
                    if (t.morph.class0_.is_adjective or t.morph.class0_.is_conjunction): 
                        has_adj = True
                    if ((isinstance(t, TextToken)) and not t.is_hiphen): 
                        if (name.termin is not None): 
                            nits.append(name.termin.canonic_text)
                            break
                        elif (not t.chars.is_letter and len(nits) > 0): 
                            nits[len(nits) - 1] += t.term
                        else: 
                            nits.append(t.term)
                            if (t == name.begin_token and t.get_morph_class_in_dictionary().is_proper): 
                                has_proper_name = True
                    elif ((isinstance(t, ReferentToken)) and name.termin is None): 
                        nits.append(t.get_source_text().upper())
                    t = t.next0_
                if (not has_adj and not has_proper_name and not name.is_in_dictionary): 
                    nits.sort()
                str_nam = Utils.joinStrings(" ", list(nits))
                if (has_proper_name and len(nits) == 2): 
                    Utils.setLengthStringIO(name_alt, 0)
                    print("{0} {1}".format(Utils.toStringStringIO(name_base), nits[1]), end="", file=name_alt, flush=True)
                print(" {0}".format(str_nam), end="", file=name_base, flush=True)
                if (name._org0_ is not None and name._org0_.referent.find_slot("NUMBER", None, True) is not None): 
                    street.add_slot("NUMBER", name._org0_.referent.get_string_value("NUMBER"), False, 0)
        adj_str = None
        adj_str2 = None
        adj_can_be_initial = False
        if (adj is not None): 
            s = None
            ss = None
            if (adj_gen == MorphGender.UNDEFINED and name is not None and ((name.morph.number) & (MorphNumber.PLURAL)) == (MorphNumber.UNDEFINED)): 
                if (name.morph.gender == MorphGender.FEMINIE or name.morph.gender == MorphGender.MASCULINE or name.morph.gender == MorphGender.NEUTER): 
                    adj_gen = name.morph.gender
            if (noun is not None and noun.termin.gender != MorphGender.UNDEFINED): 
                adj_gen = noun.termin.gender
            if (name is not None and ((name.morph.number) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                try: 
                    s = MorphologyService.get_wordform(adj.termin.canonic_text, MorphBaseInfo._new273(MorphClass.ADJECTIVE, MorphNumber.PLURAL))
                    if (adj.alt_termin is not None): 
                        ss = MorphologyService.get_wordform(adj.alt_termin.canonic_text, MorphBaseInfo._new273(MorphClass.ADJECTIVE, MorphNumber.PLURAL))
                except Exception as ex: 
                    pass
            elif (adj_gen != MorphGender.UNDEFINED): 
                try: 
                    s = MorphologyService.get_wordform(adj.termin.canonic_text, MorphBaseInfo._new275(MorphClass.ADJECTIVE, adj_gen))
                    if (adj.alt_termin is not None): 
                        ss = MorphologyService.get_wordform(adj.alt_termin.canonic_text, MorphBaseInfo._new275(MorphClass.ADJECTIVE, adj_gen))
                except Exception as ex: 
                    pass
            elif (((adj.morph.gender) & (gen)) == (MorphGender.UNDEFINED)): 
                try: 
                    ggg = noun.termin.gender
                    s = MorphologyService.get_wordform(adj.termin.canonic_text, MorphBaseInfo._new275(MorphClass.ADJECTIVE, ggg))
                    if (adj.alt_termin is not None): 
                        ss = MorphologyService.get_wordform(adj.alt_termin.canonic_text, MorphBaseInfo._new275(MorphClass.ADJECTIVE, ggg))
                except Exception as ex: 
                    pass
            else: 
                try: 
                    s = MorphologyService.get_wordform(adj.termin.canonic_text, MorphBaseInfo._new275(MorphClass.ADJECTIVE, gen))
                    if (adj.alt_termin is not None): 
                        ss = MorphologyService.get_wordform(adj.alt_termin.canonic_text, MorphBaseInfo._new275(MorphClass.ADJECTIVE, gen))
                except Exception as ex: 
                    pass
            adj_str = s
            adj_str2 = ss
            if (name is not None): 
                if (adj.end_token.is_char('.') and adj.length_char <= 3 and not adj.begin_token.chars.is_all_lower): 
                    adj_can_be_initial = True
        s1 = Utils.toStringStringIO(name_base).strip()
        s2 = Utils.toStringStringIO(name_alt).strip()
        if ((len(s1) < 3) and street.kind != StreetKind.ROAD): 
            if (street.numbers is not None): 
                if (adj_str is not None): 
                    if (adj.is_abridge): 
                        return None
                    street.add_slot(StreetReferent.ATTR_NAME, adj_str, False, 0)
                elif (MiscLocationHelper.is_user_param_address(res) and len(s1) > 0): 
                    street.add_slot(StreetReferent.ATTR_NAME, s1, False, 0)
            elif (adj_str is None): 
                if (len(s1) < 1): 
                    return None
                if (is_micro_raion or MiscLocationHelper.is_user_param_address(res)): 
                    if (len(s1) == 1): 
                        ch = LanguageHelper.get_cyr_for_lat(s1[0])
                        if ((ord(ch)) != 0): 
                            s1 = "{0}".format(ch)
                        street.add_slot(StreetReferent.ATTR_NUMBER, s1, False, 0)
                    else: 
                        street.add_slot(StreetReferent.ATTR_NAME, s1, False, 0)
                        if (not Utils.isNullOrEmpty(s2)): 
                            street.add_slot(StreetReferent.ATTR_NAME, s2, False, 0)
                else: 
                    return None
            else: 
                if (adj.is_abridge and not MiscLocationHelper.is_user_param_address(adj) and alt_noun is None): 
                    return None
                street.add_slot(StreetReferent.ATTR_NAME, adj_str, False, 0)
        elif (adj_can_be_initial): 
            street.add_slot(StreetReferent.ATTR_NAME, s1, False, 0)
            street.add_slot(StreetReferent.ATTR_NAME, MiscHelper.get_text_value(adj.begin_token, name.end_token, GetTextAttr.NO), False, 0)
            street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str, s1), False, 0)
            if (adj_str2 is not None): 
                street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str2, s1), False, 0)
        elif (adj_str is None): 
            if (not Utils.isNullOrEmpty(s1)): 
                street.add_slot(StreetReferent.ATTR_NAME, s1, False, 0)
        else: 
            street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str, s1), False, 0)
            if (adj_str2 is not None): 
                street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str2, s1), False, 0)
        if (name_alt.tell() > 0): 
            s1 = Utils.toStringStringIO(name_alt).strip()
            if (adj_str is None): 
                if (len(s1) == 1): 
                    ch = LanguageHelper.get_cyr_for_lat(s1[0])
                    if ((ord(ch)) != 0): 
                        s1 = "{0}".format(ch)
                    street.add_slot(StreetReferent.ATTR_NUMBER, s1, False, 0)
                else: 
                    street.add_slot(StreetReferent.ATTR_NAME, s1, False, 0)
            else: 
                street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str, s1), False, 0)
                if (adj_str2 is not None): 
                    street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str2, s1), False, 0)
        if (name_alt2 is not None): 
            if (adj_str is None): 
                if (for_metro and noun is not None): 
                    street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(alt_noun.termin.canonic_text, name_alt2.strip()), False, 0)
                else: 
                    street.add_slot(StreetReferent.ATTR_NAME, name_alt2.strip(), False, 0)
            else: 
                street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str, name_alt2.strip()), False, 0)
                if (adj_str2 is not None): 
                    street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(adj_str2, name_alt2.strip()), False, 0)
        if (name is not None and name.alt_value2 is not None): 
            street.add_slot(StreetReferent.ATTR_NAME, name.alt_value2, False, 0)
        if ((name is not None and adj is None and name.exist_street is not None) and not for_metro): 
            for n in name.exist_street.names: 
                street.add_slot(StreetReferent.ATTR_NAME, n, False, 0)
        if (miscs is not None): 
            for m in miscs: 
                street.add_slot(StreetReferent.ATTR_MISC, m, False, 0)
        if (alt_noun is not None and not for_metro): 
            street._add_typ(alt_noun.termin.canonic_text.lower())
        if (noun.termin.canonic_text == "ПЛОЩАДЬ" or noun.termin.canonic_text == "КВАРТАЛ" or noun.termin.canonic_text == "ПЛОЩА"): 
            res.is_doubt = True
            if (name is not None and name.is_in_dictionary): 
                res.is_doubt = False
            elif (alt_noun is not None or for_metro or adj is not None): 
                res.is_doubt = False
            elif (name is not None and StreetItemToken.check_std_name(name.begin_token) is not None): 
                res.is_doubt = False
            elif (res.begin_token.previous is None or MiscLocationHelper.check_geo_object_before(res.begin_token.previous, False)): 
                if (res.end_token.next0_ is None or AddressItemToken.check_house_after(res.end_token.next0_, False, True)): 
                    res.is_doubt = False
        if (name is not None and adj is None and name.std_adj_version is not None): 
            nams = street.names
            for n in nams: 
                if (n.find(' ') < 0): 
                    adjs = MiscLocationHelper.get_std_adj_full(name.std_adj_version.begin_token, noun.termin.gender, MorphNumber.SINGULAR, False)
                    if (adjs is not None and len(adjs) > 0): 
                        for a in adjs: 
                            street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(a, n), False, 0)
                    else: 
                        street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(name.std_adj_version.termin.canonic_text, n), False, 0)
                        if (name.std_adj_version.alt_termin is not None): 
                            street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(name.std_adj_version.alt_termin.canonic_text, n), False, 0)
        if (LanguageHelper.ends_with(noun.termin.canonic_text, "ГОРОДОК")): 
            street.kind = StreetKind.AREA
            for s in street.slots: 
                if (s.type_name == StreetReferent.ATTR_TYPE): 
                    street.upload_slot(s, "микрорайон")
                elif (s.type_name == StreetReferent.ATTR_NAME): 
                    street.upload_slot(s, "{0} {1}".format(noun.termin.canonic_text, s.value))
            if (street.find_slot(StreetReferent.ATTR_NAME, None, True) is None): 
                street.add_slot(StreetReferent.ATTR_NAME, noun.termin.canonic_text, False, 0)
        t1 = res.end_token.next0_
        if (t1 is not None and t1.is_comma): 
            t1 = t1.next0_
        non = StreetItemToken.try_parse(t1, None, False, None)
        if (non is not None and non.typ == StreetItemType.NOUN and len(street.typs) > 0): 
            if (AddressItemToken.check_house_after(non.end_token.next0_, False, True)): 
                street._correct()
                nams = street.names
                for t in street.typs: 
                    if (t != "улица"): 
                        for n in nams: 
                            street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(t.upper(), n), False, 0)
                street.add_slot(StreetReferent.ATTR_TYPE, non.termin.canonic_text.lower(), False, 0)
                res.end_token = non.end_token
        if (street.find_slot(StreetReferent.ATTR_NAME, "ПРОЕКТИРУЕМЫЙ", True) is not None and street.numbers is None): 
            if (non is not None and non.typ == StreetItemType.NUMBER): 
                street.numbers = non.value
                res.end_token = non.end_token
            else: 
                ttt = MiscHelper.check_number_prefix(res.end_token.next0_)
                if (ttt is not None): 
                    non = StreetItemToken.try_parse(ttt, None, False, None)
                    if (non is not None and non.typ == StreetItemType.NUMBER): 
                        street.numbers = non.value
                        res.end_token = non.end_token
        if (res.is_doubt): 
            if (noun.is_road): 
                street.kind = StreetKind.ROAD
                num = street.numbers
                if (num is not None and "км" in num): 
                    res.is_doubt = False
                elif (AddressItemToken.check_km_after(res.end_token.next0_)): 
                    res.is_doubt = False
                elif (AddressItemToken.check_km_before(res.begin_token.previous)): 
                    res.is_doubt = False
            elif (noun.termin.canonic_text == "ПРОЕЗД" and street.find_slot(StreetReferent.ATTR_NAME, "ПРОЕКТИРУЕМЫЙ", True) is not None): 
                res.is_doubt = False
            tt0 = res.begin_token.previous
            first_pass3782 = True
            while True:
                if first_pass3782: first_pass3782 = False
                else: tt0 = tt0.previous
                if (not (tt0 is not None)): break
                if (tt0.is_char_of(",.") or tt0.is_comma_and): 
                    continue
                str0 = Utils.asObjectOrNull(tt0.get_referent(), StreetReferent)
                if (str0 is not None): 
                    res.is_doubt = False
                break
            if (res.is_doubt): 
                if (BracketHelper.can_be_start_of_sequence(res.begin_token.previous, True, False) and BracketHelper.can_be_end_of_sequence(res.end_token.next0_, True, None, False)): 
                    return None
                if (is_proezd): 
                    res.is_doubt = False
                elif (AddressItemToken.check_house_after(res.end_token.next0_, False, False)): 
                    res.is_doubt = False
                elif (AddressItemToken.check_street_after(res.end_token.next0_, False)): 
                    res.is_doubt = False
                elif (MiscLocationHelper.check_geo_object_before(res.begin_token, False)): 
                    res.is_doubt = False
                ttt = res.begin_token.next0_
                while ttt is not None and ttt.end_char <= res.end_char: 
                    if (ttt.is_newline_before): 
                        res.is_doubt = True
                    ttt = ttt.next0_
        if (noun.termin.canonic_text == "КВАРТАЛ" and (res.whitespaces_after_count < 2) and number is None): 
            ait = AddressItemToken.try_parse_pure_item(res.end_token.next0_, None, None)
            if (ait is not None and ait.typ == AddressItemType.NUMBER and ait.value is not None): 
                street.add_slot(StreetReferent.ATTR_NUMBER, ait.value, False, 0)
                res.end_token = ait.end_token
        if (age is not None and street.find_slot(StreetReferent.ATTR_NAME, None, True) is None): 
            street.add_slot(StreetReferent.ATTR_NAME, "ЛЕТ", False, 0)
        if (name is not None): 
            street._add_misc(name.misc)
        if (street.numbers is None and ((street.kind == StreetKind.ROAD or street.kind == StreetKind.RAILWAY))): 
            t1 = res.end_token.next0_
            if (t1 is not None and t1.is_comma): 
                t1 = t1.next0_
            sit = StreetItemToken.try_parse(t1, None, False, None)
            if (sit is not None and sit.is_number_km): 
                res.end_token = sit.end_token
                street.numbers = sit.value + "км"
        for r in rli: 
            if (r._orto_terr is not None): 
                res.orto_terr = r._orto_terr
                break
            elif (r._area is not None): 
                res.area_terr = r._area
                break
        if (noun.is_road): 
            nam2 = StreetItemToken._try_parse_spec(res.end_token.next0_, noun)
            if (nam2 is not None and len(nam2) == 1 and nam2[0].is_road_name): 
                res.end_token = nam2[0].end_token
                street._add_name(nam2[0])
        if (street.kind == StreetKind.AREA and (res.whitespaces_after_count < 3)): 
            ttt = MiscLocationHelper.check_territory(res.end_token.next0_)
            if (ttt is not None): 
                ok = False
                if (ttt.next0_ is None or ttt.is_newline_after): 
                    ok = True
                elif (ttt.next0_.is_comma): 
                    ok = True
                if (ok): 
                    res.end_token = ttt
        return res
    
    @staticmethod
    def __try_detect_non_noun(sli : typing.List['StreetItemToken'], onto_regim : bool, for_metro : bool, street_before : bool, cross_street : 'StreetReferent') -> 'AddressItemToken':
        if (len(sli) > 1 and sli[len(sli) - 1].typ == StreetItemType.NUMBER and not sli[len(sli) - 1].number_has_prefix): 
            del sli[len(sli) - 1]
        street = None
        if (len(sli) == 1 and ((sli[0].typ == StreetItemType.NAME or sli[0].typ == StreetItemType.STDNAME or sli[0].typ == StreetItemType.STDADJECTIVE)) and ((onto_regim or for_metro))): 
            s = MiscHelper.get_text_value(sli[0].begin_token, sli[0].end_token, GetTextAttr.NO)
            if (s is None): 
                return None
            if (not for_metro and not sli[0].is_in_dictionary and sli[0].exist_street is None): 
                tt = sli[0].end_token.next0_
                while tt is not None: 
                    if (not tt.is_char_of(".,")): 
                        break
                    tt = tt.next0_
                ait1 = AddressItemToken.try_parse_pure_item(tt, None, None)
                if (ait1 is not None and ((ait1.typ == AddressItemType.NUMBER or ait1.typ == AddressItemType.HOUSE))): 
                    pass
                elif (tt is None or tt.is_comma or tt.is_newline_before): 
                    pass
                else: 
                    return None
            street = StreetReferent()
            if (for_metro): 
                street.add_slot(StreetReferent.ATTR_TYPE, "метро", False, 0)
            if (sli[0].value is not None): 
                street.add_slot(StreetReferent.ATTR_NAME, sli[0].value, False, 0)
            if (sli[0].alt_value is not None): 
                street.add_slot(StreetReferent.ATTR_NAME, sli[0].alt_value, False, 0)
            if (sli[0].alt_value2 is not None): 
                street.add_slot(StreetReferent.ATTR_NAME, sli[0].alt_value2, False, 0)
            street._add_misc(sli[0].misc)
            if (street.find_slot(StreetReferent.ATTR_NAME, None, True) is None): 
                street.add_slot(StreetReferent.ATTR_NAME, s, False, 0)
            res0 = AddressItemToken._new269(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, street, True)
            if (sli[0].is_in_brackets): 
                res0.is_doubt = False
            return res0
        if ((len(sli) == 1 and sli[0].typ == StreetItemType.NUMBER and sli[0].is_number_km) and MiscLocationHelper.is_user_param_address(sli[0])): 
            street = StreetReferent()
            street.numbers = sli[0].value + "км"
            res0 = AddressItemToken._new269(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, street, True)
            return res0
        if ((len(sli) == 1 and sli[0].typ == StreetItemType.NUMBER and sli[0].begin_token.morph.class0_.is_adjective) and MiscLocationHelper.is_user_param_address(sli[0])): 
            if (street_before): 
                return None
            street = StreetReferent()
            street.numbers = sli[0].value
            res0 = AddressItemToken._new269(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, street, True)
            return res0
        i1 = 0
        if (len(sli) == 1 and (((sli[0].typ == StreetItemType.STDNAME or sli[0].typ == StreetItemType.NAME or sli[0].typ == StreetItemType.STDADJECTIVE) or ((sli[0].typ == StreetItemType.NOUN and sli[0].noun_can_be_name))))): 
            if (not onto_regim): 
                is_street_before = street_before
                tt = sli[0].begin_token.previous
                sbefor = None
                if ((tt is not None and tt.is_comma_and and tt.previous is not None) and (isinstance(tt.previous.get_referent(), StreetReferent))): 
                    is_street_before = True
                    sbefor = (Utils.asObjectOrNull(tt.previous.get_referent(), StreetReferent))
                cou = 0
                tt = sli[0].end_token.next0_
                first_pass3783 = True
                while True:
                    if first_pass3783: first_pass3783 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (not tt.is_comma_and or tt.next0_ is None): 
                        break
                    sli2 = StreetItemToken.try_parse_list(tt.next0_, 10, None)
                    if (sli2 is None): 
                        break
                    noun = None
                    empty = True
                    for si in sli2: 
                        if (si.typ == StreetItemType.NOUN): 
                            noun = si
                        elif ((si.typ == StreetItemType.NAME or si.typ == StreetItemType.STDNAME or si.typ == StreetItemType.NUMBER) or si.typ == StreetItemType.STDADJECTIVE): 
                            empty = False
                    if (empty): 
                        break
                    if (noun is None): 
                        if (tt.is_and and not is_street_before): 
                            break
                        cou += 1
                        if (cou > 4): 
                            break
                        tt = sli2[len(sli2) - 1].end_token
                        continue
                    if (not tt.is_and and not is_street_before): 
                        break
                    if (noun == sli2[0]): 
                        if (sbefor is not None and (isinstance(sbefor.tag, StreetItemToken))): 
                            noun = (Utils.asObjectOrNull(sbefor.tag, StreetItemToken))
                        elif (sbefor is not None and len(sbefor.typs) > 0): 
                            noun = StreetItemToken._new284(tt, tt, StreetItemType.NOUN, sbefor.typs[0])
                            noun.termin = Termin(sbefor.typs[0])
                        else: 
                            break
                    tmp = list()
                    tmp.append(sli[0])
                    tmp.append(noun)
                    re = StreetDefineHelper._try_parse_street(tmp, False, for_metro, False, None)
                    if (re is not None): 
                        re.begin_token = sli[0].begin_token
                        re.end_token = sli[0].end_token
                        return re
                if (cross_street is not None): 
                    i1 = 0
                elif (sbefor is not None and (isinstance(sbefor.tag, StreetItemToken))): 
                    tmp = list()
                    tmp.append(sli[0])
                    tmp.append(Utils.asObjectOrNull(sbefor.tag, StreetItemToken))
                    re = StreetDefineHelper._try_parse_street(tmp, False, for_metro, False, None)
                    if (re is not None): 
                        re.begin_token = sli[0].begin_token
                        re.end_token = sli[0].end_token
                        return re
            if (sli[0].whitespaces_after_count < 2): 
                tt = MiscLocationHelper.check_territory(sli[0].end_token.next0_)
                if (tt is not None): 
                    ok1 = False
                    if ((tt.is_newline_after or tt.next0_ is None or tt.next0_.is_comma) or tt.next0_.is_char(')')): 
                        ok1 = True
                    elif (AddressItemToken.check_house_after(tt.next0_, False, False)): 
                        ok1 = True
                    elif (AddressItemToken.check_street_after(tt.next0_, False)): 
                        ok1 = True
                    if (ok1): 
                        street = StreetReferent()
                        street._add_typ("территория")
                        street.kind = StreetKind.AREA
                        street.add_slot(StreetReferent.ATTR_NAME, Utils.ifNotNull(sli[0].value, MiscHelper.get_text_value_of_meta_token(sli[0], GetTextAttr.NO)), False, 0)
                        if (sli[0].alt_value is not None): 
                            street.add_slot(StreetReferent.ATTR_NAME, sli[0].alt_value, False, 0)
                        if (sli[0].alt_value2 is not None): 
                            street.add_slot(StreetReferent.ATTR_NAME, sli[0].alt_value2, False, 0)
                        street._add_misc(sli[0].misc)
                        return AddressItemToken._new202(AddressItemType.STREET, sli[0].begin_token, tt, street)
            if (not MiscLocationHelper.is_user_param_address(sli[0]) and not street_before): 
                if (MiscLocationHelper.check_geo_object_before(sli[0].begin_token, False)): 
                    pass
                elif (AddressItemToken.check_house_after(sli[0].end_token.next0_, False, False)): 
                    tt2 = sli[0].end_token.next0_
                    if (tt2.is_comma): 
                        tt2 = tt2.next0_
                    ait = AddressItemToken.try_parse_pure_item(tt2, None, None)
                    if ((ait is not None and ((ait.typ == AddressItemType.HOUSE or ait.typ == AddressItemType.BUILDING or ait.typ == AddressItemType.CORPUS)) and not Utils.isNullOrEmpty(ait.value)) and ait.value != "0" and str.isdigit(ait.value[0])): 
                        pass
                    else: 
                        return None
                else: 
                    return None
        elif (len(sli) == 2 and ((sli[0].typ == StreetItemType.STDADJECTIVE or sli[0].typ == StreetItemType.NUMBER or sli[0].typ == StreetItemType.AGE)) and ((sli[1].typ == StreetItemType.STDNAME or sli[1].typ == StreetItemType.NAME))): 
            if (street_before): 
                ait = AddressItemToken.try_parse_pure_item(sli[0].begin_token, None, None)
                if (ait is not None and ait.value is not None): 
                    return None
            if (sli[0].typ == StreetItemType.NUMBER and sli[1].typ == StreetItemType.NAME): 
                if (AddressItemToken.try_parse_pure_item(sli[1].begin_token, None, None) is not None): 
                    return None
            i1 = 1
        elif (len(sli) == 2 and ((sli[0].typ == StreetItemType.STDNAME or sli[0].typ == StreetItemType.NAME)) and ((sli[1].typ == StreetItemType.NUMBER or sli[1].typ == StreetItemType.STDADJECTIVE))): 
            if (not MiscLocationHelper.is_user_param_address(sli[0])): 
                return None
            i1 = 0
        elif ((len(sli) == 3 and ((sli[0].typ == StreetItemType.STDNAME or sli[0].typ == StreetItemType.NAME)) and sli[1].typ == StreetItemType.NUMBER) and sli[2].typ == StreetItemType.STDNAME): 
            i1 = 0
        elif (len(sli) == 1 and sli[0].typ == StreetItemType.NUMBER and sli[0].is_number_km): 
            tt = sli[0].begin_token.previous
            first_pass3784 = True
            while True:
                if first_pass3784: first_pass3784 = False
                else: tt = tt.previous
                if (not (tt is not None)): break
                if (tt.length_char == 1): 
                    continue
                geo = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                if (geo is None): 
                    break
                ok1 = False
                if (geo.find_slot(GeoReferent.ATTR_TYPE, "станция", True) is not None): 
                    ok1 = True
                if (ok1): 
                    street = StreetReferent()
                    street.add_slot(StreetReferent.ATTR_NUMBER, "{0}км".format(sli[0].value), False, 0)
                    res0 = AddressItemToken._new269(AddressItemType.STREET, sli[0].begin_token, sli[0].end_token, street, True)
                    if (sli[0].is_in_brackets): 
                        res0.is_doubt = False
                    return res0
            return None
        else: 
            return None
        val = sli[i1].value
        alt_val = sli[i1].alt_value
        if (alt_val == val): 
            alt_val = (None)
        miscs = None
        if (val is not None and val.find(' ') > 0 and sli[i1].begin_token.next0_ == sli[i1].end_token): 
            ty = OrgTypToken.try_parse(sli[i1].end_token, False, None)
            if (ty is not None and len(ty.vals) > 0 and not ty.is_doubt): 
                alt_val = (None)
                miscs = ty.vals
                val = val[0:0+val.find(' ')]
        if (sli[i1].value is None and sli[i1].termin is not None and sli[i1].typ == StreetItemType.NOUN): 
            val = sli[i1].termin.canonic_text
        std_adj_prob = sli[i1].std_adj_version
        if (val is None): 
            if (sli[i1].exist_street is not None): 
                names = sli[i1].exist_street.names
                if (len(names) > 0): 
                    val = names[0]
                    if (len(names) > 1): 
                        alt_val = names[1]
            else: 
                te = Utils.asObjectOrNull(sli[i1].begin_token, TextToken)
                if (te is not None): 
                    for wf in te.morph.items: 
                        if (wf.class0_.is_adjective and wf.gender == MorphGender.FEMINIE and not wf.contains_attr("к.ф.", None)): 
                            val = wf.normal_case
                            break
                if (i1 > 0 and sli[0].typ == StreetItemType.AGE): 
                    val = MiscHelper.get_text_value_of_meta_token(sli[i1], GetTextAttr.NO)
                else: 
                    alt_val = MiscHelper.get_text_value_of_meta_token(sli[i1], GetTextAttr.NO)
                    if (val is None and te.morph.class0_.is_adjective): 
                        val = alt_val
                        alt_val = (None)
                if (len(sli) > 1 and val is None and alt_val is not None): 
                    val = alt_val
                    alt_val = (None)
        very_doubt = False
        if (val is None and len(sli) == 1 and sli[0].chars.is_capital_upper): 
            very_doubt = True
            t0 = sli[0].begin_token.previous
            if (t0 is not None and t0.is_char(',')): 
                t0 = t0.previous
            if ((isinstance(t0, ReferentToken)) and (isinstance(t0.get_referent(), GeoReferent))): 
                val = MiscHelper.get_text_value(sli[0].begin_token, sli[0].end_token, GetTextAttr.NO)
        if (val is None): 
            return None
        t = sli[len(sli) - 1].end_token.next0_
        while t is not None: 
            if (not t.is_char_of(",.")): 
                break
            t = t.next0_
        if (t is None): 
            if (not MiscLocationHelper.is_user_param_address(sli[0])): 
                return None
        ok = False
        doubt = True
        if (sli[i1].termin is not None and (Utils.valToEnum(sli[i1].termin.tag, StreetItemType)) == StreetItemType.FIX): 
            ok = True
            doubt = False
        elif (((sli[i1].exist_street is not None or sli[0].exist_street is not None)) and sli[0].begin_token != sli[i1].end_token): 
            ok = True
            doubt = False
            if (t.kit.process_referent("PERSON", sli[0].begin_token, None) is not None): 
                if (AddressItemToken.check_house_after(t, False, False)): 
                    pass
                else: 
                    doubt = True
        elif (cross_street is not None): 
            ok = True
        elif (t is None): 
            ok = True
        elif (t.is_char_of("\\/")): 
            ok = True
        elif (AddressItemToken.check_house_after(t, False, False)): 
            if (t.previous is not None): 
                if (t.previous.is_value("АРЕНДА", "ОРЕНДА") or t.previous.is_value("СДАЧА", "ЗДАЧА") or t.previous.is_value("СЪЕМ", "ЗНІМАННЯ")): 
                    return None
            vv = MiscLocationHelper._try_parse_npt(t.previous)
            if (vv is not None and vv.end_char >= t.begin_char): 
                return None
            ok = True
        elif (MiscLocationHelper.is_user_param_address(t) and ((t.is_newline_before or t.is_value("Д", None)))): 
            ok = True
        elif (sli[0].typ == StreetItemType.AGE and MiscLocationHelper.is_user_param_address(sli[0])): 
            ok = True
        elif ((t.is_char('(') and (isinstance(t.next0_, ReferentToken)) and (isinstance(t.next0_.get_referent(), GeoReferent))) and t.next0_.get_referent().is_city): 
            ok = True
        else: 
            ait = AddressItemToken.try_parse_pure_item(t, None, None)
            if (ait is None): 
                return None
            if (((ait.typ == AddressItemType.HOUSE or ait.typ == AddressItemType.BUILDING or ait.typ == AddressItemType.CORPUS)) and ait.value is not None): 
                ok = True
            elif (very_doubt): 
                return None
            elif (((val == "ТАБЛИЦА" or val == "РИСУНОК" or val == "ДИАГРАММА") or val == "ТАБЛИЦЯ" or val == "МАЛЮНОК") or val == "ДІАГРАМА"): 
                return None
            elif ((ait.typ == AddressItemType.NUMBER and (ait.begin_token.whitespaces_before_count < 4) and cross_street is None) and sli[0].typ != StreetItemType.AGE): 
                nt = Utils.asObjectOrNull(ait.begin_token, NumberToken)
                if ((nt is None or nt.int_value is None or nt.typ != NumberSpellingType.DIGIT) or nt.morph.class0_.is_adjective): 
                    return None
                if (ait.end_token.next0_ is not None and not ait.end_token.is_newline_after): 
                    mc = ait.end_token.next0_.get_morph_class_in_dictionary()
                    if (mc.is_adjective or mc.is_noun): 
                        return None
                if (nt.int_value > 100): 
                    return None
                if (not MiscLocationHelper.is_user_param_address(ait)): 
                    nex = NumberHelper.try_parse_number_with_postfix(ait.begin_token)
                    if (nex is not None): 
                        return None
                t = sli[0].begin_token.previous
                first_pass3785 = True
                while True:
                    if first_pass3785: first_pass3785 = False
                    else: t = t.previous
                    if (not (t is not None)): break
                    if (t.is_newline_after): 
                        break
                    if (isinstance(t.get_referent(), GeoReferent)): 
                        ok = True
                        break
                    if (t.is_char(',')): 
                        continue
                    if (t.is_char('.')): 
                        break
                    ait0 = AddressItemToken.try_parse_pure_item(t, None, None)
                    if (ait is not None): 
                        if (ait.typ == AddressItemType.PREFIX): 
                            ok = True
                            break
                    if (t.chars.is_letter): 
                        break
                if (not ok): 
                    if (MiscLocationHelper.is_user_param_address(sli[0])): 
                        ok = True
        if (not ok): 
            return None
        ooo = OrgItemToken.try_parse(sli[0].begin_token, None)
        if (ooo is None and len(sli) > 1): 
            ooo = OrgItemToken.try_parse(sli[1].begin_token, None)
        if (ooo is not None): 
            return None
        street = StreetReferent()
        if (cross_street is not None): 
            for ty in cross_street.typs: 
                street.add_slot(StreetReferent.ATTR_TYPE, ty, False, 0)
        if (len(sli) > 1): 
            if (sli[0].typ == StreetItemType.NUMBER or sli[0].typ == StreetItemType.AGE): 
                street.numbers = sli[0].value
            elif (sli[1].typ == StreetItemType.NUMBER or sli[1].typ == StreetItemType.AGE): 
                street.numbers = sli[1].value
            else: 
                adjs = None
                if (sli[0].typ == StreetItemType.STDADJECTIVE): 
                    adjs = MiscLocationHelper.get_std_adj_full(sli[0].begin_token, sli[1].morph.gender, sli[1].morph.number, True)
                    if (adjs is None): 
                        adjs = MiscLocationHelper.get_std_adj_full(sli[0].begin_token, MorphGender.FEMINIE, MorphNumber.SINGULAR, False)
                elif (sli[1].typ == StreetItemType.STDADJECTIVE): 
                    adjs = MiscLocationHelper.get_std_adj_full(sli[1].begin_token, sli[0].morph.gender, sli[0].morph.number, True)
                    if (adjs is None): 
                        adjs = MiscLocationHelper.get_std_adj_full(sli[1].begin_token, MorphGender.FEMINIE, MorphNumber.SINGULAR, False)
                if (adjs is not None): 
                    if (len(adjs) > 1): 
                        alt_val = "{0} {1}".format(adjs[1], val)
                    if (sli[0].is_abridge): 
                        alt_val = "{0} {1}".format(adjs[0], val)
                    else: 
                        val = "{0} {1}".format(adjs[0], val)
        street.add_slot(StreetReferent.ATTR_NAME, val, False, 0)
        if (alt_val is not None): 
            street.add_slot(StreetReferent.ATTR_NAME, alt_val, False, 0)
        if (miscs is not None): 
            for m in miscs: 
                street.add_slot(StreetReferent.ATTR_MISC, m, False, 0)
        if (std_adj_prob is not None): 
            adjs = MiscLocationHelper.get_std_adj_full(std_adj_prob.begin_token, MorphGender.UNDEFINED, MorphNumber.UNDEFINED, True)
            if (adjs is not None): 
                for a in adjs: 
                    street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(a, val), False, 0)
                    if (alt_val is not None): 
                        street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(a, alt_val), False, 0)
            else: 
                street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(std_adj_prob.termin.canonic_text, val), False, 0)
                if (alt_val is not None): 
                    street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(std_adj_prob.termin.canonic_text, alt_val), False, 0)
                if (std_adj_prob.alt_termin is not None): 
                    street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(std_adj_prob.alt_termin.canonic_text, val), False, 0)
                    if (alt_val is not None): 
                        street.add_slot(StreetReferent.ATTR_NAME, "{0} {1}".format(std_adj_prob.alt_termin.canonic_text, alt_val), False, 0)
        street._add_misc(sli[0].misc)
        if (len(sli) > 1): 
            street._add_misc(sli[1].misc)
        t00 = sli[0].begin_token
        if (street.kind == StreetKind.UNDEFINED): 
            cou = 0
            tt = sli[0].begin_token.previous
            while tt is not None and (cou < 4): 
                if (tt.whitespaces_after_count > 2): 
                    break
                te = MiscLocationHelper.check_territory(tt)
                if (te is not None and te.next0_ == sli[0].begin_token): 
                    street._add_typ("территория")
                    street.kind = StreetKind.AREA
                    t00 = tt
                    break
                tt = tt.previous; cou += 1
        return AddressItemToken._new269(AddressItemType.STREET, t00, sli[len(sli) - 1].end_token, street, doubt)
    
    @staticmethod
    def __try_parse_fix(sits : typing.List['StreetItemToken']) -> 'AddressItemToken':
        if ((len(sits) == 2 and sits[0].typ == StreetItemType.NOUN and sits[1].typ == StreetItemType.FIX) and sits[1]._city is not None): 
            str0_ = StreetReferent()
            str0_._add_typ(sits[0].termin.canonic_text.lower())
            if (sits[0].alt_termin is not None): 
                str0_._add_typ(sits[0].alt_termin.canonic_text.lower())
            nam = MiscHelper.get_text_value_of_meta_token(sits[1], GetTextAttr.NO)
            str0_.add_slot(StreetReferent.ATTR_NAME, nam, False, 0)
            nam1 = MiscHelper.get_text_value_of_meta_token(sits[1], GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            if (nam1 != nam): 
                str0_.add_slot(StreetReferent.ATTR_NAME, nam1, False, 0)
            return AddressItemToken._new202(AddressItemType.STREET, sits[0].begin_token, sits[1].end_token, str0_)
        if (len(sits) < 1): 
            return None
        if ((len(sits) == 2 and not sits[0].is_road and sits[0].typ == StreetItemType.NOUN) and sits[1]._org0_ is not None): 
            if (sits[0].termin.canonic_text == "ПЛОЩАДЬ" and not MiscLocationHelper.is_user_param_address(sits[0])): 
                return None
            o = sits[1]._org0_
            str0_ = StreetReferent()
            str0_._add_typ(sits[0].termin.canonic_text.lower())
            no_org = False
            for s in o.referent.slots: 
                if (s.type_name == "NAME" or s.type_name == "NUMBER"): 
                    str0_.add_slot(s.type_name, s.value, False, 0)
                elif (s.type_name == "TYPE"): 
                    ty = Utils.asObjectOrNull(s.value, str)
                    if (ty == "кадастровый квартал"): 
                        no_org = True
                        str0_.add_slot(StreetReferent.ATTR_TYPE, None, True, 0)
                        str0_._add_typ(ty)
                        continue
                    if (ty == "владение" or ty == "участок"): 
                        no_org = True
                    str0_._add_misc(ty)
            if (StreetItemToken._is_region(sits[0].termin.canonic_text)): 
                str0_.kind = StreetKind.AREA
            re = AddressItemToken(AddressItemType.STREET, sits[0].begin_token, sits[1].end_token)
            re.referent = (str0_)
            return re
        if (sits[0]._org0_ is not None): 
            o = sits[0]._org0_
            if (o.is_building): 
                return AddressItemToken._new289(AddressItemType.DETAIL, sits[0].begin_token, sits[0].end_token, o, AddressDetailType.ORG)
            str0_ = StreetReferent()
            str0_._add_typ("территория")
            no_org = o.not_org
            for s in o.referent.slots: 
                if (s.type_name == "NAME" or s.type_name == "NUMBER"): 
                    str0_.add_slot(s.type_name, s.value, False, 0)
                elif (s.type_name == "MISC2"): 
                    v = Utils.asObjectOrNull(s.value, str)
                    if (v.startswith("кадастровый")): 
                        ii = v.rfind(' ')
                        str0_.add_slot(StreetReferent.ATTR_NUMBER, v[ii + 1:], False, 0)
                    else: 
                        str0_.add_slot(StreetReferent.ATTR_PARAM, s.value, False, 0)
                elif (s.type_name == "TYPE" or s.type_name == "TYP"): 
                    ty = Utils.asObjectOrNull(s.value, str)
                    if (ty == "кадастровый квартал" or ty == "квартал"): 
                        no_org = True
                        str0_.add_slot(StreetReferent.ATTR_TYPE, None, True, 0)
                        str0_._add_typ(ty)
                        continue
                    if (ty == "владение" or ty == "участок"): 
                        no_org = True
                    str0_._add_misc(ty)
            b = sits[0].begin_token
            e0_ = sits[0].end_token
            if (len(sits) == 2 and sits[1].typ == StreetItemType.NOUN): 
                if (AddressItemToken.check_street_after(e0_.next0_, False)): 
                    pass
                else: 
                    str0_.kind = StreetKind.UNDEFINED
                    str0_.add_slot(StreetReferent.ATTR_TYPE, None, True, 0)
                    str0_._add_typ(sits[1].termin.canonic_text.lower())
                    if (sits[1].alt_termin is not None): 
                        str0_._add_typ(sits[1].alt_termin.canonic_text.lower())
                    e0_ = sits[1].end_token
                    if (str0_.find_slot(StreetReferent.ATTR_NAME, None, True) is None and str0_.find_slot(StreetReferent.ATTR_NUMBER, None, True) is None): 
                        mi = str0_.find_slot(StreetReferent.ATTR_MISC, None, True)
                        if (mi is not None): 
                            str0_.slots.remove(mi)
                            str0_.add_slot(StreetReferent.ATTR_NAME, mi.value.upper(), False, 0)
                    return AddressItemToken._new202(AddressItemType.STREET, b, e0_, str0_)
            if (no_org or o.referent.find_slot("TYPE", None, True) is None): 
                str0_.kind = StreetKind.AREA
            else: 
                str0_.kind = StreetKind.ORG
                str0_.add_slot(StreetReferent.ATTR_REF, o.referent, False, 0)
                str0_.add_ext_referent(sits[0]._org0_)
            if (sits[0].length_char > 500): 
                pass
            re = AddressItemToken(AddressItemType.STREET, b, e0_)
            re.referent = (str0_)
            if (o.not_org): 
                str0_.kind = StreetKind.AREA
            re.ref_token = (o)
            re.ref_token_is_gsk = (o.is_gsk or o.has_terr_keyword)
            re.ref_token_is_massive = o.not_org
            re.is_doubt = o.is_doubt
            if (not o.is_gsk and not o.has_terr_keyword): 
                if (not AddressItemToken.check_house_after(sits[0].end_token.next0_, False, False)): 
                    if (not MiscLocationHelper.is_user_param_address(sits[0])): 
                        re.is_doubt = True
            return re
        if (sits[0].is_railway): 
            str0_ = StreetReferent()
            str0_.kind = StreetKind.RAILWAY
            str0_.add_slot(StreetReferent.ATTR_TYPE, "железная дорога", False, 0)
            str0_.add_slot(StreetReferent.ATTR_NAME, sits[0].value.replace(" ЖЕЛЕЗНАЯ ДОРОГА", ""), False, 0)
            t0 = sits[0].begin_token
            t1 = sits[0].end_token
            if (len(sits) > 1 and sits[1].typ == StreetItemType.NUMBER): 
                num = sits[1].value
                if (t0.previous is not None and ((t0.previous.is_value("КИЛОМЕТР", None) or t0.previous.is_value("КМ", None)))): 
                    t0 = t0.previous
                    str0_.add_slot(StreetReferent.ATTR_NUMBER, num + "км", False, 0)
                    t1 = sits[1].end_token
                elif (sits[1].is_number_km): 
                    str0_.add_slot(StreetReferent.ATTR_NUMBER, num + "км", False, 0)
                    t1 = sits[1].end_token
            elif (sits[0].noun_is_doubt_coef > 1): 
                return None
            return AddressItemToken._new202(AddressItemType.STREET, t0, t1, str0_)
        if (sits[0].termin is None): 
            return None
        if (sits[0].termin.acronym == "МКАД"): 
            str0_ = StreetReferent()
            str0_.kind = StreetKind.ROAD
            str0_.add_slot(StreetReferent.ATTR_TYPE, "автодорога", False, 0)
            str0_.add_slot(StreetReferent.ATTR_NAME, "МОСКОВСКАЯ КОЛЬЦЕВАЯ", False, 0)
            t0 = sits[0].begin_token
            t1 = sits[0].end_token
            if (len(sits) > 1 and sits[1].typ == StreetItemType.NUMBER): 
                num = sits[1].value
                if (t0.previous is not None and ((t0.previous.is_value("КИЛОМЕТР", None) or t0.previous.is_value("КМ", None)))): 
                    t0 = t0.previous
                    str0_.add_slot(StreetReferent.ATTR_NUMBER, num + "км", False, 0)
                    t1 = sits[1].end_token
                elif (sits[1].is_number_km): 
                    str0_.add_slot(StreetReferent.ATTR_NUMBER, num + "км", False, 0)
                    t1 = sits[1].end_token
            return AddressItemToken._new202(AddressItemType.STREET, t0, t1, str0_)
        if (MiscLocationHelper.check_geo_object_before(sits[0].begin_token, False) or AddressItemToken.check_house_after(sits[0].end_token.next0_, False, True)): 
            str0_ = StreetReferent()
            str0_.add_slot(StreetReferent.ATTR_NAME, sits[0].termin.canonic_text, False, 0)
            return AddressItemToken._new202(AddressItemType.STREET, sits[0].begin_token, sits[0].end_token, str0_)
        return None
    
    @staticmethod
    def _try_parse_second_street(t1 : 'Token', t2 : 'Token') -> 'AddressItemToken':
        sli = StreetItemToken.try_parse_list(t1, 10, None)
        if (sli is None or (len(sli) < 1) or sli[0].typ != StreetItemType.NOUN): 
            return None
        sli2 = StreetItemToken.try_parse_list(t2, 10, None)
        if (sli2 is None or len(sli2) == 0): 
            return None
        sli2.insert(0, sli[0])
        res = StreetDefineHelper._try_parse_street(sli2, True, False, False, None)
        if (res is None): 
            return None
        res.begin_token = sli2[1].begin_token
        return res