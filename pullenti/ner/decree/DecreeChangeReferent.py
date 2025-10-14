# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.decree.DecreeChangeKind import DecreeChangeKind
from pullenti.ner.Referent import Referent
from pullenti.ner.decree.internal.MetaDecreeChange import MetaDecreeChange

class DecreeChangeReferent(Referent):
    """ Модель изменения структурной части НПА """
    
    def __init__(self) -> None:
        super().__init__(DecreeChangeReferent.OBJ_TYPENAME)
        self.instance_of = MetaDecreeChange.GLOBAL_META
    
    OBJ_TYPENAME = "DECREECHANGE"
    """ Имя типа сущности TypeName ("DECREECHANGE") """
    
    ATTR_OWNER = "OWNER"
    """ Имя атрибута - Структурный элемент, в который вносится изменение (м.б. несколько),
    DecreeReferent или DecreePartReferent. """
    
    ATTR_KIND = "KIND"
    """ Имя атрибута - тип изменения (DecreeChangeKind) """
    
    ATTR_CHILD = "CHILD"
    """ Имя атрибута - внутренние изменения (DecreeChangeReferent) """
    
    ATTR_VALUE = "VALUE"
    """ Имя атрибута - само изменение (DecreeChangeValueReferent) """
    
    ATTR_PARAM = "PARAM"
    """ Имя атрибута - дополнительный параметр DecreeChangeValueReferent (для типа Exchange - что заменяется, для Append - после чего) """
    
    ATTR_MISC = "MISC"
    """ Имя атрибута - разное """
    
    def to_string_ex(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = io.StringIO()
        if (self.kind != DecreeChangeKind.UNDEFINED): 
            print("{0} ".format(MetaDecreeChange.KIND_FEATURE.convert_inner_value_to_outer_value(Utils.enumToString(self.kind), lang)), end="", file=res, flush=True)
        for o in self.owners: 
            print("'{0}' ".format(o.to_string_ex(True, lang, 0)), end="", file=res, flush=True)
        if (self.value is not None): 
            print("{0} ".format(self.value.to_string_ex(True, lang, 0)), end="", file=res, flush=True)
        if (self.param is not None): 
            if (self.kind == DecreeChangeKind.APPEND): 
                print("после ", end="", file=res)
            elif (self.kind == DecreeChangeKind.EXCHANGE): 
                print("вместо ", end="", file=res)
            print(self.param.to_string_ex(True, lang, 0), end="", file=res)
        return Utils.toStringStringIO(res).strip()
    
    @property
    def parent_referent(self) -> 'Referent':
        return Utils.asObjectOrNull(self.get_slot_value(DecreeChangeReferent.ATTR_OWNER), Referent)
    
    @property
    def kind(self) -> 'DecreeChangeKind':
        """ Классификатор """
        s = self.get_string_value(DecreeChangeReferent.ATTR_KIND)
        if (s is None): 
            return DecreeChangeKind.UNDEFINED
        try: 
            if (s == "Add"): 
                return DecreeChangeKind.APPEND
            res = Utils.valToEnum(s, DecreeChangeKind)
            if (isinstance(res, DecreeChangeKind)): 
                return Utils.valToEnum(res, DecreeChangeKind)
        except Exception as ex1410: 
            pass
        return DecreeChangeKind.UNDEFINED
    @kind.setter
    def kind(self, value_) -> 'DecreeChangeKind':
        if (value_ != DecreeChangeKind.UNDEFINED): 
            self.add_slot(DecreeChangeReferent.ATTR_KIND, Utils.enumToString(value_), True, 0)
        return value_
    
    @property
    def owners(self) -> typing.List['Referent']:
        """ Структурный элемент, в который вносится изменение (м.б. несколько) """
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeChangeReferent.ATTR_OWNER and (isinstance(s.value, Referent))): 
                res.append(Utils.asObjectOrNull(s.value, Referent))
        return res
    
    @property
    def children(self) -> typing.List['DecreeChangeReferent']:
        """ Внутренние изменения """
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeChangeReferent.ATTR_CHILD and (isinstance(s.value, DecreeChangeReferent))): 
                res.append(Utils.asObjectOrNull(s.value, DecreeChangeReferent))
        return res
    
    @property
    def value(self) -> 'DecreeChangeValueReferent':
        """ Значение """
        from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
        return Utils.asObjectOrNull(self.get_slot_value(DecreeChangeReferent.ATTR_VALUE), DecreeChangeValueReferent)
    @value.setter
    def value(self, value_) -> 'DecreeChangeValueReferent':
        self.add_slot(DecreeChangeReferent.ATTR_VALUE, value_, True, 0)
        return value_
    
    @property
    def param(self) -> 'DecreeChangeValueReferent':
        """ Дополнительный параметр (для типа Exchange - что заменяется, для Append - после чего) """
        from pullenti.ner.decree.DecreeChangeValueReferent import DecreeChangeValueReferent
        return Utils.asObjectOrNull(self.get_slot_value(DecreeChangeReferent.ATTR_PARAM), DecreeChangeValueReferent)
    @param.setter
    def param(self, value_) -> 'DecreeChangeValueReferent':
        self.add_slot(DecreeChangeReferent.ATTR_PARAM, value_, True, 0)
        return value_
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        return obj == self
    
    def _check_correct(self) -> bool:
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        if (self.kind == DecreeChangeKind.UNDEFINED): 
            return False
        if (self.kind == DecreeChangeKind.EXPIRE or self.kind == DecreeChangeKind.REMOVE or self.kind == DecreeChangeKind.SUSPEND): 
            return True
        if (self.value is None): 
            return False
        if (self.kind == DecreeChangeKind.EXCHANGE): 
            if (self.param is None): 
                owns = self.owners
                if (len(owns) > 0 and owns[0].find_slot(DecreePartReferent.ATTR_INDENTION, None, True) is not None): 
                    self.kind = DecreeChangeKind.NEW
                elif (len(owns) > 0 and owns[0].find_slot(DecreePartReferent.ATTR_SENTENCE, None, True) is not None): 
                    self.kind = DecreeChangeKind.NEW
                else: 
                    return False
        return True
    
    @staticmethod
    def _new1400(_arg1 : 'DecreeChangeKind') -> 'DecreeChangeReferent':
        res = DecreeChangeReferent()
        res.kind = _arg1
        return res