# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Referent import Referent
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.decree.DecreeChangeValueKind import DecreeChangeValueKind
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.decree.internal.MetaDecreeChangeValue import MetaDecreeChangeValue

class DecreeChangeValueReferent(Referent):
    """ Значение изменения структурного элемента НПА """
    
    def __init__(self) -> None:
        super().__init__(DecreeChangeValueReferent.OBJ_TYPENAME)
        self.instance_of = MetaDecreeChangeValue.GLOBAL_META
    
    OBJ_TYPENAME = "DECREECHANGEVALUE"
    """ Имя типа сущности TypeName ("DECREECHANGEVALUE") """
    
    ATTR_KIND = "KIND"
    """ Имя атрибута - тип (DecreeChangeValueKind) """
    
    ATTR_VALUE = "VALUE"
    """ Имя атрибута - значение """
    
    ATTR_NEWITEM = "NEWITEM"
    """ Имя атрибута - новый структурный элемент """
    
    ATTR_BEGINCHAR = "BEGIN"
    """ Начальная позиция текста (сразу за кавычкой) """
    
    ATTR_ENDCHAR = "END"
    """ Конечная позиция текста (сразу перед закрывающей кавычкой) """
    
    def to_string_ex(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        from pullenti.ner.decree.DecreePartReferent import DecreePartReferent
        res = io.StringIO()
        nws = self.new_items
        if (len(nws) > 0): 
            for p in nws: 
                dpr = DecreePartReferent()
                ii = p.find(' ')
                if (ii < 0): 
                    dpr.add_slot(p, "", False, 0)
                else: 
                    dpr.add_slot(p[0:0+ii], p[ii + 1:], False, 0)
                print(" новый '{0}'".format(dpr.to_string_ex(True, None, 0)), end="", file=res, flush=True)
        if (self.kind != DecreeChangeValueKind.UNDEFINED): 
            print(" {0}".format(str(MetaDecreeChangeValue.KIND_FEATURE.convert_inner_value_to_outer_value(Utils.enumToString(self.kind), lang)).lower()), end="", file=res, flush=True)
        vals = self.get_string_values(DecreeChangeValueReferent.ATTR_VALUE)
        if (vals is not None and len(vals) > 0): 
            print(" ", end="", file=res)
            i = 0
            while i < len(vals): 
                if (i > 0): 
                    print(", ", end="", file=res)
                val = vals[i]
                if (len(val) > 100): 
                    val = (val[0:0+100] + "...")
                print("'{0}'".format(val), end="", file=res, flush=True)
                Utils.replaceStringIO(res, '\n', ' ')
                Utils.replaceStringIO(res, '\r', ' ')
                i += 1
        return Utils.toStringStringIO(res).strip()
    
    @property
    def kind(self) -> 'DecreeChangeValueKind':
        """ Тип значение """
        s = self.get_string_value(DecreeChangeValueReferent.ATTR_KIND)
        if (s is None): 
            return DecreeChangeValueKind.UNDEFINED
        try: 
            if (s == "Footnote"): 
                return DecreeChangeValueKind.UNDEFINED
            res = Utils.valToEnum(s, DecreeChangeValueKind)
            if (isinstance(res, DecreeChangeValueKind)): 
                return Utils.valToEnum(res, DecreeChangeValueKind)
        except Exception as ex1411: 
            pass
        return DecreeChangeValueKind.UNDEFINED
    @kind.setter
    def kind(self, value_) -> 'DecreeChangeValueKind':
        if (value_ != DecreeChangeValueKind.UNDEFINED): 
            self.add_slot(DecreeChangeValueReferent.ATTR_KIND, Utils.enumToString(value_), True, 0)
        return value_
    
    @property
    def value(self) -> str:
        """ Значение """
        return self.get_string_value(DecreeChangeValueReferent.ATTR_VALUE)
    @value.setter
    def value(self, value_) -> str:
        self.add_slot(DecreeChangeValueReferent.ATTR_VALUE, value_, True, 0)
        return value_
    
    @property
    def new_items(self) -> typing.List[str]:
        """ Новые структурные элементы, которые добавляются этим значением
        (дополнить ... статьями 10.1 и 10.2 следующего содержания) """
        res = list()
        for s in self.slots: 
            if (s.type_name == DecreeChangeValueReferent.ATTR_NEWITEM and (isinstance(s.value, str))): 
                res.append(Utils.asObjectOrNull(s.value, str))
        return res
    
    @property
    def begin_char(self) -> int:
        """ Начальная позиция текста (сразу за кавычкой) """
        val = self.get_string_value(DecreeChangeValueReferent.ATTR_BEGINCHAR)
        if (val is None): 
            return 0
        n = 0
        wrapn1412 = RefOutArgWrapper(0)
        inoutres1413 = Utils.tryParseInt(val, wrapn1412)
        n = wrapn1412.value
        if (inoutres1413): 
            return n
        return 0
    @begin_char.setter
    def begin_char(self, value_) -> int:
        self.add_slot(DecreeChangeValueReferent.ATTR_BEGINCHAR, str(value_), True, 0)
        return value_
    
    @property
    def end_char(self) -> int:
        """ Конечная позиция текста (сразу перед закрывающей кавычкой) """
        val = self.get_string_value(DecreeChangeValueReferent.ATTR_ENDCHAR)
        if (val is None): 
            return 0
        n = 0
        wrapn1414 = RefOutArgWrapper(0)
        inoutres1415 = Utils.tryParseInt(val, wrapn1414)
        n = wrapn1414.value
        if (inoutres1415): 
            return n
        return 0
    @end_char.setter
    def end_char(self, value_) -> int:
        self.add_slot(DecreeChangeValueReferent.ATTR_ENDCHAR, str(value_), True, 0)
        return value_
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        return obj == self
    
    @staticmethod
    def _new1044(_arg1 : 'DecreeChangeValueKind') -> 'DecreeChangeValueReferent':
        res = DecreeChangeValueReferent()
        res.kind = _arg1
        return res