# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils

from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.chemical.ChemicalFormulaReferent import ChemicalFormulaReferent
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Token import Token
from pullenti.ner.Referent import Referent
from pullenti.ner.core.internal.ResourceHelper3 import ResourceHelper3
from pullenti.ner.chemical.MetaChemical import MetaChemical
from pullenti.ner.chemical.internal.ChemicalToken import ChemicalToken
from pullenti.ner.Analyzer import Analyzer

class ChemicalAnalyzer(Analyzer):
    """ Анализатор химических формул (специфический анализатор) """
    
    ANALYZER_NAME = "CHEMICAL"
    """ Имя анализатора ("CHEMICAL") """
    
    @property
    def name(self) -> str:
        return ChemicalAnalyzer.ANALYZER_NAME
    
    @property
    def caption(self) -> str:
        return "Химические формулы"
    
    @property
    def description(self) -> str:
        return "Химические формулы и их текстовые аналоги"
    
    def clone(self) -> 'Analyzer':
        return ChemicalAnalyzer()
    
    @property
    def is_specific(self) -> bool:
        """ Специфический анализатор """
        return True
    
    @property
    def type_system(self) -> typing.List['ReferentClass']:
        return [MetaChemical.GLOBAL_META]
    
    @property
    def images(self) -> typing.List[tuple]:
        res = dict()
        res[str(MetaChemical.IMAGE_ID)] = ResourceHelper3.get_bytes("chemical.png")
        return res
    
    def create_referent(self, type0_ : str) -> 'Referent':
        if (type0_ == ChemicalFormulaReferent.OBJ_TYPENAME): 
            return ChemicalFormulaReferent()
        return None
    
    @property
    def progress_weight(self) -> int:
        return 1
    
    def process(self, kit : 'AnalysisKit') -> None:
        ad = kit.get_analyzer_data(self)
        probs = list()
        t = kit.first_token
        first_pass3819 = True
        while True:
            if first_pass3819: first_pass3819 = False
            else: t = t.next0_
            if (not (t is not None)): break
            li = ChemicalToken.try_parse_list(t, 0)
            if (li is None or len(li) == 0): 
                continue
            t = li[len(li) - 1].end_token
            cf = ChemicalToken.create_referent(li)
            if (cf is None): 
                probs.append(li)
                continue
            cf = (Utils.asObjectOrNull(ad.register_referent(cf), ChemicalFormulaReferent))
            rt = ReferentToken(cf, li[0].begin_token, t)
            kit.embed_token(rt)
            t = (rt)
        for pr in probs: 
            cf = ChemicalToken.create_referent(pr)
            if (cf is None): 
                continue
            cf = (Utils.asObjectOrNull(ad.register_referent(cf), ChemicalFormulaReferent))
            rt = ReferentToken(cf, pr[0].begin_token, pr[len(pr) - 1].end_token)
            kit.embed_token(rt)
    
    @staticmethod
    def initialize() -> None:
        MetaChemical.initialize()
        ChemicalToken.initialize()
        ProcessorService.register_analyzer(ChemicalAnalyzer())