# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils

from pullenti.ner.TextToken import TextToken

class MeasureHelper:
    
    @staticmethod
    def try_parse_double(val : str, f : float) -> bool:
        f.value = (0)
        if (Utils.isNullOrEmpty(val)): 
            return False
        inoutres2220 = Utils.tryParseFloat(val.replace(',', '.'), f)
        if (val.find(',') >= 0 and inoutres2220): 
            return True
        inoutres2219 = Utils.tryParseFloat(val, f)
        if (inoutres2219): 
            return True
        return False
    
    @staticmethod
    def is_mult_char(t : 'Token') -> bool:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return False
        if (tt.length_char == 1): 
            if (tt.is_char_of("*xXхХ·×◦∙•") or tt.is_char(chr(0x387)) or tt.is_char(chr(0x22C5))): 
                return True
        return False
    
    @staticmethod
    def is_mult_char_end(t : 'Token') -> bool:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return False
        term = tt.term
        if (term.endswith("X") or term.endswith("Х")): 
            return True
        return False