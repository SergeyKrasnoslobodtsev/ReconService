# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.core.Termin import Termin

class TerrTermin(Termin):
    
    def __init__(self, source : str, lang_ : 'MorphLang'=None) -> None:
        super().__init__(None, lang_, False)
        self.is_state = False
        self.is_region = False
        self.is_adjective = False
        self.is_always_prefix = False
        self.is_doubt = False
        self.is_moscow_region = False
        self.is_strong = False
        self.is_specific_prefix = False
        self.is_sovet = False
        self.init_by_normal_text(source, lang_)
    
    @staticmethod
    def _new1771(_arg1 : str, _arg2 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.gender = _arg2
        return res
    
    @staticmethod
    def _new1772(_arg1 : str, _arg2 : 'MorphLang', _arg3 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new1773(_arg1 : str, _arg2 : bool, _arg3 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new1774(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new1776(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.is_doubt = _arg3
        return res
    
    @staticmethod
    def _new1777(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.is_doubt = _arg4
        return res
    
    @staticmethod
    def _new1778(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        return res
    
    @staticmethod
    def _new1779(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        return res
    
    @staticmethod
    def _new1780(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_state = _arg2
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1781(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_state = _arg3
        res.is_adjective = _arg4
        return res
    
    @staticmethod
    def _new1782(_arg1 : str, _arg2 : bool, _arg3 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new1784(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        return res
    
    @staticmethod
    def _new1785(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new1786(_arg1 : str, _arg2 : bool, _arg3 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new1787(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1792(_arg1 : str, _arg2 : bool, _arg3 : bool, _arg4 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_always_prefix = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new1797(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool, _arg5 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_always_prefix = _arg4
        res.gender = _arg5
        return res
    
    @staticmethod
    def _new1801(_arg1 : str, _arg2 : bool, _arg3 : 'MorphGender', _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.gender = _arg3
        res.is_always_prefix = _arg4
        return res
    
    @staticmethod
    def _new1802(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_always_prefix = _arg3
        return res
    
    @staticmethod
    def _new1807(_arg1 : str, _arg2 : bool, _arg3 : 'MorphGender', _arg4 : str) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.gender = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new1809(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_strong = _arg3
        return res
    
    @staticmethod
    def _new1812(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_strong = _arg4
        return res
    
    @staticmethod
    def _new1816(_arg1 : str, _arg2 : str, _arg3 : bool, _arg4 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.canonic_text = _arg2
        res.is_sovet = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new1819(_arg1 : str, _arg2 : bool, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_adjective = _arg3
        return res
    
    @staticmethod
    def _new1820(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_adjective = _arg4
        return res
    
    @staticmethod
    def _new1821(_arg1 : str, _arg2 : bool, _arg3 : bool, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_region = _arg2
        res.is_specific_prefix = _arg3
        res.is_always_prefix = _arg4
        return res
    
    @staticmethod
    def _new1822(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : bool, _arg5 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1, _arg2)
        res.is_region = _arg3
        res.is_specific_prefix = _arg4
        res.is_always_prefix = _arg5
        return res
    
    @staticmethod
    def _new1823(_arg1 : str, _arg2 : str, _arg3 : 'MorphGender') -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.acronym = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new1824(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.acronym = _arg2
        res.is_region = _arg3
        return res
    
    @staticmethod
    def _new1825(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.canonic_text = _arg2
        res.acronym = _arg3
        res.is_region = _arg4
        return res
    
    @staticmethod
    def _new1826(_arg1 : str, _arg2 : bool) -> 'TerrTermin':
        res = TerrTermin(_arg1)
        res.is_moscow_region = _arg2
        return res