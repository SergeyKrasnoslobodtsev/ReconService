# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.geo.internal.NumToken import NumToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.geo.internal.GeoTokenType import GeoTokenType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.core.TerminToken import TerminToken
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.geo.internal.CityItemToken import CityItemToken

class OrgTypToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token', val : str=None) -> None:
        super().__init__(b, e0_, None)
        self.is_doubt = False
        self.not_org = False
        self.not_geo = False
        self.can_be_single = False
        self.is_building = False
        self.vals = list()
        if (val is not None): 
            self.vals.append(val)
    
    def clone(self) -> 'OrgTypToken':
        res = OrgTypToken(self.begin_token, self.end_token)
        res.vals.extend(self.vals)
        res.is_doubt = self.is_doubt
        res.not_org = self.not_org
        res.not_geo = self.not_geo
        res.can_be_single = self.can_be_single
        res.is_building = self.is_building
        return res
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.is_doubt): 
            print("? ", end="", file=tmp)
        i = 0
        while i < len(self.vals): 
            if (i > 0): 
                print(" / ", end="", file=tmp)
            print(self.vals[i], end="", file=tmp)
            i += 1
        if (self.not_org): 
            print(", not Org", end="", file=tmp)
        if (self.not_geo): 
            print(", not Geo", end="", file=tmp)
        if (self.can_be_single): 
            print(", Single", end="", file=tmp)
        if (self.is_building): 
            print(", Building", end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    SPEED_REGIME = False
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        if (not OrgTypToken.SPEED_REGIME): 
            return
        ad = GeoAnalyzer._get_data(t0)
        if (ad is None): 
            return
        ad.otregime = False
        last_typ = None
        t = t0
        while t is not None: 
            after_terr = False
            tt = MiscLocationHelper.check_territory(t)
            if (tt is not None and tt.next0_ is not None): 
                after_terr = True
                t = tt.next0_
            elif (last_typ is not None and last_typ.end_token.next0_ == t): 
                after_terr = True
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            ty = OrgTypToken.try_parse(t, after_terr, ad)
            if (ty is not None): 
                if (d is None): 
                    d = GeoTokenData(t)
                d.org_typ = ty
                t = ty.end_token
                last_typ = ty
            t = t.next0_
        ad.otregime = True
    
    @staticmethod
    def try_parse(t : 'Token', after_terr : bool, ad : 'GeoAnalyzerData'=None) -> 'OrgTypToken':
        if (not (isinstance(t, TextToken))): 
            return None
        if (t.length_char == 1 and not t.chars.is_letter): 
            return None
        if ((t.length_char == 1 and t.chars.is_all_lower and t.is_char('м')) and t.next0_ is not None and t.next0_.is_char('.')): 
            if (MiscLocationHelper.is_user_param_address(t)): 
                tt = t.previous
                if (tt is not None and tt.is_comma): 
                    tt = tt.previous
                if (isinstance(tt, ReferentToken)): 
                    geo_ = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                    if (geo_ is not None and geo_.is_region): 
                        mm = OrgTypToken(t, t.next0_)
                        mm.vals.append("местечко")
                        return mm
        if (((t.length_char == 1 and t.next0_ is not None and t.next0_.is_hiphen) and t.is_value("П", None) and (isinstance(t.next0_.next0_, TextToken))) and t.next0_.next0_.is_value("Т", None)): 
            if (BracketHelper.is_bracket(t.next0_.next0_.next0_, True)): 
                return OrgTypToken(t, t.next0_.next0_, "пансионат")
            tt = t.previous
            if (tt is not None and tt.is_comma): 
                tt = tt.previous
            if (isinstance(tt, ReferentToken)): 
                geo_ = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                if (geo_ is not None and geo_.is_city and not geo_.is_big_city): 
                    return OrgTypToken(t, t.next0_.next0_, "пансионат")
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (ad is not None and OrgTypToken.SPEED_REGIME and ((ad.otregime or ad.all_regime))): 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            if (d is not None): 
                return d.org_typ
            return None
        if (ad.olevel > 2): 
            return None
        ad.olevel += 1
        res = OrgTypToken.__try_parse(t, after_terr, 0)
        ad.olevel -= 1
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', after_terr : bool, lev : int=0) -> 'OrgTypToken':
        from pullenti.ner.geo.internal.NameToken import NameToken
        if (t is None): 
            return None
        if (isinstance(t, TextToken)): 
            term = t.term
            if (term == "СП"): 
                if (not after_terr and t.chars.is_all_lower): 
                    return None
            if (term == "СТ"): 
                cit = CityItemToken.try_parse(t, None, False, None)
                if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN and cit.length_char > 3): 
                    return None
                tt = t.previous
                while tt is not None and (tt.end_char + 10) > t.begin_char: 
                    cit = CityItemToken.try_parse(tt, None, False, None)
                    if (cit is not None and cit.typ == CityItemToken.ItemType.NOUN and cit.end_char > t.begin_char): 
                        return None
                    tt = tt.previous
            if (term == "БО" and t.next0_ is not None and t.next0_.is_value("ЛЕТ", None)): 
                return None
            if (term == "ГО" and t.previous is not None): 
                if (t.previous.is_hiphen or (isinstance(t.previous, NumberToken))): 
                    return None
            if (term == "ПГТ"): 
                return None
            if (term == "НП"): 
                if (not after_terr and t.chars.is_all_lower): 
                    return None
            if (term == "АК"): 
                if (t.next0_ is not None and t.next0_.is_char('.')): 
                    return None
                if (not after_terr and t.chars.is_capital_upper): 
                    return None
            if (((((t.is_value("ОФИС", None) or term == "ФАД" or term == "АД") or term == "МИРА" or term == "МАЯ") or t.is_value("КОРПУС", None) or t.is_value("ПОЛК", None)) or t.is_value("ДИВИЗИЯ", None) or t.is_value("ГВАРДИЯ", None)) or t.is_value("АРМИЯ", None) or t.is_value("РОТА", None)): 
                return None
            if ((t.is_value("ФЕДЕРАЦИЯ", None) or t.is_value("СОЮЗ", None) or t.is_value("ПРЕФЕКТУРА", None)) or t.is_value("ОТДЕЛЕНИЕ", None)): 
                return None
            if (t.is_value("РАДИО", None) or t.is_value("АППАРАТ", None) or t.is_value("ДВИЖЕНИЕ", None)): 
                return None
            if (t.is_value("ГОРОДОК", None) and not MiscLocationHelper.is_user_param_address(t)): 
                return None
            if (t.is_value2("СО", "СТ")): 
                return None
            if (t.is_value("ПОЛЕ", None) and (isinstance(t.previous, TextToken))): 
                npt = NounPhraseHelper.try_parse(t.previous, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.end_token == t): 
                    return None
            if (t.is_value("РЕКА", None) and t.previous is not None): 
                if (t.previous.is_value("НАБЕРЕЖНАЯ", None) or t.previous.is_value("НАБ", None) or ((t.previous.previous is not None and t.previous.previous.is_value("НАБ", None)))): 
                    return None
            if (term == "АО"): 
                cou = 5
                tt = t.previous
                while tt is not None and cou > 0: 
                    ter = TerrItemToken.check_onto_item(tt)
                    if (ter is not None): 
                        if (ter.item is not None and "округ" in str(ter.item.referent)): 
                            return None
                    tt = tt.previous; cou -= 1
            if ((((term == "СХ" or term == "CX")) and t.next0_ is not None and t.next0_.is_hiphen) and t.next0_.next0_ is not None): 
                if (t.next0_.next0_.is_value("З", None) or (((isinstance(t.next0_.next0_, NumberToken)) and t.next0_.next0_.value == "3"))): 
                    return OrgTypToken(t, t.next0_.next0_, "совхоз")
            if (term.startswith("УЛ")): 
                sti = StreetItemToken.try_parse(t, None, False, None)
                if (sti is not None and sti.typ == StreetItemType.NOUN): 
                    next0__ = OrgTypToken.try_parse(sti.end_token.next0_, after_terr, None)
                    if (next0__ is not None): 
                        if ("ВЧ" in next0__.vals): 
                            next0__ = next0__.clone()
                            next0__.begin_token = t
                            return next0__
        t1 = None
        typs = None
        doubt = False
        notorg = False
        notgeo = False
        building = False
        canbesingle = False
        morph_ = None
        tok = OrgTypToken._m_ontology.try_parse(t, TerminParseAttr.NO)
        if ((tok is None and after_terr and (isinstance(t, TextToken))) and t.term == "СТ"): 
            tok = TerminToken._new562(t, t, OrgTypToken.__m_st)
        if (tok is not None): 
            if (tok.end_token.is_value("УЧАСТОК", None)): 
                tt = t.next0_
                while tt is not None and (tt.end_char < tok.end_char): 
                    if (tt.is_comma): 
                        return None
                    tt = tt.next0_
            val = tok.termin.canonic_text.lower()
            if (val == "аэропорт"): 
                if (t.is_value("А", None) and tok.end_token.is_value("П", None)): 
                    if (NumToken.try_parse(tok.end_token.next0_, GeoTokenType.ANY) is not None): 
                        return OrgTypToken._new1525(t, tok.end_token, "аптечный пункт", True)
            if (val == "гаражное товарищество" and (tok.length_char < 6)): 
                tt1 = t.previous
                if (tt1 is not None and tt1.is_char('.')): 
                    tt1 = tt1.previous
                if (tt1 is not None and tt1.is_value("П", None)): 
                    return None
            tt = tok.end_token.next0_
            first_pass3985 = True
            while True:
                if first_pass3985: first_pass3985 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (not (isinstance(tt, TextToken)) or tt.whitespaces_before_count > 2): 
                    break
                if ((tt.is_char('(') and (isinstance(tt.next0_, TextToken)) and (tt.next0_.length_char < 3)) and tt.next0_.next0_ is not None and tt.next0_.next0_.is_char(')')): 
                    tt = tt.next0_.next0_
                    tok.end_token = tt
                    continue
                if ((tt.is_value("ГРАЖДАНИН", None) or tt.is_value("ЗАСТРОЙЩИК", None) or tt.is_value("ГАРАЖ", None)) or tt.is_value("СОБСТВЕННИК", None)): 
                    if (not tt.chars.is_all_lower): 
                        if (tt.next0_ is None or tt.next0_.is_comma): 
                            break
                    tok.end_token = tt
                    val = "{0} {1}".format(val, tt.term.lower())
                else: 
                    break
            t1 = tok.end_token
            typs = list()
            morph_ = tok.morph
            notorg = tok.termin.tag3 is not None
            notgeo = tok.termin.tag2 is not None
            if ((isinstance(tok.termin.tag, StreetItemType)) and (Utils.valToEnum(tok.termin.tag, StreetItemType)) == StreetItemType.STDNAME): 
                canbesingle = True
            if (isinstance(tok.termin.tag, AddressItemType)): 
                building = (Utils.valToEnum(tok.termin.tag, AddressItemType)) == AddressItemType.BUILDING
            typs.append(val)
            if (tok.termin.acronym is not None): 
                typs.append(tok.termin.acronym)
            if (tok.end_token == t): 
                if ((t.length_char < 4) and (isinstance(t, TextToken)) and LanguageHelper.ends_with(t.term, "К")): 
                    oi = TerrItemToken.check_onto_item(t.next0_)
                    if (oi is not None): 
                        if (t.next0_.get_morph_class_in_dictionary().is_adjective and oi.begin_token == oi.end_token): 
                            pass
                        elif (MiscLocationHelper.is_user_param_address(t)): 
                            pass
                        else: 
                            return None
                    if ((not after_terr and t.chars.is_all_upper and t.next0_ is not None) and t.next0_.chars.is_all_upper and t.next0_.length_char > 1): 
                        return None
            if (tok.termin.canonic_text == "МЕСТОРОЖДЕНИЕ" and (isinstance(tok.end_token.next0_, TextToken)) and tok.end_token.next0_.chars.is_all_lower): 
                npt = NounPhraseHelper.try_parse(tok.end_token.next0_, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.chars.is_all_lower): 
                    tok.end_token = npt.end_token
            if (((t.length_char == 1 and t.next0_ is not None and t.next0_.is_char('.')) and (isinstance(t.next0_.next0_, TextToken)) and t.next0_.next0_.length_char == 1) and t.next0_.next0_.next0_ == tok.end_token and tok.end_token.is_char('.')): 
                ok2 = False
                if (canbesingle): 
                    ok2 = OrgTypToken.__check_piter(t)
                if (not ok2): 
                    if (t.chars.is_all_upper and t.next0_.next0_.chars.is_all_upper): 
                        return None
                    if (tok.termin.canonic_text == "ГАРАЖНОЕ ТОВАРИЩЕСТВО"): 
                        if (not t.is_whitespace_before and t.previous is not None and t.previous.is_char('.')): 
                            return None
        else: 
            if (StreetItemToken.check_keyword(t)): 
                return None
            rtok = t.kit.process_referent("ORGANIZATION", t, "MINTYPE")
            if (rtok is not None): 
                if (t.is_value("ДИВИЗИЯ", None) or t.is_value("АРМИЯ", None) or t.is_value("СЕКТОР", None)): 
                    return None
                ait = AddressItemToken.try_parse_pure_item(t, None, None)
                if (ait is not None and ait.typ != AddressItemType.NUMBER): 
                    return None
                if (rtok.end_token == t and t.is_value("ТК", None)): 
                    if (TerrItemToken.check_onto_item(t.next0_) is not None): 
                        return None
                    if (t.chars.is_all_upper and t.next0_ is not None and t.next0_.chars.is_all_upper): 
                        return None
                if (rtok.begin_token != rtok.end_token): 
                    tt = rtok.begin_token.next0_
                    first_pass3986 = True
                    while True:
                        if first_pass3986: first_pass3986 = False
                        else: tt = tt.next0_
                        if (not (tt is not None and tt.end_char <= rtok.end_char)): break
                        if (tt.length_char > 3): 
                            continue
                        next0__ = OrgTypToken.try_parse(tt, after_terr, None)
                        if (next0__ is not None and next0__.end_char > rtok.end_char): 
                            return None
                    if (str(rtok.referent).upper() == "ЖЕЛЕЗНАЯ ДОРОГА"): 
                        if (isinstance(rtok.end_token.next0_, TextToken)): 
                            if (rtok.end_token.next0_.term.startswith("СТ")): 
                                return None
                prof = rtok.referent.get_string_value("PROFILE")
                if (Utils.compareStrings(Utils.ifNotNull(prof, ""), "UNIT", True) == 0): 
                    doubt = True
                t1 = rtok.end_token
                typs = rtok.referent.get_string_values("TYPE")
                morph_ = rtok.morph
                if (t.is_value("БРИГАДА", None)): 
                    doubt = True
                if (len(typs) > 0): 
                    if (typs[0].endswith("центр") or typs[0].endswith("комплекс") or typs[0] == "бизнес квартал"): 
                        building = True
        if (((t1 is None and (isinstance(t, TextToken)) and t.length_char >= 2) and t.length_char <= 4 and t.chars.is_all_upper) and t.chars.is_cyrillic_letter): 
            if (AddressItemToken.try_parse_pure_item(t, None, None) is not None): 
                return None
            if (t.length_char == 2): 
                return None
            if (TerrItemToken.check_onto_item(t) is not None): 
                return None
            typs = list()
            typs.append(t.term)
            t1 = t
            doubt = True
        if (t1 is None): 
            return None
        if (morph_ is None): 
            morph_ = t1.morph
        res = OrgTypToken._new1526(t, t1, doubt, typs, morph_, notorg, notgeo, canbesingle, building)
        if (t.is_value("ОБЪЕДИНЕНИЕ", None)): 
            res.is_doubt = True
        elif ((isinstance(t, TextToken)) and t.term == "СО"): 
            res.is_doubt = True
        if (canbesingle): 
            if (res.length_char < 6): 
                if (not OrgTypToken.__check_piter(t)): 
                    return None
            return res
        if ((t == t1 and (t.length_char < 3) and t.next0_ is not None) and t.next0_.is_char('.')): 
            res.end_token = t1.next0_
        if ((lev < 2) and (res.whitespaces_after_count < 3)): 
            next0__ = OrgTypToken.try_parse(res.end_token.next0_, after_terr, None)
            if (next0__ is not None and "участок" in next0__.vals): 
                next0__ = (None)
            if (next0__ is not None and not next0__.begin_token.chars.is_all_lower): 
                nam = NameToken.try_parse(next0__.end_token.next0_, GeoTokenType.ORG, 0, False)
                if (nam is None or next0__.whitespaces_after_count > 3): 
                    next0__ = (None)
                elif ((nam.number is not None and nam.name is None and next0__.length_char > 2) and next0__.is_doubt): 
                    next0__ = (None)
            if (next0__ is not None): 
                if (not next0__.is_doubt): 
                    res.is_doubt = False
                res.merge_with(next0__)
            else: 
                t1 = res.end_token.next0_
                if (t1 is not None and (t1.whitespaces_before_count < 3)): 
                    if (t1.is_value("СН", None)): 
                        res.end_token = t1
        t1 = res.end_token
        if ((t1.next0_ is not None and t1.next0_.is_and and t1.next0_.next0_ is not None) and ((t1.next0_.next0_.is_value("ПОСТРОЙКА", None) or t1.next0_.next0_.is_value("ХОЗПОСТРОЙКА", None)))): 
            res.end_token = t1.next0_.next0_
        return res
    
    @staticmethod
    def __check_piter(t : 'Token') -> bool:
        if (MiscLocationHelper.is_user_param_gar_address(t)): 
            return True
        cou = 0
        ttt = t.previous
        while ttt is not None and (cou < 20): 
            if (ttt.is_value("ПЕТЕРБУРГ", None) or ttt.is_value("СПБ", None) or ttt.is_value("ЛЕНИНГРАД", None)): 
                return True
            ttt = ttt.previous; cou += 1
        ttt = t.next0_
        while ttt is not None and cou > 0: 
            if (ttt.is_value("ПЕТЕРБУРГ", None) or ttt.is_value("СПБ", None) or ttt.is_value("ЛЕНИНГРАД", None)): 
                return True
            ttt = ttt.next0_; cou -= 1
        return False
    
    def merge_with(self, ty : 'OrgTypToken') -> None:
        is_fku = False
        for v in ty.vals: 
            if (not v in self.vals): 
                if (is_fku): 
                    self.vals.insert(0, v)
                else: 
                    self.vals.append(v)
        if (not ty.not_org): 
            self.not_org = False
        self.end_token = ty.end_token
    
    @staticmethod
    def find_termin_by_acronym(abbr : str) -> typing.List['Termin']:
        te = Termin._new1166(abbr, abbr)
        return OrgTypToken._m_ontology.find_termins_by_termin(te)
    
    __m_st = None
    
    @staticmethod
    def initialize() -> None:
        OrgTypToken._m_ontology = TerminCollection()
        t = Termin._new1166("САДОВОЕ ТОВАРИЩЕСТВО", "СТ")
        t.add_variant("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        t.acronym = "СТ"
        t.add_abridge("С/ТОВ")
        t.add_abridge("ПК СТ")
        t.add_abridge("САД.ТОВ.")
        t.add_abridge("САДОВ.ТОВ.")
        t.add_abridge("С/Т")
        t.add_variant("ВЕДЕНИЕ ГРАЖДАНАМИ САДОВОДСТВА ИЛИ ОГОРОДНИЧЕСТВА ДЛЯ СОБСТВЕННЫХ НУЖД", False)
        OrgTypToken.__m_st = t
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ДАЧНОЕ ТОВАРИЩЕСТВО", "ДТ", True)
        t.add_abridge("Д/Т")
        t.add_abridge("ДАЧ/Т")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ЖИЛИЩНОЕ ТОВАРИЩЕСТВО", "ЖТ", True)
        t.add_abridge("Ж/Т")
        t.add_abridge("ЖИЛ/Т")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("САДОВЫЙ КООПЕРАТИВ", "СК", True)
        t.add_variant("САДОВОДЧЕСКИЙ КООПЕРАТИВ", False)
        t.add_abridge("С/К")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ПК", True)
        t.add_variant("ПОТРЕБКООПЕРАТИВ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПОТРЕБИТЕЛЬСКИЙ САДОВОДЧЕСКИЙ КООПЕРАТИВ")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("САДОВОЕ ОБЩЕСТВО", "СО", True)
        t.add_variant("САДОВОДЧЕСКОЕ ОБЩЕСТВО", False)
        t.add_variant("САДОВОДСТВО", False)
        t.add_abridge("С/О")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ПОТРЕБИТЕЛЬСКОЕ САДОВОДЧЕСКОЕ ОБЩЕСТВО", "ПСО", True)
        t.add_variant("ПОТРЕБИТЕЛЬСКОЕ САДОВОЕ ОБЩЕСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("САДОВОЕ ТОВАРИЩЕСКОЕ ОБЩЕСТВО", "СТО", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("САДОВОЕ ПОТРЕБИТЕЛЬСКОЕ ОБЩЕСТВО", "СПО", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("САДОВОДЧЕСКОЕ ДАЧНОЕ ТОВАРИЩЕСТВО", "СДТ", True, True)
        t.add_variant("САДОВОЕ ДАЧНОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", "ДНО", True, True)
        t.add_variant("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ ГРАЖДАН", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", "ДНП", True, True)
        t.add_variant("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО ГРАЖДАН", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "ДНТ", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ДАЧНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ")
        t.acronym = "ДПК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ДАЧНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ДСК", True, True)
        t.add_variant("ДАЧНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", "СПК", True, True)
        t.add_variant("СПКСТ", False)
        t.add_variant("СПК СТ", False)
        t.add_abridge("СПК(СТ)")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ВОДНО МОТОРНЫЙ КООПЕРАТИВ", "ВМК", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "СНТ", True, True)
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        t.add_abridge("САДОВ.НЕКОМ.ТОВ.")
        t.add_variant("ТСНСТ", False)
        t.add_abridge("САДОВОЕ НЕКОМ-Е ТОВАРИЩЕСТВО")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", "СНО", True, True)
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("САДОВО ОГОРОДНОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", "СОНО", True, True)
        t.add_variant("САДОВО ОГОРОДНОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ ГРАЖДАН", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", "СНП", True, True)
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("САДОВОДЧЕСКИЙ НЕКОММЕРЧЕСКИЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "СНПК", True, True)
        t.add_variant("САДОВЫЙ НЕКОММЕРЧЕСКИЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "СНТ", True, True)
        t.add_variant("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("САДОВОДЧЕСКОЕ ОГОРОДНИЧЕСКОЕ ТОВАРИЩЕСТВО", "СОТ", True, True)
        t.add_variant("САДОВОЕ ОГОРОДНИЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "ДНТ", True, True)
        t.add_variant("ДАЧНО НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("НЕКОММЕРЧЕСКОЕ САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", "НСТ", True, True)
        t.add_variant("НЕКОММЕРЧЕСКОЕ САДОВОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ОБЪЕДИНЕННОЕ НЕКОММЕРЧЕСКОЕ САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО", "ОНСТ", True, True)
        t.add_variant("ОБЪЕДИНЕННОЕ НЕКОММЕРЧЕСКОЕ САДОВОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("САДОВОДЧЕСКАЯ ПОТРЕБИТЕЛЬСКАЯ КООПЕРАЦИЯ", "СПК", True, True)
        t.add_variant("САДОВАЯ ПОТРЕБИТЕЛЬСКАЯ КООПЕРАЦИЯ", False)
        t.add_variant("САДОВОДЧЕСКИЙ ПОТРЕБИТЕЛЬНЫЙ КООПЕРАТИВ", False)
        t.add_variant("САДОВОДЧЕСКИЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ДАЧНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ДСК", True, True)
        t.add_variant("ДАЧНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", False)
        OrgTypToken._m_ontology.add(t)
        OrgTypToken._m_ontology.add(Termin._new1537("ДАЧНО СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", "ДСПК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("ЖИЛИЩНЫЙ СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ", "ЖСПК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("ЖИЛИЩНЫЙ СТРОИТЕЛЬНО ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "ЖСПКИЗ", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("ЖИЛИЩНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ЖСК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("ЖИЛИЩНЫЙ СТРОИТЕЛЬНЫЙ КООПЕРАТИВ ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "ЖСКИЗ", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("ЖИЛИЩНОЕ СТРОИТЕЛЬНОЕ ТОВАРИЩЕСТВО", "ЖСТ", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("ПОТРЕБИТЕЛЬСКОЕ ОБЩЕСТВО ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "ПОТЗ", True, True))
        t = Termin._new1537("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ОБЪЕДИНЕНИЕ", "ОНО", True, True)
        t.add_variant("ОГОРОДНИЧЕСКОЕ ОБЪЕДИНЕНИЕ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО", "ОНП", True, True)
        t.add_variant("ОГОРОДНИЧЕСКОЕ ПАРТНЕРСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ОГОРОДНИЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО", "ОНТ", True, True)
        t.add_variant("ОГОРОДНИЧЕСКОЕ ТОВАРИЩЕСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ОГОРОДНИЧЕСКИЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ОПК", True, True)
        t.add_variant("ОГОРОДНИЧЕСКИЙ КООПЕРАТИВ", False)
        OrgTypToken._m_ontology.add(t)
        OrgTypToken._m_ontology.add(Termin._new1537("ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "СТСН", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "ТСН", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("САДОВОДЧЕСКОЕ ТОВАРИЩЕСТВО ЧАСТНЫХ ВЛАДЕЛЬЦЕВ", "СТЧВ", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("ТОВАРИЩЕСТВО СОБСТВЕННИКОВ ЖИЛЬЯ", "ТСЖ", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("ТОВАРИЩЕСТВО СОБСТВЕННИКОВ ЖИЛЬЯ КЛУБНОГО ПОСЕЛКА", "ТСЖКП", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("САДОВЫЕ ЗЕМЕЛЬНЫЕ УЧАСТКИ", "СЗУ", True, True))
        OrgTypToken._m_ontology.add(Termin._new1537("ТОВАРИЩЕСТВО ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "ТИЗ", True, True))
        t = Termin._new1537("КОЛЛЕКТИВ ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ", "КИЗ", True, True)
        t.add_variant("КИЗК", False)
        OrgTypToken._m_ontology.add(t)
        OrgTypToken._m_ontology.add(Termin._new1537("ОБЩЕСТВО ИНДИВИДУАЛЬНЫХ ЗАСТРОЙЩИКОВ ГАРАЖЕЙ", "ОИЗГ", True, True))
        t = Termin("БЛОК ГАРАЖЕЙ")
        t.add_variant("ГАРАЖНЫЙ БЛОК", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("САДОВОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", "СНТСН", True, True)
        t.add_variant("САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ", False)
        t.add_variant("СНТ СН", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ПОТРЕБИТЕЛЬСКОЕ ГАРАЖНО СТРОИТЕЛЬНОЕ ОБЩЕСТВО", "ПГСО", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ПОТРЕБИТЕЛЬСКОЕ КООПЕРАТИВНОЕ ОБЩЕСТВО ГАРАЖЕЙ", "ПКОГ", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО ГАРАЖНЫЙ КООПЕРАТИВ", "НПГК", True, True)
        t.add_abridge("НП ГК")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО СОБСТВЕННИКОВ", "НПС", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("СУБЪЕКТ МАЛОГО ПРЕДПРИНИМАТЕЛЬСТВА", "СМП", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1537("ЛИЧНОЕ ПОДСОБНОЕ ХОЗЯЙСТВО", "ЛПХ", True, True)
        t.add_variant("ПОДХОЗ", False)
        t.add_abridge("ПОД.ХОЗ.")
        t.add_abridge("П/Х")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ИНДИВИДУАЛЬНОЕ САДОВОДСТВО", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("КОЛЛЕКТИВНЫЙ ГАРАЖ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("КОМПЛЕКС ГАРАЖЕЙ", 1)
        t.add_variant("РАЙОН ГАРАЖЕЙ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ГАРАЖНЫЙ МАССИВ", 1)
        t.add_variant("ГАРАЖНЫЙ УЧАСТОК", False)
        OrgTypToken._m_ontology.add(t)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ПЛОЩАДКА ГАРАЖЕЙ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("КОЛЛЕКТИВНЫЙ САД", 1)
        t.add_abridge("КОЛ.САД")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("САД", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("КОМПЛЕКС ЗДАНИЙ И СООРУЖЕНИЙ", 1)
        t.add_variant("КОМПЛЕКС СТРОЕНИЙ И СООРУЖЕНИЙ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("КОМПЛЕКС ПРОИЗВОДСТВЕННЫХ ЗДАНИЙ", 1)
        t.add_variant("КОМПЛЕКС ПРОИЗВОДСТВЕННЫХ СТРОЕНИЙ", False)
        t.add_variant("КОМПЛЕКС ПРОИЗВОДСТВЕННЫХ ЗДАНИЙ И СООРУЖЕНИЙ", False)
        t.add_variant("КОМПЛЕКС ПРОИЗВОДСТВЕННЫХ СТРОЕНИЙ И СООРУЖЕНИЙ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ОБЪЕДИНЕНИЕ")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ПРОМЫШЛЕННАЯ ПЛОЩАДКА", 1)
        t.add_variant("ПРОМПЛОЩАДКА", False)
        t.add_abridge("ПРОМ.ПЛОЩАДКА")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ПРОИЗВОДСТВЕННАЯ ПЛОЩАДКА", 1)
        t.add_abridge("ПРОИЗВ.ПЛОЩАДКА")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ИМУЩЕСТВЕННЫЙ КОМПЛЕКС", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin("СОВМЕСТНОЕ ПРЕДПРИЯТИЕ")
        t.acronym = "СП"
        t.acronym_can_be_lower = True
        OrgTypToken._m_ontology.add(t)
        t = Termin("НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО")
        t.acronym = "НП"
        t.acronym_can_be_lower = True
        OrgTypToken._m_ontology.add(t)
        t = Termin("АВТОМОБИЛЬНЫЙ КООПЕРАТИВ")
        t.add_variant("АВТОКООПЕРАТИВ", False)
        t.add_variant("АВТО КООПЕРАТИВ", False)
        t.add_abridge("А/К")
        t.acronym = "АК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_ontology.add(t)
        t = Termin("ГАРАЖНЫЙ КООПЕРАТИВ")
        t.add_abridge("Г/К")
        t.add_abridge("ГР.КОП.")
        t.add_abridge("ГАР.КОП.")
        t.add_abridge("ГАР.КООП.")
        t.add_variant("ГАРАЖНЫЙ КООП", False)
        t.add_variant("ГАРАЖНЫЙ КВАРТАЛ", False)
        t.acronym = "ГК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_ontology.add(t)
        t = Termin("АВТОГАРАЖНЫЙ КООПЕРАТИВ")
        t.add_variant("АВТО ГАРАЖНЫЙ КООПЕРАТИВ", False)
        t.acronym = "АГК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_ontology.add(t)
        t = Termin("ГАРАЖНОЕ ТОВАРИЩЕСТВО")
        t.add_abridge("Г/Т")
        t.add_abridge("ГР.ТОВ.")
        t.add_abridge("ГАР.ТОВ.")
        t.add_abridge("ГАР.ТОВ-ВО")
        t.acronym = "ГТ"
        t.acronym_can_be_lower = True
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ГАРАЖНОЕ ОБЩЕСТВО", "ГО", True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ПЛОЩАДКА ГАРАЖЕЙ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ГАРАЖНЫЙ КОМПЛЕКС", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПРОИЗВОДСТВЕННЫЙ СЕЛЬСКОХОЗЯЙСТВЕННЫЙ КООПЕРАТИВ")
        t.add_variant("ПРОИЗВОДСТВЕННО СЕЛЬСКОХОЗЯЙСТВЕННЫЙ КООПЕРАТИВ", False)
        t.acronym = "ПСК"
        t.acronym_can_be_lower = True
        OrgTypToken._m_ontology.add(t)
        OrgTypToken._m_ontology.add(Termin._new1535("ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ГСК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("ГАРАЖНО САРАЙНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ГССК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("ГАРАЖНО ЭКСПЛУАТАЦИОННЫЙ КООПЕРАТИВ", "ГЭК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("ГАРАЖНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ГПК", True, True))
        t = Termin._new1535("КООПЕРАТИВ ПО СТРОИТЕЛЬСТВУ И ЭКСПЛУАТАЦИИ ГАРАЖЕЙ", "КСЭГ", True, True)
        t.add_variant("КСИЭГ", False)
        t.add_variant("КССГ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("ГАРАЖНЫЙ ЭКСПЛУАТАЦИОННО-СТРОИТЕЛЬНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ГЭСПК", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("КООПЕРАТИВ ПО СТРОИТЕЛЬСТВУ ГАРАЖЕЙ", "КСГ", True, True)
        t.add_variant("КССГ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("КОЛЛЕКТИВНАЯ СТОЯНКА ГАРАЖЕЙ")
        t.add_variant("КОЛЛЕКТИВНАЯ ГАРАЖНАЯ СТОЯНКА", False)
        t.add_variant("КОЛЛЕКТИВНЫЙ ГАРАЖ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("КОЛЛЕКТИВНАЯ ЗАСТРОЙКА ИНДИВИДУАЛЬНЫХ ГАРАЖЕЙ")
        OrgTypToken._m_ontology.add(t)
        OrgTypToken._m_ontology.add(Termin._new1535("ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ПГСК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНО ЭКСПЛУАТАЦИОННЫЙ КООПЕРАТИВ", "ПГЭК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("ОБЩЕСТВЕННО ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНЫЙ КООПЕРАТИВ", "ОПГК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("ГАРАЖНЫЙ СТРОИТЕЛЬНО ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ", "ГСПК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("КООПЕРАТИВ ПО СТРОИТЕЛЬСТВУ И ЭКСПЛУАТАЦИИ ИНДИВИДУАЛЬНЫХ ГАРАЖЕЙ", "КСЭИГ", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНЫЙ КООПЕРАТИВ", "ПГК", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("ПОТРЕБИТЕЛЬСКОЕ ГАРАЖНОЕ ОБЩЕСТВО", "ПГО", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("ИНДИВИДУАЛЬНОЕ ЖИЛИЩНОЕ СТРОИТЕЛЬСТВО", "ИЖС", True, True))
        OrgTypToken._m_ontology.add(Termin._new1535("ИНДИВИДУАЛЬНЫЙ ГАРАЖНО СТРОИТЕЛЬНЫЙ КООПЕРАТИВ", "ИГСК", True, True))
        OrgTypToken._m_ontology.add(Termin("ЖИВОТНОВОДЧЕСКАЯ ТОЧКА"))
        t = Termin._new1614("ДАЧНАЯ ЗАСТРОЙКА", "ДЗ", True, 1)
        t.add_variant("КВАРТАЛ ДАЧНОЙ ЗАСТРОЙКИ", False)
        t.add_variant("ЗОНА ДАЧНОЙ ЗАСТРОЙКИ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1615("КОТТЕДЖНЫЙ ПОСЕЛОК", "КП", True, 1, 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1615("ДАЧНЫЙ ПОСЕЛОК", "ДП", True, 1, 1)
        t.add_abridge("Д/П")
        t.add_variant("ДАЧНЫЙ ПОСЕЛОК МАССИВ", False)
        t.add_variant("ДП МАССИВ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1617("САДОВОДЧЕСКИЙ МАССИВ", 1, 1)
        t.add_variant("САД. МАССИВ", False)
        t.add_variant("САДОВЫЙ МАССИВ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("САНАТОРИЙ")
        t.add_abridge("САН.")
        t.add_variant("САНАТОРИЙ-ПРОФИЛАКТОРИЙ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПАНСИОНАТ")
        t.add_abridge("ПАНС.")
        t.add_variant("ТУРИСТИЧЕСКИЙ ПАНСИОНАТ", False)
        t.add_abridge("ТУР.ПАНСИОНАТ")
        t.add_variant("ПАНСИОНАТ С ЛЕЧЕНИЕМ", False)
        t.add_variant("ПАНСИОНАТ ОТДЫХА", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПРОФИЛАКТОРИЙ")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ДЕТСКИЙ ГОРОДОК", 1)
        t.add_abridge("ДЕТ.ГОРОДОК")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1166("ДОМ ОТДЫХА", "ДО")
        t.add_abridge("Д/О")
        OrgTypToken._m_ontology.add(t)
        t = Termin("МЕСТО ОТДЫХА")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("БАЗА ОТДЫХА", "БО", True)
        t.add_abridge("Б/О")
        t.add_variant("БАЗА ОТДЫХА РЫБАКА И ОХОТНИКА", False)
        t.add_variant("БАЗА ОТДЫХА СЕМЕЙНОГО ТИПА", False)
        t.add_variant("БАЗА ОХОТХОЗЯЙСТВА", False)
        t.add_variant("БАЗА ОХОТОХОЗЯЙСТВА", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ТУРИСТИЧЕСКАЯ БАЗА", "ТБ", True)
        t.add_abridge("Т/Б")
        t.add_variant("ТУРБАЗА", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПАКР ОТЕЛЬ")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("ФЕРМЕРСКОЕ ХОЗЯЙСТВО", "ФХ", True, True)
        t.add_abridge("Ф/Х")
        t.add_abridge("ФЕРМЕРСКОЕ Х-ВО")
        t.add_abridge("ФЕРМЕРСКОЕ ХОЗ-ВО")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("КРЕСТЬЯНСКОЕ ХОЗЯЙСТВО", "КХ", True, True)
        t.add_abridge("К/Х")
        t.add_abridge("КРЕСТЬЯНСКОЕ Х-ВО")
        t.add_abridge("КРЕСТЬЯНСКОЕ ХОЗ-ВО")
        t.add_abridge("КР.Х-ВО")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("КРЕСТЬЯНСКОЕ ФЕРМЕРСКОЕ ХОЗЯЙСТВО", "КФХ", True, True)
        t.add_variant("КРЕСТЬЯНСКОЕ (ФЕРМЕРСКОЕ) ХОЗЯЙСТВО", False)
        t.add_abridge("К.Ф.Х.")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("САД-ОГОРОД", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("ОВЦЕВОДЧЕСКАЯ ТОВАРНАЯ ФЕРМА", "ОТФ", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin("МОЛОЧНАЯ ФЕРМА")
        OrgTypToken._m_ontology.add(t)
        t = Termin("СЕМЕННОЙ ЦЕНТР")
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПИТОМНИК")
        t.add_variant("ПИТОМНИК РАСТЕНИЙ", False)
        t.add_variant("ПИТОМНИК ДЕКОРАТИВНЫХ РАСТЕНИЙ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПЛЕМЕННОЙ ПИТОМНИК")
        t.add_variant("ПЛЕМПИТОМНИК", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПЛЕМЕННОЙ ЗАВОД")
        t.add_variant("ПЛЕМЗАВОД", False)
        t.add_abridge("ПЛЕМ.ЗАВОД")
        OrgTypToken._m_ontology.add(t)
        t = Termin("СЕЛЬХОЗАРТЕЛЬ")
        t.add_variant("СЕЛЬСКОХОЗЯЙСТВЕННАЯ АТРЕЛЬ", False)
        t.add_variant("СЕЛЬСКО ХОЗЯЙСТВЕННАЯ АТРЕЛЬ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("АГРОПРОМЫШЛЕННЫЙ КОМПЛЕКС")
        t.add_variant("АГРОКОМПЛЕКС", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("АГРОПРОМЫШЛЕННЫЙ ПАРК")
        t.add_variant("АГРОПАРК", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("УЧЕБНОЕ ХОЗЯЙСТВО", "УХ", True)
        t.add_abridge("У/Х")
        t.add_variant("УЧХОЗ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ЗАВОД")
        t.add_variant("ЗВД", False)
        t.add_abridge("З-Д")
        t.add_abridge("З-ДА")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("НЕФТЕПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД", "НПЗ", True, True)
        t.add_variant("НЕФТЕ ПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("ГАЗОПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД", "ГПЗ", True, True)
        t.add_variant("ГАЗО ПЕРЕРАБАТЫВАЮЩИЙ ЗАВОД", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("КОМБИКОРМОВЫЙ ЗАВОД")
        OrgTypToken._m_ontology.add(t)
        t = Termin("ФАБРИКА")
        t.add_variant("Ф-КА", False)
        t.add_variant("Ф-КИ", False)
        t.add_abridge("ФАБР.")
        OrgTypToken._m_ontology.add(t)
        t = Termin("СОВХОЗ")
        t.add_variant("СВХ", False)
        t.add_abridge("С-ЗА")
        t.add_abridge("С/ЗА")
        t.add_abridge("С/З")
        t.add_abridge("СХ.")
        t.add_abridge("С/Х")
        OrgTypToken._m_ontology.add(t)
        t = Termin("КОЛХОЗ")
        t.add_variant("КЛХ", False)
        t.add_abridge("К-ЗА")
        t.add_abridge("К/ЗА")
        t.add_abridge("К/З")
        t.add_abridge("КХ.")
        t.add_abridge("К/Х")
        OrgTypToken._m_ontology.add(t)
        t = Termin("РЫБНОЕ ХОЗЯЙСТВО")
        t.add_variant("РЫБХОЗ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ЖИВОТНОВОДЧЕСКИЙ КОМПЛЕКС")
        OrgTypToken._m_ontology.add(t)
        t = Termin("ЖИВОТНОВОДЧЕСКАЯ СТОЯНКА")
        OrgTypToken._m_ontology.add(t)
        t = Termin("ЖИВОТНОВОДЧЕСКОЕ ТОВАРИЩЕСТВО")
        OrgTypToken._m_ontology.add(t)
        t = Termin("ХОЗЯЙСТВО")
        t.add_abridge("ХОЗ-ВО")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("СЕЛЬСКОХОЗЯЙСТВЕННАЯ ЗЕМЛЯ", 1)
        t.add_variant("СЕЛЬХОЗ ЗЕМЛЯ", False)
        t.add_abridge("С/Х ЗЕМЛЯ")
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПИОНЕРСКИЙ ЛАГЕРЬ")
        t.add_abridge("П/Л")
        t.add_abridge("П.Л.")
        t.add_abridge("ПИОНЕР.ЛАГ.")
        t.add_variant("ПИОНЕРЛАГЕРЬ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("СПОРТИВНЫЙ ЛАГЕРЬ")
        t.add_variant("СПОРТЛАГЕРЬ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ОЗДОРОВИТЕЛЬНЫЙ ЛАГЕРЬ", "ОЛ", True)
        t.add_abridge("О/Л")
        t.add_abridge("О.Л.")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ОЗДОРОВИТЕЛЬНО ОБРАЗОВАТЕЛЬНЫЙ ЛАГЕРЬ", "ООЛ", True)
        t.add_abridge("О/Л")
        t.add_abridge("О.Л.")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ДЕТСКИЙ ОЗДОРОВИТЕЛЬНЫЙ ЛАГЕРЬ", "ДОЛ", True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ДЕТСКИЙ СПОРТИВНЫЙ ЛАГЕРЬ", "ДСЛ", True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ДЕТСКИЙ ОЗДОРОВИТЕЛЬНО ОБРАЗОВАТЕЛЬНЫЙ ЛАГЕРЬ", "ДООЛ", True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ДЕТСКИЙ ОЗДОРОВИТЕЛЬНЫЙ КОМПЛЕКС", "ДОК", True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ДЕТСКИЙ ОЗДОРОВИТЕЛЬНО ОБРАЗОВАТЕЛЬНЫЙ КОМПЛЕКС", "ДООК", True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ДЕТСКИЙ ОЗДОРОВИТЕЛЬНО ОБРАЗОВАТЕЛЬНЫЙ ЦЕНТР", "ДООЦ", True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ДЕТСКИЙ ОЗДОРОВИТЕЛЬНО ОБРАЗОВАТЕЛЬНЫЙ ПРОФИЛЬНЫЙ ЦЕНТР", "ДООПЦ", True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ДЕТСКИЙ ОЗДОРОВИТЕЛЬНО ОБРАЗОВАТЕЛЬНЫЙ СПОРТИВНЫЙ ЦЕНТР", "ДООСЦ", True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ОЗДОРОВИТЕЛЬНЫЙ КОМПЛЕКС", "ОК", True)
        t.add_abridge("О/К")
        t.add_abridge("О.К.")
        OrgTypToken._m_ontology.add(t)
        t = Termin("СПОРТИВНО ОЗДОРОВИТЕЛЬНЫЙ ЛАГЕРЬ")
        OrgTypToken._m_ontology.add(t)
        t = Termin("СПОРТИВНО ОЗДОРОВИТЕЛЬНАЯ БАЗА")
        OrgTypToken._m_ontology.add(t)
        t = Termin("КУРОРТ")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("КОЛЛЕКТИВ ИНДИВИДУАЛЬНЫХ ВЛАДЕЛЬЦЕВ", "КИВ", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПОДСОБНОЕ ХОЗЯЙСТВО")
        t.add_abridge("ПОДСОБНОЕ Х-ВО")
        t.add_abridge("ПОДСОБНОЕ ХОЗ-ВО")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("АЭРОПОРТ", 1)
        t.add_abridge("А/П")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("АЭРОДРОМ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ГИДРОУЗЕЛ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ГИДРОТЕХНИЧЕСКИЙ КОМПЛЕКС", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ВОДОЗАБОР", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ВОДОХРАНИЛИЩЕ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("МОРСКОЙ ПОРТ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("РЕЧНОЙ ПОРТ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("СКЛАД", 1)
        t.add_variant("ЦЕНТРАЛЬНЫЙ СКЛАД", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ОВОЩЕХРАНИЛИЩЕ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("СВИНОКОМПЛЕКС", 1)
        t.add_variant("СВИНОВОДЧЕСКИЙ КОМПЛЕКС", False)
        t.add_variant("СВИНОКОМПЛЕКС СК", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ПОЛЕ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ПОЛЕВОЙ СТАН", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ГУРТ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("КОШАРА", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЧАБАНСКАЯ СТОЯНКА", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЛИЦЕНЗИОННЫЙ УЧАСТОК", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("УРОЧИЩЕ", 1)
        t.add_abridge("УР-ЩЕ")
        t.add_abridge("УР.")
        t.add_abridge("УРОЧ.")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ПАДЬ", 1)
        t.add_variant("ПЯДЬ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ПАРК", 1)
        t.add_variant("ПРИРОДНЫЙ ПАРК", False)
        t.add_variant("НАЦИОНАЛЬНЫЙ ПАРК", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1663("ПАРК КУЛЬТУРЫ И ОТДЫХА", "ПКО", 1)
        t.add_variant("ПКИО", False)
        t.add_variant("ПАРК РАЗВЛЕЧЕНИЙ", False)
        t.add_variant("ПАРК СЕМЕЙНОГО ОТДЫХА", False)
        t.add_variant("ГОРОДСКОЙ ПАРК КУЛЬТУРЫ И ОТДЫХА", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЗАИМКА", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("МЫС", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("РЕКА", 1)
        t.add_variant("РЕЧКА", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("БЕРЕГ РЕКИ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ОСТРОВ", 1)
        t.add_abridge("О-В")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ИСТОРИЧЕСКИЙ РАЙОН", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("СВАЛКА БЫТОВЫХ ОТХОДОВ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin("МУЗЕЙ")
        t.add_variant("МУЗЕЙ УСАДЬБА", False)
        t.add_variant("МУЗЕЙ ЗАПОВЕДНИК", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("КЛАДБИЩЕ", 1)
        t.add_abridge("КЛ-ЩЕ")
        t.add_variant("ГОРОДСКОЕ КЛАДБИЩЕ", False)
        t.add_variant("ПРАВОСЛАВНОЕ КЛАДБИЩЕ", False)
        t.add_variant("МУСУЛЬМАНСКОЕ КЛАДБИЩЕ", False)
        t.add_variant("ВОИНСКОЕ КЛАДБИЩЕ", False)
        t.add_variant("МЕМОРИАЛЬНОЕ КЛАДБИЩЕ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("БАЗА")
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПРОИЗВОДСТВЕННАЯ БАЗА")
        t.add_variant("БАЗА ПРОИЗВОДСТВЕННОГО ОБЕСПЕЧЕНИЯ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ПРОМЫШЛЕННАЯ БАЗА")
        t.add_variant("ПРОМБАЗА", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin("СТРОИТЕЛЬНАЯ БАЗА")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1166("СТРОИТЕЛЬНО МОНТАЖНОЕ УПРАВЛЕНИЕ", "СМУ")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ВОЙСКОВАЯ ЧАСТЬ", "ВЧ", True)
        t.add_variant("ВОИНСКАЯ ЧАСТЬ", False)
        t.add_variant("ВОИН. ЧАСТЬ", False)
        t.add_variant("ВОЙСК. ЧАСТЬ", False)
        t.add_variant("ВОЕННАЯ ЧАСТЬ", False)
        t.add_variant("ВОЕН. ЧАСТЬ", False)
        t.add_variant("ВОЕНЧАСТЬ", False)
        t.add_abridge("В/Ч")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("ПОЖАРНАЯ ЧАСТЬ", "ПЧ", True)
        t.add_abridge("ПОЖ. ЧАСТЬ")
        t.add_abridge("П/Ч")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1617("ВОЕННЫЙ ГОРОДОК", 1, 1)
        t.add_abridge("В.ГОРОДОК")
        t.add_abridge("В/Г")
        t.add_abridge("В/ГОРОДОК")
        t.add_abridge("В/ГОР")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("СТРОИТЕЛЬНОЕ УПРАВЛЕНИЕ", "СУ", True)
        t.add_abridge("С/У")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("МЕСТЕЧКО", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1617("ГОРОДОК", 1, 1)
        t.add_variant("ВАГОН ГОРОДОК", False)
        OrgTypToken._m_ontology.add(t)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1679("МІСТЕЧКО", MorphLang.UA, 1, MorphGender.NEUTER, 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1617("HILL", 1, 1)
        t.add_abridge("HL.")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1445("КВАРТИРНО ЭКСПЛУАТАЦИОННАЯ ЧАСТЬ", "КЭЧ", True)
        OrgTypToken._m_ontology.add(t)
        OrgTypToken._m_ontology.add(Termin._new1583("КАРЬЕР", 1))
        OrgTypToken._m_ontology.add(Termin._new1583("РУДНИК", 1))
        OrgTypToken._m_ontology.add(Termin._new1583("ПРИИСК", 1))
        OrgTypToken._m_ontology.add(Termin._new1583("РАЗРЕЗ", 1))
        OrgTypToken._m_ontology.add(Termin._new1583("ФАКТОРИЯ", 1))
        t = Termin._new1583("МЕСТОРОЖДЕНИЕ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЛОКАЛЬНОЕ ПОДНЯТИЕ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("НЕФТЯНОЕ МЕСТОРОЖДЕНИЕ", 1)
        t.add_variant("МЕСТОРОЖДЕНИЕ НЕФТИ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1690("ГАЗОВОЕ МЕСТОРОЖДЕНИЕ", "ГМ", True, True, 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1690("НЕФТЕГАЗОВОЕ МЕСТОРОЖДЕНИЕ", "НГМ", True, True, 1)
        t.add_variant("НЕФТЯНОЕ ГАЗОВОЕ МЕСТОРОЖДЕНИЕ", False)
        t.add_variant("ГАЗОНЕФТЯНОЕ МЕСТОРОЖДЕНИЕ", False)
        t.add_variant("ГАЗОВО НЕФТЯНОЕ МЕСТОРОЖДЕНИЕ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1690("НЕФТЕГАЗОКОНДЕНСАТНОЕ МЕСТОРОЖДЕНИЕ", "НГКМ", True, True, 1)
        t.add_variant("НЕФТЕГАЗОВОЕ КОНДЕНСАТНОЕ МЕСТОРОЖДЕНИЕ", False)
        t.add_variant("НЕФТЕГАЗОВОКОНДЕНСАТНОЕ МЕСТОРОЖДЕНИЕ", False)
        t.add_variant("НЕФТЕГАЗКОНДЕНСАТНОЕ МЕСТОРОЖДЕНИЕ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1690("ГАЗОВОНЕФТЕКОНДЕНСАТНОЕ МЕСТОРОЖДЕНИЕ", "ГНКМ", True, True, 1)
        t.add_variant("ГАЗОВО НЕФТЕ КОНДЕНСАТНОЕ МЕСТОРОЖДЕНИЕ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1690("ГАЗОКОНДЕНСАТНОЕ МЕСТОРОЖДЕНИЕ", "ГКМ", True, True, 1)
        t.add_variant("ГАЗОВОЕ КОНДЕНСАТНОЕ МЕСТОРОЖДЕНИЕ", False)
        t.add_variant("ГАЗОВОКОНДЕНСАТНОЕ МЕСТОРОЖДЕНИЕ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("НЕФТЕПЕРЕКАЧИВАЮЩАЯ СТАНЦИЯ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЛОДОЧНАЯ СТАНЦИЯ", 1)
        OrgTypToken._m_ontology.add(t)
        OrgTypToken._m_ontology.add(Termin._new1583("ЛЕСНОЙ ТЕРМИНАЛ", 1))
        OrgTypToken._m_ontology.add(Termin._new1583("МОЛОЧНЫЙ КОМПЛЕКС", 1))
        t = Termin._new1583("МЕСТОРОЖДЕНИЕ", 1)
        t.add_abridge("МЕСТОРОЖД.")
        t.add_variant("МЕСТОРОЖДЕНИЕ ЗОЛОТА", False)
        t.add_variant("МЕСТОРОЖДЕНИЕ РОССЫПНОГО ЗОЛОТА", False)
        t.add_variant("ЗОЛОТОЕ МЕСТОРОЖДЕНИЕ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1700("МЕСТНОСТЬ", StreetItemType.NOUN, MorphGender.FEMINIE, 1)
        t.add_abridge("МЕСТН.")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЛЕСНИЧЕСТВО", 1)
        t.add_abridge("ЛЕС-ВО")
        t.add_abridge("ЛЕСН-ВО")
        t.add_variant("УЧАСТКОВОЕ ЛЕСНИЧЕСТВО", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЛЕСОПАРК", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЛЕСОУЧАСТОК", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЗАПОВЕДНИК", 1)
        t.add_abridge("ЗАП-К")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЦЕНТРАЛЬНАЯ УСАДЬБА", 1)
        t.add_variant("УСАДЬБА", False)
        t.add_abridge("ЦЕНТР.УС.")
        t.add_abridge("ЦЕНТР.УСАДЬБА")
        t.add_abridge("Ц/У")
        t.add_abridge("УС-БА")
        t.add_abridge("ЦЕНТР.УС-БА")
        OrgTypToken._m_ontology.add(t)
        t = Termin("ЦЕНТРАЛЬНОЕ ОТДЕЛЕНИЕ")
        t.add_abridge("Ц/О")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("СЕКТОР", 1)
        t.add_abridge("СЕК.")
        t.add_abridge("СЕКТ.")
        t.add_abridge("С-Р")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1700("МАССИВ", StreetItemType.NOUN, MorphGender.MASCULINE, 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1700("ЗОНА", StreetItemType.NOUN, MorphGender.FEMINIE, 1)
        t.add_variant("ЗОНА (МАССИВ)", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1700("ЗОНА ГАРАЖЕЙ", StreetItemType.NOUN, MorphGender.FEMINIE, 1)
        t.add_variant("ЗОНА (МАССИВ) ГАРАЖЕЙ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ГАРАЖНАЯ ПЛОЩАДКА", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ПОЛЕВОЙ МАССИВ", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ПОЛЕВОЙ УЧАСТОК", 1)
        t.add_abridge("ПОЛЕВОЙ УЧ-К")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1700("ПРОМЗОНА", StreetItemType.NOUN, MorphGender.FEMINIE, 1)
        t.add_variant("ПРОМЫШЛЕННАЯ ЗОНА", False)
        t.add_variant("ПРОИЗВОДСТВЕННАЯ ЗОНА", False)
        t.add_variant("ПРОМЫШЛЕННО КОММУНАЛЬНАЯ ЗОНА", False)
        t.add_variant("ЗОНА ПРОИЗВОДСТВЕННОГО ИСПОЛЬЗОВАНИЯ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1700("ПРОМУЗЕЛ", StreetItemType.NOUN, MorphGender.MASCULINE, 1)
        t.add_variant("ПРОМЫШЛЕННЫЙ УЗЕЛ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1715("ПРОМЫШЛЕННЫЙ РАЙОН", StreetItemType.NOUN, 1, MorphGender.FEMINIE, 1)
        t.add_variant("ПРОМРАЙОН", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1715("ПЛАНИРОВОЧНЫЙ РАЙОН", StreetItemType.NOUN, 1, MorphGender.FEMINIE, 1)
        t.add_abridge("П/Р")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1715("ПРОИЗВОДСТВЕННО АДМИНИСТРАТИВНАЯ ЗОНА", StreetItemType.NOUN, 1, MorphGender.FEMINIE, 1)
        t.add_abridge("ПРОИЗВ. АДМ. ЗОНА")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1715("ЖИЛАЯ ЗОНА", StreetItemType.NOUN, 1, MorphGender.FEMINIE, 1)
        t.add_variant("ЖИЛЗОНА", False)
        t.add_variant("ЖИЛ.ЗОНА", False)
        t.add_variant("Ж.ЗОНА", False)
        t.add_abridge("Ж/З")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1719("ОСОБАЯ ЭКОНОМИЧЕСКАЯ ЗОНА", "ОЭЗ", True, True, 1, 1)
        t.add_variant("ОСОБАЯ ЭКОНОМИЧЕСКАЯ ЗОНА ПРОМЫШЛЕННО ПРОИЗВОДСТВЕННОГО ТИПА", False)
        t.add_variant("ОЭЗ ППТ", False)
        t.add_variant("ОЭЖЗППТ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1715("ЗОНА ОТДЫХА", StreetItemType.NOUN, 1, MorphGender.FEMINIE, 1)
        t.add_abridge("З/О")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1715("КОММУНАЛЬНАЯ ЗОНА", StreetItemType.NOUN, 1, MorphGender.FEMINIE, 1)
        t.add_variant("КОМЗОНА", False)
        t.add_abridge("КОММУН. ЗОНА")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1715("ЖИЛОЙ МАССИВ", StreetItemType.NOUN, 1, MorphGender.MASCULINE, 1)
        t.add_abridge("Ж.М.")
        t.add_abridge("Ж/М")
        t.add_variant("ЖИЛМАССИВ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1617("ЖИЛГОРОДОК", 1, 1)
        t.add_variant("ЖИЛИЩНЫЙ ГОРОДОК", False)
        t.add_variant("ЖИЛОЙ ГОРОДОК", False)
        t.add_abridge("Ж/Г")
        t.add_abridge("ЖИЛ.ГОР.")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЖИЛРАЙОН", 1)
        t.add_variant("ЖИЛИЩНЫЙ РАЙОН", False)
        t.add_variant("ЖИЛОЙ РАЙОН", False)
        t.add_abridge("Ж/Р")
        t.add_abridge("ЖИЛ.РАЙОН")
        t.add_abridge("ЖИЛ.Р-Н")
        t.add_abridge("Ж/Р-Н")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1583("ЗАГОРОДНЫЙ КОМПЛЕКС", 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1715("ИНДУСТРИАЛЬНЫЙ ПАРК", StreetItemType.NOUN, 1, MorphGender.MASCULINE, 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1727("КВАРТАЛ ДАЧНОЙ ЗАСТРОЙКИ", "КВАРТАЛ", StreetItemType.NOUN, 0, MorphGender.MASCULINE, 1)
        t.add_variant("ПРОМЫШЛЕННЫЙ КВАРТАЛ", False)
        t.add_variant("ИНДУСТРИАЛЬНЫЙ КВАРТАЛ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1728("ЖИЛОЙ КОМПЛЕКС", StreetItemType.NOUN, "ЖК", 0, MorphGender.MASCULINE, 1)
        t.add_variant("ЖИЛКОМПЛЕКС", False)
        t.add_abridge("ЖИЛ.К.")
        t.add_abridge("Ж/К")
        t.add_variant("ЖИЛОЙ КВАРТАЛ", False)
        t.add_variant("ЖИЛКВАРТАЛ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1728("ВАХТОВЫЙ ЖИЛОЙ КОМПЛЕКС", StreetItemType.NOUN, "ВЖК", 0, MorphGender.MASCULINE, 1)
        OrgTypToken._m_ontology.add(t)
        t = Termin("ТЕЛЕВЕЩАНИЕ")
        t.add_variant("ТЕЛЕВИЗИОННОЕ ВЕЩАНИЕ", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1191("ИСПРАВИТЕЛЬНАЯ КОЛОНИЯ", StreetItemType.NOUN, "ИК", 0)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1191("ИСПРАВИТЕЛЬНО ТРУДОВАЯ КОЛОНИЯ", StreetItemType.NOUN, "ИТК", 0)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1191("ДЕТСКАЯ ТРУДОВАЯ КОЛОНИЯ", StreetItemType.NOUN, "ДТК", 0)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1191("ЛЕЧЕБНО ТРУДОВОЙ ПРОФИЛАКТОРИЙ", StreetItemType.NOUN, "ЛТП", 0)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1734("ВАСИЛЬЕВСКИЙ ОСТРОВ", StreetItemType.STDNAME, "ВО", 1)
        t.add_abridge("В.О.")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new91("ПЕТРОГРАДСКАЯ СТОРОНА", StreetItemType.STDNAME, 1)
        t.add_abridge("П.С.")
        OrgTypToken._m_ontology.add(t)
        for s in ["АПТЕКА", "АТЕЛЬЕ", "ОТЕЛЬ", "ГОСТИНИЦА", "ХОСТЕЛ", "СТУДИЯ", "ПАРИКМАХЕРСКАЯ", "СТОЛОВАЯ", "КАФЕ", "РЕСТОРАН", "УНИВЕРМАГ", "УНИВЕРСАМ", "СУПЕРМАРКЕТ"]: 
            OrgTypToken._m_ontology.add(Termin._new84(s, AddressItemType.BUILDING))
        t = Termin._new84("МАГАЗИН", AddressItemType.BUILDING)
        t.add_abridge("МАГ.")
        t.add_abridge("МАГ-Н")
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1535("БИЗНЕС ЦЕНТР", "БЦ", True, True)
        t.add_variant("БІЗНЕС ЦЕНТР", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1739("ТОРГОВЫЙ ЦЕНТР", AddressItemType.BUILDING, "ТЦ", True, True)
        t.add_variant("ТОРГОВИЙ ЦЕНТР", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1739("ТОРГОВО ОФИСНЫЙ ЦЕНТР", AddressItemType.BUILDING, "ТОЦ", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1739("ТОРГОВО ОФИСНЫЙ КОМПЛЕКС", AddressItemType.BUILDING, "ТОК", True, True)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1739("ТОРГОВО РАЗВЛЕКАТЕЛЬНЫЙ ЦЕНТР", AddressItemType.BUILDING, "ТРЦ", True, True)
        t.add_variant("ТОРГОВО РОЗВАЖАЛЬНИЙ ЦЕНТР", False)
        OrgTypToken._m_ontology.add(t)
        t = Termin._new1739("ТОРГОВО РАЗВЛЕКАТЕЛЬНЫЙ КОМПЛЕКС", AddressItemType.BUILDING, "ТРК", True, True)
        t.add_variant("ТОРГОВО РОЗВАЖАЛЬНИЙ КОМПЛЕКС", False)
        OrgTypToken._m_ontology.add(t)
    
    _m_ontology = None
    
    @staticmethod
    def _new1525(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : bool) -> 'OrgTypToken':
        res = OrgTypToken(_arg1, _arg2, _arg3)
        res.is_building = _arg4
        return res
    
    @staticmethod
    def _new1526(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool, _arg4 : typing.List[str], _arg5 : 'MorphCollection', _arg6 : bool, _arg7 : bool, _arg8 : bool, _arg9 : bool) -> 'OrgTypToken':
        res = OrgTypToken(_arg1, _arg2)
        res.is_doubt = _arg3
        res.vals = _arg4
        res.morph = _arg5
        res.not_org = _arg6
        res.not_geo = _arg7
        res.can_be_single = _arg8
        res.is_building = _arg9
        return res