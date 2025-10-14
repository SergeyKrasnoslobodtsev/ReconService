# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.address.internal.MetaStreet import MetaStreet
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.address.StreetKind import StreetKind

class StreetReferent(Referent):
    """ Сущность: улица, проспект, площадь, шоссе и т.п. Выделяется анализатором AddressAnalyzer.
    
    """
    
    def __init__(self) -> None:
        super().__init__(StreetReferent.OBJ_TYPENAME)
        self.__m_typs = None
        self.__m_higher = None;
        self.instance_of = MetaStreet._global_meta
    
    OBJ_TYPENAME = "STREET"
    """ Имя типа сущности TypeName ("STREET") """
    
    ATTR_TYPE = "TYP"
    """ Имя атрибута - тип (улица, переулок, площадь...) """
    
    ATTR_KIND = "KIND"
    """ Класс объекта (StreetKind) """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - наименование (м.б. несколько вариантов) """
    
    ATTR_NUMBER = "NUMBER"
    """ Имя атрибута - номер (м.б. несколько вариантов) """
    
    ATTR_HIGHER = "HIGHER"
    """ Имя атрибута - вышележащая улица (например, улица в микрорайоне) """
    
    ATTR_GEO = "GEO"
    """ Имя атрибута - географический объект """
    
    ATTR_REF = "REF"
    """ Имя атрибута - дополнительная ссылка (для территории организации - на саму организацию) """
    
    ATTR_MISC = "MISC"
    """ Имя атрибута - дополнительная информация """
    
    ATTR_PARAM = "PARAM"
    """ Имя атрибута - числовая дополнительная информация (типа - очередь для ГСК и т.п.) """
    
    ATTR_FIAS = "FIAS"
    """ Имя атрибута - код ФИАС (определяется анализатором FiasAnalyzer) """
    
    ATTR_BTI = "BTI"
    
    ATTR_OKM = "OKM"
    
    @property
    def typs(self) -> typing.List[str]:
        """ Тип(ы) """
        if (self.__m_typs is not None): 
            cou = 0
            for s in self.slots: 
                if (s.type_name == StreetReferent.ATTR_TYPE): 
                    cou += 1
            if (cou == len(self.__m_typs)): 
                return self.__m_typs
        res = list()
        for s in self.slots: 
            if (s.type_name == StreetReferent.ATTR_TYPE): 
                res.append(s.value)
        self.__m_typs = res
        return res
    
    @property
    def names(self) -> typing.List[str]:
        """ Наименования """
        res = list()
        for s in self.slots: 
            if (s.type_name == StreetReferent.ATTR_NAME): 
                res.append(s.value)
        return res
    
    @property
    def numbers(self) -> str:
        """ Номер улицы (16-я Парковая). Если несколько, то разделяются плюсом """
        nums = self.get_string_values(StreetReferent.ATTR_NUMBER)
        if (nums is None or len(nums) == 0): 
            return None
        if (len(nums) == 1): 
            return nums[0]
        nums.sort()
        tmp = io.StringIO()
        for n in nums: 
            if (tmp.tell() > 0): 
                print("+", end="", file=tmp)
            print(n, end="", file=tmp)
        return Utils.toStringStringIO(tmp)
    @numbers.setter
    def numbers(self, value) -> str:
        if (value is None): 
            return value
        i = value.find('+')
        if (i > 0): 
            self.numbers = value[0:0+i]
            self.numbers = value[i + 1:]
        else: 
            self.add_slot(StreetReferent.ATTR_NUMBER, value, False, 0)
        return value
    
    @property
    def higher(self) -> 'StreetReferent':
        """ Вышележащий объект (например, микрорайон для улицы) """
        return self.__m_higher
    @higher.setter
    def higher(self, value) -> 'StreetReferent':
        if (value == self): 
            return value
        if (value is not None): 
            d = value
            li = list()
            while d is not None: 
                if (d == self): 
                    return value
                elif (str(d) == str(self)): 
                    return value
                if (d in li): 
                    return value
                li.append(d)
                d = d.higher
        self.add_slot(StreetReferent.ATTR_HIGHER, None, True, 0)
        if (value is not None): 
            self.add_slot(StreetReferent.ATTR_HIGHER, value, True, 0)
        self.__m_higher = value
        return value
    
    @property
    def geos(self) -> typing.List['GeoReferent']:
        """ Ссылка на географические объекты """
        res = list()
        for a in self.slots: 
            if (a.type_name == StreetReferent.ATTR_GEO and (isinstance(a.value, GeoReferent))): 
                res.append(Utils.asObjectOrNull(a.value, GeoReferent))
        return res
    
    @property
    def city(self) -> 'GeoReferent':
        """ Город """
        for g in self.geos: 
            if (g.is_city): 
                return g
            elif (g.higher is not None and g.higher.is_city): 
                return g.higher
        return None
    
    @property
    def parent_referent(self) -> 'Referent':
        hi = self.higher
        if (hi is not None): 
            return hi
        return Utils.asObjectOrNull(self.get_slot_value(StreetReferent.ATTR_GEO), GeoReferent)
    
    def to_string_ex(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        tmp = io.StringIO()
        nam = self.get_string_value(StreetReferent.ATTR_NAME)
        misc = None
        typs_ = self.typs
        ki = self.kind
        if (len(typs_) > 0): 
            i = 0
            first_pass3798 = True
            while True:
                if first_pass3798: first_pass3798 = False
                else: i += 1
                if (not (i < len(typs_))): break
                if (nam is not None and typs_[i].upper() in nam and len(nam) > len(typs_[i])): 
                    continue
                if (tmp.tell() > 0): 
                    print('/', end="", file=tmp)
                print(typs_[i], end="", file=tmp)
        else: 
            print(("вулиця" if lang is not None and lang.is_ua else "улица"), end="", file=tmp)
        num = self.numbers
        if ((num is not None and not "км" in num and ki != StreetKind.ORG) and ki != StreetKind.AREA): 
            print(" {0}".format(num), end="", file=tmp, flush=True)
            num = (None)
        miscs = self.get_string_values(StreetReferent.ATTR_MISC)
        for m in miscs: 
            if (str.isupper(m[0]) and (len(m) < 4)): 
                print(" {0}".format(m), end="", file=tmp, flush=True)
                misc = m
                break
        if (misc is None and len(miscs) > 0): 
            if (nam is not None and miscs[0].upper() in nam): 
                pass
            else: 
                print(" {0}".format(MiscHelper.convert_first_char_upper_and_other_lower(miscs[0])), end="", file=tmp, flush=True)
            misc = miscs[0]
        if (nam is not None): 
            print(" {0}".format(MiscHelper.convert_first_char_upper_and_other_lower(nam)), end="", file=tmp, flush=True)
        if (num is not None): 
            print(" {0}".format(num), end="", file=tmp, flush=True)
        par = self.get_string_value(StreetReferent.ATTR_PARAM)
        if (par is not None): 
            print(", {0}".format(par), end="", file=tmp, flush=True)
        if (not short_variant and self.city is not None): 
            print("; {0}".format(self.city.to_string_ex(True, lang, lev + 1)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @property
    def kind(self) -> 'StreetKind':
        """ Классификатор """
        str0_ = self.get_string_value(StreetReferent.ATTR_KIND)
        if (str0_ is None): 
            return StreetKind.UNDEFINED
        try: 
            return Utils.valToEnum(str0_, StreetKind)
        except Exception as ex457: 
            pass
        return StreetKind.UNDEFINED
    @kind.setter
    def kind(self, value) -> 'StreetKind':
        if (value == StreetKind.UNDEFINED): 
            self.add_slot(StreetReferent.ATTR_KIND, None, True, 0)
        else: 
            self.add_slot(StreetReferent.ATTR_KIND, Utils.enumToString(value).upper(), True, 0)
        return value
    
    def _add_typ(self, typ : str) -> None:
        from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
        self.add_slot(StreetReferent.ATTR_TYPE, typ, False, 0)
        if (self.kind == StreetKind.UNDEFINED): 
            if (typ == "железная дорога"): 
                self.kind = StreetKind.RAILWAY
            elif ("дорога" in typ or typ == "шоссе"): 
                self.kind = StreetKind.ROAD
            elif ("метро" in typ): 
                self.kind = StreetKind.METRO
            elif (typ == "территория"): 
                self.kind = StreetKind.AREA
            elif (StreetItemToken._is_region(typ)): 
                self.kind = StreetKind.AREA
            elif (StreetItemToken._is_spec(typ)): 
                self.kind = StreetKind.SPEC
    
    def _add_name(self, sit : 'StreetItemToken') -> None:
        self.add_slot(StreetReferent.ATTR_NAME, Utils.ifNotNull(sit.value, MiscHelper.get_text_value_of_meta_token(sit, GetTextAttr.NO)), False, 0)
        if (sit.alt_value is not None): 
            self.add_slot(StreetReferent.ATTR_NAME, sit.alt_value, False, 0)
        if (sit.alt_value2 is not None): 
            self.add_slot(StreetReferent.ATTR_NAME, sit.alt_value2, False, 0)
    
    def _add_misc(self, v : str) -> None:
        if (v is not None): 
            self.add_slot(StreetReferent.ATTR_MISC, v, False, 0)
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        return self.__can_be_equals(obj, typ, False, 0)
    
    def __can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType', ignore_geo : bool, level : int) -> bool:
        if (level > 5): 
            return False
        level += 1
        ret = self.__can_be_equals2(obj, typ, ignore_geo, level)
        level -= 1
        return ret
    
    def __can_be_equals2(self, obj : 'Referent', typ : 'ReferentsEqualType', ignore_geo : bool, level : int) -> bool:
        stri = Utils.asObjectOrNull(obj, StreetReferent)
        if (stri is None): 
            return False
        if (self.kind != stri.kind): 
            return False
        typs1 = self.typs
        typs2 = stri.typs
        ok = False
        if (len(typs1) > 0 and len(typs2) > 0): 
            for t in typs1: 
                if (t in typs2): 
                    ok = True
                    break
            if (not ok): 
                return False
        num = self.numbers
        num1 = stri.numbers
        if (num is not None or num1 is not None): 
            if (num is None or num1 is None): 
                return False
            if (num != num1): 
                return False
        par1 = self.get_string_value(StreetReferent.ATTR_PARAM)
        par2 = stri.get_string_value(StreetReferent.ATTR_PARAM)
        if (par1 is not None or par2 is not None): 
            if (par1 != par2): 
                return False
        names1 = self.names
        names2 = stri.names
        if (len(names1) > 0 or len(names2) > 0): 
            ok = False
            for n in names1: 
                if (n in names2): 
                    ok = True
                    break
            if (not ok): 
                return False
        if (self.higher is not None and stri.higher is not None): 
            if (not self.higher.__can_be_equals(stri.higher, typ, ignore_geo, level)): 
                return False
        if (ignore_geo): 
            return True
        geos1 = self.geos
        geos2 = stri.geos
        if (len(geos1) > 0 and len(geos2) > 0): 
            ok = False
            for g1 in geos1: 
                for g2 in geos2: 
                    if (g1.can_be_equals(g2, typ)): 
                        ok = True
                        break
            if (not ok): 
                if (self.city is not None and stri.city is not None): 
                    ok = self.city.can_be_equals(stri.city, typ)
            if (not ok): 
                return False
        return True
    
    def add_slot(self, attr_name : str, attr_value : object, clear_old_value : bool, stat_count : int=0) -> 'Slot':
        if (attr_name == StreetReferent.ATTR_NAME and (isinstance(attr_value, str))): 
            str0_ = Utils.asObjectOrNull(attr_value, str)
            if (str0_.find('.') > 0): 
                i = 1
                while i < (len(str0_) - 1): 
                    if (str0_[i] == '.' and str0_[i + 1] != ' '): 
                        str0_ = (str0_[0:0+i + 1] + " " + str0_[i + 1:])
                    i += 1
            attr_value = (str0_)
        return super().add_slot(attr_name, attr_value, clear_old_value, stat_count)
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().merge_slots(obj, merge_statistic)
    
    def can_be_general_for(self, obj : 'Referent') -> bool:
        if (not self.__can_be_equals(obj, ReferentsEqualType.WITHINONETEXT, True, 0)): 
            return False
        geos1 = self.geos
        geos2 = obj.geos
        if (len(geos2) == 0 or len(geos1) > 0): 
            return False
        return True
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        names_ = self.names
        for n in names_: 
            oi.termins.append(Termin(n))
        return oi
    
    def _correct(self) -> None:
        names_ = self.names
        for i in range(len(names_) - 1, -1, -1):
            ss = names_[i]
            jj = ss.find(' ')
            if (jj < 0): 
                continue
            if (ss.rfind(' ') != jj): 
                continue
            pp = Utils.splitString(ss, ' ', False)
            if (len(pp) == 2): 
                ss2 = "{0} {1}".format(pp[1], pp[0])
                if (not ss2 in names_): 
                    self.add_slot(StreetReferent.ATTR_NAME, ss2, False, 0)
    
    @staticmethod
    def _new1520(_arg1 : 'StreetKind') -> 'StreetReferent':
        res = StreetReferent()
        res.kind = _arg1
        return res