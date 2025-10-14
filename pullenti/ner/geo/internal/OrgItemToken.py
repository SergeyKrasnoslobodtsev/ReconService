# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.Referent import Referent
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.morph.MorphClass import MorphClass
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Token import Token
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.geo.internal.NumToken import NumToken
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.geo.internal.GeoTokenType import GeoTokenType
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken
from pullenti.ner.geo.internal.CityItemToken import CityItemToken
from pullenti.ner.geo.internal.OrgTypToken import OrgTypToken

class OrgItemToken(ReferentToken):
    
    def __init__(self, r : 'Referent', b : 'Token', e0_ : 'Token') -> None:
        super().__init__(r, b, e0_, None)
        self.is_doubt = False
        self.has_terr_keyword = False
        self.keyword_after = False
        self.is_gsk = False
        self.not_org = False
        self.not_geo = False
        self.is_building = False
    
    def set_gsk(self) -> None:
        self.is_gsk = False
        if (self.not_org): 
            self.is_gsk = True
            return
        if (self.is_building): 
            return
        for s in self.referent.slots: 
            if (s.type_name == "TYPE" and (isinstance(s.value, str))): 
                ty = Utils.asObjectOrNull(s.value, str)
                if (((((((("товарищество" in ty or "кооператив" in ty or "коллектив" in ty) or LanguageHelper.ends_with_ex(ty, "поселок", " отдыха", " часть", None) or "партнерство" in ty) or "объединение" in ty or "бизнес" in ty) or "офисн" in ty or (("станция" in ty and not "заправоч" in ty))) or "аэропорт" in ty or "пансионат" in ty) or "санаторий" in ty or "база" in ty) or "урочище" in ty or "кадастровый" in ty) or "лесничество" in ty): 
                    self.is_gsk = True
                    return
                if (ty == "АОЗТ" or ty == "пядь"): 
                    self.is_gsk = True
                    return
                if ("хозяйство" in ty): 
                    if ("кресьян" in ty or "фермер" in ty): 
                        self.is_gsk = True
                        return
            elif (s.type_name == "NAME" and (isinstance(s.value, str))): 
                nam = Utils.asObjectOrNull(s.value, str)
                if (LanguageHelper.ends_with_ex(nam, "ГЭС", "АЭС", "ТЭС", None)): 
                    self.is_gsk = True
                    return
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        if (self.is_doubt): 
            print("? ", end="", file=tmp)
        if (self.has_terr_keyword): 
            print("Terr ", end="", file=tmp)
        if (self.is_gsk): 
            print("Gsk ", end="", file=tmp)
        if (self.not_org): 
            print("NotOrg ", end="", file=tmp)
        if (self.not_geo): 
            print("NotGeo ", end="", file=tmp)
        if (self.is_building): 
            print("Building ", end="", file=tmp)
        print(str(self.referent), end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    
    SPEED_REGIME = False
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        if (not OrgItemToken.SPEED_REGIME): 
            return
        ad = GeoAnalyzer._get_data(t0)
        if (ad is None): 
            return
        ad.oregime = False
        t = t0
        while t is not None: 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            org0_ = OrgItemToken.try_parse(t, ad)
            if (org0_ is not None): 
                if (d is None): 
                    d = GeoTokenData(t)
                d.org0_ = org0_
                if (not t.is_value("НП", None)): 
                    if ((org0_.has_terr_keyword or org0_.not_geo or org0_.is_building) or (((org0_.is_gsk and not org0_.keyword_after and not org0_.not_org) and MiscLocationHelper.is_user_param_address(org0_)))): 
                        tt = org0_.begin_token
                        while tt is not None and tt.end_char <= org0_.end_char: 
                            dd = Utils.asObjectOrNull(tt.tag, GeoTokenData)
                            if (dd is None): 
                                dd = GeoTokenData(tt)
                            dd.no_geo = True
                            tt = tt.next0_
                        if (not org0_.has_terr_keyword): 
                            t = org0_.end_token
            t = t.next0_
        ad.oregime = True
    
    @staticmethod
    def try_parse(t : 'Token', ad : 'GeoAnalyzerData'=None) -> 'OrgItemToken':
        if (not (isinstance(t, TextToken))): 
            return None
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (OrgItemToken.SPEED_REGIME and ((ad.oregime or ad.all_regime))): 
            if ((isinstance(t, TextToken)) and t.is_char('м')): 
                pass
            else: 
                d = Utils.asObjectOrNull(t.tag, GeoTokenData)
                if (d is not None): 
                    return d.org0_
                return None
        if (ad.olevel > 1): 
            return None
        ad.olevel += 1
        res = OrgItemToken.__try_parse(t, False, 0, ad)
        if (res is not None): 
            res.__try_parse_details()
        ad.olevel -= 1
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', after_terr : bool, lev : int, ad : 'GeoAnalyzerData') -> 'OrgItemToken':
        from pullenti.ner.geo.internal.NameToken import NameToken
        if (lev > 3 or t is None or t.is_comma): 
            return None
        tt2 = MiscLocationHelper.check_territory(t)
        if (tt2 is not None and tt2.next0_ is not None): 
            tt2 = tt2.next0_
            br = False
            if (BracketHelper.is_bracket(tt2, True)): 
                br = True
                tt2 = tt2.next0_
            if (tt2 is None or lev > 3): 
                return None
            re2 = OrgItemToken.__try_parse(tt2, True, lev + 1, ad)
            if (re2 is None and tt2 is not None and tt2.is_value("ВЛАДЕНИЕ", None)): 
                re2 = OrgItemToken.__try_parse(tt2.next0_, True, lev + 1, ad)
            if (re2 is not None): 
                a = t.kit.processor.find_analyzer("GEO")
                if (a is not None and not MiscLocationHelper.is_user_param_address(t)): 
                    rt = a.process_referent(tt2, None)
                    if (rt is not None): 
                        return None
                tt = tt2
                while tt is not None and tt.end_char <= re2.end_char: 
                    sit = StreetItemToken.try_parse(tt, None, False, None)
                    if (sit is not None and sit.typ == StreetItemType.NOUN and ((sit.is_road or sit.is_railway))): 
                        return None
                    tt = tt.next0_
                if (tt2.is_value("ВЛАДЕНИЕ", None)): 
                    re2.referent.add_slot("TYPE", "владение", False, 0)
                if (AddressItemToken.M_PLOT.try_parse(t, TerminParseAttr.NO) is not None): 
                    re2.referent.add_slot("TYPE", "участок", False, 0)
                re2.begin_token = t
                if (br and BracketHelper.can_be_end_of_sequence(re2.end_token.next0_, False, None, False)): 
                    re2.end_token = re2.end_token.next0_
                re2.has_terr_keyword = True
                return re2
            elif ((isinstance(t, TextToken)) and ((t.term.startswith("ТЕР") or t.term.startswith("ПЛОЩ"))) and (tt2.whitespaces_before_count < 3)): 
                nam1 = NameToken.try_parse(tt2, GeoTokenType.ORG, 0, True)
                if (nam1 is not None and ((nam1.name is not None or ((nam1.number is not None and MiscLocationHelper.is_user_param_address(tt2)))))): 
                    if (StreetItemToken.check_keyword(tt2)): 
                        return None
                    if (t.next0_ != nam1.end_token and StreetItemToken.check_keyword(nam1.end_token)): 
                        return None
                    if (TerrItemToken.check_keyword(tt2) is not None): 
                        return None
                    if (t.next0_ != nam1.end_token and TerrItemToken.check_keyword(nam1.end_token) is not None): 
                        return None
                    ter = TerrItemToken.check_onto_item(tt2)
                    if (ter is not None): 
                        geo_ = Utils.asObjectOrNull(ter.item.referent, GeoReferent)
                        if (geo_.is_city or geo_.is_state): 
                            return None
                    if (CityItemToken.check_keyword(tt2) is not None): 
                        return None
                    if (CityItemToken.check_onto_item(tt2) is not None): 
                        return None
                    tt = nam1.end_token
                    ok = False
                    if (tt.is_newline_after): 
                        ok = True
                    elif (tt.next0_ is not None and ((tt.next0_.is_comma or tt.next0_.is_char(')')))): 
                        ok = True
                    elif (AddressItemToken.check_house_after(tt2, False, False)): 
                        ok = True
                    else: 
                        ait = AddressItemToken.try_parse_pure_item(nam1.end_token.next0_, None, None)
                        if (ait is not None and ait.typ != AddressItemType.NUMBER): 
                            ok = True
                        else: 
                            a2 = AddressItemToken.try_parse(nam1.end_token.next0_, False, None, ad)
                            if (a2 is not None): 
                                a1 = AddressItemToken.try_parse(tt2, False, None, ad)
                                if (a1 is None or (a1.end_char < a2.end_char)): 
                                    ok = True
                    if (ok): 
                        org1 = t.kit.create_referent("ORGANIZATION")
                        if (nam1.name is not None): 
                            org1.add_slot("NAME", nam1.name, False, 0)
                        if (nam1.number is not None): 
                            org1.add_slot("NUMBER", nam1.number, False, 0)
                        if (tt2.previous is not None and tt2.previous.is_value("ВЛАДЕНИЕ", None)): 
                            org1.add_slot("TYPE", "владение", False, 0)
                        res1 = OrgItemToken(org1, t, nam1.end_token)
                        res1.data = t.kit.get_analyzer_data_by_analyzer_name("ORGANIZATION")
                        res1.has_terr_keyword = True
                        return res1
                rt = t.kit.process_referent("NAMEDENTITY", tt2, None)
                if (rt is not None): 
                    res1 = OrgItemToken(rt.referent, t, rt.end_token)
                    res1.data = t.kit.get_analyzer_data_by_analyzer_name("NAMEDENTITY")
                    res1.has_terr_keyword = True
                    return res1
            if (not t.is_value("САД", None)): 
                return None
        typ_after = False
        doubt0 = False
        tok_typ = OrgTypToken.try_parse(t, after_terr, ad)
        nam = None
        ignore_num = False
        if (tok_typ is None and t.is_char('(') and MiscLocationHelper.is_user_param_address(t)): 
            nnn = NameToken.try_parse(t.next0_, GeoTokenType.ORG, 0, False)
            if (nnn is not None and nnn.end_token.next0_ is not None and nnn.end_token.next0_.is_comma): 
                ttt = OrgTypToken.try_parse(nnn.end_token.next0_.next0_, after_terr, ad)
                if (ttt is not None and ttt.end_token.next0_ is not None and ttt.end_token.next0_.is_char(')')): 
                    tok_typ = ttt
                    tok_typ.end_token = tok_typ.end_token.next0_
                    nam = nnn
                    nam.begin_token = t
            if (tok_typ is None): 
                ttt = OrgTypToken.try_parse(t.next0_, after_terr, ad)
                if (ttt is not None and ttt.end_token.next0_ is not None): 
                    nnn = NameToken.try_parse((ttt.end_token.next0_.next0_ if ttt.end_token.next0_.is_comma else ttt.end_token.next0_), GeoTokenType.ORG, 0, False)
                    if (nnn is not None): 
                        ttt2 = nnn.end_token.next0_
                        if (ttt2 is not None and ttt2.is_char('(')): 
                            br = BracketHelper.try_parse(ttt2, BracketParseAttr.NO, 100)
                            if (br is not None): 
                                nnn.end_token = br.end_token
                        if (nnn.end_token.next0_ is not None and nnn.end_token.next0_.is_char(')')): 
                            tok_typ = ttt
                            tok_typ.begin_token = t
                            nam = nnn
                            nnn.end_token = nnn.end_token.next0_
        if (tok_typ is None): 
            num = NumToken.try_parse(t, GeoTokenType.ORG)
            if (num is not None and num.has_spec_word): 
                next0__ = OrgItemToken.try_parse(num.end_token.next0_, ad)
                if (next0__ is not None and next0__.referent.find_slot("NUMBER", None, True) is None): 
                    next0__.begin_token = t
                    next0__.referent.add_slot("NUMBER", num.value, False, 0)
                    return next0__
            if (num is not None and num.end_token.next0_ is not None and after_terr): 
                sss = StreetItemToken.try_parse(num.end_token.next0_, None, False, None)
                if (sss is not None and sss.typ == StreetItemType.NOUN and sss.termin.canonic_text == "КВАРТАЛ"): 
                    sr = StreetReferent._new1520(StreetKind.AREA)
                    sr._add_typ("квартал")
                    sr.add_slot(StreetReferent.ATTR_NUMBER, num.value, False, 0)
                    res3 = OrgItemToken(sr, t, sss.end_token)
                    res3.not_org = True
                    res3.has_terr_keyword = after_terr
                    res3.not_geo = True
                    return res3
            ait = AddressItemToken.try_parse_pure_item(t, None, None)
            if ((ait is not None and ait.typ == AddressItemType.HOUSE and ait.house_type == AddressHouseType.ESTATE) and ait.value is not None): 
                ok3 = False
                if (after_terr): 
                    ok3 = True
                elif (AddressItemToken.check_street_after(ait.end_token.next0_, False)): 
                    ok3 = True
                if (ok3): 
                    org3 = t.kit.create_referent("ORGANIZATION")
                    org3.add_slot("TYPE", "владение", False, 0)
                    num3 = io.StringIO()
                    nam3 = io.StringIO()
                    for ch in ait.value: 
                        if (str.isdigit(ch)): 
                            print(ch, end="", file=num3)
                        elif (str.isalpha(ch)): 
                            print(ch, end="", file=nam3)
                    if (num3.tell() > 0): 
                        org3.add_slot("NUMBER", Utils.toStringStringIO(num3), False, 0)
                    if (nam3.tell() > 0): 
                        org3.add_slot("NAME", Utils.toStringStringIO(nam3), False, 0)
                    res3 = OrgItemToken(org3, t, ait.end_token)
                    res3.data = t.kit.get_analyzer_data_by_analyzer_name("ORGANIZATION")
                    res3.not_org = True
                    res3.has_terr_keyword = after_terr
                    res3.not_geo = True
                    return res3
            if ((after_terr and ait is not None and ait.typ == AddressItemType.HOUSE) and ait.house_type == AddressHouseType.SPECIAL and ait.value is not None): 
                org3 = t.kit.create_referent("ORGANIZATION")
                val = ait.value
                ii = val.find('-')
                if (ii < 0): 
                    org3.add_slot("TYPE", val, False, 0)
                else: 
                    org3.add_slot("TYPE", val[0:0+ii], False, 0)
                    org3.add_slot("NUMBER", val[ii + 1:], False, 0)
                res3 = OrgItemToken(org3, t, ait.end_token)
                res3.data = t.kit.get_analyzer_data_by_analyzer_name("ORGANIZATION")
                res3.not_org = True
                res3.has_terr_keyword = after_terr
                res3.not_geo = True
                return res3
            if ((after_terr and ait is not None and ait.typ == AddressItemType.GENPLAN) and ait.value is not None): 
                org3 = t.kit.create_referent("ORGANIZATION")
                org3.add_slot("TYPE", "ГП", False, 0)
                org3.add_slot("NUMBER", ait.value, False, 0)
                res3 = OrgItemToken(org3, t, ait.end_token)
                res3.data = t.kit.get_analyzer_data_by_analyzer_name("ORGANIZATION")
                res3.not_org = True
                res3.has_terr_keyword = after_terr
                res3.not_geo = True
                return res3
            ok = 0
            if (BracketHelper.can_be_start_of_sequence(t, True, False)): 
                ok = 2
            elif (t.is_value("ИМ", None) or t.is_value("ИМЕНИ", None)): 
                ok = 2
            elif (after_terr): 
                ok = 1
            elif ((isinstance(t, TextToken)) and not t.chars.is_all_lower and t.length_char > 1): 
                if (t.previous is not None and t.previous.is_hiphen and not t.is_whitespace_before): 
                    pass
                else: 
                    ok = 1
            if (ok == 0): 
                return None
            if (CityItemToken.check_keyword(t) is not None): 
                return None
            if (CityItemToken.check_onto_item(t) is not None): 
                return None
            if ((t.length_char > 5 and (isinstance(t, TextToken)) and not t.chars.is_all_upper) and not t.chars.is_all_lower and not t.chars.is_capital_upper): 
                namm = t.get_source_text()
                if (str.isupper(namm[0]) and str.isupper(namm[1])): 
                    i = 0
                    while i < len(namm): 
                        if (str.islower(namm[i]) and i > 2): 
                            abbr = namm[0:0+i - 1]
                            te = Termin._new1166(abbr, abbr)
                            li = OrgTypToken.find_termin_by_acronym(abbr)
                            if (li is not None and len(li) > 0): 
                                nam = NameToken(t, t)
                                nam.name = t.term[i - 1:]
                                tok_typ = OrgTypToken(t, t)
                                tok_typ.vals.append(li[0].canonic_text.lower())
                                tok_typ.vals.append(abbr)
                                nam.try_attach_number()
                                break
                        i += 1
            if (nam is None): 
                if (after_terr): 
                    ok = 2
                if (ok < 2): 
                    kk = 0
                    tt = t.next0_
                    first_pass3983 = True
                    while True:
                        if first_pass3983: first_pass3983 = False
                        else: tt = tt.next0_; kk += 1
                        if (not (tt is not None and (kk < 5))): break
                        if (tt.is_newline_before): 
                            break
                        ty22 = OrgTypToken.try_parse(tt, False, ad)
                        if (ty22 is None or ty22.is_doubt or ty22.can_be_single): 
                            continue
                        ok = 2
                        break
                if (ok < 2): 
                    return None
                typ_after = True
                nam = NameToken.try_parse(t, GeoTokenType.ORG, 0, False)
                if (nam is None): 
                    return None
                tok_typ = OrgTypToken.try_parse(nam.end_token.next0_, False, None)
                if ((tok_typ is not None and (tok_typ.whitespaces_after_count < 3) and not after_terr) and nam.begin_token == nam.end_token): 
                    if (MiscLocationHelper.check_territory(tok_typ.end_token.next0_) is not None): 
                        pass
                    else: 
                        nam2 = NameToken.try_parse(tok_typ.end_token.next0_, GeoTokenType.ORG, lev + 1, False)
                        if (nam2 is not None and nam2.number is not None): 
                            return None
                if (tok_typ is None and not after_terr and MiscLocationHelper.is_user_param_address(t)): 
                    tt2 = MiscLocationHelper.check_territory(nam.end_token.next0_)
                    if (tt2 is not None and tt2.next0_ is not None): 
                        tok_typ = OrgTypToken.try_parse(tt2.next0_, True, ad)
                        if (tok_typ is not None): 
                            nam2 = NameToken.try_parse(tok_typ.end_token.next0_, GeoTokenType.ORG, 0, False)
                            if (nam2 is not None and nam2.name is not None): 
                                tok_typ = (None)
                if (tok_typ is None and nam.begin_token != nam.end_token): 
                    tok_typ = OrgTypToken.try_parse(nam.end_token, False, None)
                    if (tok_typ is not None): 
                        nam.end_token = nam.end_token.previous
                        nam.name = (None)
                        ntt = nam.begin_token
                        while ntt.end_char <= nam.end_char: 
                            if (not (isinstance(ntt, TextToken))): 
                                nam.name = MiscHelper.get_text_value_of_meta_token(nam, GetTextAttr.NO)
                                break
                            v = ntt.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, tok_typ.morph.gender, False)
                            if (v is None): 
                                v = ntt.term
                            if (nam.name is None): 
                                nam.name = v
                            else: 
                                nam.name = "{0} {1}".format(nam.name, v)
                            ntt = ntt.next0_
                if (nam.name is None and nam.misc_typ is None): 
                    if (nam.number is not None and tok_typ is not None): 
                        pass
                    elif (after_terr): 
                        pass
                    else: 
                        return None
                if (tok_typ is not None): 
                    if (nam.begin_token == nam.end_token): 
                        mc = nam.get_morph_class_in_dictionary()
                        if (mc.is_conjunction or mc.is_preposition or mc.is_pronoun): 
                            return None
                    rt2 = OrgItemToken.try_parse(tok_typ.begin_token, None)
                    if (rt2 is not None and rt2.is_doubt): 
                        rt2 = (None)
                    if (rt2 is not None): 
                        if (MiscLocationHelper.check_territory(tok_typ.end_token.next0_) is not None): 
                            rt3 = OrgItemToken.try_parse(tok_typ.end_token.next0_, ad)
                            if (rt3 is not None): 
                                rt2 = (None)
                    nam2 = NameToken.try_parse(tok_typ.end_token.next0_, GeoTokenType.ORG, 0, False)
                    if (tok_typ.is_newline_after): 
                        nam2 = (None)
                    if (rt2 is not None and rt2.end_char > tok_typ.end_char): 
                        if (nam2 is None or nam2.end_token != rt2.end_token): 
                            return None
                        if (((nam.number is None and nam2.name is None and nam2.number is not None)) or (((nam.name is None and nam.number is not None and nam2.number is None) and nam2.name is not None))): 
                            if (nam2.number is not None): 
                                nam.number = nam2.number
                            if (nam2.name is not None): 
                                nam.name = nam2.name
                            tok_typ = tok_typ.clone()
                            tok_typ.end_token = nam2.end_token
                        else: 
                            return None
                    elif ((nam.number is None and nam2 is not None and nam2.name is None) and nam2.number is not None): 
                        nam.number = nam2.number
                        tok_typ = tok_typ.clone()
                        tok_typ.end_token = nam2.end_token
                    nam.end_token = tok_typ.end_token
                    doubt0 = True
                elif (nam.name is not None or nam.misc_typ is not None): 
                    busines = False
                    if (nam.misc_typ is not None): 
                        pass
                    elif (nam.name.endswith("ПЛАЗА") or nam.name.startswith("БИЗНЕС")): 
                        busines = True
                    elif (after_terr and MiscLocationHelper.is_user_param_address(nam)): 
                        if (StreetItemToken.check_keyword(nam.begin_token)): 
                            return None
                    elif (nam.begin_token == nam.end_token): 
                        return None
                    elif (nam.name is not None and len(nam.name) == 1 and nam.number is None): 
                        return None
                    elif (BracketHelper.can_be_start_of_sequence(nam.begin_token, False, False) and MiscLocationHelper.is_user_param_address(nam)): 
                        pass
                    else: 
                        tok_typ = OrgTypToken.try_parse(nam.end_token, False, ad)
                        if ((tok_typ) is None): 
                            return None
                        elif (nam.morph.case_.is_genitive and not nam.morph.case_.is_nominative): 
                            nam.name = MiscHelper.get_text_value_of_meta_token(nam, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVESINGLE).replace("-", " ")
                            if (tok_typ is not None and len(tok_typ.vals) > 0): 
                                if (Utils.endsWithString(nam.name, tok_typ.vals[0], True)): 
                                    nam.name = nam.name[0:0+len(nam.name) - len(tok_typ.vals[0])].strip()
                    if (tok_typ is None): 
                        tok_typ = OrgTypToken(t, t)
                        if (busines): 
                            tok_typ.vals.append("бизнес центр")
                            tok_typ.vals.append("БЦ")
                        elif (t.previous is not None and t.previous.is_value("САД", None)): 
                            tok_typ.vals.append("сад")
                        elif (nam.misc_typ is not None): 
                            tok_typ.vals.append(nam.misc_typ)
                    nam.is_doubt = len(tok_typ.vals) == 0
                    doubt0 = len(tok_typ.vals) == 0
                else: 
                    return None
        else: 
            if (tok_typ.whitespaces_after_count > 3 and not tok_typ.is_newline_after): 
                return None
            tt3 = MiscLocationHelper.check_territory(tok_typ.end_token.next0_)
            if (tt3 is not None): 
                tok_typ = tok_typ.clone()
                tok_typ.end_token = tt3
                after_terr = True
                tok_typ2 = OrgTypToken.try_parse(tok_typ.end_token.next0_, True, ad)
                if (tok_typ2 is not None and not tok_typ2.is_doubt): 
                    tok_typ.merge_with(tok_typ2)
            else: 
                tok_typ2 = OrgTypToken.try_parse(tok_typ.end_token.next0_, True, ad)
                if (tok_typ2 is not None and tok_typ2.begin_token == tok_typ2.end_token): 
                    mc = tok_typ2.begin_token.get_morph_class_in_dictionary()
                    if (not mc.is_undefined): 
                        tok_typ2 = (None)
                if (tok_typ2 is not None and not tok_typ2.is_doubt): 
                    tok_typ = tok_typ.clone()
                    tok_typ.merge_with(tok_typ2)
            if (BracketHelper.is_bracket(tok_typ.end_token.next0_, True)): 
                tok_typ2 = OrgTypToken.try_parse(tok_typ.end_token.next0_.next0_, after_terr, ad)
                if (tok_typ2 is not None and not tok_typ2.is_doubt): 
                    tok_typ = tok_typ.clone()
                    tok_typ.is_doubt = False
                    nam = NameToken.try_parse(tok_typ2.end_token.next0_, GeoTokenType.ORG, 0, False)
                    if (nam is not None and BracketHelper.can_be_end_of_sequence(nam.end_token.next0_, False, None, False)): 
                        tok_typ.merge_with(tok_typ2)
                        nam.end_token = nam.end_token.next0_
                    elif (nam is not None and BracketHelper.can_be_end_of_sequence(nam.end_token, False, None, False)): 
                        tok_typ.merge_with(tok_typ2)
                    else: 
                        nam = (None)
        if (OrgItemToken._m_onto.try_parse(tok_typ.end_token.next0_, TerminParseAttr.NO) is not None): 
            pass
        elif (StreetItemToken.check_keyword(tok_typ.end_token.next0_) and not tok_typ.end_token.next0_.chars.is_capital_upper): 
            pass
        elif ((tok_typ.end_token.next0_ is not None and tok_typ.end_token.next0_.chars.is_all_lower and CityItemToken.check_keyword(tok_typ.end_token.next0_) is not None) and NumToken.try_parse(tok_typ.end_token.next0_, GeoTokenType.ORG) is None): 
            pass
        else: 
            if (nam is None and (tok_typ.whitespaces_after_count < 3)): 
                nam = NameToken.try_parse(tok_typ.end_token.next0_, GeoTokenType.ORG, 0, True)
            if ((nam is None and tok_typ.end_token.next0_ is not None and tok_typ.chars.is_all_upper) and tok_typ.end_token.next0_.is_hiphen and not tok_typ.is_whitespace_after): 
                nam = NameToken.try_parse(tok_typ.end_token.next0_.next0_, GeoTokenType.ORG, 0, True)
                if (nam is not None): 
                    if (nam.chars.is_all_lower or (nam.length_char < 4)): 
                        nam = (None)
            if ((nam is not None and nam.length_char == 1 and nam.chars.is_all_lower) and ((nam.begin_token.is_value("С", None) or nam.is_value("Д", None) or nam.is_value("П", None)))): 
                nam = (None)
            if (nam is None): 
                ok = False
                if (after_terr and MiscLocationHelper.is_user_param_address(tok_typ)): 
                    ok = True
                elif (tok_typ.can_be_single): 
                    ok = True
                elif (tok_typ.begin_token != tok_typ.end_token): 
                    if (MiscLocationHelper.check_geo_object_before(tok_typ.begin_token, False)): 
                        ok = True
                    elif (MiscLocationHelper.is_user_param_address(tok_typ) and ((tok_typ.end_token.is_newline_after or tok_typ.end_token.next0_.is_comma))): 
                        ok = True
                    elif (AddressItemToken.check_house_after(tok_typ.end_token.next0_, False, False)): 
                        ok = True
                if (not ok): 
                    return None
                if (len(tok_typ.vals) > 0 and tok_typ.vals[0].endswith("район")): 
                    return None
        if (tok_typ.is_doubt and ((nam is None or nam.is_doubt or nam.chars.is_all_upper))): 
            return None
        if (((tok_typ.length_char < 3) and nam is not None and nam.name is None) and nam.pref is None): 
            if (after_terr or MiscLocationHelper.is_user_param_address(tok_typ)): 
                pass
            else: 
                return None
        if (((tok_typ.begin_token.is_value("СП", None) or tok_typ.begin_token.is_value("ГП", None))) and nam is not None): 
            tt = nam.end_token.next0_
            if (tt is not None and tt.is_comma): 
                tt = tt.next0_
            if (AddressItemToken.check_house_after(tt, False, False)): 
                pass
            elif (CityItemToken.check_keyword(tt) is not None): 
                return None
        org0_ = t.kit.create_referent("ORGANIZATION")
        res = OrgItemToken(org0_, t, (nam.end_token if nam is not None and nam.end_char > tok_typ.end_char else tok_typ.end_token))
        res.data = t.kit.get_analyzer_data_by_analyzer_name("ORGANIZATION")
        res.has_terr_keyword = after_terr
        res.is_doubt = (doubt0 or tok_typ.is_doubt or nam is None)
        res.keyword_after = typ_after
        res.not_org = tok_typ.not_org
        res.not_geo = tok_typ.not_geo
        if (not after_terr): 
            res.is_building = tok_typ.is_building
        if (tok_typ.can_be_single): 
            org0_.add_slot("NAME", tok_typ.vals[0].upper(), False, 0)
            res.is_doubt = False
            res.is_gsk = True
            return res
        for ty in tok_typ.vals: 
            if (nam is not None and ty == nam.misc_typ and not "квартал" in ty): 
                continue
            org0_.add_slot("TYPE", ty, False, 0)
            if (ty == "поле"): 
                res.is_doubt = True
        ignore_next = False
        if ((res.whitespaces_after_count < 3) and res.end_token.next0_ is not None): 
            ttt = MiscLocationHelper.check_territory(res.end_token.next0_)
            if (ttt is not None and OrgItemToken.__try_parse(ttt.next0_, True, lev + 1, ad) is None): 
                res.end_token = ttt
                ignore_next = True
            elif (nam is not None): 
                tok_typ2 = OrgTypToken.try_parse(res.end_token.next0_, False, None)
                if (tok_typ2 is not None): 
                    rrr2 = OrgItemToken.__try_parse(res.end_token.next0_, False, lev + 1, ad)
                    if (rrr2 is None or rrr2.end_char <= tok_typ2.end_char): 
                        res.end_token = tok_typ2.end_token
                        for ty in tok_typ2.vals: 
                            org0_.add_slot("TYPE", ty, False, 0)
        if (((res.whitespaces_after_count < 3) and nam is not None and (isinstance(res.end_token.next0_, TextToken))) and res.end_token.next0_.length_char == 1 and res.end_token.next0_.chars.is_letter): 
            tt3 = res.end_token.next0_
            if (((tt3.next0_ is not None and tt3.next0_.is_char('.') and (isinstance(tt3.next0_.next0_, TextToken))) and tt3.next0_.next0_.chars.is_letter and tt3.next0_.next0_.length_char == 1) and tt3.next0_.next0_.next0_ is not None and tt3.next0_.next0_.next0_.is_char('.')): 
                res.end_token = tt3.next0_.next0_.next0_
        if ((res.whitespaces_after_count < 3) and not tok_typ.not_org): 
            tt = res.end_token.next0_
            next0__ = OrgItemToken.__try_parse(tt, False, lev + 1, ad)
            if (next0__ is not None): 
                merge = True
                if (next0__.is_gsk): 
                    merge = False
                    if ((nam is not None and nam.name is not None and nam.number is None) and next0__.referent.find_slot("NAME", None, True) is None and next0__.referent.find_slot("NUMBER", None, True) is not None): 
                        for ty in org0_.get_string_values("TYPE"): 
                            if (next0__.referent.find_slot("TYPE", ty, True) is not None): 
                                merge = True
                if (merge): 
                    res.end_token = next0__.end_token
                    for s in next0__.referent.slots: 
                        res.referent.add_slot(s.type_name, s.value, False, 0)
                ignore_next = True
            else: 
                if (tt is not None and tt.is_value("ПРИ", None)): 
                    tt = tt.next0_
                rt = t.kit.process_referent("ORGANIZATION", tt, None)
                if (rt is not None): 
                    pass
                if (rt is not None): 
                    res.end_token = rt.end_token
                    ter = TerrItemToken.check_onto_item(res.end_token.next0_)
                    if (ter is not None): 
                        res.end_token = ter.end_token
                    ignore_next = True
        suff_name = None
        if (not ignore_next and (res.whitespaces_after_count < 2) and not tok_typ.not_org): 
            tok_typ2 = OrgTypToken.try_parse(res.end_token.next0_, True, ad)
            if (tok_typ2 is not None): 
                res.end_token = tok_typ2.end_token
                if (tok_typ2.is_doubt and nam is not None and nam.name is not None): 
                    suff_name = tok_typ2.vals[0]
                else: 
                    for ty in tok_typ2.vals: 
                        org0_.add_slot("TYPE", ty, False, 0)
                if (nam is not None and nam.number is None): 
                    nam2 = NameToken.try_parse(res.end_token.next0_, GeoTokenType.ORG, 0, False)
                    if ((nam2 is not None and nam2.number is not None and nam2.name is None) and nam2.pref is None): 
                        nam.number = nam2.number
                        res.end_token = nam2.end_token
        if (nam is None): 
            res.set_gsk()
            return res
        if (nam is not None and nam.name is not None): 
            if (nam.pref is not None): 
                org0_.add_slot("NAME", "{0} {1}".format(nam.pref, nam.name), False, 0)
                if (suff_name is not None): 
                    org0_.add_slot("NAME", "{0} {1} {2}".format(nam.pref, nam.name, suff_name), False, 0)
            else: 
                org0_.add_slot("NAME", nam.name, False, 0)
                if (suff_name is not None): 
                    org0_.add_slot("NAME", "{0} {1}".format(nam.name, suff_name), False, 0)
        elif (nam.pref is not None): 
            org0_.add_slot("NAME", nam.pref, False, 0)
        elif (nam.number is not None and (res.whitespaces_after_count < 2)): 
            nam2 = NameToken.try_parse(res.end_token.next0_, GeoTokenType.ORG, 0, False)
            if (nam2 is not None and nam2.name is not None and nam2.number is None): 
                res.end_token = nam2.end_token
                org0_.add_slot("NAME", nam2.name, False, 0)
        if (nam.number is not None): 
            if (nam.misc_typ is not None): 
                org0_.add_slot("MISC2", "{0} {1}".format(nam.misc_typ, nam.number), False, 0)
            else: 
                org0_.add_slot("NUMBER", nam.number, False, 0)
        elif (res.end_token.next0_ is not None and res.end_token.next0_.is_hiphen and (isinstance(res.end_token.next0_.next0_, NumberToken))): 
            nam2 = NameToken.try_parse(res.end_token.next0_.next0_, GeoTokenType.ORG, 0, False)
            if (nam2 is not None and nam2.number is not None and nam2.name is None): 
                if (nam2.misc_typ is not None): 
                    org0_.add_slot("MISC2", "{0} {1}".format(nam2.misc_typ, nam2.number), False, 0)
                else: 
                    org0_.add_slot("NUMBER", nam2.number, False, 0)
                res.end_token = nam2.end_token
        ok1 = False
        cou = 0
        tt = res.begin_token
        while tt is not None and tt.end_char <= res.end_char: 
            if ((isinstance(tt, TextToken)) and tt.length_char > 1): 
                if (nam is not None and tt.begin_char >= nam.begin_char and tt.end_char <= nam.end_char): 
                    if (tok_typ is not None and tt.begin_char >= tok_typ.begin_char and tt.end_char <= tok_typ.end_char): 
                        pass
                    else: 
                        cou += 1
                if (not tt.chars.is_all_lower): 
                    ok1 = True
            elif (isinstance(tt, ReferentToken)): 
                ok1 = True
            tt = tt.next0_
        res.set_gsk()
        if (not ok1): 
            if (not res.is_gsk and not res.has_terr_keyword and not MiscLocationHelper.is_user_param_address(res)): 
                return None
        if (cou > 4): 
            return None
        if (tok_typ is not None and tok_typ.begin_token.is_value("СП", None)): 
            tt2 = res.end_token.next0_
            if (tt2 is not None and tt2.is_comma): 
                tt2 = tt2.next0_
            cits = CityItemToken.try_parse_list(tt2, 3, None)
            if (cits is not None and len(cits) == 2 and cits[0].typ == CityItemToken.ItemType.NOUN): 
                return None
        if (res.not_org and (res.whitespaces_after_count < 2)): 
            tt = res.end_token.next0_
            if ((isinstance(tt, TextToken)) and tt.length_char == 1 and ((tt.is_value("П", None) or tt.is_value("Д", None)))): 
                if (not AddressItemToken.check_house_after(tt, False, False)): 
                    res.end_token = res.end_token.next0_
                    if (res.end_token.next0_ is not None and res.end_token.next0_.is_char('.')): 
                        res.end_token = res.end_token.next0_
        if (tok_typ is not None and "лесничество" in tok_typ.vals and MiscLocationHelper.is_user_param_address(tok_typ)): 
            tt2 = tok_typ.end_token.next0_
            if (tt2 is not None and tt2.is_comma): 
                tt2 = tt2.next0_
            ait = AddressItemToken.try_parse_pure_item(tt2, None, None)
            if (ait is not None and ait.typ == AddressItemType.FLAT and ait.value is not None): 
                org0_.add_slot("NUMBER", ait.value, False, 0)
                res.end_token = ait.end_token
                tt2 = res.end_token.next0_
                while tt2 is not None: 
                    if (not tt2.is_comma_and): 
                        break
                    ait = AddressItemToken.try_parse_pure_item(tt2.next0_, None, None)
                    if (ait is None or ait.value is None): 
                        break
                    if (ait.typ != AddressItemType.NUMBER and ait.typ != AddressItemType.FLAT): 
                        break
                    org0_.add_slot("NUMBER", ait.value, False, 0)
                    tt2 = ait.end_token
                    res.end_token = tt2
                    tt2 = tt2.next0_
            else: 
                nu = NumToken.try_parse(tt2, GeoTokenType.ORG)
                if (nu is not None): 
                    if (nu.misc_type is not None): 
                        org0_.add_slot("MISC2", "{0} {1}".format(nu.misc_type, nu.value), False, 0)
                    else: 
                        org0_.add_slot("NUMBER", nu.value, False, 0)
                    res.end_token = nu.end_token
                else: 
                    sit = StreetItemToken.try_parse(tt2, None, False, None)
                    if (sit is not None and sit.typ == StreetItemType.NOUN and "КВАРТАЛ" in sit.termin.canonic_text): 
                        tt2 = sit.end_token.next0_
                        while tt2 is not None: 
                            num = NumToken.try_parse(tt2, GeoTokenType.ORG)
                            if (num is None): 
                                break
                            org0_.add_slot("NUMBER", num.value, False, 0)
                            res.end_token = num.end_token
                            tt2 = num.end_token.next0_
                            if (tt2 is None): 
                                break
                            if (not tt2.is_comma_and): 
                                break
                            tt2 = tt2.next0_
        if (not ignore_next and (res.whitespaces_after_count < 2) and not tok_typ.not_org): 
            ttt2 = res.end_token.next0_
            if (ttt2 is not None and ttt2.is_comma): 
                ttt2 = ttt2.next0_
            nn = NumToken.try_parse(ttt2, GeoTokenType.ORG)
            if (nn is not None and nn.has_spec_word): 
                res.end_token = nn.end_token
                if (nn.misc_type is not None): 
                    org0_.add_slot("MISC2", "{0} {1}".format(nn.misc_type, nn.value), False, 0)
                else: 
                    num = org0_.get_string_value("NUMBER")
                    if (num is None): 
                        num = nn.value
                    else: 
                        num = "{0}+{1}".format(num, nn.value)
                    org0_.add_slot("NUMBER", num, True, 0)
        return res
    
    @staticmethod
    def try_parse_railway(t : 'Token') -> 'StreetItemToken':
        if (not (isinstance(t, TextToken)) or not t.chars.is_letter): 
            return None
        if (t.is_value("ДОРОГА", None) and (t.whitespaces_after_count < 3)): 
            next0__ = OrgItemToken.try_parse_railway(t.next0_)
            if (next0__ is not None): 
                next0__.begin_token = t
                return next0__
        ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (ad.olevel > 0): 
            return None
        ad.olevel += 1
        res = OrgItemToken.__try_parse_railway(t)
        ad.olevel -= 1
        return res
    
    @staticmethod
    def __try_parse_railway_org(t : 'Token') -> 'ReferentToken':
        if (t is None): 
            return None
        cou = 0
        ok = False
        tt = t
        while tt is not None and (cou < 4): 
            if (isinstance(tt, TextToken)): 
                val = tt.term
                if (val == "Ж" or val.startswith("ЖЕЛЕЗ")): 
                    ok = True
                    break
                if (LanguageHelper.ends_with(val, "ЖД")): 
                    ok = True
                    break
            tt = tt.next0_; cou += 1
        if (not ok): 
            return None
        rt = t.kit.process_referent("ORGANIZATION", t, None)
        if (rt is None): 
            return None
        for ty in rt.referent.get_string_values("TYPE"): 
            if (ty.endswith("дорога")): 
                return rt
        return None
    
    @staticmethod
    def __try_parse_railway(t : 'Token') -> 'StreetItemToken':
        rt0 = OrgItemToken.__try_parse_railway_org(t)
        if (rt0 is not None): 
            res = StreetItemToken._new1522(t, rt0.end_token, StreetItemType.FIX, True)
            res.value = rt0.referent.get_string_value("NAME")
            t = res.end_token.next0_
            if (t is not None and t.is_comma): 
                t = t.next0_
            next0__ = OrgItemToken.__try_parse_rzd_dir(t)
            if (next0__ is not None): 
                res.end_token = next0__.end_token
                res.value = "{0} {1}".format(res.value, next0__.value)
            elif ((isinstance(t, TextToken)) and t.morph.class0_.is_adjective and not t.chars.is_all_lower): 
                ok = False
                if (t.is_newline_after or t.next0_ is None): 
                    ok = True
                elif (t.next0_.is_char_of(".,")): 
                    ok = True
                elif (AddressItemToken.check_house_after(t.next0_, False, False) or AddressItemToken.check_km_after(t.next0_)): 
                    ok = True
                if (ok): 
                    res.value = "{0} {1} НАПРАВЛЕНИЕ".format(res.value, t.term)
                    res.end_token = t
            if (res.value == "РОССИЙСКИЕ ЖЕЛЕЗНЫЕ ДОРОГИ"): 
                res.noun_is_doubt_coef = 2
            return res
        dir0_ = OrgItemToken.__try_parse_rzd_dir(t)
        if (dir0_ is not None and dir0_.noun_is_doubt_coef == 0): 
            return dir0_
        return None
    
    @staticmethod
    def __try_parse_rzd_dir(t : 'Token') -> 'StreetItemToken':
        napr = None
        tt0 = None
        tt1 = None
        val = None
        cou = 0
        tt = t
        first_pass3984 = True
        while True:
            if first_pass3984: first_pass3984 = False
            else: tt = tt.next0_; cou += 1
            if (not (tt is not None and (cou < 4))): break
            if (tt.is_char_of(",.")): 
                continue
            if (tt.is_newline_before): 
                break
            if (tt.is_value("НАПРАВЛЕНИЕ", None)): 
                napr = tt
                continue
            if (tt.is_value("НАПР", None)): 
                if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                    tt = tt.next0_
                napr = tt
                continue
            npt = MiscLocationHelper._try_parse_npt(tt)
            if (npt is not None and len(npt.adjectives) > 0 and npt.noun.is_value("КОЛЬЦО", None)): 
                tt0 = tt
                tt1 = npt.end_token
                val = npt.get_normal_case_text(None, MorphNumber.SINGULAR, MorphGender.UNDEFINED, False)
                break
            if ((isinstance(tt, TextToken)) and ((not tt.chars.is_all_lower or napr is not None)) and ((tt.morph.gender) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                tt1 = tt
                tt0 = tt1
                continue
            if ((((isinstance(tt, TextToken)) and ((not tt.chars.is_all_lower or napr is not None)) and tt.next0_ is not None) and tt.next0_.is_hiphen and (isinstance(tt.next0_.next0_, TextToken))) and ((tt.next0_.next0_.morph.gender) & (MorphGender.NEUTER)) != (MorphGender.UNDEFINED)): 
                tt0 = tt
                tt = tt.next0_.next0_
                tt1 = tt
                continue
            break
        if (tt0 is None): 
            return None
        res = StreetItemToken._new1523(tt0, tt1, StreetItemType.FIX, True, 1)
        if (val is not None): 
            res.value = val
        else: 
            res.value = tt1.get_normal_case_text(MorphClass.ADJECTIVE, MorphNumber.SINGULAR, MorphGender.NEUTER, False)
            if (tt0 != tt1): 
                res.value = "{0} {1}".format(tt0.term, res.value)
            res.value += " НАПРАВЛЕНИЕ"
        if (napr is not None and napr.end_char > res.end_char): 
            res.end_token = napr
        t = res.end_token.next0_
        if (t is not None and t.is_comma): 
            t = t.next0_
        if (t is not None): 
            rt0 = OrgItemToken.__try_parse_railway_org(t)
            if (rt0 is not None): 
                res.value = "{0} {1}".format(rt0.referent.get_string_value("NAME"), res.value)
                res.end_token = rt0.end_token
                res.noun_is_doubt_coef = 0
        return res
    
    def __try_parse_details(self) -> None:
        from pullenti.ner.geo.internal.NameToken import NameToken
        from pullenti.ner.geo.internal.CityAttachHelper import CityAttachHelper
        if (self.whitespaces_after_count > 2): 
            return
        t = self.end_token.next0_
        if (t is None): 
            return
        is_garaz = False
        for s in self.referent.slots: 
            if (s.type_name == "TYPE" and (isinstance(s.value, str))): 
                ty = Utils.asObjectOrNull(s.value, str)
                if ("гараж" in ty or "автомоб" in ty): 
                    is_garaz = True
                    break
        t1 = None
        tok = OrgItemToken._m_onto.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            t1 = tok.end_token.next0_
        elif (is_garaz and self.referent.find_slot("NAME", None, True) is None): 
            t1 = self.end_token.next0_
        if (t1 is not None): 
            t = t1
            cits = CityItemToken.try_parse_list(t, 5, None)
            if (cits is not None and len(cits) > 1): 
                rt = CityAttachHelper.try_define(cits, None, False)
                if (rt is not None): 
                    self.end_token = rt.end_token
                    t = self.end_token.next0_
                    self.__merge_with(rt.referent)
            ait = AddressItemToken.try_parse(t, False, None, None)
            if (ait is not None and ait.typ == AddressItemType.STREET and ait.referent is not None): 
                self.end_token = ait.end_token
                t = self.end_token.next0_
                self.__merge_with(ait.referent)
                ait = AddressItemToken.try_parse(t, False, None, None)
                if (ait is not None and ((ait.typ == AddressItemType.HOUSE or ait.typ == AddressItemType.NUMBER)) and ait.value is not None): 
                    self.referent.add_slot("NUMBER", ait.value, False, 0)
                    self.end_token = ait.end_token
                    t = self.end_token.next0_
            elif ((ait is not None and ait.typ == AddressItemType.HOUSE and ait.house_type != AddressHouseType.SPECIAL) and ait.value is not None): 
                self.referent.add_slot("NUMBER", ait.value, False, 0)
                self.end_token = ait.end_token
                t = self.end_token.next0_
            if (tok is not None and t == tok.end_token.next0_): 
                if (t is None or tok.is_newline_after): 
                    self.end_token = tok.end_token
                    return
                name = NameToken.try_parse(t, GeoTokenType.ORG, 0, False)
                if (name is not None and name.name is not None and self.referent.find_slot("NAME", None, True) is None): 
                    self.referent.add_slot("NAME", name.name, False, 0)
                    if (name.number is not None): 
                        self.referent.add_slot("NUMBER", name.number, False, 0)
                    self.end_token = name.end_token
                    t = self.end_token.next0_
        if (is_garaz): 
            ait = AddressItemToken.try_parse(t, False, None, None)
            if (ait is not None and ait.typ == AddressItemType.STREET and ait.referent is not None): 
                pass
            elif (ait is not None and ait.typ == AddressItemType.HOUSE and ait.value is not None): 
                self.referent.add_slot("NUMBER", ait.value, False, 0)
                self.end_token = ait.end_token
                t = self.end_token.next0_
            elif (ait is not None and ait.detail_type == AddressDetailType.NEAR): 
                ait2 = AddressItemToken.try_parse(ait.end_token.next0_, False, None, None)
                if (ait2 is not None and ait2.typ == AddressItemType.HOUSE and ait2.value is not None): 
                    self.referent.add_slot("NUMBER", ait2.value, False, 0)
                    self.end_token = ait2.end_token
                    t = self.end_token.next0_
    
    def __merge_with(self, r : 'Referent') -> None:
        names = self.referent.get_string_values("NAME")
        for n in r.get_string_values("NAME"): 
            if (len(names) > 0): 
                for n0 in names: 
                    self.referent.add_slot("NAME", "{0} {1}".format(n0, n), False, 0)
            else: 
                self.referent.add_slot("NAME", n, False, 0)
        for n in r.get_string_values("NUMBER"): 
            self.referent.add_slot("NUMBER", n, False, 0)
        for n in r.get_string_values("MISC"): 
            self.referent.add_slot("MISC", n, False, 0)
        for n in r.get_string_values("MISC2"): 
            self.referent.add_slot("MISC2", n, False, 0)
    
    _m_onto = None
    
    @staticmethod
    def initialize() -> None:
        OrgItemToken._m_onto = TerminCollection()
        t = None
        t = Termin("В РАЙОНЕ")
        t.add_abridge("В Р-НЕ")
        OrgItemToken._m_onto.add(t)
        t = Termin("РАЙОН")
        t.add_abridge("Р-Н")
        t.add_abridge("Р-ОН")
        OrgItemToken._m_onto.add(t)
        OrgItemToken._m_onto.add(Termin("ПО"))
        OrgItemToken._m_onto.add(Termin("ОКОЛО"))
        OrgItemToken._m_onto.add(Termin("ВО ДВОРЕ"))