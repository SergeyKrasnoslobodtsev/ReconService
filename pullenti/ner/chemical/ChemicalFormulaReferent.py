# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils

from pullenti.ner.core.IntOntologyItem import IntOntologyItem
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.chemical.MetaChemical import MetaChemical
from pullenti.ner.Referent import Referent

class ChemicalFormulaReferent(Referent):
    """ Химическая формула """
    
    def __init__(self) -> None:
        super().__init__(ChemicalFormulaReferent.OBJ_TYPENAME)
        self.instance_of = MetaChemical.GLOBAL_META
    
    OBJ_TYPENAME = "CHEMICALFORMULA"
    """ Имя типа сущности TypeName ("CHEMICALFORMULA") """
    
    ATTR_VALUE = "VALUE"
    """ Имя атрибута - значение самой формулы """
    
    ATTR_NAME = "NAME"
    """ Имя атрибута - наименование формулы """
    
    @property
    def value(self) -> str:
        """ Значение формулы (например, H2O) """
        return self.get_string_value(ChemicalFormulaReferent.ATTR_VALUE)
    @value.setter
    def value(self, value_) -> str:
        self.add_slot(ChemicalFormulaReferent.ATTR_VALUE, value_, True, 0)
        return value_
    
    @property
    def name(self) -> str:
        """ Наименование формулы (например, "вода") """
        return self.get_string_value(ChemicalFormulaReferent.ATTR_NAME)
    @name.setter
    def name(self, value_) -> str:
        self.add_slot(ChemicalFormulaReferent.ATTR_NAME, value_, True, 0)
        return value_
    
    def to_string_ex(self, short_variant : bool, lang : 'MorphLang'=None, lev : int=0) -> str:
        res = self.value
        if (res is None): 
            nam = self.name
            if (nam is None): 
                return "?"
            return nam.lower()
        if (not short_variant and self.name is not None): 
            names = self.get_string_values(ChemicalFormulaReferent.ATTR_NAME)
            tmp = io.StringIO()
            print("{0} (".format(res), end="", file=tmp, flush=True)
            i = 0
            while i < len(names): 
                if (i > 0): 
                    print(", ", end="", file=tmp)
                print(names[i].lower(), end="", file=tmp)
                i += 1
            print(")", end="", file=tmp)
            res = Utils.toStringStringIO(tmp)
        return res
    
    def can_be_equals(self, obj : 'Referent', typ : 'ReferentsEqualType'=ReferentsEqualType.WITHINONETEXT) -> bool:
        cf = Utils.asObjectOrNull(obj, ChemicalFormulaReferent)
        if (cf is None): 
            return False
        if (self.value is not None and cf.value is not None): 
            return self.value == cf.value
        if (self.name is not None and cf.name is not None): 
            return self.name == cf.name
        return False
    
    def create_ontology_item(self) -> 'IntOntologyItem':
        oi = IntOntologyItem(self)
        oi.termins.append(Termin(Utils.ifNotNull(self.value, self.name)))
        return oi