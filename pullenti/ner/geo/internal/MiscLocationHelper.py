# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.internal.MorphDeserializer import MorphDeserializer
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.Token import Token
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr

class MiscLocationHelper:
    
    @staticmethod
    def is_user_param_address(t : 'Token') -> bool:
        if (t is None): 
            return False
        if (t.kit.sofa.user_params is not None): 
            if ("ADDRESS" in t.kit.sofa.user_params or "GARADDRESS" in t.kit.sofa.user_params): 
                return True
        return False
    
    @staticmethod
    def is_user_param_gar_address(t : 'Token') -> bool:
        if (t is None): 
            return False
        if (t.kit.sofa.user_params is not None): 
            if ("GARADDRESS" in t.kit.sofa.user_params): 
                return True
        return False
    
    @staticmethod
    def is_user_param_no_flats(t : 'Token') -> bool:
        if (t is None): 
            return False
        if (t.kit.sofa.user_params is not None): 
            if ("NOFLATS" in t.kit.sofa.user_params): 
                return True
        return False
    
    NAME_CHECKER = None
    
    @staticmethod
    def check_name_long(mt : 'MetaToken') -> 'Token':
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        if (mt is None or mt.whitespaces_after_count > 2): 
            return None
        if (not MiscLocationHelper.is_user_param_address(mt)): 
            return None
        if (mt.begin_token != mt.end_token): 
            return None
        t = mt.end_token.next0_
        if (t is None): 
            return None
        mc = t.get_morph_class_in_dictionary()
        if (((mc.is_preposition or t.is_and)) and t.next0_ is not None): 
            t = t.next0_
        if (isinstance(t, NumberToken)): 
            return None
        ok = False
        if (t.next0_ is None or t.is_newline_after): 
            ok = True
        elif (t.next0_.is_comma): 
            ok = True
        if (isinstance(t, TextToken)): 
            mc = t.get_morph_class_in_dictionary()
            if (not t.chars.is_letter or (t.length_char < 2)): 
                return None
            if (mc.is_adjective): 
                ok = False
            else: 
                if ((mc.is_proper_surname and not t.is_value("ГОРА", None) and not t.is_value("ГЛИНКА", None)) and not MiscLocationHelper.is_user_param_gar_address(t)): 
                    return None
                if (t.is_value("УЛ", None)): 
                    return None
                if (MiscLocationHelper.check_territory(t) is not None and not t.is_value("САД", None)): 
                    return None
                if (mc.is_noun or mc.is_proper_geo): 
                    pass
                elif (mc.is_undefined and t.chars.is_all_lower): 
                    pass
                else: 
                    ok = False
        if (ok): 
            if (isinstance(mt, StreetItemToken)): 
                if (StreetItemToken.check_keyword(t)): 
                    return None
        elif (MiscLocationHelper.NAME_CHECKER is not None): 
            str0_ = MiscHelper.get_text_value(mt.begin_token, t, GetTextAttr.NO)
            is_street = True
            if ((isinstance(mt, CityItemToken)) or (isinstance(mt, TerrItemToken))): 
                is_street = False
            if (MiscLocationHelper.NAME_CHECKER.check(str0_, is_street)): 
                ok = True
        if (t.is_newline_after and MiscLocationHelper.is_user_param_gar_address(t)): 
            ok = True
            if (t.is_value("ГОРА", None)): 
                pass
            else: 
                rt = t.kit.process_referent("PERSON", mt.end_token, None)
                if (rt is not None and rt.end_token == t): 
                    ok = False
        if (ok): 
            return t
        return None
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        pass
    
    @staticmethod
    def _try_parse_npt(t : 'Token') -> 'NounPhraseToken':
        if (t is None): 
            return None
        return NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
    
    @staticmethod
    def check_territory(t : 'Token') -> 'Token':
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.internal.OrgTypToken import OrgTypToken
        if (not (isinstance(t, TextToken))): 
            return None
        tok = MiscLocationHelper.__m_terrs.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        if (tok.termin.canonic_text == "ТЕРРИТОРИЯ"): 
            if (t.previous is not None and t.previous.is_value("ФЕДЕРАЛЬНЫЙ", None)): 
                return None
        if (tok.termin.canonic_text == "УЧАСТОК"): 
            if (not MiscLocationHelper.is_user_param_address(t)): 
                return None
            ait = AddressItemToken.try_parse_pure_item(t, None, None)
            if ((ait is not None and not Utils.isNullOrEmpty(ait.value) and (len(ait.value) < 4)) and str.isdigit(ait.value[0])): 
                return None
        tt2 = tok.end_token
        tok2 = MiscLocationHelper.__m_terrs.try_parse(tt2.next0_, TerminParseAttr.NO)
        if (tok2 is not None): 
            tt2 = tok2.end_token
        if (tt2.next0_ is not None and tt2.next0_.is_value("МЕСТНОСТЬ", None)): 
            tt2 = tt2.next0_
        if (tt2.next0_ is not None and tt2.next0_.is_value("ПЛОЩАДКА", None)): 
            if (OrgTypToken.try_parse(tt2.next0_, False, None) is None): 
                tt2 = tt2.next0_
        npt = MiscLocationHelper._try_parse_npt(tt2.next0_)
        if (npt is not None and npt.end_token.is_value("ЗЕМЛЯ", None)): 
            tt2 = npt.end_token
        if (tt2.next0_ is not None): 
            if (tt2.next0_.is_value("БЫВШИЙ", None) or tt2.next0_.is_value("РАЙОН", None)): 
                tt2 = tt2.next0_
            elif (tt2.next0_.is_value("БЫВШ", None)): 
                tt2 = tt2.next0_
                if (tt2.next0_ is not None and tt2.next0_.is_char('.')): 
                    tt2 = tt2.next0_
        return tt2
    
    @staticmethod
    def check_geo_object_before(t : 'Token', pure_geo : bool=False) -> bool:
        from pullenti.ner.address.StreetReferent import StreetReferent
        if (t is None): 
            return False
        tt = t.previous
        first_pass3974 = True
        while True:
            if first_pass3974: first_pass3974 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if ((tt.is_char_of(",.;:") or tt.is_hiphen or tt.is_and) or tt.morph.class0_.is_conjunction or tt.morph.class0_.is_preposition): 
                continue
            if (MiscLocationHelper.__m_terrs.try_parse(tt, TerminParseAttr.NO) is not None): 
                continue
            if (MiscLocationHelper.__m_geo_before.try_parse(tt, TerminParseAttr.NO) is not None): 
                return True
            if (tt.length_char == 2 and (isinstance(tt, TextToken)) and tt.chars.is_all_upper): 
                term = tt.term
                if (not Utils.isNullOrEmpty(term) and term[0] == 'Р'): 
                    return True
            rt = Utils.asObjectOrNull(tt, ReferentToken)
            if (rt is not None): 
                if (isinstance(rt.referent, GeoReferent)): 
                    return True
                if (not pure_geo): 
                    if ((isinstance(rt.referent, AddressReferent)) or (isinstance(rt.referent, StreetReferent))): 
                        return True
            break
        return False
    
    @staticmethod
    def check_geo_object_before_brief(t : 'Token', ad : 'GeoAnalyzerData'=None) -> bool:
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.address.StreetReferent import StreetReferent
        if (t is None): 
            return False
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return False
        miss = 0
        tt = t.previous
        first_pass3975 = True
        while True:
            if first_pass3975: first_pass3975 = False
            else: tt = tt.previous
            if (not (tt is not None)): break
            if (tt.is_newline_after): 
                break
            if (tt.is_char_of(",.;") or tt.is_hiphen or tt.morph.class0_.is_conjunction): 
                continue
            if (MiscLocationHelper.check_territory(tt) is not None): 
                return True
            rt = Utils.asObjectOrNull(tt, ReferentToken)
            if (rt is not None): 
                if ((isinstance(rt.referent, GeoReferent)) or (isinstance(rt.referent, AddressReferent)) or (isinstance(rt.referent, StreetReferent))): 
                    return True
                break
            d = Utils.asObjectOrNull(tt.tag, GeoTokenData)
            if (d is not None): 
                if (d.cit is not None and ((d.cit.typ == CityItemToken.ItemType.NOUN or d.cit.typ == CityItemToken.ItemType.CITY))): 
                    return True
                if (d.terr is not None and ((d.terr.termin_item is not None or d.terr.onto_item is not None))): 
                    return True
                if (d.street is not None and d.street.typ == StreetItemType.NOUN and d.street.noun_is_doubt_coef == 0): 
                    return True
            miss += 1
            if (miss > 2): 
                break
        return False
    
    @staticmethod
    def check_geo_object_after_brief(t : 'Token', ad : 'GeoAnalyzerData'=None) -> bool:
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.address.StreetReferent import StreetReferent
        if (t is None): 
            return False
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return False
        miss = 0
        tt = t.next0_
        first_pass3976 = True
        while True:
            if first_pass3976: first_pass3976 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_newline_before): 
                break
            if (tt.is_char_of(",.;") or tt.is_hiphen or tt.morph.class0_.is_conjunction): 
                continue
            if (MiscLocationHelper.check_territory(tt) is not None): 
                return True
            rt = Utils.asObjectOrNull(tt, ReferentToken)
            if (rt is not None): 
                if ((isinstance(rt.referent, GeoReferent)) or (isinstance(rt.referent, AddressReferent)) or (isinstance(rt.referent, StreetReferent))): 
                    return True
                break
            d = Utils.asObjectOrNull(tt.tag, GeoTokenData)
            if (d is not None): 
                if (d.cit is not None and ((d.cit.typ == CityItemToken.ItemType.NOUN or d.cit.typ == CityItemToken.ItemType.CITY))): 
                    return True
                if (d.terr is not None and ((d.terr.termin_item is not None or d.terr.onto_item is not None))): 
                    return True
                if (d.street is not None and d.street.typ == StreetItemType.NOUN and d.street.noun_is_doubt_coef == 0): 
                    return True
            if (CityItemToken.check_keyword(tt) is not None): 
                return True
            if ((isinstance(tt, TextToken)) and tt.chars.is_all_lower): 
                if (not tt.morph.class0_.is_preposition): 
                    break
            miss += 1
            if (miss > 4): 
                break
        return False
    
    @staticmethod
    def check_geo_object_after(t : 'Token', dont_check_city : bool=False, check_terr : bool=False) -> bool:
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        from pullenti.ner.address.StreetReferent import StreetReferent
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        if (t is None): 
            return False
        cou = 0
        tt = t.next0_
        first_pass3977 = True
        while True:
            if first_pass3977: first_pass3977 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt.is_char_of(",.;") or tt.is_hiphen or tt.morph.class0_.is_conjunction): 
                continue
            if (tt.morph.class0_.is_preposition): 
                if (not dont_check_city and tt.is_value("С", None) and tt.next0_ is not None): 
                    ttt = tt.next0_
                    if (ttt.is_char('.') and (ttt.whitespaces_after_count < 3)): 
                        ttt = ttt.next0_
                    cits = CityItemToken.try_parse_list(ttt, 3, None)
                    if (cits is not None and len(cits) == 1 and ((cits[0].typ == CityItemToken.ItemType.PROPERNAME or cits[0].typ == CityItemToken.ItemType.CITY))): 
                        if (tt.chars.is_all_upper and not cits[0].chars.is_all_upper): 
                            pass
                        else: 
                            return True
                continue
            if (MiscLocationHelper.check_territory(tt) is not None): 
                return True
            rt = Utils.asObjectOrNull(tt, ReferentToken)
            if (rt is None): 
                if (not dont_check_city and cou == 0): 
                    cits = CityItemToken.try_parse_list(tt, 3, None)
                    if ((cits is not None and len(cits) >= 2 and cits[0].typ == CityItemToken.ItemType.NOUN) and ((cits[1].typ == CityItemToken.ItemType.PROPERNAME or cits[1].typ == CityItemToken.ItemType.CITY))): 
                        if (cits[0].chars.is_all_upper and not cits[1].chars.is_all_upper): 
                            pass
                        else: 
                            return True
                    if (cits is not None and cits[0].typ == CityItemToken.ItemType.NOUN and (cits[0].whitespaces_after_count < 3)): 
                        if (OrgItemToken.try_parse(cits[0].end_token.next0_, None) is not None): 
                            return True
                if (check_terr and cou == 0): 
                    ters = TerrItemToken.try_parse_list(tt, 4, None)
                    if (ters is not None): 
                        if (len(ters) == 2 and (ters[0].whitespaces_after_count < 3)): 
                            if (ters[0].termin_item is not None and ters[1].termin_item is None and ters[1].onto_item is None): 
                                return True
                            if (ters[1].termin_item is not None and ters[0].termin_item is None): 
                                return True
                        if (len(ters) == 1 and ters[0].onto_item is not None): 
                            return True
                if ((isinstance(tt, TextToken)) and tt.length_char > 2 and cou == 0): 
                    cou += 1
                    continue
                else: 
                    break
            if ((isinstance(rt.referent, GeoReferent)) or (isinstance(rt.referent, AddressReferent)) or (isinstance(rt.referent, StreetReferent))): 
                return True
            break
        return False
    
    @staticmethod
    def check_near_before(t : 'Token', ad : 'GeoAnalyzerData') -> 'Token':
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        if (t is None or t.previous is None): 
            return None
        cou = 0
        tt = t.previous
        while tt is not None and (cou < 5): 
            if (tt.morph.class0_.is_preposition and (cou < 2)): 
                if (MiscLocationHelper.__m_near.try_parse(tt, TerminParseAttr.NO) is not None): 
                    return tt
            ait = AddressItemToken.try_parse_pure_item(tt, None, ad)
            if (ait is not None and ait.typ == AddressItemType.DETAIL): 
                return tt
            tt = tt.previous; cou += 1
        return None
    
    @staticmethod
    def check_unknown_region(t : 'Token') -> 'Token':
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        if (not (isinstance(t, TextToken))): 
            return None
        npt = MiscLocationHelper._try_parse_npt(t)
        if (npt is None): 
            return None
        if (TerrItemToken._m_unknown_regions.try_parse(npt.end_token, TerminParseAttr.FULLWORDSONLY) is not None): 
            return npt.end_token
        return None
    
    @staticmethod
    def get_std_adj_full(t : 'Token', gen : 'MorphGender', num : 'MorphNumber', strict : bool) -> typing.List[str]:
        if (not (isinstance(t, TextToken))): 
            return None
        return MiscLocationHelper.get_std_adj_full_str(t.term, gen, num, strict)
    
    @staticmethod
    def get_std_adj_full_str(v : str, gen : 'MorphGender', num : 'MorphNumber', strict : bool) -> typing.List[str]:
        res = list()
        if (v.startswith("Б")): 
            if (num == MorphNumber.PLURAL): 
                res.append("БОЛЬШИЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("БОЛЬШИЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("БОЛЬШАЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("БОЛЬШОЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("БОЛЬШОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("М")): 
            if (num == MorphNumber.PLURAL): 
                res.append("МАЛЫЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("МАЛЫЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("МАЛАЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("МАЛЫЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("МАЛОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("В")): 
            if (num == MorphNumber.PLURAL): 
                res.append("ВЕРХНИЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("ВЕРХНИЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("ВЕРХНЯЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("ВЕРХНИЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("ВЕРХНЕЕ")
            if (len(res) == 0 and gen == MorphGender.UNDEFINED): 
                res.append("ВЕРХНИЙ")
            if (len(res) > 0): 
                return res
            return None
        if (v == "Н"): 
            r1 = MiscLocationHelper.get_std_adj_full_str("НОВ", gen, num, strict)
            r2 = MiscLocationHelper.get_std_adj_full_str("НИЖ", gen, num, strict)
            if (r1 is None and r2 is None): 
                return None
            if (r1 is None): 
                return r2
            if (r2 is None): 
                return r1
            r1.insert(1, r2[0])
            del r2[0]
            r1.extend(r2)
            return r1
        if (v == "С" or v == "C"): 
            r1 = MiscLocationHelper.get_std_adj_full_str("СТ", gen, num, strict)
            r2 = MiscLocationHelper.get_std_adj_full_str("СР", gen, num, strict)
            if (r1 is None and r2 is None): 
                return None
            if (r1 is None): 
                return r2
            if (r2 is None): 
                return r1
            r1.insert(1, r2[0])
            del r2[0]
            r1.extend(r2)
            return r1
        if (v.startswith("НОВ")): 
            if (num == MorphNumber.PLURAL): 
                res.append("НОВЫЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("НОВЫЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("НОВАЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("НОВЫЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("НОВОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("НИЖ")): 
            if (num == MorphNumber.PLURAL): 
                res.append("НИЖНИЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("НИЖНИЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("НИЖНЯЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("НИЖНИЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("НИЖНЕЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("КР")): 
            if (num == MorphNumber.PLURAL): 
                res.append("КРАСНЫЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("КРАСНЫЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("КРАСНАЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("КРАСНЫЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("КРАСНОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("СТ")): 
            if (num == MorphNumber.PLURAL): 
                res.append("СТАРЫЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("СТАРЫЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("СТАРАЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("СТАРЫЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("СТАРОЕ")
            if (len(res) > 0): 
                return res
            return None
        if (v.startswith("СР")): 
            if (num == MorphNumber.PLURAL): 
                res.append("СРЕДНИЕ")
                return res
            if (not strict and ((num) & (MorphNumber.PLURAL)) != (MorphNumber.UNDEFINED)): 
                res.append("СРЕДНИЕ")
            if (((gen) & (MorphGender.FEMINIE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.FEMINIE): 
                    res.append("СРЕДНЯЯ")
            if (((gen) & (MorphGender.MASCULINE)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.MASCULINE): 
                    res.append("СРЕДНИЙ")
            if (((gen) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                if (not strict or gen == MorphGender.NEUTER): 
                    res.append("СРЕДНЕЕ")
            if (len(res) > 0): 
                return res
            return None
        return None
    
    @staticmethod
    def get_geo_referent_by_name(name : str) -> 'GeoReferent':
        from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
        res = None
        wrapres1488 = RefOutArgWrapper(None)
        inoutres1489 = Utils.tryGetValue(MiscLocationHelper.__m_geo_ref_by_name, name, wrapres1488)
        res = wrapres1488.value
        if (inoutres1489): 
            return res
        for r in TerrItemToken._m_all_states: 
            if (r.find_slot(None, name, True) is not None): 
                res = (Utils.asObjectOrNull(r, GeoReferent))
                break
        MiscLocationHelper.__m_geo_ref_by_name[name] = res
        return res
    
    __m_geo_ref_by_name = None
    
    @staticmethod
    def try_attach_nord_west(t : 'Token') -> 'MetaToken':
        if (not (isinstance(t, TextToken))): 
            return None
        tok = MiscLocationHelper.__m_nords.try_parse(t, TerminParseAttr.NO)
        if (tok is None): 
            return None
        res = MetaToken._new674(t, t, t.morph)
        t1 = None
        if ((t.next0_ is not None and t.next0_.is_hiphen and (t.whitespaces_after_count < 2)) and (t.next0_.whitespaces_after_count < 2)): 
            t1 = t.next0_.next0_
        elif (t.morph.class0_.is_adjective and (t.whitespaces_after_count < 2)): 
            t1 = t.next0_
        if (t1 is not None): 
            tok = MiscLocationHelper.__m_nords.try_parse(t1, TerminParseAttr.NO)
            if ((tok) is not None): 
                res.end_token = tok.end_token
                res.morph = tok.morph
        return res
    
    __m_terrs = None
    
    __m_geo_before = None
    
    __m_near = None
    
    @staticmethod
    def _initialize() -> None:
        if (MiscLocationHelper.__m_nords is not None): 
            return
        MiscLocationHelper.__m_nords = TerminCollection()
        for s in ["СЕВЕРНЫЙ", "ЮЖНЫЙ", "ЗАПАДНЫЙ", "ВОСТОЧНЫЙ", "ЦЕНТРАЛЬНЫЙ", "БЛИЖНИЙ", "ДАЛЬНИЙ", "СРЕДНИЙ", "СЕВЕР", "ЮГ", "ЗАПАД", "ВОСТОК", "СЕВЕРО", "ЮГО", "ЗАПАДНО", "ВОСТОЧНО", "СЕВЕРОЗАПАДНЫЙ", "СЕВЕРОВОСТОЧНЫЙ", "ЮГОЗАПАДНЫЙ", "ЮГОВОСТОЧНЫЙ"]: 
            MiscLocationHelper.__m_nords.add(Termin(s, MorphLang.RU, True))
        MiscLocationHelper.__m_near = TerminCollection()
        for s in ["У", "ОКОЛО", "ВБЛИЗИ", "ВБЛИЗИ ОТ", "НЕДАЛЕКО ОТ", "НЕПОДАЛЕКУ ОТ"]: 
            MiscLocationHelper.__m_near.add(Termin(s))
        MiscLocationHelper.__m_geo_before = TerminCollection()
        for s in ["ПРОЖИВАТЬ", "ПРОЖИВАТИ", "РОДИТЬ", "НАРОДИТИ", "ЗАРЕГИСТРИРОВАТЬ", "ЗАРЕЄСТРУВАТИ", "АДРЕС", "УРОЖЕНЕЦ", "УРОДЖЕНЕЦЬ", "УРОЖЕНКА", "УРОДЖЕНКА"]: 
            MiscLocationHelper.__m_geo_before.add(Termin(s))
        MiscLocationHelper.__m_terrs = TerminCollection()
        t = Termin("ТЕРРИТОРИЯ")
        t.add_variant("ТЕР", False)
        t.add_variant("ТЕРР", False)
        t.add_variant("ТЕРИТОРІЯ", False)
        t.add_abridge("ТЕР.")
        t.add_abridge("ТЕРР.")
        MiscLocationHelper.__m_terrs.add(t)
        MiscLocationHelper.__m_terrs.add(Termin("ГРАНИЦА"))
        MiscLocationHelper.__m_terrs.add(Termin("В ГРАНИЦАХ"))
        t = Termin("УЧАСТОК")
        t.add_abridge("УЧ.")
        t.add_abridge("УЧ-К")
        MiscLocationHelper.__m_terrs.add(t)
        table = "\nAF\tAFG\nAX\tALA\nAL\tALB\nDZ\tDZA\nAS\tASM\nAD\tAND\nAO\tAGO\nAI\tAIA\nAQ\tATA\nAG\tATG\nAR\tARG\nAM\tARM\nAW\tABW\nAU\tAUS\nAT\tAUT\nAZ\tAZE\nBS\tBHS\nBH\tBHR\nBD\tBGD\nBB\tBRB\nBY\tBLR\nBE\tBEL\nBZ\tBLZ\nBJ\tBEN\nBM\tBMU\nBT\tBTN\nBO\tBOL\nBA\tBIH\nBW\tBWA\nBV\tBVT\nBR\tBRA\nVG\tVGB\nIO\tIOT\nBN\tBRN\nBG\tBGR\nBF\tBFA\nBI\tBDI\nKH\tKHM\nCM\tCMR\nCA\tCAN\nCV\tCPV\nKY\tCYM\nCF\tCAF\nTD\tTCD\nCL\tCHL\nCN\tCHN\nHK\tHKG\nMO\tMAC\nCX\tCXR\nCC\tCCK\nCO\tCOL\nKM\tCOM\nCG\tCOG\nCD\tCOD\nCK\tCOK\nCR\tCRI\nCI\tCIV\nHR\tHRV\nCU\tCUB\nCY\tCYP\nCZ\tCZE\nDK\tDNK\nDJ\tDJI\nDM\tDMA\nDO\tDOM\nEC\tECU\nEG\tEGY\nSV\tSLV\nGQ\tGNQ\nER\tERI\nEE\tEST\nET\tETH\nFK\tFLK\nFO\tFRO\nFJ\tFJI\nFI\tFIN\nFR\tFRA\nGF\tGUF\nPF\tPYF\nTF\tATF\nGA\tGAB\nGM\tGMB\nGE\tGEO\nDE\tDEU\nGH\tGHA\nGI\tGIB\nGR\tGRC\nGL\tGRL\nGD\tGRD\nGP\tGLP\nGU\tGUM\nGT\tGTM\nGG\tGGY\nGN\tGIN\nGW\tGNB\nGY\tGUY\nHT\tHTI\nHM\tHMD\nVA\tVAT\nHN\tHND\nHU\tHUN\nIS\tISL\nIN\tIND\nID\tIDN\nIR\tIRN\nIQ\tIRQ\nIE\tIRL\nIM\tIMN\nIL\tISR\nIT\tITA\nJM\tJAM\nJP\tJPN\nJE\tJEY\nJO\tJOR\nKZ\tKAZ\nKE\tKEN\nKI\tKIR\nKP\tPRK\nKR\tKOR\nKW\tKWT\nKG\tKGZ\nLA\tLAO\nLV\tLVA\nLB\tLBN\nLS\tLSO\nLR\tLBR\nLY\tLBY\nLI\tLIE\nLT\tLTU\nLU\tLUX\nMK\tMKD\nMG\tMDG\nMW\tMWI\nMY\tMYS\nMV\tMDV\nML\tMLI\nMT\tMLT\nMH\tMHL\nMQ\tMTQ\nMR\tMRT\nMU\tMUS\nYT\tMYT\nMX\tMEX\nFM\tFSM\nMD\tMDA\nMC\tMCO\nMN\tMNG\nME\tMNE\nMS\tMSR\nMA\tMAR\nMZ\tMOZ\nMM\tMMR\nNA\tNAM\nNR\tNRU\nNP\tNPL\nNL\tNLD\nAN\tANT\nNC\tNCL\nNZ\tNZL\nNI\tNIC\nNE\tNER\nNG\tNGA\nNU\tNIU\nNF\tNFK\nMP\tMNP\nNO\tNOR\nOM\tOMN\nPK\tPAK\nPW\tPLW\nPS\tPSE\nPA\tPAN\nPG\tPNG\nPY\tPRY\nPE\tPER\nPH\tPHL\nPN\tPCN\nPL\tPOL\nPT\tPRT\nPR\tPRI\nQA\tQAT\nRE\tREU\nRO\tROU\nRU\tRUS\nRW\tRWA\nBL\tBLM\nSH\tSHN\nKN\tKNA\nLC\tLCA\nMF\tMAF\nPM\tSPM\nVC\tVCT\nWS\tWSM\nSM\tSMR\nST\tSTP\nSA\tSAU\nSN\tSEN\nRS\tSRB\nSC\tSYC\nSL\tSLE\nSG\tSGP\nSK\tSVK\nSI\tSVN\nSB\tSLB\nSO\tSOM\nZA\tZAF\nGS\tSGS\nSS\tSSD\nES\tESP\nLK\tLKA\nSD\tSDN\nSR\tSUR\nSJ\tSJM\nSZ\tSWZ\nSE\tSWE\nCH\tCHE\nSY\tSYR\nTW\tTWN\nTJ\tTJK\nTZ\tTZA\nTH\tTHA\nTL\tTLS\nTG\tTGO\nTK\tTKL\nTO\tTON\nTT\tTTO\nTN\tTUN\nTR\tTUR\nTM\tTKM\nTC\tTCA\nTV\tTUV\nUG\tUGA\nUA\tUKR\nAE\tARE\nGB\tGBR\nUS\tUSA\nUM\tUMI\nUY\tURY\nUZ\tUZB\nVU\tVUT\nVE\tVEN\nVN\tVNM\nVI\tVIR\nWF\tWLF\nEH\tESH\nYE\tYEM\nZM\tZMB\nZW\tZWE "
        for s in Utils.splitString(table, '\n', False): 
            ss = s.strip()
            if ((len(ss) < 6) or not Utils.isWhitespace(ss[2])): 
                continue
            cod2 = ss[0:0+2]
            cod3 = ss[3:].strip()
            if (len(cod3) != 3): 
                continue
            if (not cod2 in MiscLocationHelper._m_alpha2_3): 
                MiscLocationHelper._m_alpha2_3[cod2] = cod3
            if (not cod3 in MiscLocationHelper._m_alpha3_2): 
                MiscLocationHelper._m_alpha3_2[cod3] = cod2
    
    __m_nords = None
    
    _m_alpha2_3 = None
    
    _m_alpha3_2 = None
    
    @staticmethod
    def _deflate(zip0_ : bytearray) -> bytearray:
        with MemoryStream() as unzip: 
            data = MemoryStream(zip0_)
            data.position = 0
            MorphDeserializer.deflate_gzip(data, unzip)
            data.close()
            return unzip.toarray()
    
    # static constructor for class MiscLocationHelper
    @staticmethod
    def _static_ctor():
        MiscLocationHelper.__m_geo_ref_by_name = dict()
        MiscLocationHelper._m_alpha2_3 = dict()
        MiscLocationHelper._m_alpha3_2 = dict()

MiscLocationHelper._static_ctor()