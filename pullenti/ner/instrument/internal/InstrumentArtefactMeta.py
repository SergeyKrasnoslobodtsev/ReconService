# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru


from pullenti.ner.metadata.ReferentClass import ReferentClass
from pullenti.ner.instrument.InstrumentParticipantReferent import InstrumentParticipantReferent

class InstrumentArtefactMeta(ReferentClass):
    
    @staticmethod
    def initialize() -> None:
        from pullenti.ner.instrument.InstrumentArtefactReferent import InstrumentArtefactReferent
        InstrumentArtefactMeta.GLOBAL_META = InstrumentArtefactMeta()
        InstrumentArtefactMeta.GLOBAL_META.add_feature(InstrumentArtefactReferent.ATTR_TYPE, "Тип", 0, 1)
        InstrumentArtefactMeta.GLOBAL_META.add_feature(InstrumentArtefactReferent.ATTR_VALUE, "Значение", 0, 1)
        InstrumentArtefactMeta.GLOBAL_META.add_feature(InstrumentArtefactReferent.ATTR_REF, "Ссылка на объект", 0, 1).show_as_parent = True
    
    @property
    def name(self) -> str:
        return InstrumentParticipantReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Артефакт"
    
    IMAGE_ID = "artefact"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return InstrumentArtefactMeta.IMAGE_ID
    
    GLOBAL_META = None