# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import xml.etree
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.core.Termin import Termin
from pullenti.ner.org.OrgProfile import OrgProfile
from pullenti.ner.org.internal.OrgItemTypeTyp import OrgItemTypeTyp

class OrgItemTypeTermin(Termin):
    
    def __init__(self, s : str, lang_ : 'MorphLang'=None, p1 : 'OrgProfile'=OrgProfile.UNDEFINED, p2 : 'OrgProfile'=OrgProfile.UNDEFINED) -> None:
        super().__init__(s, lang_, False)
        self.__m_typ = OrgItemTypeTyp.UNDEFINED
        self.must_be_partof_name = False
        self.is_pure_prefix = False
        self.can_be_normal_dep = False
        self.can_has_number = False
        self.can_has_single_name = False
        self.can_has_latin_name = False
        self.must_has_capital_name = False
        self.is_top = False
        self.can_be_single_geo = False
        self.is_doubt_word = False
        self.coeff = 0
        self.profiles = list()
        if (p1 != OrgProfile.UNDEFINED): 
            self.profiles.append(p1)
        if (p2 != OrgProfile.UNDEFINED): 
            self.profiles.append(p2)
    
    @property
    def typ(self) -> 'OrgItemTypeTyp':
        if (self.is_pure_prefix): 
            return OrgItemTypeTyp.PREFIX
        return self.__m_typ
    @typ.setter
    def typ(self, value) -> 'OrgItemTypeTyp':
        if (value == OrgItemTypeTyp.PREFIX): 
            self.is_pure_prefix = True
            self.__m_typ = OrgItemTypeTyp.ORG
        else: 
            self.__m_typ = value
            if (self.__m_typ == OrgItemTypeTyp.DEP or self.__m_typ == OrgItemTypeTyp.DEPADD): 
                if (not OrgProfile.UNIT in self.profiles): 
                    self.profiles.append(OrgProfile.UNIT)
        return value
    
    @property
    def _profile(self) -> 'OrgProfile':
        return OrgProfile.UNDEFINED
    @_profile.setter
    def _profile(self, value) -> 'OrgProfile':
        self.profiles.append(value)
        return value
    
    def __copy_from(self, it : 'OrgItemTypeTermin') -> None:
        self.profiles.extend(it.profiles)
        self.is_pure_prefix = it.is_pure_prefix
        self.can_be_normal_dep = it.can_be_normal_dep
        self.can_has_number = it.can_has_number
        self.can_has_single_name = it.can_has_single_name
        self.can_has_latin_name = it.can_has_latin_name
        self.must_be_partof_name = it.must_be_partof_name
        self.must_has_capital_name = it.must_has_capital_name
        self.is_top = it.is_top
        self.can_be_normal_dep = it.can_be_normal_dep
        self.can_be_single_geo = it.can_be_single_geo
        self.is_doubt_word = it.is_doubt_word
        self.coeff = it.coeff
    
    @staticmethod
    def deserialize_src(xml0_ : xml.etree.ElementTree.Element, set0_ : 'OrgItemTypeTermin') -> typing.List['OrgItemTypeTermin']:
        res = list()
        is_set = Utils.getXmlLocalName(xml0_) == "set"
        if (is_set): 
            set0_ = OrgItemTypeTermin(None)
            res.append(set0_)
        if (xml0_.attrib is None): 
            return res
        for a in xml0_.attrib.items(): 
            nam = Utils.getXmlAttrLocalName(a)
            if (not nam.startswith("name")): 
                continue
            lang_ = MorphLang.RU
            if (nam == "nameUa"): 
                lang_ = MorphLang.UA
            elif (nam == "nameEn"): 
                lang_ = MorphLang.EN
            it = None
            for s in Utils.splitString(a[1], ';', False): 
                if (not Utils.isNullOrEmpty(s)): 
                    if (it is None): 
                        it = OrgItemTypeTermin(s, lang_)
                        res.append(it)
                        if (set0_ is not None): 
                            it.__copy_from(set0_)
                    else: 
                        it.add_variant(s, False)
        for a in xml0_.attrib.items(): 
            nam = Utils.getXmlAttrLocalName(a)
            if (nam.startswith("name")): 
                continue
            if (nam.startswith("abbr")): 
                lang_ = MorphLang.RU
                if (nam == "abbrUa"): 
                    lang_ = MorphLang.UA
                elif (nam == "abbrEn"): 
                    lang_ = MorphLang.EN
                for r in res: 
                    if (r.lang.equals(lang_)): 
                        r.acronym = a[1]
                continue
            if (nam == "profile"): 
                li = list()
                for s in Utils.splitString(a[1], ';', False): 
                    try: 
                        p = Utils.valToEnum(s, OrgProfile)
                        if (p != OrgProfile.UNDEFINED): 
                            li.append(p)
                    except Exception as ex: 
                        pass
                for r in res: 
                    r.profiles = li
                continue
            if (nam == "coef"): 
                v = float(a[1])
                for r in res: 
                    r.coeff = v
                continue
            if (nam == "partofname"): 
                for r in res: 
                    r.must_be_partof_name = a[1] == "true"
                continue
            if (nam == "top"): 
                for r in res: 
                    r.is_top = a[1] == "true"
                continue
            if (nam == "geo"): 
                for r in res: 
                    r.can_be_single_geo = a[1] == "true"
                continue
            if (nam == "purepref"): 
                for r in res: 
                    r.is_pure_prefix = a[1] == "true"
                continue
            if (nam == "number"): 
                for r in res: 
                    r.can_has_number = a[1] == "true"
                continue
            raise Utils.newException("Unknown Org Type Tag: " + Utils.getXmlAttrName(a), None)
        return res
    
    @staticmethod
    def _new2465(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : 'OrgItemTypeTyp', _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.coeff = _arg4
        res.typ = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new2466(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : 'OrgItemTypeTyp', _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.coeff = _arg4
        res.typ = _arg5
        res.is_top = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new2469(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.coeff = _arg4
        return res
    
    @staticmethod
    def _new2470(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res._profile = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new2471(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : float, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.coeff = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new2474(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new2475(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new2476(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2477(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        return res
    
    @staticmethod
    def _new2478(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new2484(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_top = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new2486(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_top = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new2487(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2489(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new2492(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2494(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res.can_be_normal_dep = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2496(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2497(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_single_geo = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2498(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2500(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_number = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2507(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2508(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2509(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2512(_arg1 : str, _arg2 : float, _arg3 : 'MorphLang', _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.lang = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2521(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new2522(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new2523(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new2526(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        return res
    
    @staticmethod
    def _new2531(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res._profile = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2535(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2536(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgProfile', _arg5 : 'OrgItemTypeTyp', _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res._profile = _arg4
        res.typ = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2539(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2545(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile', _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res._profile = _arg5
        res.can_be_single_geo = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2546(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_single_name = _arg6
        res.can_has_latin_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new2553(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2565(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_be_single_geo = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2567(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile', _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res._profile = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2573(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.is_doubt_word = _arg3
        return res
    
    @staticmethod
    def _new2576(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : 'OrgProfile', _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        res.can_has_latin_name = _arg7
        return res
    
    @staticmethod
    def _new2577(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : str, _arg6 : bool, _arg7 : 'OrgProfile', _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.acronym = _arg5
        res.can_has_number = _arg6
        res._profile = _arg7
        res.can_has_latin_name = _arg8
        return res
    
    @staticmethod
    def _new2578(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2592(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.acronym = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2593(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : str, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.acronym = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2594(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new2605(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : str, _arg5 : 'OrgItemTypeTyp', _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.acronym = _arg4
        res.typ = _arg5
        res.can_has_number = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2606(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2607(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new2610(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_top = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        res.can_be_single_geo = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new2611(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.is_top = _arg5
        res.can_has_single_name = _arg6
        res.can_has_latin_name = _arg7
        res.can_be_single_geo = _arg8
        return res
    
    @staticmethod
    def _new2615(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2616(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2617(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2618(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2619(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2620(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.must_be_partof_name = _arg4
        return res
    
    @staticmethod
    def _new2621(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.canonic_text = _arg4
        return res
    
    @staticmethod
    def _new2623(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.must_be_partof_name = _arg5
        return res
    
    @staticmethod
    def _new2624(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.canonic_text = _arg5
        return res
    
    @staticmethod
    def _new2630(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_number = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2631(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        return res
    
    @staticmethod
    def _new2634(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2636(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_be_single_geo = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2637(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.typ = _arg3
        res.coeff = _arg4
        res.can_be_single_geo = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2638(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2639(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2641(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2642(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.is_doubt_word = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2643(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.is_doubt_word = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2644(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2645(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : str, _arg5 : 'OrgItemTypeTyp', _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.acronym = _arg4
        res.typ = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2650(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2657(_arg1 : str, _arg2 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        return res
    
    @staticmethod
    def _new2658(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        return res
    
    @staticmethod
    def _new2660(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new2665(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.is_doubt_word = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new2666(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.is_doubt_word = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2667(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_number = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2669(_arg1 : str, _arg2 : str, _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.acronym = _arg2
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_number = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2670(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_number = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2672(_arg1 : str, _arg2 : str, _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.acronym = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new2675(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.acronym = _arg3
        res.typ = _arg4
        res.can_be_normal_dep = _arg5
        return res
    
    @staticmethod
    def _new2678(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_be_normal_dep = _arg3
        return res
    
    @staticmethod
    def _new2679(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        return res
    
    @staticmethod
    def _new2692(_arg1 : str, _arg2 : str, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.acronym = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2693(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_be_normal_dep = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new2694(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2698(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        res.is_doubt_word = _arg4
        return res
    
    @staticmethod
    def _new2699(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        res.is_doubt_word = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2700(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_number = _arg4
        res.is_doubt_word = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        return res
    
    @staticmethod
    def _new2708(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_number = _arg3
        return res
    
    @staticmethod
    def _new2709(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_number = _arg4
        return res
    
    @staticmethod
    def _new2710(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2711(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res._profile = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new2717(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new2720(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2724(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        return res
    
    @staticmethod
    def _new2741(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new2743(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2851(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.acronym_can_be_lower = _arg4
        res.can_be_single_geo = _arg5
        return res
    
    @staticmethod
    def _new2852(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new2855(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2856(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new2859(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        return res
    
    @staticmethod
    def _new2864(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : str, _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        res.acronym_smart = _arg5
        return res
    
    @staticmethod
    def _new2878(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str, _arg6 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        res.acronym_smart = _arg6
        return res
    
    @staticmethod
    def _new2896(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.acronym_smart = _arg4
        return res
    
    @staticmethod
    def _new2899(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : str, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.acronym = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2900(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : str, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.acronym = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2903(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res._profile = _arg4
        return res
    
    @staticmethod
    def _new2904(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2906(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        return res
    
    @staticmethod
    def _new2910(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2914(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.can_has_number = _arg4
        res.acronym = _arg5
        return res
    
    @staticmethod
    def _new2915(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        res.acronym = _arg6
        return res
    
    @staticmethod
    def _new2920(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : str, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.acronym = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        return res
    
    @staticmethod
    def _new2934(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2935(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2936(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : 'OrgProfile', _arg4 : bool, _arg5 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res._profile = _arg3
        res.can_has_latin_name = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new2937(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2938(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : 'OrgProfile', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res._profile = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2939(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : 'OrgProfile', _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res._profile = _arg5
        res.can_has_single_name = _arg6
        res.can_has_latin_name = _arg7
        return res
    
    @staticmethod
    def _new2940(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2941(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2942(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_single_name = _arg5
        res.can_has_latin_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new2945(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_be_normal_dep = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2947(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_be_normal_dep = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2948(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res.is_doubt_word = _arg5
        return res
    
    @staticmethod
    def _new2950(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.is_doubt_word = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2951(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res.is_doubt_word = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new2952(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_single_name = _arg3
        res.can_has_latin_name = _arg4
        res._profile = _arg5
        return res
    
    @staticmethod
    def _new2953(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_single_name = _arg4
        res.can_has_latin_name = _arg5
        res.is_doubt_word = _arg6
        return res
    
    @staticmethod
    def _new2954(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_single_name = _arg4
        return res
    
    @staticmethod
    def _new2955(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2967(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        return res
    
    @staticmethod
    def _new2968(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        return res
    
    @staticmethod
    def _new2969(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_be_single_geo = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new2970(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : str, _arg6 : bool, _arg7 : bool, _arg8 : bool, _arg9 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.acronym = _arg5
        res.can_has_latin_name = _arg6
        res.can_has_single_name = _arg7
        res.can_be_single_geo = _arg8
        res._profile = _arg9
        return res
    
    @staticmethod
    def _new2978(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2979(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        return res
    
    @staticmethod
    def _new2980(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : float, _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.typ = _arg3
        res.coeff = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new2981(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : 'OrgItemTypeTyp', _arg5 : float, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.coeff = _arg5
        res.can_has_latin_name = _arg6
        return res
    
    @staticmethod
    def _new2989(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : 'OrgItemTypeTyp', _arg5 : float, _arg6 : bool, _arg7 : str) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.typ = _arg4
        res.coeff = _arg5
        res.can_has_latin_name = _arg6
        res.acronym = _arg7
        return res
    
    @staticmethod
    def _new2993(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : bool, _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.can_has_latin_name = _arg3
        res.can_has_single_name = _arg4
        res.must_has_capital_name = _arg5
        res.can_has_number = _arg6
        return res
    
    @staticmethod
    def _new2994(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new2995(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res._profile = _arg7
        return res
    
    @staticmethod
    def _new2996(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res._profile = _arg8
        return res
    
    @staticmethod
    def _new3000(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.lang = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new3001(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        return res
    
    @staticmethod
    def _new3003(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.must_has_capital_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new3004(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res.can_has_number = _arg8
        return res
    
    @staticmethod
    def _new3006(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res.can_has_number = _arg8
        return res
    
    @staticmethod
    def _new3007(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : str, _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.acronym = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new3009(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_single_name = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new3010(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_be_single_geo = _arg7
        return res
    
    @staticmethod
    def _new3018(_arg1 : str, _arg2 : float, _arg3 : str, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.acronym = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.can_has_number = _arg7
        return res
    
    @staticmethod
    def _new3019(_arg1 : str, _arg2 : str, _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool, _arg7 : bool, _arg8 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.acronym = _arg2
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        res.can_has_single_name = _arg6
        res.must_has_capital_name = _arg7
        res.can_has_number = _arg8
        return res
    
    @staticmethod
    def _new3024(_arg1 : str, _arg2 : 'MorphLang', _arg3 : float, _arg4 : 'OrgItemTypeTyp', _arg5 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2)
        res.coeff = _arg3
        res.typ = _arg4
        res.can_has_latin_name = _arg5
        return res
    
    @staticmethod
    def _new3025(_arg1 : str, _arg2 : float, _arg3 : 'OrgItemTypeTyp', _arg4 : bool, _arg5 : bool, _arg6 : 'OrgProfile') -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.typ = _arg3
        res.can_has_latin_name = _arg4
        res.can_has_number = _arg5
        res._profile = _arg6
        return res
    
    @staticmethod
    def _new3029(_arg1 : str, _arg2 : float, _arg3 : bool, _arg4 : 'OrgItemTypeTyp', _arg5 : bool, _arg6 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.coeff = _arg2
        res.can_be_normal_dep = _arg3
        res.typ = _arg4
        res.can_has_number = _arg5
        res.can_be_single_geo = _arg6
        return res
    
    @staticmethod
    def _new3042(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'OrgProfile', _arg4 : bool, _arg5 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1, _arg2, _arg3)
        res.can_has_latin_name = _arg4
        res.coeff = _arg5
        return res
    
    @staticmethod
    def _new3047(_arg1 : str, _arg2 : bool, _arg3 : float) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.can_has_latin_name = _arg2
        res.coeff = _arg3
        return res
    
    @staticmethod
    def _new3051(_arg1 : str, _arg2 : 'OrgItemTypeTyp', _arg3 : float, _arg4 : bool) -> 'OrgItemTypeTermin':
        res = OrgItemTypeTermin(_arg1)
        res.typ = _arg2
        res.coeff = _arg3
        res.can_has_latin_name = _arg4
        return res