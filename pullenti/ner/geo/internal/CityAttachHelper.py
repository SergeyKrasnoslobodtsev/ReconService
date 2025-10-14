# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
from pullenti.ner.geo.internal.CityItemToken import CityItemToken
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.Referent import Referent
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.TextToken import TextToken
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.Token import Token
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.geo.internal.NameToken import NameToken
from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.core.ProperNameHelper import ProperNameHelper
from pullenti.ner.core.AnalyzerDataWithOntology import AnalyzerDataWithOntology
from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper

class CityAttachHelper:
    
    @staticmethod
    def try_define(li : typing.List['CityItemToken'], ad : 'GeoAnalyzerData', always : bool=False) -> 'ReferentToken':
        if (li is None): 
            return None
        oi = None
        if (len(li) > 2 and li[0].typ == CityItemToken.ItemType.MISC and li[1].typ == CityItemToken.ItemType.NOUN): 
            li[1].doubtful = False
            del li[0]
        if ((len(li) == 1 and li[0].onto_item is not None and MiscLocationHelper.is_user_param_address(li[0])) and ((li[0].is_newline_before or li[0].begin_token.previous.is_comma))): 
            sty = StreetItemToken.try_parse(li[0].end_token.next0_, None, False, None)
            if (sty is not None and sty.typ == StreetItemType.NOUN): 
                if (sty.end_token.is_newline_after or sty.end_token.next0_.is_comma): 
                    return None
        res = None
        if (res is None and len(li) > 1): 
            res = CityAttachHelper.__try4(li)
            if (res is not None and res.end_char <= li[1].end_char): 
                res = (None)
        if (res is None): 
            wrapoi1428 = RefOutArgWrapper(None)
            res = CityAttachHelper.__try1(li, wrapoi1428, ad)
            oi = wrapoi1428.value
        if (res is None): 
            wrapoi1429 = RefOutArgWrapper(None)
            res = CityAttachHelper.__try_noun_name(li, wrapoi1429, False)
            oi = wrapoi1429.value
        if (res is None): 
            wrapoi1430 = RefOutArgWrapper(None)
            res = CityAttachHelper.__try_name_exist(li, wrapoi1430, False)
            oi = wrapoi1430.value
        if (res is None): 
            res = CityAttachHelper.__try4(li)
        if (res is None and always): 
            wrapoi1431 = RefOutArgWrapper(None)
            res = CityAttachHelper.__try_noun_name(li, wrapoi1431, True)
            oi = wrapoi1431.value
        if (res is None and always): 
            if (OrgItemToken.try_parse(li[0].begin_token, ad) is not None): 
                pass
            else: 
                wrapoi1432 = RefOutArgWrapper(None)
                res = CityAttachHelper.__try_name_exist(li, wrapoi1432, True)
                oi = wrapoi1432.value
        if ((res is None and len(li) == 1 and li[0].typ == CityItemToken.ItemType.NOUN) and li[0].geo_object_before and (li[0].whitespaces_after_count < 3)): 
            rt = Utils.asObjectOrNull(li[0].end_token.next0_, ReferentToken)
            if ((rt is not None and rt.begin_token == rt.end_token and not rt.begin_token.chars.is_all_lower) and (isinstance(rt.begin_token, TextToken))): 
                nam = CityItemToken.try_parse(rt.begin_token, None, False, None)
                if (nam is not None and nam.end_token == rt.end_token and ((nam.typ == CityItemToken.ItemType.PROPERNAME or nam.typ == CityItemToken.ItemType.CITY))): 
                    t = li[0].kit.debed_token(rt)
                    g = GeoReferent()
                    g._add_typ(li[0].value)
                    g._add_name(nam.value)
                    g._add_name(nam.alt_value)
                    return ReferentToken(g, li[0].begin_token, rt.end_token)
        if (((res is None and li[0].typ == CityItemToken.ItemType.PROPERNAME and li[0].geo_object_before) and MiscLocationHelper.is_user_param_address(li[0]) and li[0].org_ref is None) and ((len(li) == 1 or li[1].typ == CityItemToken.ItemType.PROPERNAME)) and not StreetItemToken.check_keyword(li[0].begin_token)): 
            tt = li[0].begin_token.previous
            while tt is not None and tt.is_comma:
                tt = tt.previous
            if (tt is not None and (isinstance(tt.get_referent(), GeoReferent))): 
                gee = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                if (gee.is_region or gee.is_state): 
                    if (AddressItemToken.check_street_after(li[0].begin_token.previous, False)): 
                        pass
                    else: 
                        city = GeoReferent()
                        city._add_typ("населенный пункт")
                        city._add_name(li[0].value)
                        return ReferentToken(city, li[0].begin_token, li[0].end_token)
        if (res is None): 
            return None
        if (res is not None and res.morph is not None): 
            pass
        if (isinstance(res.begin_token.previous, TextToken)): 
            if (res.begin_token.previous.is_value("ТЕРРИТОРИЯ", None)): 
                res.begin_token = res.begin_token.previous
                res.morph = res.begin_token.morph
            if ((BracketHelper.can_be_start_of_sequence(res.begin_token.previous, False, False) and BracketHelper.can_be_end_of_sequence(res.end_token.next0_, False, None, False) and res.begin_token.previous.previous is not None) and res.begin_token.previous.previous.is_value("ТЕРРИТОРИЯ", None)): 
                res.begin_token = res.begin_token.previous.previous
                res.morph = res.begin_token.morph
                res.end_token = res.end_token.next0_
        city2 = None
        for s in res.referent.slots: 
            if (s.type_name == GeoReferent.ATTR_NAME): 
                val = Utils.asObjectOrNull(s.value, str)
                if (val.find(' ') < 0): 
                    continue
                if (val.find('-') > 0): 
                    continue
                try: 
                    ar1 = ProcessorService.get_empty_processor().process(SourceOfAnalysis(val), None, None)
                    tt = ar1.first_token
                    first_pass3964 = True
                    while True:
                        if first_pass3964: first_pass3964 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        cit = CityItemToken.try_parse(tt, None, False, None)
                        if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN): 
                            if (cit.value == "СЛОБОДА" or cit.value == "ВЫСЕЛКИ"): 
                                continue
                            if (city2 is None): 
                                city2 = GeoReferent()
                                for ty in res.referent.typs: 
                                    city2._add_typ(ty)
                            city2._add_typ(cit.value.lower())
                            if (tt != ar1.first_token): 
                                city2.add_slot(GeoReferent.ATTR_NAME, val[0:0+tt.previous.end_char + 1], False, 0)
                            elif (cit.end_token.next0_ is not None): 
                                city2.add_slot(GeoReferent.ATTR_NAME, val[cit.end_token.next0_.begin_char:], False, 0)
                            else: 
                                city2 = (None)
                except Exception as ex1433: 
                    pass
        if (city2 is not None): 
            res.referent = (city2)
        return res
    
    @staticmethod
    def __try1(li : typing.List['CityItemToken'], oi : 'IntOntologyItem', ad : 'AnalyzerDataWithOntology') -> 'ReferentToken':
        oi.value = (None)
        if (li is None or (len(li) < 1)): 
            return None
        elif (li[0].typ != CityItemToken.ItemType.CITY): 
            if (len(li) == 1): 
                return None
            if (li[0].typ != CityItemToken.ItemType.PROPERNAME or li[1].typ != CityItemToken.ItemType.NOUN): 
                return None
            if (len(li) == 2): 
                pass
            elif (((len(li) >= 3 or MiscLocationHelper.is_user_param_address(li[0]))) and li[2].typ == CityItemToken.ItemType.PROPERNAME): 
                if (li[2].doubtful): 
                    del li[2:2+len(li) - 2]
                elif (AddressItemToken.check_street_after(li[2].begin_token, False)): 
                    del li[2:2+len(li) - 2]
                else: 
                    return None
            else: 
                return None
        elif (len(li) > 2 and li[1].typ == CityItemToken.ItemType.NOUN and ((li[2].typ == CityItemToken.ItemType.PROPERNAME or li[2].typ == CityItemToken.ItemType.CITY))): 
            if (li[1].value != "ГОРОД"): 
                del li[1:1+2]
        i = 1
        oi.value = li[0].onto_item
        ok = not li[0].doubtful
        if ((ok and li[0].onto_item is not None and li[0].onto_item.misc_attr is None) and ad is not None): 
            if (li[0].onto_item.owner != ad.local_ontology and not li[0].onto_item.owner.is_ext_ontology): 
                if (li[0].begin_token.previous is not None and li[0].begin_token.previous.is_value("В", None)): 
                    pass
                else: 
                    ok = False
        if (len(li) == 1 and li[0].begin_token.morph.class0_.is_adjective): 
            sits = StreetItemToken.try_parse_list(li[0].begin_token, 3, None)
            if (sits is not None and len(sits) == 2 and sits[1].typ == StreetItemType.NOUN): 
                return None
        typ = None
        alttyp = None
        mc = li[0].morph
        if (i < len(li)): 
            if (li[i].typ == CityItemToken.ItemType.NOUN): 
                at = None
                if (not li[i].chars.is_all_lower and (li[i].whitespaces_after_count < 2)): 
                    if (StreetItemToken.check_keyword(li[i].end_token.next0_)): 
                        at = AddressItemToken.try_parse(li[i].begin_token, False, None, None)
                        if (at is not None): 
                            at2 = AddressItemToken.try_parse(li[i].end_token.next0_, False, None, None)
                            if (at2 is not None and at2.typ == AddressItemType.STREET): 
                                at = (None)
                if (at is None): 
                    typ = li[i].value
                    alttyp = li[i].alt_value
                    if (li[i].begin_token.is_value("СТ", None) and li[i].begin_token.chars.is_all_upper): 
                        if (li[i].begin_token.next0_ is not None and li[i].end_token.previous is not None and li[i].begin_token.next0_.end_char > li[i].end_token.previous.begin_char): 
                            return None
                    if ((i + 1) == len(li)): 
                        dd = False
                        if (NameToken.check_initial(li[i].begin_token) is not None): 
                            dd = True
                        elif (NameToken.check_initial_back(li[i].begin_token)): 
                            dd = True
                        if (dd): 
                            if (li[0].chars.is_latin_letter): 
                                return None
                            rt1 = li[0].kit.process_referent("PERSON", li[0].begin_token, None)
                            if (rt1 is not None and rt1.referent.type_name == "PERSON"): 
                                return None
                        if (li[i].doubtful and i == 1 and li[0].typ == CityItemToken.ItemType.PROPERNAME): 
                            if (StreetItemToken.check_keyword(li[0].begin_token)): 
                                return None
                        ok = True
                        if (not li[i].morph.case_.is_undefined): 
                            mc = li[i].morph
                        i += 1
                    elif (ok): 
                        i += 1
                    else: 
                        tt0 = li[0].begin_token.previous
                        if ((isinstance(tt0, TextToken)) and (tt0.whitespaces_after_count < 3)): 
                            if (tt0.is_value("МЭР", "МЕР") or tt0.is_value("ГЛАВА", None) or tt0.is_value("ГРАДОНАЧАЛЬНИК", None)): 
                                ok = True
                                i += 1
        if (not ok and oi.value is not None and (len(oi.value.canonic_text) < 4)): 
            return None
        if (not ok and li[0].begin_token.morph.class0_.is_proper_name): 
            return None
        if (not ok): 
            if (not MiscHelper.is_exists_in_dictionary(li[0].begin_token, li[0].end_token, (MorphClass.ADJECTIVE) | MorphClass.NOUN | MorphClass.PRONOUN)): 
                ok = (li[0].geo_object_before or li[i - 1].geo_object_after)
                if (ok and li[0].begin_token == li[0].end_token): 
                    mcc = li[0].begin_token.get_morph_class_in_dictionary()
                    if (mcc.is_proper_name or mcc.is_proper_surname): 
                        ok = False
                    elif (li[0].geo_object_before and (li[0].whitespaces_after_count < 2)): 
                        ad1 = AddressItemToken.try_parse(li[0].begin_token, False, None, None)
                        if (ad1 is not None and ad1.typ == AddressItemType.STREET): 
                            ad2 = AddressItemToken.try_parse(li[0].end_token.next0_, False, None, None)
                            if (ad2 is None or ad2.typ != AddressItemType.STREET): 
                                ok = False
                        elif (OrgItemToken.try_parse(li[0].begin_token, None) is not None): 
                            ok = False
            if (ok): 
                if (li[0].kit.process_referent("PERSON", li[0].begin_token, None) is not None): 
                    ok = False
        if (not ok): 
            ok = CityAttachHelper.check_year_after(li[0].end_token.next0_)
        if (not ok and ((not li[0].begin_token.morph.class0_.is_adjective or li[0].begin_token != li[0].end_token))): 
            ok = CityAttachHelper.check_city_after(li[0].end_token.next0_)
        if (not ok): 
            return None
        if (i < len(li)): 
            del li[i:i+len(li) - i]
        rt = None
        if (oi.value is None): 
            if (li[0].value is not None and li[0].higher_geo is not None): 
                cap = GeoReferent()
                cap._add_name(li[0].value)
                cap._add_typ_city(li[0].kit.base_language, li[0].typ == CityItemToken.ItemType.CITY)
                cap._add_misc(li[0].misc)
                cap._add_misc(li[0].misc2)
                cap.higher = li[0].higher_geo
                if (typ is not None): 
                    cap._add_typ(typ)
                if (alttyp is not None): 
                    cap._add_typ(alttyp)
                rt = ReferentToken(cap, li[0].begin_token, li[0].end_token)
            else: 
                if (li[0].value is None): 
                    return None
                if (typ is None): 
                    if ((len(li) == 1 and li[0].begin_token.previous is not None and li[0].begin_token.previous.is_hiphen) and (isinstance(li[0].begin_token.previous.previous, ReferentToken)) and (isinstance(li[0].begin_token.previous.previous.get_referent(), GeoReferent))): 
                        pass
                    else: 
                        return None
                else: 
                    if (not LanguageHelper.ends_with_ex(typ, "ПУНКТ", "ПОСЕЛЕНИЕ", "ПОСЕЛЕННЯ", "ПОСЕЛОК")): 
                        if (not LanguageHelper.ends_with(typ, "CITY")): 
                            if (typ == "СТАНЦИЯ" and ((MiscLocationHelper.check_geo_object_before(li[0].begin_token, False)))): 
                                pass
                            elif (len(li) > 1 and li[1].typ == CityItemToken.ItemType.NOUN and li[0].typ == CityItemToken.ItemType.CITY): 
                                pass
                            elif (len(li) == 2 and li[1].typ == CityItemToken.ItemType.NOUN and li[0].typ == CityItemToken.ItemType.PROPERNAME): 
                                if (li[0].geo_object_before or li[1].geo_object_after): 
                                    pass
                                elif ((li[0].begin_token.previous is not None and li[0].begin_token.previous.is_char('(') and li[1].end_token.next0_ is not None) and li[1].end_token.next0_.is_char(')')): 
                                    pass
                                elif (MiscLocationHelper.is_user_param_address(li[0]) and ((li[1].begin_token.is_value(li[1].value, None) or li[0].is_newline_before))): 
                                    pass
                                else: 
                                    return None
                            else: 
                                return None
                    if ((len(li) > 1 and li[0].begin_token.morph.class0_.is_adjective and not li[0].begin_token.morph.contains_attr("к.ф.", None)) and li[1].morph.gender != MorphGender.UNDEFINED): 
                        li[0].value = ProperNameHelper.get_name_ex(li[0].begin_token, li[0].end_token, MorphClass.ADJECTIVE, li[1].morph.case_, li[1].morph.gender, False, False)
        elif (isinstance(oi.value.referent, GeoReferent)): 
            city = Utils.asObjectOrNull(oi.value.referent.clone(), GeoReferent)
            city.occurrence.clear()
            rt = ReferentToken._new948(city, li[0].begin_token, li[len(li) - 1].end_token, mc)
        elif (typ is None): 
            typ = oi.value.typ
        if (rt is None): 
            if (len(li) == 1 and li[0].typ == CityItemToken.ItemType.CITY): 
                if (OrgItemToken.try_parse(li[0].begin_token, None) is not None): 
                    return None
            city = GeoReferent()
            city._add_name((li[0].value if oi.value is None else oi.value.canonic_text))
            city._add_misc(li[0].misc)
            city._add_misc(li[0].misc2)
            if (typ is not None): 
                city._add_typ(typ)
            else: 
                city._add_typ_city(li[0].kit.base_language, oi.value is not None)
            if (alttyp is not None): 
                city._add_typ(alttyp)
            rt = ReferentToken._new948(city, li[0].begin_token, li[len(li) - 1].end_token, mc)
            if (len(li) == 1 and li[0].end_token.next0_ is not None and li[0].end_token.next0_.is_comma): 
                cit2 = CityItemToken.try_parse(li[0].end_token.next0_.next0_, None, False, None)
                if (cit2 is not None and cit2.typ == CityItemToken.ItemType.CITY and cit2.onto_item == li[0].onto_item): 
                    if (cit2.end_token.next0_ is not None and cit2.end_token.next0_.is_comma): 
                        rt.end_token = cit2.end_token
        if ((isinstance(rt.referent, GeoReferent)) and len(li) == 1 and rt.referent.is_city): 
            if (rt.begin_token.previous is not None and rt.begin_token.previous.is_value("Г", None)): 
                rt.begin_token = rt.begin_token.previous
            elif ((rt.begin_token.previous is not None and rt.begin_token.previous.is_char('.') and rt.begin_token.previous.previous is not None) and rt.begin_token.previous.previous.is_value("Г", None)): 
                rt.begin_token = rt.begin_token.previous.previous
            elif (rt.end_token.next0_ is not None and (rt.whitespaces_after_count < 2) and rt.end_token.next0_.is_value("Г", None)): 
                rt.end_token = rt.end_token.next0_
                if (rt.end_token.next0_ is not None and rt.end_token.next0_.is_char('.')): 
                    rt.end_token = rt.end_token.next0_
        return rt
    
    @staticmethod
    def __try_noun_name(li : typing.List['CityItemToken'], oi : 'IntOntologyItem', always : bool) -> 'ReferentToken':
        oi.value = (None)
        if (li is None or (len(li) < 2) or ((li[0].typ != CityItemToken.ItemType.NOUN and li[0].typ != CityItemToken.ItemType.MISC))): 
            return None
        ok = not li[0].doubtful
        if (ok and li[0].typ == CityItemToken.ItemType.MISC): 
            ok = False
        if (not ok and li[0].typ == CityItemToken.ItemType.NOUN and li[0].is_newline_after): 
            return None
        typ = (None if li[0].typ == CityItemToken.ItemType.MISC else li[0].value)
        typ2 = (None if li[0].typ == CityItemToken.ItemType.MISC else li[0].alt_value)
        prob_adj = None
        i1 = 1
        if ((typ is not None and li[i1].typ == CityItemToken.ItemType.NOUN and ((i1 + 1) < len(li))) and li[0].whitespaces_after_count <= 1 and (((LanguageHelper.ends_with(typ, "ПОСЕЛОК") or LanguageHelper.ends_with(typ, "СЕЛИЩЕ") or typ == "ДЕРЕВНЯ") or typ == "СЕЛО"))): 
            if (li[i1].begin_token == li[i1].end_token): 
                ooo = OrgItemToken.try_parse(li[i1].begin_token, None)
                if (ooo is not None): 
                    return None
            typ2 = li[i1].value
            if (typ2 == "СТАНЦИЯ" and li[i1].begin_token.is_value("СТ", None) and ((i1 + 1) < len(li))): 
                m = li[i1 + 1].morph
                if (m.number == MorphNumber.PLURAL): 
                    prob_adj = "СТАРЫЕ"
                elif (m.gender == MorphGender.FEMINIE): 
                    prob_adj = "СТАРАЯ"
                elif (m.gender == MorphGender.MASCULINE): 
                    prob_adj = "СТАРЫЙ"
                else: 
                    prob_adj = "СТАРОЕ"
            i1 += 1
        name = Utils.ifNotNull(li[i1].value, ((None if li[i1].onto_item is None else li[i1].onto_item.canonic_text)))
        if (li[i1].onto_item is not None and MiscLocationHelper.is_user_param_address(li[i1]) and li[i1].begin_token == li[i1].end_token): 
            if (li[i1].begin_token.is_value(li[i1].onto_item.canonic_text, None)): 
                name = MiscHelper.get_text_value_of_meta_token(li[i1], GetTextAttr.NO)
        alt_name = li[i1].alt_value
        if (name is None): 
            return None
        mc = li[0].morph
        if (i1 == 1 and li[i1].typ == CityItemToken.ItemType.CITY and ((((li[0].value == "ГОРОД" and ((li[i1].onto_item is None or li[i1].onto_item.referent is None or li[i1].onto_item.referent.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None)))) or li[0].value == "МІСТО" or li[0].typ == CityItemToken.ItemType.MISC))): 
            if (typ is None and ((i1 + 1) < len(li)) and li[i1 + 1].typ == CityItemToken.ItemType.NOUN): 
                return None
            oi.value = li[i1].onto_item
            if (oi.value is not None and not MiscLocationHelper.is_user_param_address(li[i1])): 
                name = oi.value.canonic_text
            if (len(name) > 2 or oi.value.misc_attr is not None): 
                if (not li[1].doubtful or ((oi.value is not None and oi.value.misc_attr is not None))): 
                    ok = True
                elif (not ok and not li[1].is_newline_before): 
                    if (li[0].geo_object_before or li[1].geo_object_after): 
                        ok = True
                    elif (StreetDefineHelper.check_street_after(li[1].end_token.next0_)): 
                        ok = True
                    elif (li[1].end_token.next0_ is not None and (isinstance(li[1].end_token.next0_.get_referent(), DateReferent))): 
                        ok = True
                    elif ((li[1].whitespaces_before_count < 2) and li[1].onto_item is not None): 
                        if (li[1].is_newline_after): 
                            ok = True
                        else: 
                            ok = True
                if (li[1].doubtful and li[1].end_token.next0_ is not None and li[1].end_token.chars.equals(li[1].end_token.next0_.chars)): 
                    ok = False
                if (li[0].begin_token.previous is not None and li[0].begin_token.previous.is_value("В", None)): 
                    ok = True
            if (not ok): 
                ok = CityAttachHelper.check_year_after(li[1].end_token.next0_)
            if (not ok): 
                ok = CityAttachHelper.check_city_after(li[1].end_token.next0_)
            if (not ok and MiscLocationHelper.is_user_param_address(li[0])): 
                ok = True
        elif (li[i1].typ == CityItemToken.ItemType.PROPERNAME or li[i1].typ == CityItemToken.ItemType.CITY or li[i1].can_be_name): 
            if (((li[0].value == "АДМИНИСТРАЦИЯ" or li[0].value == "АДМІНІСТРАЦІЯ")) and i1 == 1): 
                return None
            if (li[i1].value == "ВЛАДИМИР" and li[i1].end_token.next0_ is not None and li[i1].end_token.next0_.is_value("ЛЕНИН", None)): 
                return None
            if (li[i1].is_newline_before): 
                if (len(li) != 2): 
                    return None
            if (not li[0].doubtful): 
                ok = True
                if (len(name) < 2): 
                    ok = False
                elif ((len(name) < 3) and li[0].morph.number != MorphNumber.SINGULAR): 
                    ok = False
                if (li[i1].doubtful and not li[i1].geo_object_after and not li[0].geo_object_before): 
                    if (li[i1].morph.case_.is_genitive): 
                        if (li[i1].end_token.next0_ is None or MiscLocationHelper.check_geo_object_after(li[i1].end_token.next0_, False, False) or AddressItemToken.check_house_after(li[i1].end_token.next0_, False, True)): 
                            pass
                        elif (li[0].begin_token.previous is None or MiscLocationHelper.check_geo_object_before(li[0].begin_token, False)): 
                            pass
                        else: 
                            ok = False
                    if (ok): 
                        rt0 = li[i1].kit.process_referent("PERSONPROPERTY", li[0].begin_token.previous, None)
                        if (rt0 is not None): 
                            rt1 = li[i1].kit.process_referent("PERSON", li[i1].begin_token, None)
                            if (rt1 is not None): 
                                ok = False
                npt = MiscLocationHelper._try_parse_npt(li[i1].begin_token)
                if (npt is not None and npt.end_token.is_value("КИЛОМЕТР", None)): 
                    npt = (None)
                if (npt is not None): 
                    if (npt.end_token.end_char > li[i1].end_char and len(npt.adjectives) > 0 and not npt.adjectives[0].end_token.next0_.is_comma): 
                        ok = False
                        li2 = list(li)
                        del li2[0:0+i1 + 1]
                        if (len(li2) > 1): 
                            oi2 = None
                            wrapoi21436 = RefOutArgWrapper(None)
                            inoutres1437 = CityAttachHelper.__try_noun_name(li2, wrapoi21436, False)
                            oi2 = wrapoi21436.value
                            if (inoutres1437 is not None): 
                                ok = True
                            elif (len(li2) == 2 and li2[0].typ == CityItemToken.ItemType.NOUN and ((li2[1].typ == CityItemToken.ItemType.PROPERNAME or li2[1].typ == CityItemToken.ItemType.CITY))): 
                                ok = True
                        if (not ok): 
                            if (OrgItemToken.try_parse(li[i1].end_token.next0_, None) is not None): 
                                ok = True
                            elif (len(li2) == 1 and li2[0].typ == CityItemToken.ItemType.NOUN and OrgItemToken.try_parse(li2[0].end_token.next0_, None) is not None): 
                                ok = True
                    if (ok and TerrItemToken._m_unknown_regions.try_parse(npt.end_token, TerminParseAttr.FULLWORDSONLY) is not None): 
                        ok1 = False
                        if (li[0].begin_token.previous is not None): 
                            ttt = li[0].begin_token.previous
                            if (ttt.is_comma and ttt.previous is not None): 
                                ttt = ttt.previous
                            geo_ = Utils.asObjectOrNull(ttt.get_referent(), GeoReferent)
                            if (geo_ is not None and not geo_.is_city): 
                                ok1 = True
                        if (npt.end_token.next0_ is not None): 
                            ttt = npt.end_token.next0_
                            if (ttt.is_comma and ttt.next0_ is not None): 
                                ttt = ttt.next0_
                            geo_ = Utils.asObjectOrNull(ttt.get_referent(), GeoReferent)
                            if (geo_ is not None and not geo_.is_city): 
                                ok1 = True
                            elif (AddressItemToken.check_house_after(ttt, False, False)): 
                                ok1 = True
                            elif (CityAttachHelper.check_street_after(ttt)): 
                                ok1 = True
                        else: 
                            ok1 = True
                        if (not ok1): 
                            return None
                if (li[0].value == "ПОРТ"): 
                    if (li[i1].chars.is_all_upper or li[i1].chars.is_latin_letter): 
                        return None
            elif (li[0].geo_object_before): 
                ok = True
            elif (li[i1].geo_object_after and not li[i1].is_newline_after): 
                ok = True
            else: 
                ok = CityAttachHelper.check_year_after(li[i1].end_token.next0_)
            if (not ok): 
                ok = CityAttachHelper.check_street_after(li[i1].end_token.next0_)
                if (ok and not MiscLocationHelper.is_user_param_address(li[0]) and li[0].begin_token.get_morph_class_in_dictionary().is_preposition): 
                    npt = NounPhraseHelper.try_parse(li[0].begin_token, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
                    if (npt is not None and npt.end_char > li[i1].end_char): 
                        ok = False
            if (not ok and li[0].begin_token.previous is not None and li[0].begin_token.previous.is_value("В", None)): 
                ok = True
            if ((not ok and len(li) == 2 and li[1].typ == CityItemToken.ItemType.CITY) and li[0].begin_token != li[0].end_token): 
                ok = True
        else: 
            return None
        if (not ok and not always): 
            if (len(li) == 3 and li[2].typ == CityItemToken.ItemType.NOUN): 
                pass
            elif (MiscLocationHelper.is_user_param_address(li[0])): 
                pass
            elif (MiscLocationHelper.check_near_before(li[0].begin_token, None) is None): 
                return None
            if ((li[0].typ == CityItemToken.ItemType.NOUN and li[0].doubtful and li[0].length_char == 2) and li[0].end_token.is_char('.')): 
                cou = 3
                tt2 = li[0].begin_token.previous
                while tt2 is not None and cou >= 0: 
                    st = StreetItemToken.try_parse(tt2, None, False, None)
                    if (st is not None and st.typ == StreetItemType.NOUN and st.end_token.next0_ == li[0].begin_token): 
                        return None
                    cou -= 1; tt2 = tt2.previous
        city = GeoReferent()
        if (oi.value is not None and oi.value.referent is not None): 
            city = (Utils.asObjectOrNull(oi.value.referent.clone(), GeoReferent))
            city.occurrence.clear()
        if (len(li) > (i1 + 1)): 
            if (len(li) == (i1 + 2) and li[i1 + 1].typ == CityItemToken.ItemType.NOUN): 
                typ2 = li[i1 + 1].value
            else: 
                del li[i1 + 1:i1 + 1+len(li) - i1 - 1]
        if (not li[0].morph.case_.is_undefined and li[0].morph.gender != MorphGender.UNDEFINED): 
            if (li[i1].end_token.morph.class0_.is_adjective and li[i1].begin_token == li[i1].end_token and li[i1].onto_item is None): 
                nam = ProperNameHelper.get_name_ex(li[i1].begin_token, li[i1].end_token, MorphClass.ADJECTIVE, li[0].morph.case_, li[0].morph.gender, False, False)
                if (li[i1].begin_token == li[i1].end_token and (isinstance(li[i1].begin_token, NumberToken))): 
                    nam = li[i1].value
                if (nam is not None and nam != name): 
                    if (name.endswith("ГО") or name.endswith("ОЙ")): 
                        alt_name = nam
                    else: 
                        if (li[i1].end_token.get_morph_class_in_dictionary().is_undefined): 
                            alt_name = name
                        name = nam
        if (typ == "НАСЕЛЕННЫЙ ПУНКТ" and name.endswith("КМ")): 
            ait = AddressItemToken.try_parse(li[1].begin_token, False, None, None)
            if (ait is not None and ait.typ == AddressItemType.STREET): 
                ss = Utils.asObjectOrNull(ait.referent, StreetReferent)
                ss.add_slot(StreetReferent.ATTR_NUMBER, None, True, 0)
                name = "{0} {1}".format(name, str(ss).upper())
                li[1].end_token = ait.end_token
        if (li[0].morph.case_.is_nominative and li[0].typ != CityItemToken.ItemType.MISC): 
            if (alt_name is not None): 
                city._add_name(alt_name)
            alt_name = (None)
        city._add_name(name)
        if (prob_adj is not None): 
            city._add_name(prob_adj + " " + name)
        if (alt_name is not None): 
            city._add_name(alt_name)
            if (prob_adj is not None): 
                city._add_name(prob_adj + " " + alt_name)
        if (typ is not None): 
            if ((typ == "ДЕРЕВНЯ" and not MiscLocationHelper.check_geo_object_before(li[0].begin_token, False) and li[0].begin_token.is_value("Д", None)) and li[1].onto_item is not None): 
                typ = "ГОРОД"
            city._add_typ(typ)
        elif (not city.is_city): 
            city._add_typ_city(li[0].kit.base_language, True)
        if (typ2 is not None): 
            city._add_typ(typ2.lower())
        if (li[0].higher_geo is not None and GeoOwnerHelper.can_be_higher(li[0].higher_geo, city, None, None)): 
            city.higher = li[0].higher_geo
        if (li[0].typ == CityItemToken.ItemType.MISC): 
            del li[0]
        if (i1 < len(li)): 
            city._add_misc(li[i1].misc)
            city._add_misc(li[i1].misc2)
        res = ReferentToken._new948(city, li[0].begin_token, li[len(li) - 1].end_token, mc)
        num = None
        if (res.end_token.next0_ is not None and res.end_token.next0_.is_hiphen and (isinstance(res.end_token.next0_.next0_, NumberToken))): 
            num = (Utils.asObjectOrNull(res.end_token.next0_.next0_, NumberToken))
        elif ((isinstance(res.end_token.next0_, NumberToken)) and (res.whitespaces_after_count < 3)): 
            if (AddressItemToken.check_street_after(res.end_token.next0_, False)): 
                pass
            else: 
                tt1 = res.end_token.next0_.next0_
                ok1 = False
                if (tt1 is None or tt1.is_newline_before): 
                    ok1 = True
                elif (AddressItemToken.check_street_after(tt1, False)): 
                    ok1 = True
                if (ok1): 
                    num = (Utils.asObjectOrNull(res.end_token.next0_, NumberToken))
        if ((num is not None and num.typ == NumberSpellingType.DIGIT and not num.morph.class0_.is_adjective) and num.int_value is not None and (num.int_value < 100)): 
            if (num.value == "77" and city.find_slot(GeoReferent.ATTR_NAME, "МОСКВА", True) is not None): 
                pass
            elif (num.value == "78" and city.find_slot(GeoReferent.ATTR_NAME, "САНКТ-ПЕТЕРБУРГ", True) is not None): 
                pass
            elif (city.find_slot(GeoReferent.ATTR_NAME, "СЕВАСТОПОЛЬ", True) is not None): 
                pass
            else: 
                for s in city.slots: 
                    if (s.type_name == GeoReferent.ATTR_NAME): 
                        city.upload_slot(s, "{0}-{1}".format(s.value, num.value))
                res.end_token = num
        if (li[0].begin_token == li[0].end_token and li[0].begin_token.is_value("ГОРОДОК", None)): 
            if (AddressItemToken.check_house_after(res.end_token.next0_, True, False)): 
                return None
        if (li[0].typ == CityItemToken.ItemType.NOUN and li[0].length_char == 1 and not (isinstance(li[1].begin_token, TextToken))): 
            return None
        if (city.find_slot(GeoReferent.ATTR_NAME, "МОСКВА", True) is not None): 
            if (res.end_token.is_value("СТОЛИЦА", None)): 
                tt = res.end_token.next0_
                if (tt is not None and (isinstance(tt.get_referent(), GeoReferent)) and tt.get_referent().alpha2 == "RU"): 
                    res.end_token = tt
                    tt = tt.next0_
                cits = CityItemToken.try_parse_list(tt, 3, None)
                if ((cits is not None and len(cits) == 1 and cits[0].typ == CityItemToken.ItemType.NOUN) and cits[0].value == "ГОРОД"): 
                    res.end_token = cits[0].end_token
        return res
    
    @staticmethod
    def __try_name_exist(li : typing.List['CityItemToken'], oi : 'IntOntologyItem', always : bool) -> 'ReferentToken':
        oi.value = (None)
        if (li is None or len(li) == 0): 
            return None
        if (li[0].typ == CityItemToken.ItemType.CITY): 
            pass
        elif (li[0].typ == CityItemToken.ItemType.PROPERNAME and len(li) == 1 and ((MiscLocationHelper.is_user_param_address(li[0]) or li[0].misc is not None))): 
            ttt = li[0].begin_token.previous
            while ttt is not None and ttt.is_comma:
                ttt = ttt.previous
            if (not (isinstance(ttt, ReferentToken))): 
                return None
            geo_ = Utils.asObjectOrNull(ttt.get_referent(), GeoReferent)
            if (geo_ is None): 
                return None
            if (not geo_.is_region and not geo_.is_state): 
                if (not geo_.is_city or li[0].value is None): 
                    return None
                if (geo_.find_slot("NAME", li[0].value, True) is None): 
                    return None
                if (geo_.find_slot("TYPE", "город", True) is not None): 
                    return None
                if (len(li) != 1): 
                    return None
                if (AddressItemToken.check_street_after(li[0].begin_token, False)): 
                    return None
                ngeo = GeoReferent()
                ngeo._add_name(li[0].value)
                ngeo._add_misc(li[0].misc)
                ngeo._add_typ("населенный пункт")
                return ReferentToken(ngeo, li[0].begin_token, li[0].end_token)
            else: 
                ait = AddressItemToken.try_parse_pure_item(li[0].begin_token, None, None)
                if (ait is not None and ait.end_char > li[0].end_char): 
                    return None
                if (AddressItemToken.check_street_after(li[0].begin_token, False)): 
                    return None
        else: 
            return None
        if (len(li) == 1 and (li[0].whitespaces_after_count < 3)): 
            tt1 = MiscLocationHelper.check_territory(li[0].end_token.next0_)
            if (tt1 is not None): 
                if (tt1.is_newline_after or tt1.next0_ is None or tt1.next0_.is_comma): 
                    return None
                if (AddressItemToken.check_house_after(tt1.next0_, False, False)): 
                    return None
                if (AddressItemToken.check_street_after(tt1.next0_, False)): 
                    return None
        oi.value = li[0].onto_item
        tt = Utils.asObjectOrNull(li[0].begin_token, TextToken)
        if (tt is None): 
            return None
        ok = False
        nam = (li[0].value if oi.value is None else oi.value.canonic_text)
        if (nam is None): 
            return None
        if (nam == "РИМ"): 
            if (tt.term == "РИМ"): 
                if ((isinstance(tt.next0_, TextToken)) and tt.next0_.get_morph_class_in_dictionary().is_proper_secname): 
                    pass
                else: 
                    ok = True
            elif (tt.previous is not None and tt.previous.is_value("В", None) and tt.term == "РИМЕ"): 
                ok = True
            elif (MiscLocationHelper.check_geo_object_before(tt, False)): 
                ok = True
        elif (oi.value is not None and oi.value.referent is not None and oi.value.owner.is_ext_ontology): 
            ok = True
        elif (LanguageHelper.ends_with_ex(nam, "ГРАД", "СК", "TOWN", None) or nam.startswith("SAN")): 
            ok = True
        elif (li[0].chars.is_latin_letter and li[0].begin_token.previous is not None and ((li[0].begin_token.previous.is_value("IN", None) or li[0].begin_token.previous.is_value("FROM", None)))): 
            ok = True
        else: 
            tt2 = li[0].end_token.next0_
            first_pass3965 = True
            while True:
                if first_pass3965: first_pass3965 = False
                else: tt2 = tt2.next0_
                if (not (tt2 is not None)): break
                if (tt2.is_newline_before): 
                    break
                if ((tt2.is_char_of(",(") or tt2.morph.class0_.is_preposition or tt2.morph.class0_.is_conjunction) or tt2.morph.class0_.is_misc): 
                    continue
                if ((isinstance(tt2.get_referent(), GeoReferent)) and tt2.chars.is_cyrillic_letter == li[0].chars.is_cyrillic_letter): 
                    ok = True
                break
            ok2 = False
            if (not ok): 
                tt2 = li[0].begin_token.previous
                first_pass3966 = True
                while True:
                    if first_pass3966: first_pass3966 = False
                    else: tt2 = tt2.previous
                    if (not (tt2 is not None)): break
                    if (tt2.is_newline_after): 
                        break
                    if ((tt2.is_char_of(",)") or tt2.morph.class0_.is_preposition or tt2.morph.class0_.is_conjunction) or tt2.morph.class0_.is_misc): 
                        continue
                    if ((isinstance(tt2.get_referent(), GeoReferent)) and tt2.chars.is_cyrillic_letter == li[0].chars.is_cyrillic_letter): 
                        ok2 = True
                        ok = ok2
                    if (ok): 
                        sits = StreetItemToken.try_parse_list(li[0].begin_token, 10, None)
                        if (sits is not None and len(sits) > 1): 
                            ss = StreetDefineHelper._try_parse_street(sits, False, False, False, None)
                            if (ss is not None): 
                                if ((len(sits) == 3 and sits[0].typ == StreetItemType.NAME and sits[1].typ == StreetItemType.NUMBER) and sits[2].typ == StreetItemType.NOUN): 
                                    ok = False
                                else: 
                                    del sits[0]
                                    if (StreetDefineHelper._try_parse_street(sits, False, False, False, None) is None): 
                                        ok = False
                    if (ok): 
                        if (len(li) > 1 and li[1].typ == CityItemToken.ItemType.PROPERNAME and (li[1].whitespaces_before_count < 3)): 
                            ok = False
                        elif (not ok2): 
                            mc = li[0].begin_token.get_morph_class_in_dictionary()
                            if (mc.is_proper_name or mc.is_proper_surname or mc.is_adjective): 
                                ok = False
                            else: 
                                npt = MiscLocationHelper._try_parse_npt(li[0].begin_token)
                                if (npt is not None and npt.end_char > li[0].end_char): 
                                    ok = False
                    if (OrgItemToken.try_parse(li[0].begin_token, None) is not None): 
                        ok = False
                        break
                    if (li[0].doubtful and not MiscLocationHelper.is_user_param_address(li[0])): 
                        rt1 = li[0].kit.process_referent("PERSON", li[0].begin_token, None)
                        if (rt1 is not None): 
                            return None
                    break
        if (always): 
            if (li[0].whitespaces_before_count > 3 and li[0].doubtful and li[0].begin_token.get_morph_class_in_dictionary().is_proper_surname): 
                pp = li[0].kit.process_referent("PERSON", li[0].begin_token, None)
                if (pp is not None): 
                    always = False
        if (li[0].begin_token.chars.is_latin_letter and li[0].begin_token == li[0].end_token): 
            tt1 = li[0].end_token.next0_
            if (tt1 is not None and tt1.is_char(',')): 
                tt1 = tt1.next0_
            if (((isinstance(tt1, TextToken)) and tt1.chars.is_latin_letter and (tt1.length_char < 3)) and not tt1.chars.is_all_lower): 
                ok = False
        if (not ok and not always): 
            if (oi.value is not None and MiscLocationHelper.is_user_param_address(li[0])): 
                if (not li[0].is_newline_before): 
                    t0 = li[0].begin_token.previous
                    if (t0 is not None and t0.is_hiphen): 
                        t0 = t0.previous
                    if (isinstance(t0, NumberToken)): 
                        return None
                    if (StreetItemToken.check_keyword(t0)): 
                        return None
            else: 
                return None
        city = None
        end_tok = None
        if (oi.value is not None and (isinstance(oi.value.referent, GeoReferent)) and not oi.value.owner.is_ext_ontology): 
            city = (Utils.asObjectOrNull(oi.value.referent.clone(), GeoReferent))
            city.occurrence.clear()
        else: 
            city = GeoReferent()
            if (oi.value is None and nam.startswith("П ")): 
                city._add_typ("поселок")
                city._add_typ("поселение")
                city._add_name(nam[2:])
            elif (oi.value is None and nam.endswith(" П")): 
                city._add_typ("поселок")
                city._add_typ("поселение")
                city._add_name(nam[0:0+len(nam) - 2])
            elif (oi.value is None and nam.startswith("С ")): 
                city._add_typ("село")
                city._add_typ("селение")
                city._add_name(nam[2:])
            elif (oi.value is None and nam.endswith(" С")): 
                city._add_typ("село")
                city._add_typ("селение")
                city._add_name(nam[0:0+len(nam) - 2])
            elif (oi.value is None and nam.startswith("Д ")): 
                city._add_typ("деревня")
                city._add_name(nam[2:])
            elif (oi.value is None and nam.endswith(" Д")): 
                city._add_typ("деревня")
                city._add_name(nam[0:0+len(nam) - 2])
            else: 
                city._add_name(nam)
                if (li[0].alt_value is not None): 
                    city._add_name(li[0].alt_value)
                if (oi.value is not None and (isinstance(oi.value.referent, GeoReferent))): 
                    city._merge_slots2(Utils.asObjectOrNull(oi.value.referent, GeoReferent), li[0].kit.base_language)
                if (not city.is_city and MiscLocationHelper.is_user_param_address(li[0])): 
                    tt1 = li[0].end_token.next0_
                    if (tt1 is not None and tt1.is_comma): 
                        tt1 = tt1.next0_
                    cits = CityItemToken.try_parse_list(tt1, 2, None)
                    if (cits is not None and len(cits) == 1 and cits[0].typ == CityItemToken.ItemType.NOUN): 
                        end_tok = cits[0].end_token
                        city._add_typ(cits[0].value.lower())
                if (not city.is_city): 
                    city._add_typ_city(li[0].kit.base_language, li[0].typ == CityItemToken.ItemType.CITY)
        city._add_misc(li[0].misc)
        city._add_misc(li[0].misc2)
        return ReferentToken._new948(city, li[0].begin_token, Utils.ifNotNull(end_tok, li[0].end_token), li[0].morph)
    
    @staticmethod
    def __try4(li : typing.List['CityItemToken']) -> 'ReferentToken':
        if ((len(li) == 1 and li[0].typ == CityItemToken.ItemType.NOUN and "ПОСЕЛЕНИЕ" in li[0].value) and (isinstance(li[0].end_token.next0_, ReferentToken))): 
            geo_ = Utils.asObjectOrNull(li[0].end_token.next0_.get_referent(), GeoReferent)
            if (geo_ is not None and "волость" in geo_.typs): 
                city = GeoReferent()
                nam = geo_.get_string_value(GeoReferent.ATTR_NAME)
                city._add_name(nam + " ВОЛОСТЬ")
                city._add_name(nam)
                city._add_typ(li[0].value.lower())
                return ReferentToken(city, li[0].begin_token, li[0].end_token.next0_)
        if ((len(li) == 2 and li[0].org_ref is not None and li[1].typ == CityItemToken.ItemType.NOUN) and MiscLocationHelper.is_user_param_address(li[0])): 
            geo_ = GeoReferent()
            geo_._add_typ(li[1].value)
            geo_._add_misc(li[1].misc)
            geo_._add_misc(li[1].misc2)
            geo_._add_org_referent(li[0].org_ref.referent)
            geo_.add_ext_referent(li[0].org_ref)
            return ReferentToken(geo_, li[0].begin_token, li[1].end_token)
        if ((len(li) > 0 and li[0].typ == CityItemToken.ItemType.NOUN and li[0].value != "ГОРОД") and li[0].value != "МІСТО" and li[0].value != "CITY"): 
            ok = False
            if (MiscLocationHelper.is_user_param_address(li[0])): 
                ok = True
            elif (not li[0].doubtful or li[0].geo_object_before or li[0].length_char > 2): 
                ok = True
            if (ok): 
                if (len(li) > 1 and li[1].org_ref is not None and (li[1].whitespaces_before_count < 3)): 
                    geo_ = GeoReferent()
                    geo_._add_typ(li[0].value)
                    geo_._add_misc(li[0].misc)
                    geo_._add_misc(li[0].misc2)
                    geo_._add_org_referent(li[1].org_ref.referent)
                    geo_.add_ext_referent(li[1].org_ref)
                    return ReferentToken(geo_, li[0].begin_token, li[1].end_token)
                elif (li[0].whitespaces_after_count < 3): 
                    org0_ = OrgItemToken.try_parse(li[0].end_token.next0_, None)
                    if (org0_ is not None): 
                        if (len(li) > 1 and OrgItemToken.try_parse(li[1].end_token.next0_, None) is not None): 
                            pass
                        else: 
                            geo_ = GeoReferent()
                            geo_._add_typ(li[0].value)
                            geo_._add_org_referent(org0_.referent)
                            geo_.add_ext_referent(org0_)
                            return ReferentToken(geo_, li[0].begin_token, org0_.end_token)
        if (len(li) == 1 and li[0].typ == CityItemToken.ItemType.NOUN and (li[0].whitespaces_after_count < 3)): 
            geo_ = li[0].end_token.next0_.get_referent()
            if (geo_ is not None and geo_.find_slot(GeoReferent.ATTR_TYPE, "волость", True) is not None and "ПОСЕЛЕНИЕ" in li[0].value): 
                city = GeoReferent()
                city._add_typ(li[0].value.lower())
                for n in geo_.get_string_values(GeoReferent.ATTR_NAME): 
                    city.add_slot(GeoReferent.ATTR_NAME, n, False, 0)
                city.add_slot(GeoReferent.ATTR_MISC, "волость", False, 0)
                return ReferentToken(city, li[0].begin_token, li[0].end_token.next0_)
        if ((len(li) >= 2 and li[0].geo_object_before and li[0].typ == CityItemToken.ItemType.PROPERNAME) and li[1].typ == CityItemToken.ItemType.PROPERNAME and MiscLocationHelper.is_user_param_address(li[0])): 
            tt = li[0].begin_token.previous
            if (tt is not None and tt.is_comma): 
                tt = tt.previous
            if (tt is not None and (isinstance(tt.get_referent(), GeoReferent)) and not tt.get_referent().is_city): 
                if (li[0].begin_token.is_value("РЕВОЛЮЦИЯ", None)): 
                    if (AddressItemToken.check_street_after(li[0].begin_token, False)): 
                        return None
                if (isinstance(li[0].begin_token, NumberToken)): 
                    return None
                if (StreetItemToken.check_keyword(li[0].begin_token)): 
                    pass
                else: 
                    aa = AddressItemToken.try_parse(li[1].begin_token, False, None, None)
                    if (aa is not None): 
                        city = GeoReferent()
                        city._add_typ("населенный пункт")
                        city._add_name(li[0].value)
                        if (li[0].alt_value is not None): 
                            city._add_name(li[0].alt_value)
                        return ReferentToken(city, li[0].begin_token, li[0].end_token)
        if ((len(li) == 3 and li[0].typ == CityItemToken.ItemType.PROPERNAME and li[1].typ == CityItemToken.ItemType.NOUN) and li[2].typ == CityItemToken.ItemType.NOUN): 
            npt = NounPhraseHelper.try_parse(li[0].begin_token, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None and npt.end_token == li[1].end_token): 
                city = GeoReferent()
                city._add_typ(li[2].value)
                city._add_name(MiscHelper.get_text_value_of_meta_token(npt, GetTextAttr.NO))
                return ReferentToken(city, li[0].begin_token, li[2].end_token)
        if ((len(li) == 1 and li[0].typ == CityItemToken.ItemType.PROPERNAME and li[0].org_ref is None) and li[0].geo_object_before and MiscLocationHelper.is_user_param_address(li[0])): 
            if (li[0].is_newline_after or li[0].end_token.next0_.is_comma): 
                has_city = False
                tt = li[0].begin_token.previous
                while tt is not None: 
                    g = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                    if (g is not None and g.is_city): 
                        has_city = True
                        break
                    tt = tt.previous
                if (not has_city): 
                    if (not li[0].is_newline_after and AddressItemToken.check_street_after(li[0].begin_token, False)): 
                        pass
                    else: 
                        city = GeoReferent()
                        city._add_typ("населенный пункт")
                        city._add_name(li[0].value)
                        return ReferentToken(city, li[0].begin_token, li[0].end_token)
        return None
    
    @staticmethod
    def check_year_after(tt : 'Token') -> bool:
        if (tt is not None and ((tt.is_comma or tt.is_hiphen))): 
            tt = tt.next0_
        if (tt is not None and tt.is_newline_after): 
            if ((isinstance(tt, NumberToken)) and tt.int_value is not None): 
                year = tt.int_value
                if (year > 1990 and (year < 2100)): 
                    return True
            elif (tt.get_referent() is not None and tt.get_referent().type_name == "DATE"): 
                return True
        return False
    
    @staticmethod
    def check_street_after(tt : 'Token') -> bool:
        if (tt is not None and ((tt.is_comma_and or tt.is_hiphen or tt.morph.class0_.is_preposition))): 
            tt = tt.next0_
        if (tt is None): 
            return False
        ait = AddressItemToken.try_parse(tt, False, None, None)
        if (ait is not None and ait.typ == AddressItemType.STREET): 
            return True
        return False
    
    @staticmethod
    def check_city_after(tt : 'Token') -> bool:
        while tt is not None and (((tt.is_comma_and or tt.is_hiphen or tt.morph.class0_.is_preposition) or tt.is_char('.'))):
            tt = tt.next0_
        if (tt is None): 
            return False
        cits = CityItemToken.try_parse_list(tt, 5, None)
        if (cits is None or len(cits) == 0): 
            if (tt.length_char == 1 and tt.chars.is_all_lower and ((tt.is_value("Д", None) or tt.is_value("П", None)))): 
                tt1 = tt.next0_
                if (tt1 is not None and tt1.is_char('.')): 
                    tt1 = tt1.next0_
                ci = CityItemToken.try_parse(tt1, None, False, None)
                if (ci is not None and ((ci.typ == CityItemToken.ItemType.PROPERNAME or ci.typ == CityItemToken.ItemType.CITY))): 
                    return True
            return False
        if (CityAttachHelper.try_define(cits, None, False) is not None): 
            return True
        if (cits[0].typ == CityItemToken.ItemType.NOUN): 
            if (tt.previous is not None and tt.previous.is_comma): 
                return True
            if (len(cits) > 1 and ((cits[1].typ == CityItemToken.ItemType.CITY or cits[1].typ == CityItemToken.ItemType.PROPERNAME))): 
                return True
        return False