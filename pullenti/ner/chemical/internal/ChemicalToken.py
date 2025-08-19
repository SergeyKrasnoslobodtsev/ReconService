# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.chemical.ChemicalFormulaReferent import ChemicalFormulaReferent
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.NumberToken import NumberToken
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.Token import Token
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.chemical.internal.ChemicalUnit import ChemicalUnit
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.TerminCollection import TerminCollection

class ChemicalToken(MetaToken):
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (self.hiphen_before): 
            print("-", end="", file=res)
        if (self.name is not None): 
            print(self.name, end="", file=res)
        if (self.subtokens is not None): 
            print(self.bracket, end="", file=res)
            for s in self.subtokens: 
                print(str(s), end="", file=res)
            print((']' if self.bracket == '[' else ')'), end="", file=res)
        if (self.items is not None and self.name is None): 
            for u in self.items: 
                print(u.mnem[0], end="", file=res)
                if (len(u.mnem) > 1): 
                    print(str.lower(u.mnem[1]), end="", file=res)
        if (self.num > 0): 
            print(self.num, end="", file=res)
        return Utils.toStringStringIO(res)
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.subtokens = None
        self.bracket = chr(0)
        self.hiphen_before = False
        self.name = None
        self.items = None
        self.num = 0
        self.is_doubt = False
    
    @staticmethod
    def try_parse_list(t : 'Token', lev : int=0) -> typing.List['ChemicalToken']:
        ChemicalToken.initialize()
        res = None
        tt = t
        first_pass3817 = True
        while True:
            if first_pass3817: first_pass3817 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            it = ChemicalToken.__try_parse(tt, (None if res is None or len(res) == 0 else res[len(res) - 1]), lev)
            if (it is not None): 
                if (res is None): 
                    res = list()
                if (it.name is None and len(res) > 0 and it.is_whitespace_before): 
                    if (res[len(res) - 1].name is None): 
                        break
                res.append(it)
                tt = it.end_token
                continue
            if ((tt.is_value("ИЛИ", None) and res is not None and len(res) == 1) and res[0].name is not None): 
                it = ChemicalToken.__try_parse(tt.next0_, None, lev)
                if (it is not None and it.name is not None): 
                    res.append(it)
                    tt = it.end_token
                    continue
            break
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', prev : 'ChemicalToken', lev : int) -> 'ChemicalToken':
        if (lev > 3): 
            return None
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        if (tt.is_char_of("[(")): 
            li = ChemicalToken.try_parse_list(tt.next0_, lev + 1)
            if (li is None or len(li) == 0): 
                return None
            ee = li[len(li) - 1].end_token.next0_
            if (ee is None or not ee.is_char_of("])")): 
                return None
            ct = ChemicalToken._new532(t, ee, li)
            if (tt.is_char('(')): 
                ct.bracket = '('
            else: 
                ct.bracket = '['
            ct.__add_num()
            return ct
        if (tt.is_hiphen): 
            if (prev is None): 
                return None
            must_be_name = False
            if (tt.is_whitespace_before or tt.is_whitespace_after): 
                if (prev.name is not None): 
                    pass
                else: 
                    must_be_name = True
            ct = ChemicalToken.__try_parse(tt.next0_, None, lev + 1)
            if (ct is None): 
                return None
            if (must_be_name and ct.name is None): 
                return None
            if (prev.name is not None and ct.name is not None): 
                return None
            if (prev.name is None and ct.name is None): 
                ct.hiphen_before = True
            ct.begin_token = tt
            return ct
        if (tt.chars.is_letter and not tt.chars.is_all_lower): 
            str0_ = tt.get_source_text()
            cus = None
            i = 0
            i = 0
            while i < len(str0_): 
                ch0 = str0_[i]
                if (str.islower(ch0)): 
                    break
                if ((ord(ch0)) > 0x80): 
                    ch0 = LanguageHelper.get_lat_for_cyr(ch0)
                    if ((ord(ch0)) == 0): 
                        break
                mnem = "{0}".format(ch0)
                if (((i + 1) < len(str0_)) and str.islower(str0_[i + 1])): 
                    ch1 = str.upper(str0_[i + 1])
                    if ((ord(ch1)) > 0x80): 
                        ch1 = LanguageHelper.get_lat_for_cyr(ch1)
                        if ((ord(ch1)) == 0): 
                            break
                    mnem = "{0}{1}".format(ch0, ch1)
                    i += 1
                cu = None
                wrapcu533 = RefOutArgWrapper(None)
                inoutres534 = Utils.tryGetValue(ChemicalToken.__m_units_by_mnem, mnem, wrapcu533)
                cu = wrapcu533.value
                if (not inoutres534): 
                    break
                if (cus is None): 
                    cus = list()
                cus.append(cu)
                i += 1
            if (i >= len(str0_) and cus is not None): 
                ct = ChemicalToken._new535(t, t, cus)
                ct.__add_num()
                if (ct.num == 0 and ((not t.get_morph_class_in_dictionary().is_undefined or (t.length_char < 2)))): 
                    ct.is_doubt = True
                ii = 0
                while ii < (len(ct.items) - 1): 
                    jj = ii + 1
                    while jj < len(ct.items): 
                        if (ct.items[ii] == ct.items[jj]): 
                            ct.is_doubt = True
                        jj += 1
                    ii += 1
                if (len(ct.items) > 6): 
                    ct.is_doubt = True
                return ct
        tt1 = None
        t = (tt)
        first_pass3818 = True
        while True:
            if first_pass3818: first_pass3818 = False
            else: t = t.next0_
            if (not (t is not None)): break
            tok = ChemicalToken.__m_termins.try_parse(t, TerminParseAttr.NO)
            if (tok is not None): 
                t = tok.end_token
                tt1 = t
                continue
            npt = NounPhraseHelper.try_parse(t, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                ok = False
                ttt = npt.begin_token
                while ttt is not None and ttt.end_char <= npt.end_char: 
                    if (ChemicalToken.__can_be_part_name(Utils.asObjectOrNull(ttt, TextToken))): 
                        ok = True
                    ttt = ttt.next0_
                if (ok): 
                    t = npt.end_token
                    tt1 = t
                    continue
            if (ChemicalToken.__can_be_part_name(Utils.asObjectOrNull(t, TextToken))): 
                tt1 = t
                continue
            break
        if (tt1 is not None): 
            ci = ChemicalToken(tt, tt1)
            ci.name = MiscHelper.get_text_value(tt, tt1, GetTextAttr.FIRSTNOUNGROUPTONOMINATIVE)
            if (tt == tt1): 
                ci.is_doubt = True
                tok = ChemicalToken.__m_termins.try_parse(tt, TerminParseAttr.NO)
                if (tok is not None and (isinstance(tok.termin.tag, ChemicalUnit))): 
                    ci.is_doubt = False
            if (tt.previous is not None and tt.previous.is_value("ФОРМУЛА", None)): 
                ci.is_doubt = False
            return ci
        return None
    
    @staticmethod
    def __can_be_part_name(t : 'TextToken') -> bool:
        if (t is None): 
            return False
        tok = ChemicalToken.__m_termins.try_parse(t, TerminParseAttr.NO)
        if (tok is not None): 
            return True
        val = t.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
        mc = t.get_morph_class_in_dictionary()
        if (((((val.endswith("ИД") or val.endswith("ОЛ") or val.endswith("КИСЬ")) or val.endswith("ТАН") or val.endswith("ОЗА")) or val.endswith("ИН") or val.endswith("АТ")) or val.endswith("СИД") or val.startswith("ДИ")) or val.startswith("ТРИ") or val.startswith("ЧЕТЫР")): 
            if (mc.is_undefined): 
                return True
            if ((((val.endswith("КИСЬ") or val.endswith("ТОРИД") or val.endswith("ЦЕТАТ")) or val.endswith("РАЗИН") or val.endswith("КСИД")) or val.endswith("ФИД") or val.endswith("РИД")) or val.endswith("ОНАТ")): 
                return True
        if ((((((val.startswith("ГЕКСА") or val.startswith("ДЕКА") or val.startswith("ТЕТРА")) or val.startswith("ПЕНТА") or val.startswith("ГЕПТА")) or val.startswith("ОКТА") or val.startswith("НОНА")) or val.startswith("УНДЕКА") or val.startswith("ДОДЕКА")) or val.startswith("ЭЙКОЗА") or val.startswith("ГЕКТА")) or val.startswith("КИЛА") or val.startswith("МИРИА")): 
            return True
        return False
    
    @staticmethod
    def create_referent(li : typing.List['ChemicalToken']) -> 'ChemicalFormulaReferent':
        if (len(li) == 1): 
            if (li[0].is_doubt): 
                return None
            if ((ord(li[0].bracket)) != 0): 
                return None
            if (((li[0].items is not None and len(li[0].items) == 1)) or (((li[0].length_char < 5) or li[0].is_doubt))): 
                ok = False
                cou = 40
                tt = li[0].begin_token.previous
                while tt is not None and cou > 0: 
                    if (isinstance(tt.get_referent(), ChemicalFormulaReferent)): 
                        ok = True
                        break
                    if (ChemicalToken.__m_termins.try_parse(tt, TerminParseAttr.NO) is not None or ChemicalToken.__m_keywords.try_parse(tt, TerminParseAttr.NO) is not None): 
                        ok = True
                        break
                    tt = tt.previous; cou -= 1
                cou = 40
                if (not ok): 
                    tt = li[len(li) - 1].end_token.next0_
                    while tt is not None and cou > 0: 
                        if (isinstance(tt.get_referent(), ChemicalFormulaReferent)): 
                            ok = True
                            break
                        if (ChemicalToken.__m_termins.try_parse(tt, TerminParseAttr.NO) is not None or ChemicalToken.__m_keywords.try_parse(tt, TerminParseAttr.NO) is not None): 
                            ok = True
                            break
                        tt = tt.next0_; cou -= 1
                if (not ok): 
                    return None
        res = ChemicalFormulaReferent()
        val = None
        i = 0
        while i < len(li): 
            if (li[i].name is not None): 
                res.add_slot(ChemicalFormulaReferent.ATTR_NAME, li[i].name, False, 0)
            elif (val is None): 
                val = str(li[i])
            else: 
                val += str(li[i])
            i += 1
        if (val is not None): 
            res.value = val
        return res
    
    def __add_num(self) -> None:
        if (self.end_token.is_whitespace_after): 
            return
        if (isinstance(self.end_token.next0_, NumberToken)): 
            self.end_token = self.end_token.next0_
            self.num = self.end_token.int_value
            return
        if (self.end_token.next0_.length_char == 1): 
            for i in range(2, 10, 1):
                if (self.end_token.next0_.is_char(chr((0x2080 + i)))): 
                    self.end_token = self.end_token.next0_
                    self.num = 2
                    return
        if ((self.end_token.next0_ is not None and self.end_token.next0_.is_char_of("<[") and (isinstance(self.end_token.next0_.next0_, NumberToken))) and self.end_token.next0_.next0_.next0_ is not None and self.end_token.next0_.next0_.next0_.is_char_of(">]")): 
            self.num = self.end_token.next0_.next0_.int_value
            self.end_token = self.end_token.next0_.next0_.next0_
            return
    
    @staticmethod
    def initialize() -> None:
        if (ChemicalToken.UNITS is not None): 
            return
        ChemicalToken.__m_termins = TerminCollection()
        ChemicalToken.__m_keywords = TerminCollection()
        ChemicalToken.__m_units_by_mnem = dict()
        ChemicalToken.UNITS = list()
        all0_ = (((((("Водород,H;Гелий,He;Литий,Li;Бериллий,Be;Бор,B;Углерод,C;Азот,N;Кислород,O;Фтор,F;" + "Неон,Ne;Натрий,Na;Магний,Mg;Алюминий,Al;Кремний,Si;Фосфор,P;Сера,S;Хлор,Cl;Аргон,Ar;Калий,K;" + "Кальций,Ca;Скандий,Sc;Титан,Ti;Ванадий,V;Хром,Cr;Марганец,Mn;Железо,Fe;Кобальт,Co;Никель,Ni;") + "Медь,Cu;Цинк,Zn;Галлий,Ga;Германий,Ge;Мышьяк,As;Селен,Se;Бром,Br;Криптон,Kr;Рубидий,Rb;" + "Стронций,Sr;Иттрий,Y;Цирконий,Zr;Ниобий,Nb;Молибден,Mo;Технеций,Tc;Рутений,Ru;Родий,Rh;") + "Палладий,Pd;Серебро,Ag;Кадмий,Cd;Индий,In;Олово,Sn;Сурьма,Sb;Теллур,Te;Иод,I;Ксенон,Xe;" + "Цезий,Cs;Барий,Ba;Лантан,La;Церий,Ce;Празеодим,Pr;Неодим,Nd;Прометий,Pm;Самарий,Sm;") + "Европий,Eu;Гадолиний,Gd;Тербий,Tb;Диспрозий,Dy;Гольмий,Ho;Эрбий,Er;Тулий,Tm;Иттербий,Yb;" + "Лютеций,Lu;Гафний,Hf;Тантал,Ta;Вольфрам,W;Рений,Re;Осмий,Os;Иридий,Ir;Платина,Pt;") + "Золото,Au;Ртуть,Hg;Таллий,Tl;Свинец,Pb;Висмут,Bi;Полоний,Po;Астат,At;Радон,Rn;Франций,Fr;" + "Радий,Ra;Актиний,Ac;Торий,Th;Протактиний,Pa;Уран,U;Нептуний,Np;Плутоний,Pu;Америций,Am;") + "Кюрий,Cm;Берклий,Bk;Калифорний,Cf;Эйнштейний,Es;Фермий,Fm;Менделевий,Md;Нобелий,No;Лоуренсий,Lr;" + "Резерфордий,Rf;Дубний,Db;Сиборгий,Sg;Борий,Bh;Хассий,Hs;Мейтнерий,Mt;Дармштадтий,Ds;Рентгений,Rg;") + "Коперниций,Cn;Нихоний,Nh;Флеровий,Fl;Московий,Mc;Ливерморий,Lv;Теннессин,Ts;Оганесон,Og"
        for p in Utils.splitString(all0_.upper(), ';', False): 
            i = p.find(',')
            if (i < 0): 
                continue
            ci = ChemicalUnit(p[i + 1:], p[0:0+i])
            ChemicalToken.UNITS.append(ci)
            ChemicalToken.__m_termins.add(Termin._new84(ci.name_cyr, ci))
            ChemicalToken.__m_units_by_mnem[ci.mnem] = ci
        for s in ["КИСЛОТА", "РАСТВОР", "СПИРТ", "ВОДА", "СОЛЬ", "АММИАК", "БУТАН", "БЕНЗОЛ", "КЕРОСИН", "АМИН", "СКИПИДАР", "ОКИСЬ", "ГИДРИТ", "АММОНИЙ", "ПЕРЕКИСЬ", "КАРБОНАТ"]: 
            ChemicalToken.__m_termins.add(Termin(s))
        for s in ["МЕТАЛЛ", "ГАЗ", "ТОПЛИВО", "МОНОТОПЛИВО", "СМЕСЬ", "ХИМИЧЕСКИЙ", "МОЛЕКУЛА", "АТОМ", "МОЛЕКУЛЯРНЫЙ", "АТОМАРНЫЙ"]: 
            ChemicalToken.__m_keywords.add(Termin(s))
    
    __m_termins = None
    
    __m_keywords = None
    
    __m_units_by_mnem = None
    
    UNITS = None
    
    @staticmethod
    def _new532(_arg1 : 'Token', _arg2 : 'Token', _arg3 : typing.List['ChemicalToken']) -> 'ChemicalToken':
        res = ChemicalToken(_arg1, _arg2)
        res.subtokens = _arg3
        return res
    
    @staticmethod
    def _new535(_arg1 : 'Token', _arg2 : 'Token', _arg3 : typing.List['ChemicalUnit']) -> 'ChemicalToken':
        res = ChemicalToken(_arg1, _arg2)
        res.items = _arg3
        return res