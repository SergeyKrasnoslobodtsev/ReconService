# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.MetaToken import MetaToken

class TerminToken(MetaToken):
    """ Метатокен - результат привязки термина Termin словаря TerminCollection. Формируется методом TryParse или TryParseAll у TerminCollection.
    Токен привязки к словарю
    """
    
    def __init__(self, begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.termin = None;
        self.abridge_without_point = False
    
    @staticmethod
    def _new562(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'Termin') -> 'TerminToken':
        res = TerminToken(_arg1, _arg2)
        res.termin = _arg3
        return res
    
    @staticmethod
    def _new736(_arg1 : 'Token', _arg2 : 'Token', _arg3 : bool) -> 'TerminToken':
        res = TerminToken(_arg1, _arg2)
        res.abridge_without_point = _arg3
        return res
    
    @staticmethod
    def _new744(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection') -> 'TerminToken':
        res = TerminToken(_arg1, _arg2)
        res.morph = _arg3
        return res
    
    @staticmethod
    def _new750(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'MorphCollection', _arg4 : 'Termin') -> 'TerminToken':
        res = TerminToken(_arg1, _arg2)
        res.morph = _arg3
        res.termin = _arg4
        return res