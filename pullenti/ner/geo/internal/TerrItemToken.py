# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
import xml.etree
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import MemoryStream
from pullenti.unisharp.Streams import Stream

from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.morph.MorphWordForm import MorphWordForm
from pullenti.ner.geo.internal.TerrTermin import TerrTermin
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.IntOntologyCollection import IntOntologyCollection
from pullenti.ner.address.internal.PullentiNerAddressInternalResourceHelper import PullentiNerAddressInternalResourceHelper
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.ner.Referent import Referent
from pullenti.ner.geo.internal.GeoAnalyzerData import GeoAnalyzerData
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.MorphCollection import MorphCollection
from pullenti.ner.Token import Token
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken

class TerrItemToken(MetaToken):
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.onto_item = None;
        self.onto_item2 = None;
        self.termin_item = None;
        self.termin_item2 = None;
        self.is_adjective = False
        self.is_district_name = False
        self.adjective_ref = None;
        self.named_by = None;
        self.real_name = None;
        self.can_be_city = False
        self.can_be_surname = False
        self.is_adj_in_dictionary = False
        self.is_geo_in_dictionary = False
        self.is_doubt = False
        self.additional_typ = None;
    
    @property
    def is_city_region(self) -> bool:
        if (self.termin_item is None): 
            return False
        return ("ГОРОДС" in self.termin_item.canonic_text or "МІСЬК" in self.termin_item.canonic_text or "МУНИЦИПАЛ" in self.termin_item.canonic_text) or "МУНІЦИПАЛ" in self.termin_item.canonic_text or self.termin_item.canonic_text == "ПОЧТОВОЕ ОТДЕЛЕНИЕ"
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.onto_item is not None): 
            print("{0} ".format(self.onto_item.canonic_text), end="", file=res, flush=True)
        elif (self.termin_item is not None): 
            print("{0} ".format(self.termin_item.canonic_text), end="", file=res, flush=True)
        else: 
            print("{0} ".format(super().__str__()), end="", file=res, flush=True)
        if (self.adjective_ref is not None): 
            print(" (Adj: {0})".format(str(self.adjective_ref.referent)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res).strip()
    
    SPEED_REGIME = False
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        if (not TerrItemToken.SPEED_REGIME): 
            return
        ad = GeoAnalyzer._get_data(t0)
        if (ad is None): 
            return
        ad.tregime = False
        t = t0
        while t is not None: 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            ter = TerrItemToken.try_parse(t, None, ad)
            if (ter is not None): 
                if (d is None): 
                    d = GeoTokenData(t)
                d.terr = ter
            t = t.next0_
        t = t0
        first_pass3993 = True
        while True:
            if first_pass3993: first_pass3993 = False
            else: t = t.next0_
            if (not (t is not None)): break
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            if (d is None or d.terr is None or ((d.terr.termin_item is None and d.terr.onto_item is None))): 
                continue
            tt = d.terr.end_token.next0_
            if (tt is None): 
                continue
            dd = Utils.asObjectOrNull(tt.tag, GeoTokenData)
            ter = TerrItemToken.try_parse(tt, d.terr, ad)
            if (ter is None): 
                continue
            if (dd is None): 
                dd = GeoTokenData(tt)
            if (dd.terr is None or (dd.terr.end_char < ter.end_char)): 
                dd.terr = ter
        ad.tregime = True
    
    @staticmethod
    def try_parse(t : 'Token', prev : 'TerrItemToken'=None, ad : 'GeoAnalyzerData'=None) -> 'TerrItemToken':
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        if (t is None): 
            return None
        if (ad is None): 
            ad = (Utils.asObjectOrNull(GeoAnalyzer._get_data(t), GeoAnalyzerData))
        if (ad is None): 
            return None
        d = Utils.asObjectOrNull(t.tag, GeoTokenData)
        if (d is not None and d.no_geo): 
            return None
        if (TerrItemToken.SPEED_REGIME and ((ad.tregime or ad.all_regime)) and ((t.length_char != 2 or not t.chars.is_all_upper))): 
            if (d is not None): 
                return d.terr
            if (t.tag is None): 
                return None
        if (ad.tlevel > 1): 
            return None
        ad.tlevel += 1
        res = TerrItemToken.__try_parse(t, prev, False)
        ad.tlevel -= 1
        if (res is None): 
            if (t.is_value("ОБ", None) and MiscLocationHelper.is_user_param_address(t)): 
                res = TerrItemToken._new1748(t, t, TerrItemToken.__m_obl)
                if (t.next0_ is not None and t.next0_.is_char('.')): 
                    res.end_token = t.next0_
                return res
            if (t.chars.is_all_upper and t.length_char == 2 and (isinstance(t, TextToken))): 
                term = t.term
                if (((term == "РБ" or term == "РК" or term == "TC") or term == "ТС" or term == "РТ") or term == "УР" or term == "РД"): 
                    if ((term == "РБ" and (isinstance(t.previous, TextToken)) and (t.whitespaces_before_count < 3)) and not t.previous.chars.is_all_lower and t.previous.morph.class0_.is_adjective): 
                        return None
                    for it in ad.local_ontology.items: 
                        if (isinstance(it.referent, GeoReferent)): 
                            alph2 = it.referent.alpha2
                            if (((alph2 == "BY" and term == "РБ")) or ((alph2 == "KZ" and term == "РК"))): 
                                return TerrItemToken._new1749(t, t, it)
                            if (term == "РТ"): 
                                if (it.referent.find_slot(None, "ТАТАРСТАН", True) is not None): 
                                    return TerrItemToken._new1749(t, t, it)
                            if (term == "РД"): 
                                if (it.referent.find_slot(None, "ДАГЕСТАН", True) is not None): 
                                    return TerrItemToken._new1749(t, t, it)
                            if (term == "РБ"): 
                                if (it.referent.find_slot(None, "БАШКИРИЯ", True) is not None): 
                                    return TerrItemToken._new1749(t, t, it)
                    ok = False
                    if ((t.whitespaces_before_count < 2) and (isinstance(t.previous, TextToken))): 
                        term2 = t.previous.term
                        if ((t.previous.is_value("КОДЕКС", None) or t.previous.is_value("ЗАКОН", None) or term2 == "КОАП") or term2 == "ПДД" or term2 == "МЮ"): 
                            ok = True
                        elif ((t.previous.chars.is_all_upper and t.previous.length_char > 1 and (t.previous.length_char < 4)) and term2.endswith("К")): 
                            ok = True
                        elif (term == "РТ" or term == "УР" or term == "РД"): 
                            tt = t.previous
                            if (tt is not None and tt.is_comma): 
                                tt = tt.previous
                            if (tt is not None): 
                                if ((isinstance(tt.get_referent(), GeoReferent)) and tt.get_referent().alpha2 == "RU"): 
                                    ok = True
                                elif ((isinstance(tt, NumberToken)) and tt.length_char == 6 and tt.typ == NumberSpellingType.DIGIT): 
                                    ok = True
                            if (not ok and t.next0_ is not None): 
                                tt = t.next0_
                                if (tt.is_comma): 
                                    tt = tt.next0_
                                if (tt is not None): 
                                    if ((isinstance(tt.get_referent(), GeoReferent)) and tt.get_referent().alpha2 == "RU"): 
                                        ok = True
                                    elif ((isinstance(tt, NumberToken)) and tt.length_char == 6 and tt.typ == NumberSpellingType.DIGIT): 
                                        ok = True
                        if (not ok): 
                            if (t.next0_ is not None and t.next0_.is_hiphen): 
                                pass
                            elif (AddressItemToken.try_parse_pure_item(t.next0_, None, None) is not None): 
                                pass
                            else: 
                                cou = 0
                                tt = t.previous
                                while tt is not None and (cou < 4): 
                                    org0_ = OrgItemToken.try_parse(tt, None)
                                    if (org0_ is not None): 
                                        ok = True
                                        break
                                    kk = tt.kit.process_referent("PERSONPROPERTY", tt, None)
                                    if (kk is not None): 
                                        ok = True
                                        break
                                    tt = tt.previous; cou += 1
                    elif (((t.whitespaces_before_count < 2) and (isinstance(t.previous, NumberToken)) and t.previous.length_char == 6) and t.previous.typ == NumberSpellingType.DIGIT): 
                        ok = True
                    if (ok): 
                        if (term == "РК" and TerrItemToken.__m_kazahstan is not None): 
                            return TerrItemToken._new1749(t, t, TerrItemToken.__m_kazahstan)
                        if (term == "РТ" and TerrItemToken.__m_tatarstan is not None): 
                            return TerrItemToken._new1749(t, t, TerrItemToken.__m_tatarstan)
                        if (term == "РД" and TerrItemToken.__m_dagestan is not None): 
                            return TerrItemToken._new1749(t, t, TerrItemToken.__m_dagestan)
                        if (term == "УР" and TerrItemToken.__m_udmurtia is not None): 
                            return TerrItemToken._new1749(t, t, TerrItemToken.__m_udmurtia)
                        if (term == "РБ" and TerrItemToken.__m_belorussia is not None and ad.step > 0): 
                            return TerrItemToken._new1749(t, t, TerrItemToken.__m_belorussia)
                        if (((term == "ТС" or term == "TC")) and TerrItemToken.__m_tamog_sous is not None): 
                            return TerrItemToken._new1749(t, t, TerrItemToken.__m_tamog_sous)
            if (((isinstance(t, TextToken)) and ((t.is_value("Р", None) or t.is_value("P", None))) and t.next0_ is not None) and t.next0_.is_char('.') and not t.next0_.is_newline_after): 
                res = TerrItemToken.try_parse(t.next0_.next0_, None, ad)
                if (res is not None and res.onto_item is not None): 
                    str0_ = str(res.onto_item).upper()
                    if ("РЕСПУБЛИКА" in str0_): 
                        res.begin_token = t
                        res.is_doubt = False
                        return res
                if (MiscLocationHelper.is_user_param_address(t)): 
                    tt = t.next0_.next0_
                    if ((isinstance(tt, TextToken)) and tt.term.endswith("Й") and (tt.whitespaces_before_count < 3)): 
                        return TerrItemToken._new1748(t, t.next0_, TerrItemToken.__m_raion)
            if (t.is_char('(') and MiscLocationHelper.is_user_param_address(t) and t.next0_ is not None): 
                next0__ = TerrItemToken.try_parse(t.next0_, prev, ad)
                if ((next0__ is not None and next0__.termin_item is not None and next0__.end_token.next0_ is not None) and next0__.end_token.next0_.is_char(')')): 
                    next0__.begin_token = t
                    next0__.end_token = next0__.end_token.next0_
                    res = next0__
                elif (((t.next0_.is_value("Р", None) or t.next0_.is_value("P", None))) and t.next0_.next0_ is not None and t.next0_.next0_.is_char(')')): 
                    res = TerrItemToken._new1748(t, t.next0_.next0_, TerrItemToken.__m_raion)
            if (res is None): 
                return TerrItemToken.__try_parse_district_name(t, 0, prev)
        if ((res.begin_token.length_char == 1 and res.begin_token.chars.is_all_upper and res.begin_token.next0_ is not None) and res.begin_token.next0_.is_char('.')): 
            if ((prev is not None and prev.onto_item is not None and not prev.onto_item.referent.is_state) and res.termin_item is not None): 
                pass
            else: 
                return None
        if ((res.end_token.next0_ is not None and res.end_token.next0_.is_char('.') and res.end_token.next0_.next0_ is not None) and res.end_token.next0_.next0_.is_comma): 
            res.end_token = res.end_token.next0_
        if (res.termin_item is not None and res.termin_item.canonic_text == "ОКРУГ"): 
            if (t.previous is not None and ((t.previous.is_value("ГОРОДСКОЙ", None) or t.previous.is_value("МІСЬКИЙ", None)))): 
                return None
        tt = res.end_token.next0_
        while tt is not None: 
            if (tt.whitespaces_before_count > 3): 
                break
            if (tt.is_value("ЭВЕНКИЙСКИЙ", None) or tt.is_value("НАЦИОНАЛЬНЫЙ", None)): 
                res2 = TerrItemToken.__try_parse(tt, None, False)
                if (res2 is not None and res2.termin_item is not None): 
                    break
                if (res.real_name is None): 
                    res.real_name = MetaToken(res.begin_token, res.end_token)
                res.end_token = tt
            else: 
                break
            tt = tt.next0_
        if (res.termin_item is not None and (("МУНИЦИПАЛ" in res.termin_item.canonic_text or "ГОРОДСК" in res.termin_item.canonic_text)) and (res.whitespaces_after_count < 3)): 
            li = CityItemToken.try_parse_list(res.end_token.next0_, 3, ad)
            if ((li is not None and len(li) == 2 and li[0].typ == CityItemToken.ItemType.NOUN) and li[0].value == "ГОРОД"): 
                if (li[1].end_token.is_newline_after or li[1].end_token.next0_.is_comma): 
                    res.end_token = li[0].end_token
        if (res.termin_item is None and res.onto_item is None): 
            if (MiscLocationHelper.check_territory(res.begin_token) is not None): 
                return None
        if (res.onto_item is not None): 
            cit1 = CityItemToken.check_onto_item(res.begin_token)
            if (cit1 is not None and cit1.item.misc_attr is not None): 
                if (cit1.end_token.is_value("CITY", None)): 
                    return None
                if (cit1.end_token == res.end_token): 
                    res.can_be_city = True
                    if (cit1.end_token.next0_ is not None and cit1.end_token.next0_.is_value("CITY", None)): 
                        return None
            cit = CityItemToken.try_parse_back(res.begin_token.previous, True)
            if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN and ((res.is_adjective or (cit.whitespaces_after_count < 1)))): 
                res.can_be_city = True
        if (res.termin_item is not None): 
            if (((res.termin_item.canonic_text == "МУНИЦИПАЛЬНЫЙ ОКРУГ" or res.termin_item.canonic_text == "ГОРОДСКОЙ ОКРУГ")) and (res.whitespaces_after_count < 3)): 
                next0 = TerrItemToken.try_parse(res.end_token.next0_, None, None)
                if (next0 is not None and next0.termin_item is not None and next0.termin_item.acronym == "ЗАТО"): 
                    res.end_token = next0.end_token
                    res.termin_item2 = next0.termin_item
                next0__ = CityItemToken.check_keyword(res.end_token.next0_)
                if (next0__ is not None): 
                    res.end_token = next0__.end_token
                    res.additional_typ = next0__.termin.canonic_text
            res.is_doubt = res.termin_item.is_doubt
            if (not res.termin_item.is_region): 
                if (res.termin_item.is_moscow_region and res.begin_token == res.end_token): 
                    res.is_doubt = True
                elif (res.termin_item.acronym == "МО" and res.begin_token == res.end_token and res.length_char == 2): 
                    if (res.begin_token.previous is not None and res.begin_token.previous.is_value("ВЕТЕРАН", None)): 
                        return None
                    res.is_doubt = True
                    if (res.begin_token == res.end_token and res.length_char == 2): 
                        if (res.begin_token.previous is None or res.begin_token.previous.is_char_of(",") or res.begin_token.is_newline_before): 
                            if (res.end_token.next0_ is None or res.end_token.next0_.is_char_of(",") or res.is_newline_after): 
                                res.termin_item = (None)
                                res.onto_item = TerrItemToken.__m_mos_regru
                        tt = res.end_token.next0_
                        if (tt is not None and tt.is_comma): 
                            tt = tt.next0_
                        cit = CityItemToken.try_parse(tt, None, False, None)
                        is_reg = False
                        if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN): 
                            is_reg = True
                        else: 
                            tt = t.previous
                            if (tt is not None and tt.is_comma): 
                                tt = tt.previous
                            cit = CityItemToken.try_parse_back(tt, False)
                            if (cit is not None and cit.typ == CityItemToken.ItemType.CITY): 
                                is_reg = True
                            elif (cit is not None and cit.typ == CityItemToken.ItemType.PROPERNAME): 
                                cit = CityItemToken.try_parse_back(cit.begin_token.previous, True)
                                if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN): 
                                    is_reg = True
                        if (is_reg): 
                            res.termin_item = (None)
                            res.is_doubt = False
                            res.onto_item = TerrItemToken.__m_mos_regru
                elif (res.termin_item.acronym == "ЛО" and res.begin_token == res.end_token and res.length_char == 2): 
                    res.is_doubt = True
                    if (res.begin_token.previous is None or res.begin_token.previous.is_comma_and or res.begin_token.is_newline_before): 
                        res.termin_item = (None)
                        res.onto_item = TerrItemToken.__m_len_regru
                    else: 
                        tt = res.end_token.next0_
                        if (tt is not None and tt.is_comma): 
                            tt = tt.next0_
                        cit = CityItemToken.try_parse(tt, None, False, None)
                        if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN): 
                            res.termin_item = (None)
                            res.onto_item = TerrItemToken.__m_len_regru
                elif (not res.morph.case_.is_nominative and not res.morph.case_.is_accusative): 
                    res.is_doubt = True
                elif (res.morph.number != MorphNumber.SINGULAR): 
                    if (res.termin_item.is_moscow_region and res.morph.number != MorphNumber.PLURAL): 
                        pass
                    else: 
                        res.is_doubt = True
            if (((res.termin_item is not None and res.termin_item.canonic_text == "АО")) or ((res.onto_item == TerrItemToken.__m_mos_regru and res.length_char == 2 and res.is_doubt))): 
                tt = res.end_token.next0_
                rt = res.kit.process_referent("ORGANIZATION", res.begin_token, None)
                if (rt is None): 
                    rt = res.kit.process_referent("ORGANIZATION", res.begin_token.next0_, None)
                if (rt is not None): 
                    for s in rt.referent.slots: 
                        if (s.type_name == "TYPE"): 
                            ty = s.value
                            if (res.termin_item is not None and ty != res.termin_item.canonic_text): 
                                return None
        if (res is not None and res.begin_token == res.end_token and res.termin_item is None): 
            if (isinstance(t, TextToken)): 
                str0_ = t.term
                if (str0_ == "ЧАДОВ" or str0_ == "ТОГОВ"): 
                    return None
            if ((((isinstance(t.next0_, TextToken)) and (t.whitespaces_after_count < 2) and not t.next0_.chars.is_all_lower) and t.chars.equals(t.next0_.chars) and not t.chars.is_latin_letter) and ((not t.morph.case_.is_genitive and not t.morph.case_.is_accusative))): 
                mc = t.next0_.get_morph_class_in_dictionary()
                if (mc.is_proper_surname or mc.is_proper_secname): 
                    res.is_doubt = True
            if ((isinstance(t.previous, TextToken)) and (t.whitespaces_before_count < 2) and not t.previous.chars.is_all_lower): 
                mc = t.previous.get_morph_class_in_dictionary()
                if (mc.is_proper_surname): 
                    if (t.get_morph_class_in_dictionary().is_proper_name): 
                        res.is_doubt = True
                    elif (t.next0_ is not None and t.next0_.get_morph_class_in_dictionary().is_proper_secname): 
                        res.is_doubt = True
            if ((t.length_char <= 2 and res.onto_item is not None and not t.is_value("РФ", None)) and not t.is_value("МО", None)): 
                res.is_doubt = True
                tt = t.next0_
                if (tt is not None and ((tt.is_char_of(":") or tt.is_hiphen))): 
                    tt = tt.next0_
                if (tt is not None and tt.get_referent() is not None and tt.get_referent().type_name == "PHONE"): 
                    res.is_doubt = False
                elif (t.length_char == 2 and t.chars.is_all_upper and t.chars.is_latin_letter): 
                    res.is_doubt = False
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', prev : 'TerrItemToken', ignore_onto : bool=False) -> 'TerrItemToken':
        from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        if (not (isinstance(t, TextToken))): 
            return None
        li = None
        if (not ignore_onto): 
            if (t.kit.ontology is not None): 
                li = t.kit.ontology.attach_token(GeoReferent.OBJ_TYPENAME, t)
            if (li is None or len(li) == 0): 
                li = TerrItemToken._m_terr_ontology.try_attach(t, None, False)
            else: 
                li1 = TerrItemToken._m_terr_ontology.try_attach(t, None, False)
                if (li1 is not None and len(li1) > 0): 
                    if (li1[0].length_char > li[0].length_char): 
                        li = li1
        tt = Utils.asObjectOrNull(t, TextToken)
        if (li is not None): 
            for i in range(len(li) - 1, -1, -1):
                if (li[i].item is not None): 
                    g = Utils.asObjectOrNull(li[i].item.referent, GeoReferent)
                    if (g is None): 
                        continue
                    if (g.is_city and not g.is_region and not g.is_state): 
                        del li[i]
                    elif (g.is_state and t.length_char == 2 and li[i].length_char == 2): 
                        if (not t.is_whitespace_before and t.previous is not None and t.previous.is_char('.')): 
                            del li[i]
                        elif (t.previous is not None and t.previous.is_value("ДОМЕН", None)): 
                            del li[i]
                    elif (g.is_state and li[i].begin_token.is_value("ЛЮКСЕМБУРГ", None)): 
                        if (MiscLocationHelper.is_user_param_address(li[i])): 
                            del li[i]
                        elif (li[i].begin_token.previous is not None and li[i].begin_token.previous.is_value("РОЗА", None)): 
                            del li[i]
                    elif (li[i].begin_token.is_value("КАТАР", None) or li[i].begin_token.is_value("КРЫМ", None) or li[i].begin_token.is_value("КУБА", None)): 
                        ttt = li[i].begin_token
                        if (ttt.next0_ is not None and ttt.next0_.is_hiphen): 
                            del li[i]
                        elif (ttt.previous is not None and ttt.previous.is_hiphen): 
                            del li[i]
                        elif (MiscLocationHelper.is_user_param_address(ttt)): 
                            is_loc = False
                            cits = CityItemToken.try_parse_list(ttt.next0_, 3, None)
                            if (cits is not None and len(cits) == 1 and cits[0].typ == CityItemToken.ItemType.NOUN): 
                                is_loc = True
                            else: 
                                tt2 = ttt.previous
                                while tt2 is not None and (tt2.end_char + 20) > ttt.begin_char: 
                                    cit = CityItemToken.try_parse(tt2, None, False, None)
                                    if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN and cit.end_token.next0_ == ttt): 
                                        is_loc = True
                                        break
                                    tt2 = tt2.previous
                            if (is_loc): 
                                del li[i]
            for nt in li: 
                if (nt.item is not None and not (isinstance(nt.termin.tag, IntOntologyItem))): 
                    if (not MiscHelper.is_all_characters_lower(nt.begin_token, nt.end_token, False) or nt.begin_token != nt.end_token or MiscLocationHelper.is_user_param_address(nt)): 
                        res0 = TerrItemToken._new1761(nt.begin_token, nt.end_token, nt.item, nt.morph)
                        if (nt.end_token.morph.class0_.is_adjective and nt.begin_token == nt.end_token): 
                            if (nt.begin_token.get_morph_class_in_dictionary().is_proper_geo): 
                                pass
                            else: 
                                res0.is_adjective = True
                        npt2 = NounPhraseHelper.try_parse(nt.begin_token, NounPhraseParseAttr.NO, 0, None)
                        if (npt2 is not None and npt2.end_char >= nt.end_char): 
                            res0.morph = npt2.morph
                        if (nt.begin_token == nt.end_token and nt.chars.is_latin_letter): 
                            if (nt.item.referent.is_state): 
                                pass
                            elif (nt.item.referent.find_slot(GeoReferent.ATTR_TYPE, "state", True) is not None): 
                                pass
                            else: 
                                res0.is_doubt = True
                        if (nt.begin_token == nt.end_token): 
                            for wf in nt.begin_token.morph.items: 
                                f = Utils.asObjectOrNull(wf, MorphWordForm)
                                if (not f.is_in_dictionary): 
                                    continue
                                if (((wf.class0_.is_proper_surname or wf.class0_.is_proper_name)) and f.is_in_dictionary): 
                                    res0.can_be_surname = True
                        if ((len(li) == 2 and nt == li[0] and li[1].item is not None) and not (isinstance(li[1].termin.tag, IntOntologyItem))): 
                            res0.onto_item2 = li[1].item
                        return res0
            for nt in li: 
                if (nt.item is not None and (isinstance(nt.termin.tag, IntOntologyItem))): 
                    if (nt.end_token.next0_ is None or not nt.end_token.next0_.is_hiphen): 
                        res1 = TerrItemToken._new1762(nt.begin_token, nt.end_token, nt.item, True, nt.morph)
                        if ((len(li) == 2 and nt == li[0] and li[1].item is not None) and (isinstance(li[1].termin.tag, IntOntologyItem))): 
                            res1.onto_item2 = li[1].item
                        if (t.kit.base_language.is_ua and res1.onto_item.canonic_text == "СУДАН" and t.is_value("СУД", None)): 
                            return None
                        if (res1.onto_item.canonic_text == "ЭВЕНКИЙСКИЙ"): 
                            tt2 = res1.end_token.next0_
                            if (tt2 is not None and tt2.is_value("НАЦИОНАЛЬНЫЙ", None)): 
                                tt2 = tt2.next0_
                            next0__ = TerrItemToken.__try_parse(tt2, None, False)
                            if (next0__ is not None and next0__.termin_item is not None and "РАЙОН" in next0__.termin_item.canonic_text): 
                                next0__.begin_token = t
                                return next0__
                        return res1
            for nt in li: 
                if (nt.termin is not None and nt.item is None): 
                    if (nt.end_token.next0_ is None or not nt.end_token.next0_.is_hiphen or not nt.termin.is_adjective): 
                        res1 = TerrItemToken._new1763(nt.begin_token, nt.end_token, Utils.asObjectOrNull(nt.termin, TerrTermin), nt.termin.is_adjective, nt.morph)
                        if (not res1.is_adjective): 
                            if (res1.termin_item.canonic_text == "РАЙОН"): 
                                if (t.previous is not None): 
                                    ttt = t.previous
                                    if (ttt.is_char_of("\\/.") and ttt.previous is not None): 
                                        ttt = ttt.previous
                                    si = StreetItemToken.try_parse(ttt, None, False, None)
                                    if (si is not None and si.typ == StreetItemType.NOUN and si.end_token == nt.end_token): 
                                        return None
                                    if (si is not None and si._org0_ is not None and si.end_char > nt.end_char): 
                                        return None
                                if (not res1.begin_token.is_value(res1.termin_item.canonic_text, None)): 
                                    if (res1.end_token.next0_ is not None and res1.end_token.next0_.is_char('.')): 
                                        res1.end_token = res1.end_token.next0_
                            if (res1.termin_item.canonic_text == "РЕСПУБЛИКА" or res1.termin_item.canonic_text == "ШТАТ"): 
                                npt1 = MiscLocationHelper._try_parse_npt(res1.begin_token.previous)
                                if (npt1 is not None and npt1.morph.number == MorphNumber.PLURAL): 
                                    res2 = TerrItemToken.try_parse(res1.end_token.next0_, None, None)
                                    if ((res2 is not None and res2.onto_item is not None and res2.onto_item.referent is not None) and res2.onto_item.referent.find_slot(GeoReferent.ATTR_TYPE, "республика", True) is not None): 
                                        pass
                                    else: 
                                        return None
                            if (res1.termin_item.canonic_text == "КРАЙ" and res1.begin_token.is_value("КР", None)): 
                                if (res1.begin_token.chars.is_capital_upper): 
                                    return None
                            if (res1.termin_item.canonic_text == "ВНУТРИГОРОДСКАЯ ТЕРРИТОРИЯ"): 
                                next0__ = TerrItemToken.try_parse(res1.end_token.next0_, None, None)
                                if (next0__ is not None and next0__.termin_item is not None and next0__.termin_item.canonic_text == "МУНИЦИПАЛЬНЫЙ ОКРУГ"): 
                                    next0__.begin_token = res1.begin_token
                                    res1 = next0__
                            if (res1.termin_item.canonic_text == "ГОСУДАРСТВО"): 
                                if (t.previous is not None and t.previous.is_value("СОЮЗНЫЙ", None)): 
                                    return None
                            if (nt.begin_token == nt.end_token and ((nt.begin_token.is_value("ОПС", None) or nt.begin_token.is_value("ЗАО", None)))): 
                                if (not MiscLocationHelper.check_geo_object_before(nt.begin_token, False)): 
                                    return None
                            if (nt.begin_token.length_char == 1 and nt.begin_token != nt.end_token and nt.begin_token.next0_.is_char('.')): 
                                if (nt.kit.base_language.is_en): 
                                    return None
                        return res1
        if (tt is None): 
            return None
        if (not tt.chars.is_capital_upper and not tt.chars.is_all_upper): 
            if (tt.is_value("ИМЕНИ", None) or tt.is_value("ИМ", None)): 
                pass
            else: 
                if (not MiscLocationHelper.is_user_param_address(tt)): 
                    return None
                if (tt.length_char < 7): 
                    return None
        if (((tt.length_char == 2 or tt.length_char == 3)) and tt.chars.is_all_upper): 
            if (tt.term in TerrItemToken._m_alpha2state): 
                ok = False
                tt2 = tt.next0_
                if (tt2 is not None and tt2.is_char(':')): 
                    tt2 = tt2.next0_
                if (isinstance(tt2, ReferentToken)): 
                    r = tt2.get_referent()
                    if (r is not None and r.type_name == "PHONE"): 
                        ok = True
                if (ok): 
                    return TerrItemToken._new1749(tt, tt, TerrItemToken._m_alpha2state[tt.term])
        if (isinstance(tt, TextToken)): 
            if (tt.term == "ИМ" or tt.term == "ИМЕНИ"): 
                str0_ = StreetItemToken.try_parse(tt, None, False, None)
                if (str0_ is not None and str0_.typ == StreetItemType.NAME and TerrItemToken._m_terr_ontology.try_attach(tt.next0_, None, False) is None): 
                    return TerrItemToken._new1765(tt, str0_.end_token, str0_)
        if (tt.length_char < 3): 
            return None
        if (MiscHelper.is_eng_article(tt)): 
            return None
        if (tt.length_char < 5): 
            if (tt.next0_ is None): 
                return None
            if (tt.next0_.is_value("ГОРОДСКОЙ", None)): 
                pass
            elif (not tt.next0_.is_hiphen): 
                return None
        t0 = tt
        prefix = None
        if (t0.next0_ is not None and t0.next0_.is_hiphen and (isinstance(t0.next0_.next0_, TextToken))): 
            tt = (Utils.asObjectOrNull(t0.next0_.next0_, TextToken))
            if (not tt.chars.is_all_lower and ((t0.is_whitespace_after or t0.next0_.is_whitespace_after))): 
                tit = TerrItemToken.__try_parse(tt, prev, False)
                if (tit is not None): 
                    if (tit.onto_item is not None): 
                        return None
            if (tt.length_char > 1): 
                if (tt.chars.is_capital_upper): 
                    prefix = t0.term
                elif (not tt.is_whitespace_before and not t0.is_whitespace_after): 
                    prefix = t0.term
                if (((not tt.is_whitespace_after and tt.next0_ is not None and tt.next0_.is_hiphen) and not tt.next0_.is_whitespace_after and (isinstance(tt.next0_.next0_, TextToken))) and tt.next0_.next0_.chars.equals(t0.chars)): 
                    prefix = "{0}-{1}".format(prefix, tt.term)
                    tt = (Utils.asObjectOrNull(tt.next0_.next0_, TextToken))
            if (prefix is None): 
                tt = t0
        if (tt.morph.class0_.is_adverb): 
            return None
        if (CityItemToken.check_keyword(t0) is not None): 
            return None
        if (not tt.morph.class0_.is_adjective): 
            oii = CityItemToken.check_onto_item(t0)
            if (oii is not None): 
                if ((prev is not None and prev.termin_item is not None and "МУНИЦИПАЛ" in prev.termin_item.canonic_text) and MiscLocationHelper.is_user_param_address(t0)): 
                    pass
                elif (oii.end_token.next0_ is not None and oii.end_token.next0_.is_value("ГОРОДСКОЙ", None)): 
                    pass
                else: 
                    return None
        npt = MiscLocationHelper._try_parse_npt(t0)
        if (npt is not None): 
            if (((npt.noun.is_value("ФЕДЕРАЦИЯ", None) or npt.noun.is_value("ФЕДЕРАЦІЯ", None))) and len(npt.adjectives) == 1): 
                if (MiscHelper.is_not_more_than_one_error("РОССИЙСКАЯ", npt.adjectives[0]) or MiscHelper.is_not_more_than_one_error("РОСІЙСЬКА", npt.adjectives[0])): 
                    return TerrItemToken._new1761(npt.begin_token, npt.end_token, (TerrItemToken.__m_russiaua if t0.kit.base_language.is_ua else TerrItemToken.__m_russiaru), npt.morph)
        if (t0.morph.class0_.is_proper_name): 
            if (t0.is_whitespace_after or t0.next0_.is_whitespace_after): 
                return None
        if (not t0.chars.is_all_lower): 
            tok2 = TerrItemToken.__m_spec_names.try_parse(t0, TerminParseAttr.NO)
            if (tok2 is not None): 
                return TerrItemToken._new1767(t0, tok2.end_token, True)
        if (npt is not None and npt.end_token != npt.begin_token): 
            if (npt.end_token.is_value("КИЛОМЕТР", None)): 
                npt = (None)
            elif (npt.end_token.is_value("ПАРК", None)): 
                pass
            elif (AddressItemToken.check_street_after(npt.end_token, True)): 
                npt = (None)
            else: 
                tok = TerrItemToken._m_terr_ontology.try_attach(npt.end_token, None, False)
                if (tok is not None): 
                    npt = (None)
                else: 
                    next0__ = TerrItemToken.try_parse(npt.end_token, None, None)
                    if (next0__ is not None and next0__.termin_item is not None): 
                        if (MiscLocationHelper.check_geo_object_after(npt.end_token.previous, False, False)): 
                            npt = (None)
                    elif (CityItemToken.check_keyword(npt.end_token) is not None): 
                        if (MiscLocationHelper.check_geo_object_after(npt.end_token.previous, False, False)): 
                            npt = (None)
            if (npt is not None): 
                if (prev is not None and prev.termin_item is not None): 
                    pass
                else: 
                    mc = npt.end_token.get_morph_class_in_dictionary()
                    if (not mc.is_noun): 
                        npt = (None)
        if (npt is not None and npt.end_token == tt.next0_): 
            adj = False
            reg_after = False
            if (len(npt.adjectives) == 1 and not t0.chars.is_all_lower): 
                if (((((tt.next0_.is_value("РАЙОН", None) or tt.next0_.is_value("ОБЛАСТЬ", None) or tt.next0_.is_value("КРАЙ", None)) or tt.next0_.is_value("ВОЛОСТЬ", None) or tt.next0_.is_value("УЛУС", None)) or tt.next0_.is_value("ОКРУГ", None) or tt.next0_.is_value("АВТОНОМИЯ", "АВТОНОМІЯ")) or tt.next0_.is_value("РЕСПУБЛИКА", "РЕСПУБЛІКА") or tt.next0_.is_value("COUNTY", None)) or tt.next0_.is_value("STATE", None) or tt.next0_.is_value("REGION", None)): 
                    reg_after = True
                else: 
                    tok = TerrItemToken._m_terr_ontology.try_attach(tt.next0_, None, False)
                    if (tok is not None): 
                        if ((((tok[0].termin.canonic_text == "РАЙОН" or tok[0].termin.canonic_text == "ОБЛАСТЬ" or tok[0].termin.canonic_text == "УЛУС") or tok[0].termin.canonic_text == "КРАЙ" or tok[0].termin.canonic_text == "ВОЛОСТЬ") or tok[0].termin.canonic_text == "ОКРУГ" or tok[0].termin.canonic_text == "АВТОНОМИЯ") or tok[0].termin.canonic_text == "АВТОНОМІЯ" or ((tok[0].chars.is_latin_letter and (isinstance(tok[0].termin, TerrTermin)) and tok[0].termin.is_region))): 
                            reg_after = True
            if (reg_after): 
                adj = True
                for wff in tt.morph.items: 
                    wf = Utils.asObjectOrNull(wff, MorphWordForm)
                    if (wf is None): 
                        continue
                    if (wf.class0_.is_verb and wf.is_in_dictionary): 
                        adj = False
                        break
                    elif (wf.is_in_dictionary and not wf.class0_.is_adjective): 
                        pass
                if (not adj and prefix is not None): 
                    adj = True
                if (not adj): 
                    if (CityItemToken.check_keyword(tt.next0_.next0_) is not None or CityItemToken.check_onto_item(tt.next0_.next0_) is not None): 
                        adj = True
                if (not adj): 
                    if (MiscLocationHelper.check_geo_object_before(npt.begin_token, False)): 
                        adj = True
                te = tt.next0_.next0_
                if (te is not None and te.is_char_of(",")): 
                    te = te.next0_
                if (not adj and (isinstance(te, ReferentToken))): 
                    if (isinstance(te.get_referent(), GeoReferent)): 
                        adj = True
                if (not adj): 
                    te = t0.previous
                    if (te is not None and te.is_char_of(",")): 
                        te = te.previous
                    if (isinstance(te, ReferentToken)): 
                        if (isinstance(te.get_referent(), GeoReferent)): 
                            adj = True
                if (adj and npt.adjectives[0].begin_token != npt.adjectives[0].end_token): 
                    if (not npt.adjectives[0].begin_token.chars.equals(npt.adjectives[0].end_token.chars)): 
                        return None
            elif ((len(npt.adjectives) == 1 and (isinstance(npt.end_token, TextToken)) and npt.end_token.get_morph_class_in_dictionary().is_noun) and prev is not None and prev.termin_item is not None): 
                adj = True
                tt = (Utils.asObjectOrNull(npt.end_token, TextToken))
            if (not adj and not t0.chars.is_latin_letter): 
                return None
        res = TerrItemToken(t0, tt)
        res.is_adjective = tt.morph.class0_.is_adjective
        res.morph = tt.morph
        if (npt is not None and npt.end_char > res.end_char and npt.morph.gender != MorphGender.UNDEFINED): 
            res.morph = MorphCollection(tt.morph)
            res.morph.remove_items(npt.morph.gender, False)
        if (isinstance(t0, TextToken)): 
            for wf in t0.morph.items: 
                f = Utils.asObjectOrNull(wf, MorphWordForm)
                if (not f.is_in_dictionary): 
                    continue
                if (((wf.class0_.is_proper_surname or wf.class0_.is_proper_name)) and f.is_in_dictionary): 
                    res.can_be_surname = True
                elif (wf.class0_.is_adjective and f.is_in_dictionary): 
                    res.is_adj_in_dictionary = True
                elif (wf.class0_.is_proper_geo): 
                    if (not t0.chars.is_all_lower): 
                        res.is_geo_in_dictionary = True
        if ((tt.whitespaces_after_count < 2) and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_capital_upper): 
            dir0_ = MiscLocationHelper.try_attach_nord_west(tt.next0_)
            if (dir0_ is not None): 
                res.end_token = dir0_.end_token
            elif (t0 == tt and t0.is_value("ОЗЕРО", None)): 
                rtt = t0.kit.process_referent("NAMEDENTITY", t0, None)
                if (rtt is not None): 
                    res.end_token = rtt.end_token
        if (((res.begin_token == res.end_token and res.is_adjective and (res.whitespaces_after_count < 2)) and (isinstance(res.end_token.next0_, TextToken)) and res.end_token.next0_.chars.is_capital_upper) and prev is not None): 
            if (MiscLocationHelper.check_geo_object_after(res.end_token.next0_, False, False)): 
                res.end_token = res.end_token.next0_
            elif (AddressItemToken.check_street_after(res.end_token.next0_.next0_, False)): 
                res.end_token = res.end_token.next0_
        return res
    
    @staticmethod
    def __try_parse_district_name(t : 'Token', lev : int=0, prev : 'TerrItemToken'=None) -> 'TerrItemToken':
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        if (lev > 2): 
            return None
        if (not (isinstance(t, TextToken)) or not t.chars.is_capital_upper or not t.chars.is_cyrillic_letter): 
            return None
        if ((t.next0_ is not None and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, TextToken))) and t.next0_.next0_.chars.equals(t.chars)): 
            tok = TerrItemToken._m_terr_ontology.try_attach(t, None, False)
            if ((tok is not None and tok[0].item is not None and (isinstance(tok[0].item.referent, GeoReferent))) and tok[0].item.referent.is_state): 
                return None
            tok = TerrItemToken._m_terr_ontology.try_attach(t.next0_.next0_, None, False)
            if ((tok is not None and tok[0].item is not None and (isinstance(tok[0].item.referent, GeoReferent))) and tok[0].item.referent.is_state): 
                return None
            if (t.next0_.is_whitespace_before or t.next0_.is_whitespace_after): 
                if (not MiscLocationHelper.is_user_param_address(t)): 
                    return None
            res1 = TerrItemToken(t, t.next0_.next0_)
            res1.is_adjective = res1.end_token.morph.class0_.is_adjective
            return res1
        if ((isinstance(t.next0_, TextToken)) and t.next0_.chars.equals(t.chars)): 
            npt = MiscLocationHelper._try_parse_npt(t)
            if (npt is not None and npt.end_token == t.next0_ and len(npt.adjectives) == 1): 
                if (not npt.end_token.morph.class0_.is_adjective or ((npt.end_token.morph.case_.is_nominative and (isinstance(npt.end_token, TextToken)) and LanguageHelper.ends_with(npt.end_token.term, "О")))): 
                    ty = TerrItemToken.__try_parse(t.next0_, None, False)
                    if (ty is not None and ty.termin_item is not None): 
                        return None
                    return TerrItemToken(t, t.next0_)
        str0_ = t.term
        res = TerrItemToken._new1768(t, t, True)
        if (not LanguageHelper.ends_with(str0_, "О")): 
            res.is_doubt = True
        dir0_ = MiscLocationHelper.try_attach_nord_west(t)
        if (dir0_ is not None): 
            res.end_token = dir0_.end_token
            res.is_doubt = False
            if (res.end_token.whitespaces_after_count < 2): 
                res2 = TerrItemToken.__try_parse_district_name(res.end_token.next0_, lev + 1, None)
                if (res2 is not None and res2.termin_item is None): 
                    res.end_token = res2.end_token
        cit = CityItemToken.try_parse(t, None, False, None)
        if (cit is not None and cit.typ == CityItemToken.ItemType.CITY and cit.onto_item is not None): 
            if (prev is not None and prev.termin_item is not None): 
                if ("ГОРОД" in prev.termin_item.canonic_text): 
                    return TerrItemToken(t, cit.end_token)
            return None
        return res
    
    @staticmethod
    def try_parse_list(t : 'Token', max_count : int, ad : 'GeoAnalyzerData'=None) -> typing.List['TerrItemToken']:
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        ci = TerrItemToken.try_parse(t, None, ad)
        if (ci is None): 
            return None
        li = list()
        li.append(ci)
        t = ci.end_token.next0_
        if (t is None): 
            return li
        if (ci.termin_item is not None and ci.termin_item.canonic_text == "АВТОНОМИЯ"): 
            if (t.morph.case_.is_genitive): 
                return None
        t = ci.end_token.next0_
        while t is not None: 
            if (t.is_newline_before): 
                if (MiscLocationHelper.is_user_param_address(t)): 
                    if (len(li) == 1 and li[0].termin_item is not None): 
                        pass
                    else: 
                        break
            ci = TerrItemToken.try_parse(t, li[len(li) - 1], ad)
            if (ci is None): 
                if (t.chars.is_capital_upper and len(li) == 1 and ((li[0].is_city_region or ((li[0].termin_item is not None and li[0].termin_item.is_specific_prefix))))): 
                    cit = CityItemToken.try_parse(t, None, False, None)
                    if (cit is not None and cit.typ == CityItemToken.ItemType.PROPERNAME): 
                        ci = TerrItemToken(cit.begin_token, cit.end_token)
                elif ((BracketHelper.can_be_start_of_sequence(t, False, False) and t.next0_ is not None and ((t.next0_.chars.is_capital_upper or t.next0_.chars.is_all_upper))) and len(li) == 1 and ((li[0].is_city_region or ((li[0].termin_item is not None and li[0].termin_item.is_specific_prefix))))): 
                    cit = CityItemToken.try_parse(t.next0_, None, False, None)
                    if (cit is not None and ((cit.typ == CityItemToken.ItemType.PROPERNAME or cit.typ == CityItemToken.ItemType.CITY)) and BracketHelper.can_be_end_of_sequence(cit.end_token.next0_, False, None, False)): 
                        ci = TerrItemToken(t, cit.end_token.next0_)
                    else: 
                        brr = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                        if (brr is not None): 
                            ok = False
                            rt = t.kit.process_referent("ORGANIZATION", t.next0_, None)
                            if (rt is not None and "СОВЕТ" in str(rt).upper()): 
                                ok = True
                            elif (brr.length_char < 40): 
                                ok = True
                            if (ok): 
                                ci = TerrItemToken(t, brr.end_token)
                elif (t.is_char_of("(/\\")): 
                    ci = TerrItemToken.try_parse(t.next0_, None, ad)
                    if (ci is not None and ci.end_token.next0_ is not None and ci.end_token.next0_.is_char_of(")/\\")): 
                        ci0 = li[len(li) - 1]
                        if (ci0.onto_item is not None and ci.onto_item == ci0.onto_item): 
                            ci0.end_token = ci.end_token.next0_
                            t = ci0.end_token.next0_
                        else: 
                            ci1 = TerrItemToken._new1769(t, ci.end_token.next0_, ci.onto_item, ci.termin_item)
                            li.append(ci1)
                            t = ci1.end_token.next0_
                        continue
                elif ((t.is_comma and len(li) == 1 and li[0].termin_item is None) and (t.whitespaces_after_count < 3)): 
                    li2 = TerrItemToken.try_parse_list(t.next0_, 2, None)
                    if (li2 is not None and len(li2) == 1 and li2[0].termin_item is not None): 
                        tt2 = li2[0].end_token.next0_
                        ok = False
                        if (tt2 is None or tt2.whitespaces_before_count > 3): 
                            ok = True
                        elif (((tt2.length_char == 1 and not tt2.is_letters)) or not (isinstance(tt2, TextToken))): 
                            ok = True
                        if (ok): 
                            li.append(li2[0])
                            t = li2[0].end_token
                            break
                if (ci is None and BracketHelper.can_be_start_of_sequence(t, False, False)): 
                    lii = TerrItemToken.try_parse_list(t.next0_, max_count, None)
                    if (lii is not None and BracketHelper.can_be_end_of_sequence(lii[len(lii) - 1].end_token.next0_, False, None, False)): 
                        li.extend(lii)
                        return li
                if ((ci is None and t.is_value("Р", None) and MiscLocationHelper.is_user_param_address(t)) and len(li) == 1 and li[0].termin_item is None): 
                    ci = TerrItemToken._new1748(t, t, TerrItemToken.__m_raion)
                    if (t.next0_ is not None and t.next0_.is_char('.')): 
                        ci.end_token = t.next0_
                if (ci is None): 
                    break
            if (t.is_table_control_char): 
                break
            if (t.is_newline_before): 
                if (t.newlines_before_count > 1): 
                    break
                if (len(li) > 0 and li[len(li) - 1].is_adjective and ci.termin_item is not None): 
                    pass
                elif (len(li) == 1 and li[0].termin_item is not None and ci.termin_item is None): 
                    pass
                else: 
                    break
            if (ci.termin_item is not None and ci.termin_item.canonic_text == "ТЕРРИТОРИЯ"): 
                break
            li.append(ci)
            t = ci.end_token.next0_
            if (max_count > 0 and len(li) >= max_count): 
                break
        for cc in li: 
            if (cc.onto_item is not None and not cc.is_adjective): 
                if (not cc.begin_token.chars.is_cyrillic_letter): 
                    continue
                alpha2 = None
                if (isinstance(cc.onto_item.referent, GeoReferent)): 
                    alpha2 = cc.onto_item.referent.alpha2
                if (alpha2 == "TG"): 
                    if (isinstance(cc.begin_token, TextToken)): 
                        if (cc.begin_token.get_source_text() != "Того"): 
                            return None
                        if (len(li) == 1 and cc.begin_token.previous is not None and cc.begin_token.previous.is_char('.')): 
                            return None
                        npt = NounPhraseHelper.try_parse(cc.begin_token, NounPhraseParseAttr.PARSEPRONOUNS, 0, None)
                        if (npt is not None and npt.end_token != cc.begin_token): 
                            return None
                        if (cc.begin_token.next0_ is not None): 
                            if (cc.begin_token.next0_.morph.class0_.is_personal_pronoun or cc.begin_token.next0_.morph.class0_.is_pronoun): 
                                return None
                    if (len(li) < 2): 
                        return None
                if (alpha2 == "PE"): 
                    if (isinstance(cc.begin_token, TextToken)): 
                        if (cc.begin_token.get_source_text() != "Перу"): 
                            return None
                        if (len(li) == 1 and cc.begin_token.previous is not None and cc.begin_token.previous.is_char('.')): 
                            return None
                    if (len(li) < 2): 
                        return None
                if (alpha2 == "DM"): 
                    if (cc.end_token.next0_ is not None): 
                        if (cc.end_token.next0_.chars.is_capital_upper or cc.end_token.next0_.chars.is_all_upper): 
                            return None
                    return None
                if (alpha2 == "JE"): 
                    if (cc.begin_token.previous is not None and cc.begin_token.previous.is_hiphen): 
                        return None
                return li
            elif (cc.onto_item is not None and cc.is_adjective): 
                alpha2 = None
                if (isinstance(cc.onto_item.referent, GeoReferent)): 
                    alpha2 = cc.onto_item.referent.alpha2
                if (alpha2 == "SU"): 
                    if (cc.end_token.next0_ is None or not cc.end_token.next0_.is_value("СОЮЗ", None)): 
                        cc.onto_item = (None)
        i = 0
        first_pass3994 = True
        while True:
            if first_pass3994: first_pass3994 = False
            else: i += 1
            if (not (i < len(li))): break
            if (li[i].onto_item is not None and li[i].onto_item2 is not None): 
                nou = None
                if (i > 0 and li[i - 1].termin_item is not None): 
                    nou = (li[i - 1].termin_item)
                elif (((i + 1) < len(li)) and li[i + 1].termin_item is not None): 
                    nou = (li[i + 1].termin_item)
                if (nou is None or li[i].onto_item.referent is None or li[i].onto_item2.referent is None): 
                    continue
                if (li[i].onto_item.referent.find_slot(GeoReferent.ATTR_TYPE, nou.canonic_text.lower(), True) is None and li[i].onto_item2.referent.find_slot(GeoReferent.ATTR_TYPE, nou.canonic_text.lower(), True) is not None): 
                    li[i].onto_item = li[i].onto_item2
                    li[i].onto_item2 = (None)
                elif (li[i].onto_item.referent.find_slot(GeoReferent.ATTR_TYPE, "республика", True) is not None and nou.canonic_text != "РЕСПУБЛИКА"): 
                    li[i].onto_item = li[i].onto_item2
                    li[i].onto_item2 = (None)
            elif ((li[i].termin_item is not None and ((i + 1) < len(li)) and li[i + 1].termin_item is not None) and str(li[i + 1].termin_item) in str(li[i].termin_item)): 
                li[i].end_token = li[i + 1].end_token
                del li[i + 1]
                i -= 1
        if ((len(li) >= 3 and li[0].termin_item is None and li[1].termin_item is not None) and li[2].termin_item is None): 
            if (len(li) == 3 or ((len(li) >= 5 and ((((li[3].termin_item is not None and li[4].termin_item is None)) or ((li[4].termin_item is not None and li[3].termin_item is None))))))): 
                t1 = li[0].begin_token.previous
                if (t1 is not None and t1.is_char('.') and t1.previous is not None): 
                    t1 = t1.previous
                    cit = CityItemToken.try_parse_back(t1, False)
                    if (cit is not None): 
                        del li[0]
                    elif (t1.chars.is_all_lower and ((t1.is_value("С", None) or t1.is_value("П", None) or t1.is_value("ПОС", None)))): 
                        del li[0]
        for cc in li: 
            if (cc.onto_item is not None or ((cc.termin_item is not None and not cc.is_adjective))): 
                return li
        if (len(li) > 0 and MiscLocationHelper.is_user_param_address(li[0].begin_token)): 
            return li
        return None
    
    @staticmethod
    def initialize() -> None:
        if (TerrItemToken._m_terr_ontology is not None): 
            return
        TerrItemToken._m_terr_ontology = IntOntologyCollection()
        TerrItemToken.M_TERR_ADJS = TerminCollection()
        TerrItemToken.M_MANS_BY_STATE = TerminCollection()
        TerrItemToken._m_unknown_regions = TerminCollection()
        TerrItemToken._m_terr_noun_adjectives = TerminCollection()
        TerrItemToken._m_capitals_by_state = TerminCollection()
        TerrItemToken._m_geo_abbrs = TerminCollection()
        t = TerrTermin._new1771("РЕСПУБЛИКА", MorphGender.FEMINIE)
        t.add_abridge("РЕСП.")
        t.add_abridge("РЕСП-КА")
        t.add_abridge("РЕСПУБ.")
        t.add_abridge("РЕСПУБЛ.")
        t.add_abridge("Р-КА")
        t.add_abridge("РЕСП-КА")
        TerrItemToken._m_terr_ontology.add(t)
        TerrItemToken._m_terr_ontology.add(TerrTermin._new1772("РЕСПУБЛІКА", MorphLang.UA, MorphGender.FEMINIE))
        t = TerrTermin._new1773("ГОСУДАРСТВО", True, MorphGender.NEUTER)
        t.add_abridge("ГОС-ВО")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1774("ДЕРЖАВА", MorphLang.UA, True, MorphGender.FEMINIE)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1771("АВТОНОМНАЯ СОВЕТСКАЯ СОЦИАЛИСТИЧЕСКАЯ РЕСПУБЛИКА", MorphGender.FEMINIE)
        t.acronym = "АССР"
        TerrItemToken._m_terr_ontology.add(t)
        for s in ["СОЮЗ", "СОДРУЖЕСТВО", "ФЕДЕРАЦИЯ", "КОНФЕДЕРАЦИЯ"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1776(s, True, True))
        for s in ["СОЮЗ", "СПІВДРУЖНІСТЬ", "ФЕДЕРАЦІЯ", "КОНФЕДЕРАЦІЯ"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1777(s, MorphLang.UA, True, True))
        for s in ["КОРОЛЕВСТВО", "КНЯЖЕСТВО", "ГЕРЦОГСТВО", "ИМПЕРИЯ", "ЦАРСТВО", "KINGDOM", "DUCHY", "EMPIRE"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1778(s, True))
        for s in ["КОРОЛІВСТВО", "КНЯЗІВСТВО", "ГЕРЦОГСТВО", "ІМПЕРІЯ"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1779(s, MorphLang.UA, True))
        for s in ["НЕЗАВИСИМЫЙ", "ОБЪЕДИНЕННЫЙ", "СОЕДИНЕННЫЙ", "НАРОДНЫЙ", "НАРОДНО", "ФЕДЕРАТИВНЫЙ", "ДЕМОКРАТИЧЕСКИЙ", "СОВЕТСКИЙ", "СОЦИАЛИСТИЧЕСКИЙ", "КООПЕРАТИВНЫЙ", "ИСЛАМСКИЙ", "АРАБСКИЙ", "МНОГОНАЦИОНАЛЬНЫЙ", "СУВЕРЕННЫЙ", "САМОПРОВОЗГЛАШЕННЫЙ", "НЕПРИЗНАННЫЙ"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1780(s, True, True))
        for s in ["НЕЗАЛЕЖНИЙ", "ОБЄДНАНИЙ", "СПОЛУЧЕНИЙ", "НАРОДНИЙ", "ФЕДЕРАЛЬНИЙ", "ДЕМОКРАТИЧНИЙ", "РАДЯНСЬКИЙ", "СОЦІАЛІСТИЧНИЙ", "КООПЕРАТИВНИЙ", "ІСЛАМСЬКИЙ", "АРАБСЬКИЙ", "БАГАТОНАЦІОНАЛЬНИЙ", "СУВЕРЕННИЙ"]: 
            TerrItemToken._m_terr_ontology.add(TerrTermin._new1781(s, MorphLang.UA, True, True))
        t = TerrTermin._new1782("ОБЛАСТЬ", True, MorphGender.FEMINIE)
        t.add_abridge("ОБЛ.")
        TerrItemToken._m_terr_noun_adjectives.add(Termin._new84("ОБЛАСТНОЙ", t))
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1784("REGION", True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1785("ОБЛАСТЬ", MorphLang.UA, True, MorphGender.FEMINIE)
        t.add_abridge("ОБЛ.")
        TerrItemToken.__m_obl = t
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1786(None, True, "АО")
        t.add_variant("АОБЛ", False)
        t.add_abridge("А.О.")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1787(None, MorphLang.UA, True, "АО")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1782("РАЙОН", True, MorphGender.MASCULINE)
        t.add_abridge("Р-Н")
        t.add_abridge("Р-ОН")
        t.add_abridge("РН.")
        TerrItemToken._m_terr_noun_adjectives.add(Termin._new84("РАЙОННЫЙ", t))
        TerrItemToken._m_terr_ontology.add(t)
        TerrItemToken.__m_raion = t
        t = TerrTermin._new1785("РАЙОН", MorphLang.UA, True, MorphGender.MASCULINE)
        t.add_abridge("Р-Н")
        t.add_abridge("Р-ОН")
        t.add_abridge("РН.")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1782("УЕЗД", True, MorphGender.MASCULINE)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1792("ГУБЕРНАТОРСТВО", True, True, MorphGender.NEUTER)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1782("АЙЫЛЬНЫЙ АЙМАК", True, MorphGender.MASCULINE)
        t.add_abridge("А/А")
        t.add_variant("АЙЫЛ АЙМАГЫ", False)
        t.add_variant("АЙМАК", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1782("ВЕЛАЯТ", True, MorphGender.MASCULINE)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1792("ШТАТ", True, True, MorphGender.MASCULINE)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1784("STATE", True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1797("ШТАТ", MorphLang.UA, True, True, MorphGender.MASCULINE)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1792("ПРОВИНЦИЯ", True, True, MorphGender.FEMINIE)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1797("ПРОВІНЦІЯ", MorphLang.UA, True, True, MorphGender.FEMINIE)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1784("PROVINCE", True)
        t.add_variant("PROVINCIAL", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1801("ПРЕФЕКТУРА", True, MorphGender.FEMINIE, True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1802("PREFECTURE", True, True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1792("ГРАФСТВО", True, True, MorphGender.NEUTER)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1782("АВТОНОМИЯ", True, MorphGender.FEMINIE)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1784("AUTONOMY", True)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1785("АВТОНОМІЯ", MorphLang.UA, True, MorphGender.FEMINIE)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1807("ЗАКРЫТОЕ АДМИНИСТРАТИВНО ТЕРРИТОРИАЛЬНОЕ ОБРАЗОВАНИЕ", True, MorphGender.NEUTER, "ЗАТО")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1782("ФЕДЕРАЛЬНАЯ ТЕРРИТОРИЯ", True, MorphGender.NEUTER)
        t.add_abridge("Ф.Т.")
        TerrItemToken._m_terr_ontology.add(t)
        for s in ["РЕСПУБЛИКА", "КРАЙ", "ОКРУГ", "ФЕДЕРАЛЬНЫЙ ОКРУГ", "АВТОНОМНЫЙ ОКРУГ", "АВТОНОМНАЯ ОБЛАСТЬ", "НАЦИОНАЛЬНЫЙ ОКРУГ", "ВОЛОСТЬ", "ФЕДЕРАЛЬНАЯ ЗЕМЛЯ", "ВОЕВОДСТВО", "МУНИЦИПАЛЬНЫЙ РАЙОН", "МУНИЦИПАЛЬНЫЙ ОКРУГ", "АДМИНИСТРАТИВНЫЙ ОКРУГ", "ГОРОДСКОЙ ОКРУГ", "ГОРОДСКОЙ РАЙОН", "ВНУТРИГОРОДСКОЙ РАЙОН", "АДМИНИСТРАТИВНЫЙ РАЙОН", "СУДЕБНЫЙ РАЙОН", "ВНУТРИГОРОДСКОЕ МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ", "МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ", "СЕЛЬСКОЕ МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ", "ВНУТРИГОРОДСКАЯ ТЕРРИТОРИЯ", "МЕЖСЕЛЕННАЯ ТЕРРИТОРИЯ", "REPUBLIC", "COUNTY", "BOROUGH", "PARISH", "MUNICIPALITY", "CENSUS AREA", "AUTONOMOUS REGION", "ADMINISTRATIVE REGION", "SPECIAL ADMINISTRATIVE REGION"]: 
            t = TerrTermin._new1809(s, True, " " in s)
            if (s == "КРАЙ"): 
                t.add_abridge("КР.")
                TerrItemToken._m_terr_noun_adjectives.add(Termin._new84("КРАЕВОЙ", t))
                t.gender = MorphGender.MASCULINE
            elif (s == "ВНУТРИГОРОДСКАЯ ТЕРРИТОРИЯ"): 
                t.add_abridge("ВН.ГОР.ТЕР.")
                t.add_abridge("ВН.Г.ТЕР.")
                t.add_abridge("ВН.ТЕР.Г.")
            elif (s == "ОКРУГ"): 
                TerrItemToken._m_terr_noun_adjectives.add(Termin._new84("ОКРУЖНОЙ", t))
                t.add_abridge("ОКР.")
            elif (s == "ФЕДЕРАЛЬНЫЙ ОКРУГ"): 
                t.acronym = "ФО"
            if (LanguageHelper.ends_with(s, "РАЙОН")): 
                t.add_abridge(s.replace("РАЙОН", "Р-Н"))
                t.gender = MorphGender.MASCULINE
                if (s == "МУНИЦИПАЛЬНЫЙ РАЙОН"): 
                    t.add_abridge("М.Р.")
                    t.add_abridge("М.Р-Н")
                    t.add_abridge("М Р-Н")
                    t.add_abridge("МУН.Р-Н")
            if (LanguageHelper.ends_with(s, "ОКРУГ")): 
                t.gender = MorphGender.MASCULINE
                if (s != "ОКРУГ"): 
                    t.add_variant(s + " ОКРУГ", False)
                if (s == "МУНИЦИПАЛЬНЫЙ ОКРУГ"): 
                    t.add_abridge("М.О.")
                    t.add_abridge("МУН.ОКРУГ")
            if (LanguageHelper.ends_with(s, "ОБРАЗОВАНИЕ")): 
                t.gender = MorphGender.NEUTER
            TerrItemToken._m_terr_ontology.add(t)
        for s in ["РЕСПУБЛІКА", "КРАЙ", "ОКРУГ", "ФЕДЕРАЛЬНИЙ ОКРУГ", "АВТОНОМНИЙ ОКРУГ", "АВТОНОМНА ОБЛАСТЬ", "НАЦІОНАЛЬНИЙ ОКРУГ", "ВОЛОСТЬ", "ФЕДЕРАЛЬНА ЗЕМЛЯ", "МУНІЦИПАЛЬНИЙ РАЙОН", "МУНІЦИПАЛЬНИЙ ОКРУГ", "АДМІНІСТРАТИВНИЙ ОКРУГ", "МІСЬКИЙ РАЙОН", "ВНУТРИГОРОДСКОЕ МУНІЦИПАЛЬНЕ УТВОРЕННЯ"]: 
            t = TerrTermin._new1812(s, MorphLang.UA, True, " " in s)
            if (LanguageHelper.ends_with(s, "РАЙОН")): 
                t.add_abridge(s.replace("РАЙОН", "Р-Н"))
                t.gender = MorphGender.MASCULINE
            TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1782("ГОРОДСКОЙ ОКРУГ", True, MorphGender.MASCULINE)
        t.add_abridge("ГОР. ОКРУГ")
        t.add_abridge("Г.О.")
        t.add_abridge("Г/ОКРУГ")
        t.add_abridge("Г/О")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1782("СЕЛЬСКИЙ ОКРУГ", True, MorphGender.MASCULINE)
        t.add_abridge("С.О.")
        t.add_abridge("C.O.")
        t.add_abridge("ПС С.О.")
        t.add_abridge("С/ОКРУГ")
        t.add_abridge("С/О")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1785("СІЛЬСЬКИЙ ОКРУГ", MorphLang.UA, True, MorphGender.MASCULINE)
        t.add_abridge("С.О.")
        t.add_abridge("C.O.")
        t.add_abridge("С/ОКРУГ")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1816("СЕЛЬСКИЙ СОВЕТ", "СЕЛЬСКИЙ ОКРУГ", True, MorphGender.MASCULINE)
        t.add_variant("СЕЛЬСОВЕТ", False)
        t.add_abridge("С.С.")
        t.add_abridge("С/С")
        t.add_abridge("С.СОВЕТ")
        t.add_variant("СЕЛЬСКАЯ АДМИНИСТРАЦИЯ", False)
        t.add_abridge("С.А.")
        t.add_abridge("С.АДМ.")
        t.add_abridge("C/C")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1784("ПОСЕЛКОВЫЙ ОКРУГ", True)
        t.add_variant("ПОСЕЛКОВАЯ АДМИНИСТРАЦИЯ", False)
        t.add_abridge("П.А.")
        t.add_abridge("П.АДМ.")
        t.add_abridge("П/А")
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1816("ПОСЕЛКОВЫЙ СОВЕТ", "ПОСЕЛКОВЫЙ ОКРУГ", True, MorphGender.MASCULINE)
        t.add_abridge("П.С.")
        t.add_abridge("П.СОВЕТ")
        TerrItemToken._m_terr_ontology.add(t)
        TerrItemToken._m_terr_ontology.add(TerrTermin._new1819("АВТОНОМНЫЙ", True, True))
        TerrItemToken._m_terr_ontology.add(TerrTermin._new1820("АВТОНОМНИЙ", MorphLang.UA, True, True))
        TerrItemToken._m_terr_ontology.add(TerrTermin._new1821("МУНИЦИПАЛЬНОЕ СОБРАНИЕ", True, True, True))
        TerrItemToken._m_terr_ontology.add(TerrTermin._new1822("МУНІЦИПАЛЬНЕ ЗБОРИ", MorphLang.UA, True, True, True))
        t = TerrTermin._new1823("МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ", "МО", MorphGender.NEUTER)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1824("МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ МУНИЦИПАЛЬНЫЙ РАЙОН", "МОМР", True)
        t.add_variant("МО МР", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1825("МУНИЦИПАЛЬНЫЙ ОКРУГ ГОРОДСКОЙ ОКРУГ", "МУНИЦИПАЛЬНЫЙ ОКРУГ", "МОГО", True)
        t.add_variant("МУНИЦИПАЛЬНОЕ ОБРАЗОВАНИЕ ГОРОДСКОЙ ОКРУГ", False)
        t.add_variant("МО ГО", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("ЦЕНТРАЛЬНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("ЦАО")
        t.add_variant("ЦЕНТРАЛЬНЫЙ АО", False)
        t.add_variant("ЦЕНТРАЛЬНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("СЕВЕРНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("САО")
        t.add_variant("СЕВЕРНЫЙ АО", False)
        t.add_variant("СЕВЕРНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("СЕВЕРО-ВОСТОЧНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("СВАО")
        t.add_variant("СЕВЕРО-ВОСТОЧНЫЙ АО", False)
        t.add_variant("СЕВЕРО-ВОСТОЧНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("ВОСТОЧНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("ВАО")
        t.add_variant("ВОСТОЧНЫЙ АО", False)
        t.add_variant("ВОСТОЧНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("ЮГО-ВОСТОЧНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("ЮВАО")
        t.add_variant("ЮГО-ВОСТОЧНЫЙ АО", False)
        t.add_variant("ЮГО-ВОСТОЧНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("ЮЖНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("ЮАО")
        t.add_variant("ЮЖНЫЙ АО", False)
        t.add_variant("ЮЖНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("ЗАПАДНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("ЗАО")
        t.add_variant("ЗАПАДНЫЙ АО", False)
        t.add_variant("ЗАПАДНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("СЕВЕРО-ЗАПАДНЫЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("СЗАО")
        t.add_variant("СЕВЕРО-ЗАПАДНЫЙ АО", False)
        t.add_variant("СЕВЕРО-ЗАПАДНЫЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("ЗЕЛЕНОГРАДСКИЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("ЗЕЛАО")
        t.add_variant("ЗЕЛЕНОГРАДСКИЙ АО", False)
        t.add_variant("ЗЕЛЕНОГРАДСКИЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("ТРОИЦКИЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("ТАО")
        t.add_variant("ТРОИЦКИЙ АО", False)
        t.add_variant("ТРОИЦКИЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("НОВОМОСКОВСКИЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("НАО")
        t.add_variant("НОВОМОСКОВСКИЙ АО", False)
        t.add_variant("НОВОМОСКОВСКИЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        t = TerrTermin._new1826("ТРОИЦКИЙ И НОВОМОСКОВСКИЙ АДМИНИСТРАТИВНЫЙ ОКРУГ", True)
        t.add_abridge("ТИНАО")
        t.add_abridge("НИТАО")
        t.add_variant("ТРОИЦКИЙ И НОВОМОСКОВСКИЙ АО", False)
        t.add_variant("ТРОИЦКИЙ И НОВОМОСКОВСКИЙ ОКРУГ", False)
        TerrItemToken._m_terr_ontology.add(t)
        TerrItemToken.__m_spec_names = TerminCollection()
        for s in ["МАРЬИНА РОЩА", "ПРОСПЕКТ ВЕРНАДСКОГО"]: 
            TerrItemToken.__m_spec_names.add(Termin(s))
        TerrItemToken._m_alpha2state = dict()
        dat = PullentiNerAddressInternalResourceHelper.get_bytes("t.dat")
        if (dat is None): 
            raise Utils.newException("Not found resource file t.dat in Analyzer.Location", None)
        dat = MiscLocationHelper._deflate(dat)
        with MemoryStream(dat) as tmp: 
            tmp.position = 0
            xml0_ = None # new XmlDocument
            xml0_ = Utils.parseXmlFromStream(tmp)
            for x in xml0_.getroot(): 
                lang = MorphLang.RU
                a = Utils.getXmlAttrByName(x.attrib, "l")
                if (a is not None): 
                    if (a[1] == "en"): 
                        lang = MorphLang.EN
                    elif (a[1] == "ua"): 
                        lang = MorphLang.UA
                if (Utils.getXmlName(x) == "state"): 
                    TerrItemToken.__load_state(x, lang)
                elif (Utils.getXmlName(x) == "reg"): 
                    TerrItemToken.__load_region(x, lang)
                elif (Utils.getXmlName(x) == "unknown"): 
                    a = Utils.getXmlAttrByName(x.attrib, "name")
                    if (a is not None and a[1] is not None): 
                        TerrItemToken._m_unknown_regions.add(Termin._new1165(a[1], lang))
    
    _m_terr_ontology = None
    
    _m_geo_abbrs = None
    
    __m_russiaru = None
    
    __m_russiaua = None
    
    __m_mos_regru = None
    
    __m_len_regru = None
    
    __m_belorussia = None
    
    __m_kazahstan = None
    
    __m_tamog_sous = None
    
    __m_tatarstan = None
    
    __m_udmurtia = None
    
    __m_dagestan = None
    
    M_TERR_ADJS = None
    
    M_MANS_BY_STATE = None
    
    _m_unknown_regions = None
    
    _m_terr_noun_adjectives = None
    
    _m_capitals_by_state = None
    
    __m_obl = None
    
    _m_alpha2state = None
    
    __m_spec_names = None
    
    __m_raion = None
    
    _m_all_states = None
    
    @staticmethod
    def __load_state(xml0_ : xml.etree.ElementTree.Element, lang : 'MorphLang') -> None:
        state = GeoReferent()
        c = IntOntologyItem(state)
        acrs = None
        for x in xml0_: 
            if (Utils.getXmlName(x) == "n"): 
                te = Termin()
                te.init_by_normal_text(Utils.getXmlInnerText(x), None)
                te.ignore_terms_order = True
                if (Utils.getXmlInnerText(x) == "КОТ ДИВУАР"): 
                    te.ignore_terms_order = False
                c.termins.append(te)
                state._add_name(Utils.getXmlInnerText(x))
            elif (Utils.getXmlName(x) == "acr"): 
                c.termins.append(Termin._new1839(Utils.getXmlInnerText(x), lang))
                state._add_name(Utils.getXmlInnerText(x))
                if (acrs is None): 
                    acrs = list()
                acrs.append(Utils.getXmlInnerText(x))
            elif (Utils.getXmlName(x) == "a"): 
                te = Termin()
                te.init_by_normal_text(Utils.getXmlInnerText(x), lang)
                te.tag = (c)
                c.termins.append(te)
                TerrItemToken.M_TERR_ADJS.add(te)
            elif (Utils.getXmlName(x) == "a2"): 
                state.alpha2 = Utils.getXmlInnerText(x)
            elif (Utils.getXmlName(x) == "m"): 
                te = Termin()
                te.init_by_normal_text(Utils.getXmlInnerText(x), lang)
                te.tag = (state)
                te.gender = MorphGender.MASCULINE
                TerrItemToken.M_MANS_BY_STATE.add(te)
            elif (Utils.getXmlName(x) == "w"): 
                te = Termin()
                te.init_by_normal_text(Utils.getXmlInnerText(x), lang)
                te.tag = (state)
                te.gender = MorphGender.FEMINIE
                TerrItemToken.M_MANS_BY_STATE.add(te)
            elif (Utils.getXmlName(x) == "cap"): 
                te = Termin()
                te.init_by_normal_text(Utils.getXmlInnerText(x), lang)
                te.tag = (state)
                TerrItemToken._m_capitals_by_state.add(te)
        c.set_shortest_canonical_text(True)
        if (c.canonic_text == "ГОЛЛАНДИЯ" or c.canonic_text.startswith("КОРОЛЕВСТВО НИДЕР")): 
            c.canonic_text = "НИДЕРЛАНДЫ"
        elif (c.canonic_text == "ГОЛЛАНДІЯ" or c.canonic_text.startswith("КОРОЛІВСТВО НІДЕР")): 
            c.canonic_text = "НІДЕРЛАНДИ"
        if (state.alpha2 == "RU"): 
            if (lang.is_ua): 
                TerrItemToken.__m_russiaua = c
            else: 
                TerrItemToken.__m_russiaru = c
        elif (state.alpha2 == "BY"): 
            if (not lang.is_ua): 
                TerrItemToken.__m_belorussia = c
        elif (state.alpha2 == "KZ"): 
            if (not lang.is_ua): 
                TerrItemToken.__m_kazahstan = c
        elif (c.canonic_text == "ТАМОЖЕННЫЙ СОЮЗ"): 
            if (not lang.is_ua): 
                TerrItemToken.__m_tamog_sous = c
        if (state.find_slot(GeoReferent.ATTR_TYPE, None, True) is None): 
            if (lang.is_ua): 
                state._add_typ_state(lang)
            else: 
                state._add_typ_state(MorphLang.RU)
                state._add_typ_state(MorphLang.EN)
        TerrItemToken._m_terr_ontology.add_item(c)
        if (lang.is_ru): 
            TerrItemToken._m_all_states.append(state)
        a2 = state.alpha2
        if (a2 is not None): 
            if (not a2 in TerrItemToken._m_alpha2state): 
                TerrItemToken._m_alpha2state[a2] = c
            a3 = None
            wrapa31840 = RefOutArgWrapper(None)
            inoutres1841 = Utils.tryGetValue(MiscLocationHelper._m_alpha2_3, a2, wrapa31840)
            a3 = wrapa31840.value
            if (inoutres1841): 
                if (not a3 in TerrItemToken._m_alpha2state): 
                    TerrItemToken._m_alpha2state[a3] = c
        if (acrs is not None): 
            for a in acrs: 
                if (not a in TerrItemToken._m_alpha2state): 
                    TerrItemToken._m_alpha2state[a] = c
    
    @staticmethod
    def __load_region(xml0_ : xml.etree.ElementTree.Element, lang : 'MorphLang') -> None:
        reg = GeoReferent()
        r = IntOntologyItem(reg)
        aterm = None
        for x in xml0_: 
            if (Utils.getXmlName(x) == "n"): 
                v = Utils.getXmlInnerText(x)
                if (v.startswith("ЦЕНТРАЛ")): 
                    pass
                te = Termin()
                te.init_by_normal_text(v, lang)
                if (lang.is_ru and TerrItemToken.__m_mos_regru is None and v == "ПОДМОСКОВЬЕ"): 
                    TerrItemToken.__m_mos_regru = r
                    te.add_abridge("МОС.ОБЛ.")
                    te.add_abridge("МОСК.ОБЛ.")
                    te.add_abridge("МОСКОВ.ОБЛ.")
                    te.add_abridge("МОС.ОБЛАСТЬ")
                    te.add_abridge("МОСК.ОБЛАСТЬ")
                    te.add_abridge("МОСКОВ.ОБЛАСТЬ")
                elif (lang.is_ru and TerrItemToken.__m_len_regru is None and v == "ЛЕНОБЛАСТЬ"): 
                    te.acronym = "ЛО"
                    te.add_abridge("ЛЕН.ОБЛ.")
                    te.add_abridge("ЛЕН.ОБЛАСТЬ")
                    TerrItemToken.__m_len_regru = r
                r.termins.append(te)
                reg._add_name(v)
            elif (Utils.getXmlName(x) == "t"): 
                reg._add_typ(Utils.getXmlInnerText(x))
            elif (Utils.getXmlName(x) == "a"): 
                te = Termin()
                te.init_by_normal_text(Utils.getXmlInnerText(x), lang)
                te.tag = (r)
                r.termins.append(te)
            elif (Utils.getXmlName(x) == "ab"): 
                if (aterm is None): 
                    aterm = Termin._new504(reg.get_string_value(GeoReferent.ATTR_NAME), lang, reg)
                aterm.add_abridge(Utils.getXmlInnerText(x))
        if (aterm is not None): 
            TerrItemToken._m_geo_abbrs.add(aterm)
        r.set_shortest_canonical_text(True)
        if (r.canonic_text.startswith("КАРАЧАЕВО")): 
            r.canonic_text = "КАРАЧАЕВО - ЧЕРКЕССИЯ"
        elif (r.canonic_text == "ЮГРА"): 
            r.termins.append(Termin("ХАНТЫ-МАНСИЙСКИЙ-ЮГРА"))
        elif ("ТАТАРСТАН" in r.canonic_text): 
            TerrItemToken.__m_tatarstan = r
        elif ("УДМУРТ" in r.canonic_text): 
            TerrItemToken.__m_udmurtia = r
        elif ("ДАГЕСТАН" in r.canonic_text): 
            TerrItemToken.__m_dagestan = r
        if (reg.is_state and reg.is_region): 
            reg._add_typ_reg(lang)
        TerrItemToken._m_terr_ontology.add_item(r)
    
    @staticmethod
    def check_onto_item(t : 'Token') -> 'IntOntologyToken':
        if (not (isinstance(t, TextToken))): 
            return None
        li = TerrItemToken._m_terr_ontology.try_attach(t, None, False)
        if (li is not None): 
            for nt in li: 
                if (nt.item is not None): 
                    if (nt.begin_token == nt.end_token and t.get_morph_class_in_dictionary().is_adjective): 
                        pass
                    else: 
                        return nt
        return None
    
    @staticmethod
    def check_keyword(t : 'Token') -> 'MetaToken':
        if (not (isinstance(t, TextToken))): 
            return None
        li = TerrItemToken._m_terr_ontology.try_attach(t, None, False)
        if (li is not None): 
            for nt in li: 
                if (nt.item is None): 
                    tt = Utils.asObjectOrNull(nt.termin, TerrTermin)
                    if (tt.is_adjective): 
                        pass
                    else: 
                        return nt
        return None
    
    @staticmethod
    def check_keyword_before(last : 'Token') -> 'MetaToken':
        cou = 5
        tt = last
        first_pass3995 = True
        while True:
            if first_pass3995: first_pass3995 = False
            else: tt = tt.previous; cou -= 1
            if (not (tt is not None and cou > 0)): break
            res = TerrItemToken.check_keyword(tt)
            if (res is None): 
                continue
            if (res.end_token == last): 
                return res
        return None
    
    @staticmethod
    def _new1748(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'TerrTermin') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.termin_item = _arg3
        return res
    
    @staticmethod
    def _new1749(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'IntOntologyItem') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.onto_item = _arg3
        return res
    
    @staticmethod
    def _new1761(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'IntOntologyItem', _arg4 : 'MorphCollection') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.onto_item = _arg3
        res.morph = _arg4
        return res
    
    @staticmethod
    def _new1762(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'IntOntologyItem', _arg4 : bool, _arg5 : 'MorphCollection') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.onto_item = _arg3
        res.is_adjective = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1763(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'TerrTermin', _arg4 : bool, _arg5 : 'MorphCollection') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.termin_item = _arg3
        res.is_adjective = _arg4
        res.morph = _arg5
        return res
    
    @staticmethod
    def _new1765(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'StreetItemToken') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.named_by = _arg3
        return res
    
    @staticmethod
    def _new1767(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.is_district_name = _arg3
        return res
    
    @staticmethod
    def _new1768(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.is_doubt = _arg3
        return res
    
    @staticmethod
    def _new1769(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'IntOntologyItem', _arg4 : 'TerrTermin') -> 'TerrItemToken':
        res = TerrItemToken(_arg1, _arg2)
        res.onto_item = _arg3
        res.termin_item = _arg4
        return res
    
    # static constructor for class TerrItemToken
    @staticmethod
    def _static_ctor():
        TerrItemToken._m_all_states = list()

TerrItemToken._static_ctor()