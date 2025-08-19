# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import math
import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.ner.core.NumberExType import NumberExType
from pullenti.ner.address.StreetKind import StreetKind
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.morph.MorphGender import MorphGender
from pullenti.ner.Referent import Referent
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.geo.internal.GeoTokenType import GeoTokenType
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.NumberToken import NumberToken
from pullenti.morph.MorphLang import MorphLang
from pullenti.ner.NumberSpellingType import NumberSpellingType
from pullenti.ner.geo.internal.GeoTokenData import GeoTokenData
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.TextToken import TextToken
from pullenti.ner.core.Termin import Termin
from pullenti.ner.core.BracketParseAttr import BracketParseAttr
from pullenti.ner.geo.GeoAnalyzer import GeoAnalyzer
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.Token import Token
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.core.NumberHelper import NumberHelper
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.BracketHelper import BracketHelper
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken

class AddressItemToken(MetaToken):
    
    @staticmethod
    def initialize() -> None:
        if (AddressItemToken.__m_ontology is not None): 
            return
        StreetItemToken.initialize()
        AddressItemToken.__m_ontology = TerminCollection()
        t = None
        t = Termin._new84("ДОМ", AddressItemType.HOUSE)
        t.add_abridge("Д.")
        t.add_variant("КОТТЕДЖ", False)
        t.add_abridge("КОТ.")
        t.add_variant("ДАЧА", False)
        t.add_variant("ЖИЛОЙ ДОМ", False)
        t.add_abridge("ЖИЛ.ДОМ")
        t.add_variant("ДО ДОМА", False)
        t.add_variant("ДОМ ОФИЦЕРСКОГО СОСТАВА", False)
        t.add_variant("ДОС", False)
        t.add_variant("ЗДАНИЕ", False)
        t.add_abridge("ЗД.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new85("БУДИНОК", AddressItemType.HOUSE, MorphLang.UA)
        t.add_abridge("Б.")
        t.add_variant("КОТЕДЖ", False)
        t.add_abridge("БУД.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ВЛАДЕНИЕ", AddressItemType.HOUSE, AddressHouseType.ESTATE)
        t.add_abridge("ВЛАД.")
        t.add_abridge("ВЛД.")
        t.add_abridge("ВЛ.")
        AddressItemToken.__m_ontology.add(t)
        AddressItemToken.M_OWNER = t
        t = Termin._new86("ДОМОВЛАДЕНИЕ", AddressItemType.HOUSE, AddressHouseType.HOUSEESTATE)
        t.add_variant("ДОМОВЛАДЕНИЕ", False)
        t.add_abridge("ДВЛД.")
        t.add_abridge("ДМВЛД.")
        t.add_variant("ДОМОВЛ", False)
        t.add_variant("ДОМОВА", False)
        t.add_variant("ДОМОВЛАД", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new88("ОБЪЕКТ НЕЗАВЕРШЕННОГО СТРОИТЕЛЬСТВА", "ОНС", AddressItemType.HOUSE, AddressHouseType.UNFINISHED)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("ПОДЪЕЗД ДОМА", AddressItemType.HOUSE)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("ЭТАЖ", AddressItemType.FLOOR)
        t.add_abridge("ЭТ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new91("ЦОКОЛЬ", AddressItemType.FLOOR, "цокольный")
        t.add_variant("ЦОКОЛ", False)
        t.add_variant("ЦОКОЛЬНЫЙ", False)
        t.add_variant("ЦОКОЛЬНЫЙ ЭТАЖ", False)
        t.add_variant("ЭТАЖ ЦОКОЛЬНЫЙ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new91("МАНСАРДА", AddressItemType.FLOOR, "мансарда")
        t.add_variant("МАНСАРДНЫЙ", False)
        t.add_variant("МАНСАРДА ЭТАЖ", False)
        t.add_variant("ЭТАЖ МАНСАРДА", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("ПОДЪЕЗД", AddressItemType.POTCH)
        t.add_abridge("ПОД.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("КОРПУС", AddressItemType.CORPUS)
        t.add_abridge("КОРП.")
        t.add_abridge("КОР.")
        t.add_abridge("Д.КОРП.")
        t.add_abridge("БЛ/СЕК")
        t.add_abridge("БЛ/ЖД")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("К", AddressItemType.CORPUSORFLAT)
        t.add_abridge("К.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("СТРОЕНИЕ", AddressItemType.BUILDING)
        t.add_abridge("СТРОЕН.")
        t.add_abridge("СТР.")
        t.add_abridge("СТ.")
        t.add_abridge("ПОМ.СТР.")
        t.add_abridge("Д.СТР.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new88("СООРУЖЕНИЕ", "РК", AddressItemType.BUILDING, AddressBuildingType.CONSTRUCTION)
        t.add_abridge("СООР.")
        t.add_abridge("СООРУЖ.")
        t.add_abridge("СООРУЖЕН.")
        t.add_variant("БАШНЯ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ЛИТЕРА", AddressItemType.BUILDING, AddressBuildingType.LITER)
        t.add_abridge("ЛИТ.")
        t.add_variant("ЛИТЕР", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("УЧАСТОК", AddressItemType.PLOT)
        t.add_abridge("УЧАСТ.")
        t.add_abridge("УЧ.")
        t.add_abridge("УЧ-К")
        t.add_abridge("ДОМ УЧ.")
        t.add_abridge("ДОМ.УЧ.")
        t.add_abridge("У-К")
        t.add_variant("ЗЕМЕЛЬНЫЙ УЧАСТОК", False)
        t.add_abridge("ЗЕМ.УЧ.")
        t.add_abridge("ЗЕМ.УЧ-К")
        t.add_abridge("З/У")
        t.add_variant("ЧАСТЬ ВЫДЕЛА", False)
        t.add_variant("ВЫДЕЛ", False)
        t.add_variant("НАДЕЛ", False)
        t.add_variant("КОНТУР", False)
        t.add_abridge("ЗУ")
        t.add_abridge("ВЫД.")
        t.add_variant("МЕСТО", False)
        t.add_variant("ПОЗИЦИЯ", False)
        t.add_abridge("ПОЗ.")
        AddressItemToken.__m_ontology.add(t)
        AddressItemToken.M_PLOT = t
        t = Termin._new84("ПОЛЕ", AddressItemType.FIELD)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new101("ГЕНЕРАЛЬНЫЙ ПЛАН", "ГП", AddressItemType.GENPLAN)
        t.add_variant("ГЕНПЛАН", False)
        t.add_abridge("ГЕН.ПЛАН")
        t.add_abridge("Г/П")
        t.add_abridge("Г.П.")
        t.add_variant("ПО ГП", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("КВАРТИРА", AddressItemType.FLAT)
        t.add_abridge("КВАРТ.")
        t.add_abridge("КВАР.")
        t.add_abridge("КВ.")
        t.add_abridge("KB.")
        t.add_abridge("КВ-РА")
        t.add_abridge("КВ.КОМ")
        t.add_abridge("КВ.ОБЩ")
        t.add_abridge("КВ.Ч.")
        t.add_abridge("КВЮ")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("ОФИС", AddressItemType.OFFICE)
        t.add_abridge("ОФ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new85("ОФІС", AddressItemType.OFFICE, MorphLang.UA)
        t.add_abridge("ОФ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("ПАВИЛЬОН", AddressItemType.PAVILION)
        t.add_abridge("ПАВ.")
        t.add_variant("ТОРГОВЫЙ ПАВИЛЬОН", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new85("ПАВІЛЬЙОН", AddressItemType.PAVILION, MorphLang.UA)
        t.add_abridge("ПАВ.")
        t.add_variant("ТОРГОВИЙ ПАВІЛЬЙОН", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("СЕКЦИЯ", AddressItemType.BLOCK)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("БОКС", AddressItemType.BOX)
        t.add_variant("ГАРАЖ", False)
        t.add_abridge("ГАР.")
        t.add_variant("ГАРАЖНАЯ ЯЧЕЙКА", False)
        t.add_abridge("Г-Ж")
        t.add_variant("ПОДЪЕЗД", False)
        t.add_abridge("ГАРАЖ-БОКС")
        t.add_variant("ИНДИВИДУАЛЬНЫЙ ГАРАЖ", False)
        t.add_variant("ГАРАЖНЫЙ БОКС", False)
        t.add_abridge("ГБ.")
        t.add_abridge("Г.Б.")
        t.add_variant("ЭЛЛИНГ", False)
        t.add_variant("ЭЛИНГ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("ЧАСТЬ", AddressItemType.PART)
        t.add_abridge("Ч.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("СКВАЖИНА", AddressItemType.WELL)
        t.add_abridge("СКВАЖ.")
        t.add_variant("СКВАЖИНА ГАЗОКОНДЕНСАТНАЯ ЭКСПЛУАТАЦИОННАЯ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("ПОМЕЩЕНИЕ", AddressItemType.SPACE)
        t.add_variant("ПОМЕЩЕНИЕ", False)
        t.add_abridge("ПОМ.")
        t.add_abridge("ПОМЕЩ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new112("НЕЖИЛОЕ ПОМЕЩЕНИЕ", "НЕЖИЛОЕ", AddressItemType.SPACE, 1)
        t.add_abridge("Н.П.")
        t.add_variant("НП", False)
        t.add_variant("НЖ", False)
        t.add_variant("НЕЖИЛОЕ", False)
        t.add_abridge("НЕЖИЛ.")
        t.add_variant("НЕЖИЛОЕ ВСТРОЕННОЕ ПОМЕЩЕНИЕ", False)
        t.add_abridge("НЕЖ.ПОМ")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new113("МЕСТО ОБЩЕГО ПОЛЬЗОВАНИЯ", "МОП", True, "МОП", AddressItemType.SPACE, 1)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("КЛАДОВКА", AddressItemType.SPACE, 1)
        t.add_abridge("КЛАД.")
        t.add_abridge("КЛ.")
        t.add_variant("КЛАДОВАЯ", False)
        t.add_variant("КЛАДОВОЕ ПОМЕЩЕНИЕ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("СКЛАД", AddressItemType.SPACE, 1)
        t.add_abridge("СКЛ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("КОТЕЛЬНАЯ", AddressItemType.SPACE, 1)
        t.add_abridge("КОТ.")
        t.add_abridge("КОТЕЛ.")
        t.add_abridge("КОТЕЛН.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ТОРГОВЫЙ ЗАЛ", AddressItemType.SPACE, 1)
        t.add_abridge("ТОРГ.ЗАЛ")
        t.add_abridge("ТОРГОВ.ЗАЛ")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new112("ЦЕХ", "цех", AddressItemType.SPACE, 1)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("РАБОЧИЙ УЧАСТОК", AddressItemType.SPACE, 1)
        t.add_abridge("РАБ.УЧ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new120("ЛЕСТНИЧНАЯ КЛЕТКА", "ЛК", "ЛК", AddressItemType.SPACE, 1)
        t.add_variant("ЛФЛК", False)
        t.add_variant("ЛКЛК", False)
        t.add_variant("МОПЛК", False)
        t.add_variant("МОП ЛК", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ПОДВАЛ", AddressItemType.SPACE, 1)
        t.add_variant("ПОДВАЛЬНОЕ ПОМЕЩЕНИЕ", False)
        t.add_abridge("ПОДВ.ПОМ.")
        t.add_abridge("ПОДВАЛ.ПОМ.")
        t.add_abridge("ПОДВ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("АНТРЕСОЛЬ", AddressItemType.SPACE, 1)
        t.add_variant("АНТРЕСОЛ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("МАСТЕРСКАЯ", AddressItemType.SPACE, 1)
        t.add_abridge("МАСТ.")
        AddressItemToken.__m_ontology.add(t)
        for s in ["ЧЕРДАК", "КРЫША", "ПОГРЕБ"]: 
            AddressItemToken.__m_ontology.add(Termin._new86(s, AddressItemType.SPACE, 1))
        for s in ["АПТЕКА", "АТЕЛЬЕ", "ОТЕЛЬ", "ГОСТИНИЦА", "ХОСТЕЛ", "СТУДИЯ", "САРАЙ", "ПАРИКМАХЕРСКАЯ", "СТОЛОВАЯ", "КАФЕ", "РЕСТОРАН", "УНИВЕРМАГ", "УНИВЕРСАМ", "СУПЕРМАРКЕТ"]: 
            AddressItemToken.__m_ontology.add(Termin._new86(s, AddressItemType.SPACE, 1))
        t = Termin._new126("МАГАЗИН", AddressItemType.SPACE, 1, 1)
        t.add_abridge("МАГ.")
        t.add_abridge("МАГ-Н")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new126("АПТЕЧНЫЙ ПУНКТ", AddressItemType.SPACE, 1, 1)
        t.add_abridge("А.П.")
        t.add_abridge("А/П")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("МАШИНОМЕСТО", AddressItemType.CARPLACE)
        t.add_abridge("М/М")
        t.add_abridge("МАШ.МЕСТО")
        t.add_abridge("М.МЕСТО")
        t.add_abridge("МАШ.М.")
        t.add_variant("МАШИНО-МЕСТО", False)
        t.add_variant("ПАРКОВОЧНОЕ МЕСТО", False)
        t.add_abridge("ММ")
        t.add_abridge("MM")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("КОМНАТА", AddressItemType.ROOM)
        t.add_abridge("КОМ.")
        t.add_abridge("КОМН.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("КАБИНЕТ", AddressItemType.OFFICE)
        t.add_abridge("КАБ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("НОМЕР", AddressItemType.NUMBER)
        t.add_abridge("НОМ.")
        t.add_abridge("№")
        t.add_abridge("N")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new132("БЕЗ НОМЕРА", "Б/Н", AddressItemType.NONUMBER)
        t.add_variant("НЕ ОПРЕДЕЛЕНО", False)
        t.add_variant("НЕОПРЕДЕЛЕНО", False)
        t.add_variant("НЕ ЗАДАН", False)
        t.add_abridge("Б.Н.")
        t.add_abridge("БН")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new133("АБОНЕНТСКИЙ ЯЩИК", AddressItemType.POSTOFFICEBOX, "АЯ")
        t.add_abridge("А.Я.")
        t.add_variant("ПОЧТОВЫЙ ЯЩИК", False)
        t.add_abridge("П.Я.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new133("ГОРОДСКАЯ СЛУЖЕБНАЯ ПОЧТА", AddressItemType.CSP, "ГСП")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("ДОСТАВОЧНЫЙ УЧАСТОК", AddressItemType.DELIVERYAREA)
        t.add_abridge("ДОСТ.УЧАСТОК")
        t.add_abridge("ДОСТ.УЧ.")
        t.add_abridge("ДОСТ.УЧ-К")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new136("АДРЕС", AddressItemType.PREFIX, True)
        t.add_variant("ЮРИДИЧЕСКИЙ АДРЕС", False)
        t.add_variant("ФАКТИЧЕСКИЙ АДРЕС", False)
        t.add_abridge("ЮР.АДРЕС")
        t.add_abridge("ПОЧТ.АДРЕС")
        t.add_abridge("ФАКТ.АДРЕС")
        t.add_abridge("П.АДРЕС")
        t.add_variant("ЮРИДИЧЕСКИЙ/ФАКТИЧЕСКИЙ АДРЕС", False)
        t.add_variant("ЮРИДИЧЕСКИЙ И ФАКТИЧЕСКИЙ АДРЕС", False)
        t.add_variant("ПОЧТОВЫЙ АДРЕС", False)
        t.add_variant("АДРЕС ПРОЖИВАНИЯ", False)
        t.add_variant("МЕСТО НАХОЖДЕНИЯ", False)
        t.add_variant("МЕСТОНАХОЖДЕНИЕ", False)
        t.add_variant("МЕСТОПОЛОЖЕНИЕ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new136("АДРЕСА", AddressItemType.PREFIX, True)
        t.add_variant("ЮРИДИЧНА АДРЕСА", False)
        t.add_variant("ФАКТИЧНА АДРЕСА", False)
        t.add_variant("ПОШТОВА АДРЕСА", False)
        t.add_variant("АДРЕСА ПРОЖИВАННЯ", False)
        t.add_variant("МІСЦЕ ПЕРЕБУВАННЯ", False)
        t.add_variant("ПРОПИСКА", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("КИЛОМЕТР", AddressItemType.KILOMETER)
        t.add_abridge("КИЛОМ.")
        t.add_abridge("КМ.")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("ПЕРЕСЕЧЕНИЕ", AddressDetailType.CROSS)
        t.add_variant("НА ПЕРЕСЕЧЕНИИ", False)
        t.add_variant("ПЕРЕКРЕСТОК", False)
        t.add_variant("УГОЛ", False)
        t.add_variant("НА ПЕРЕКРЕСТКЕ", False)
        AddressItemToken.__m_ontology.add(t)
        AddressItemToken.__m_ontology.add(Termin._new84("НА ТЕРРИТОРИИ", AddressDetailType.NEAR))
        AddressItemToken.__m_ontology.add(Termin._new84("СЕРЕДИНА", AddressDetailType.NEAR))
        AddressItemToken.__m_ontology.add(Termin._new84("ПРИМЫКАТЬ", AddressDetailType.NEAR))
        AddressItemToken.__m_ontology.add(Termin._new84("ГРАНИЧИТЬ", AddressDetailType.NEAR))
        t = Termin._new84("ВБЛИЗИ", AddressDetailType.NEAR)
        t.add_variant("У", False)
        t.add_abridge("ВБЛ.")
        t.add_variant("В БЛИЗИ", False)
        t.add_variant("ВОЗЛЕ", False)
        t.add_variant("ОКОЛО", False)
        t.add_variant("НЕДАЛЕКО ОТ", False)
        t.add_variant("РЯДОМ С", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new84("РАЙОН", AddressDetailType.NEAR)
        t.add_abridge("Р-Н")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new132("В РАЙОНЕ", "РАЙОН", AddressDetailType.NEAR)
        t.add_abridge("В Р-НЕ")
        AddressItemToken.__m_ontology.add(t)
        AddressItemToken.__m_ontology.add(Termin._new84("ПРИМЕРНО", AddressDetailType.UNDEFINED))
        AddressItemToken.__m_ontology.add(Termin._new84("ПОРЯДКА", AddressDetailType.UNDEFINED))
        AddressItemToken.__m_ontology.add(Termin._new84("ПРИБЛИЗИТЕЛЬНО", AddressDetailType.UNDEFINED))
        AddressItemToken.__m_ontology.add(Termin._new84("ОРИЕНТИР", AddressDetailType.UNDEFINED))
        AddressItemToken.__m_ontology.add(Termin._new84("НАПРАВЛЕНИЕ", AddressDetailType.UNDEFINED))
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = True
        AddressItemToken.__m_ontology.add(Termin._new84("СЕВЕРНЕЕ", AddressDetailType.NORTH))
        AddressItemToken.__m_ontology.add(Termin._new84("СЕВЕР", AddressDetailType.NORTH))
        AddressItemToken.__m_ontology.add(Termin._new84("ЮЖНЕЕ", AddressDetailType.SOUTH))
        AddressItemToken.__m_ontology.add(Termin._new84("ЮГ", AddressDetailType.SOUTH))
        AddressItemToken.__m_ontology.add(Termin._new84("ЗАПАДНЕЕ", AddressDetailType.WEST))
        AddressItemToken.__m_ontology.add(Termin._new84("ЗАПАД", AddressDetailType.WEST))
        AddressItemToken.__m_ontology.add(Termin._new84("ВОСТОЧНЕЕ", AddressDetailType.EAST))
        AddressItemToken.__m_ontology.add(Termin._new84("ВОСТОК", AddressDetailType.EAST))
        AddressItemToken.__m_ontology.add(Termin._new84("СЕВЕРО-ЗАПАДНЕЕ", AddressDetailType.NORTHWEST))
        AddressItemToken.__m_ontology.add(Termin._new84("СЕВЕРО-ЗАПАД", AddressDetailType.NORTHWEST))
        AddressItemToken.__m_ontology.add(Termin._new84("СЕВЕРО-ВОСТОЧНЕЕ", AddressDetailType.NORTHEAST))
        AddressItemToken.__m_ontology.add(Termin._new84("СЕВЕРО-ВОСТОК", AddressDetailType.NORTHEAST))
        AddressItemToken.__m_ontology.add(Termin._new84("ЮГО-ЗАПАДНЕЕ", AddressDetailType.SOUTHWEST))
        AddressItemToken.__m_ontology.add(Termin._new84("ЮГО-ЗАПАД", AddressDetailType.SOUTHWEST))
        AddressItemToken.__m_ontology.add(Termin._new84("ЮГО-ВОСТОЧНЕЕ", AddressDetailType.SOUTHEAST))
        AddressItemToken.__m_ontology.add(Termin._new84("ЮГО-ВОСТОК", AddressDetailType.SOUTHEAST))
        t = Termin._new86("ЦЕНТРАЛЬНАЯ ЧАСТЬ", AddressDetailType.CENTRAL, 1)
        t.add_abridge("ЦЕНТР.ЧАСТЬ")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("СЕВЕРНАЯ ЧАСТЬ", AddressDetailType.NORTH, 1)
        t.add_abridge("СЕВ.ЧАСТЬ")
        t.add_abridge("СЕВЕРН.ЧАСТЬ")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("СЕВЕРО-ВОСТОЧНАЯ ЧАСТЬ", AddressDetailType.NORTHEAST, 1)
        t.add_variant("СЕВЕРОВОСТОЧНАЯ ЧАСТЬ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("СЕВЕРО-ЗАПАДНАЯ ЧАСТЬ", AddressDetailType.NORTHWEST, 1)
        t.add_variant("СЕВЕРОЗАПАДНАЯ ЧАСТЬ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ЮЖНАЯ ЧАСТЬ", AddressDetailType.SOUTH, 1)
        t.add_abridge("ЮЖН.ЧАСТЬ")
        t.add_abridge("ЮЖ.ЧАСТЬ")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ЮГО-ВОСТОЧНАЯ ЧАСТЬ", AddressDetailType.SOUTHEAST, 1)
        t.add_variant("ЮГОВОСТОЧНАЯ ЧАСТЬ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ЮГО-ЗАПАДНАЯ ЧАСТЬ", AddressDetailType.SOUTHWEST, 1)
        t.add_variant("ЮГОЗАПАДНАЯ ЧАСТЬ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ЗАПАДНАЯ ЧАСТЬ", AddressDetailType.WEST, 1)
        t.add_abridge("ЗАП.ЧАСТЬ")
        t.add_abridge("ЗАПАД.ЧАСТЬ")
        t.add_abridge("ЗАПАДН.ЧАСТЬ")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ВОСТОЧНАЯ ЧАСТЬ", AddressDetailType.EAST, 1)
        t.add_abridge("ВОСТ.ЧАСТЬ")
        t.add_abridge("ВОСТОЧ.ЧАСТЬ")
        t.add_abridge("ВОСТОЧН.ЧАСТЬ")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ПРАВАЯ ЧАСТЬ", AddressDetailType.RIGHT, 1)
        t.add_abridge("СПРАВА")
        t.add_abridge("ПРАВ.ЧАСТЬ")
        t.add_variant("ПРАВАЯ СТОРОНА", False)
        t.add_abridge("ПРАВ.СТОРОНА")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new86("ЛЕВАЯ ЧАСТЬ", AddressDetailType.LEFT, 1)
        t.add_abridge("СЛЕВА")
        t.add_abridge("ЛЕВ.ЧАСТЬ")
        t.add_variant("ЛЕВАЯ СТОРОНА", False)
        t.add_abridge("ЛЕВ.СТОРОНА")
        AddressItemToken.__m_ontology.add(t)
        t = Termin("ТАМ ЖЕ")
        t.add_abridge("ТАМЖЕ")
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("АВТОЗАПРАВОЧНАЯ СТАНЦИЯ", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "АЗС", True, True)
        t.add_variant("АВТО ЗАПРАВОЧНАЯ СТАНЦИЯ", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("АВТОНОМНАЯ ТЕПЛОВАЯ СТАНЦИЯ", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "АТС", True, True)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("ДОРОЖНО РЕМОНТНЫЙ ПУНКТ", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "ДРП", True, True)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("УСТАНОВКА КОМПЛЕКСНОЙ ПОДГОТОВКИ ГАЗА", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "УКПГ", True, True)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("УСТАНОВКА ПРЕДВАРИТЕЛЬНОЙ ПОДГОТОВКИ ГАЗА", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "УППГ", True, True)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("ЦЕНТРАЛЬНЫЙ ПУНКТ СБОРА НЕФТИ", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "ЦПС", True, True)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("КОМПЛЕКТНАЯ ТРАНСФОРМАТОРНАЯ ПОДСТАНЦИЯ", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "КТП", True, True)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("ТРАНСФОРМАТОРНАЯ ПОДСТАНЦИЯ", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "ТП", True, True)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("ДИСПЕТЧЕРСКАЯ НЕФТЕПРОВОДНАЯ СЛУЖБА", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "ДНС", True, True)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("КУСТОВАЯ НАСОСНАЯ СТАНЦИЯ", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "КНС", True, True)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("ЦЕНТРАЛЬНЫЙ РАСПРЕДЕЛИТЕЛЬНЫЙ ПУНКТ", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "ЦРП", True, True)
        t.add_variant("ЦРП ТП", False)
        AddressItemToken.__m_ontology.add(t)
        t = Termin._new179("ТРАНСФОРМАТОРНАЯ ПОДСТАНЦИЯ", AddressItemType.HOUSE, AddressHouseType.SPECIAL, "ТП", True, True)
        AddressItemToken.__m_ontology.add(t)
        Termin.ASSIGN_ALL_TEXTS_AS_NORMAL = False
    
    __m_ontology = None
    
    M_PLOT = None
    
    M_OWNER = None
    
    @staticmethod
    def goto_end_of_address(t : 'Token', is_house_ : bool) -> 'Token':
        is_house_.value = False
        br_start = None
        br_end = None
        t1 = t
        tt = t.next0_
        first_pass3759 = True
        while True:
            if first_pass3759: first_pass3759 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if ((isinstance(tt, NumberToken)) or tt.is_newline_before): 
                break
            ttt = Utils.asObjectOrNull(tt, TextToken)
            if (ttt is None): 
                break
            if (ttt.is_char('(')): 
                br_start = tt
            if (ttt.is_char(')')): 
                br_end = tt
            if (not ttt.chars.is_letter): 
                continue
            if ((ttt.is_value("ЧАСНЫЙ", None) or ttt.is_value("ЧАСТНЫЙ", None) or ttt.term == "Ч") or ttt.term == "ЧАСТН"): 
                tt2 = ttt.next0_
                if (tt2 is not None and tt2.is_char_of(".\\/-")): 
                    tt2 = tt2.next0_
                if (isinstance(tt2, TextToken)): 
                    if ((tt2.is_value("С", None) or tt2.is_value("ДОМ", None) or tt2.is_value("СЕКТ", None)) or tt2.is_value("СЕКТОР", None) or tt2.is_value("Д", None)): 
                        if (tt2.is_value("ДОМ", None)): 
                            is_house_.value = True
                        tt = tt2
                        t1 = tt
                        continue
            if ((ttt.term == "ЛПХ" or ttt.term == "ИЖС" or ttt.term == "ЖД") or ttt.term == "ПС" or ttt.term == "ВЧ"): 
                t1 = tt
                continue
            if (ttt.term.startswith("ОБЩ") or ttt.term == "МОП"): 
                is_house_.value = True
                t1 = tt
                continue
            if (ttt.term.startswith("СЕМ") or ttt.term.startswith("ВЕД")): 
                continue
            if ((ttt.length_char == 3 and ttt.chars.is_all_upper and MiscLocationHelper.is_user_param_address(ttt)) and NumberHelper.try_parse_roman(ttt) is None): 
                t1 = tt
                continue
            if ((ttt.length_char == 1 and ttt.next0_ is not None and ttt.next0_.is_char_of("\\/")) and (isinstance(ttt.next0_.next0_, TextToken)) and ttt.next0_.next0_.length_char == 1): 
                tt = tt.next0_.next0_
                t1 = tt
                continue
            break
        if (br_start is not None and t1.end_char > br_start.begin_char): 
            if (br_end is not None and br_end.end_char > t1.end_char): 
                t1 = br_end
            else: 
                br = BracketHelper.try_parse(br_start, BracketParseAttr.NO, 100)
                if (br is not None and br.end_char > t1.end_char): 
                    t1 = br.end_token
        return t1
    
    @staticmethod
    def try_parse_pure_item(t : 'Token', prev : 'AddressItemToken'=None, ad : 'GeoAnalyzerData'=None) -> 'AddressItemToken':
        from pullenti.ner.geo.internal.NumToken import NumToken
        from pullenti.ner.geo.internal.OrgTypToken import OrgTypToken
        if (t is None): 
            return None
        if (t.is_char(',')): 
            return None
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        max_level = 0
        if ((prev is not None and (isinstance(t, NumberToken)) and t.length_char == 5) and t.typ == NumberSpellingType.DIGIT and not t.morph.class0_.is_adjective): 
            if (prev.typ == AddressItemType.COUNTRY or prev.typ == AddressItemType.REGION or prev.typ == AddressItemType.CITY): 
                return AddressItemToken._new191(AddressItemType.ZIP, t, t, str(t.value))
        if ((prev is not None and ((prev.typ == AddressItemType.HOUSE or prev.typ == AddressItemType.CORPUS or prev.typ == AddressItemType.BUILDING)) and t.is_value("БЛОК", None)) and (t.whitespaces_after_count < 3)): 
            nn = NumToken.try_parse(t.next0_, GeoTokenType.STRONG)
            if (nn is not None): 
                return AddressItemToken._new191(AddressItemType.BLOCK, t, nn.end_token, nn.value)
        if ((prev is not None and prev.typ == AddressItemType.STREET and t.length_char == 1) and ((t.is_value("С", None) or t.is_value("Д", None)))): 
            max_level = 1
        elif (AddressItemToken.SPEED_REGIME and ((ad.aregime or ad.all_regime)) and not (isinstance(t, ReferentToken))): 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            if (d is None): 
                return None
            if (d.addr is None): 
                return None
            if (d.addr.house_type == AddressHouseType.ESTATE and d.no_geo): 
                return None
            ok = True
            tt = t
            while tt is not None and tt.begin_char <= d.addr.end_char: 
                if (isinstance(tt, ReferentToken)): 
                    ok = False
                    max_level = 1
                    break
                tt = tt.next0_
            if (ok): 
                return d.addr
        if (ad.alevel > (max_level + 1)): 
            return None
        if (ad.level > 1): 
            return None
        ad.level += 1
        res = AddressItemToken.__try_parse_pure_item(t, False, prev)
        if (res is None and BracketHelper.is_bracket(t, False) and (t.whitespaces_after_count < 2)): 
            res1 = AddressItemToken.__try_parse_pure_item(t.next0_, False, prev)
            if (res1 is not None and BracketHelper.is_bracket(res1.end_token.next0_, False)): 
                res = res1
                res.begin_token = t
                res.end_token = res1.end_token.next0_
        if ((res is None and prev is not None and t.length_char == 1) and t.is_value("С", None)): 
            if (prev.typ == AddressItemType.CORPUS or prev.typ == AddressItemType.HOUSE or prev.typ == AddressItemType.STREET): 
                next0__ = AddressItemToken.__try_parse_pure_item(t.next0_, False, None)
                if (next0__ is not None and next0__.typ == AddressItemType.NUMBER): 
                    next0__.typ = AddressItemType.BUILDING
                    next0__.begin_token = t
                    res = next0__
        if (res is not None and res.typ == AddressItemType.DETAIL): 
            pass
        else: 
            det = AddressItemToken.__try_attach_detail(t, None)
            if (res is None): 
                res = det
            elif (det is not None and det.end_char > res.end_char): 
                res = det
        if ((res is not None and not Utils.isNullOrEmpty(res.value) and str.isdigit(res.value[len(res.value) - 1])) and MiscLocationHelper.is_user_param_address(res)): 
            t1 = res.end_token.next0_
            if (((isinstance(t1, TextToken)) and (t1.whitespaces_before_count < 3) and t1.chars.is_letter) and t1.length_char == 1): 
                res2 = AddressItemToken.__try_parse_pure_item(t1, False, None)
                if (res2 is None): 
                    sit = StreetItemToken.try_parse(t1, None, False, None)
                    if (sit is not None and sit.typ == StreetItemType.NOUN): 
                        pass
                    elif (t1.is_value2("В", "ГРАНИЦА")): 
                        pass
                    else: 
                        ch = AddressItemToken.__correct_char_token(t1)
                        if (OrgTypToken.try_parse(t1, False, None) is not None): 
                            ch = (None)
                        if (ch is not None and ch != "К" and ch != "С"): 
                            res.value = "{0}{1}".format(res.value, ch)
                            res.end_token = t1
        if ((res is not None and res.typ == AddressItemType.NUMBER and res.end_token.next0_ is not None) and res.end_token.next0_.is_value("ДОЛЯ", None)): 
            res.end_token = res.end_token.next0_
            res.typ = AddressItemType.PART
            res.value = "1"
        if (res is None and t.get_morph_class_in_dictionary().is_preposition): 
            next0__ = AddressItemToken.try_parse_pure_item(t.next0_, None, None)
            if (next0__ is not None and next0__.typ != AddressItemType.NUMBER and not t.next0_.is_value("СТ", None)): 
                next0__.begin_token = t
                res = next0__
        if (res is not None and ((res.typ == AddressItemType.NUMBER or res.typ == AddressItemType.HOUSE or res.typ == AddressItemType.PLOT))): 
            tt = res.end_token.next0_
            if (tt is not None and tt.is_hiphen): 
                tt = tt.next0_
            if (tt is not None and tt.is_value("ЛПХ", None)): 
                res.end_token = tt
            if (tt is not None and tt.is_char_of("\\/")): 
                tt = tt.next0_
            if ((isinstance(tt, TextToken)) and len(tt.term) == 2): 
                if (tt.term[1] == 'П' or tt.term[1] == 'С'): 
                    ne = AddressItemToken.__try_parse_pure_item(tt, False, None)
                    if (ne is None or ne.end_token == tt): 
                        res.end_token = tt
        if (res is not None and res.value is not None): 
            res.__corr_num()
        ad.level -= 1
        return res
    
    @staticmethod
    def __try_parse_pure_item(t : 'Token', prefix_before : bool, prev : 'AddressItemToken') -> 'AddressItemToken':
        from pullenti.ner.geo.internal.CityItemToken import CityItemToken
        from pullenti.ner.geo.internal.NumToken import NumToken
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        if (isinstance(t, NumberToken)): 
            n = Utils.asObjectOrNull(t, NumberToken)
            if (((n.length_char == 6 or ((n.length_char == 5 and t.kit.base_language.is_ua)))) and n.typ == NumberSpellingType.DIGIT and not n.morph.class0_.is_adjective): 
                return AddressItemToken._new191(AddressItemType.ZIP, t, t, str(n.value))
            if ((not t.is_whitespace_after and t.next0_ is not None and t.next0_.is_char_of(":")) and not t.next0_.is_whitespace_after and (isinstance(t.next0_.next0_, NumberToken))): 
                return None
            ok = False
            if ((t.previous is not None and t.previous.morph.class0_.is_preposition and t.next0_ is not None) and t.next0_.chars.is_letter and t.next0_.chars.is_all_lower): 
                ok = True
            elif (t.morph.class0_.is_adjective and not t.morph.class0_.is_noun): 
                ok = True
            tok0 = AddressItemToken.__m_ontology.try_parse(t.next0_, TerminParseAttr.NO)
            if (tok0 is not None and (isinstance(tok0.termin.tag, AddressItemType))): 
                typ0 = Utils.valToEnum(tok0.termin.tag, AddressItemType)
                if (tok0.end_token.next0_ is None or tok0.end_token.is_newline_after): 
                    ok = True
                elif (tok0.end_token.next0_.is_comma and (isinstance(tok0.end_token.next0_.next0_, NumberToken)) and typ0 == AddressItemType.FLAT): 
                    return AddressItemToken._new191(AddressItemType.HOUSE, t, t, n.value)
                if (t.previous is not None and t.previous.is_comma and tok0.length_char > 1): 
                    tt = tok0.end_token.next0_
                    if (tt is None or tt.is_comma or tok0.is_newline_after): 
                        return AddressItemToken._new191(typ0, t, tok0.end_token, n.value)
                if (typ0 == AddressItemType.FLAT): 
                    if ((isinstance(t.next0_, TextToken)) and t.next0_.is_value("КВ", None)): 
                        if (t.next0_.get_source_text() == "кВ" and not MiscLocationHelper.is_user_param_address(t)): 
                            return None
                        si = StreetItemToken.try_parse(t.next0_, None, False, None)
                        if (si is not None and si.typ == StreetItemType.NOUN and si.end_char > tok0.end_char): 
                            return None
                        suf = NumberHelper.try_parse_postfix_only(t.next0_)
                        if (suf is not None): 
                            return None
                    if ((isinstance(tok0.end_token.next0_, NumberToken)) and (tok0.end_token.whitespaces_after_count < 3)): 
                        if (prev is not None and ((prev.typ == AddressItemType.STREET or prev.typ == AddressItemType.CITY))): 
                            return AddressItemToken._new191(AddressItemType.NUMBER, t, t, str(n.value))
                if (isinstance(tok0.end_token.next0_, NumberToken)): 
                    pass
                elif (tok0.end_token.next0_ is not None and tok0.end_token.next0_.is_value("НЕТ", None)): 
                    pass
                elif ((((typ0 == AddressItemType.KILOMETER or typ0 == AddressItemType.FLOOR or typ0 == AddressItemType.BLOCK) or typ0 == AddressItemType.POTCH or typ0 == AddressItemType.FLAT) or typ0 == AddressItemType.PLOT or typ0 == AddressItemType.BOX) or typ0 == AddressItemType.OFFICE): 
                    next0__ = AddressItemToken.__try_parse_pure_item(tok0.end_token.next0_, False, None)
                    if (next0__ is not None and next0__.typ == AddressItemType.NUMBER): 
                        pass
                    elif (tok0.end_token.is_value("ПОД", None)): 
                        pass
                    else: 
                        next0__ = AddressItemToken.__try_parse_pure_item(tok0.end_token, False, None)
                        if (next0__ is not None and next0__.value is not None and next0__.value != "0"): 
                            pass
                        else: 
                            return AddressItemToken._new191(typ0, t, tok0.end_token, str(n.value))
        prepos = False
        tok = None
        if (t is not None and t.morph.class0_.is_preposition): 
            tok = AddressItemToken.__m_ontology.try_parse(t, TerminParseAttr.NO)
            if ((tok) is None): 
                if (t.begin_char < t.end_char): 
                    return None
                if (t.is_value("В", None) and MiscLocationHelper.is_user_param_address(t)): 
                    tt = t.next0_
                    if (tt is not None and tt.is_char('.')): 
                        tt = tt.next0_
                    num1 = NumToken.try_parse(tt, GeoTokenType.HOUSE)
                    if (num1 is not None): 
                        tt0 = t.previous
                        while tt0 is not None: 
                            if (tt0.is_value("КВАРТАЛ", None) or tt0.is_value("КВ", None) or tt0.is_value("ЛЕСНИЧЕСТВО", None)): 
                                return AddressItemToken._new191(AddressItemType.PLOT, t, num1.end_token, num1.value)
                            if (tt0.is_newline_before): 
                                break
                            tt0 = tt0.previous
                if (not t.is_char_of("КСкс")): 
                    t = t.next0_
                prepos = True
        if (t is None): 
            return None
        if ((((isinstance(t, TextToken)) and t.length_char == 1 and t.chars.is_letter) and not t.is_value("V", None) and not t.is_value("I", None)) and not t.is_value("X", None)): 
            if (t.previous is not None and t.previous.is_comma): 
                if (((t.next0_ is not None and t.next0_.is_comma and (isinstance(t.next0_.next0_, NumberToken))) and t.is_value("Д", None) and prev is not None) and prev.typ == AddressItemType.STREET): 
                    pass
                elif (t.is_newline_after or t.next0_.is_comma): 
                    return AddressItemToken._new199(AddressItemType.BUILDING, t, t, AddressBuildingType.LITER, t.term)
        if (BracketHelper.is_bracket(t, True)): 
            br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
            if ((br is not None and (isinstance(t.next0_, TextToken)) and t.next0_.length_char <= 2) and t.next0_.next0_ == br.end_token and t.next0_.length_char == 1): 
                return AddressItemToken._new199(AddressItemType.BUILDING, t, br.end_token, AddressBuildingType.LITER, t.next0_.term)
        if (t.is_char('/')): 
            next0__ = AddressItemToken.try_parse_pure_item(t.next0_, prev, None)
            if (next0__ is not None and next0__.end_token.next0_ is not None and next0__.end_token.next0_.is_char('/')): 
                next0__.begin_token = t
                next0__.end_token = next0__.end_token.next0_
                return next0__
            if (next0__ is not None and next0__.end_token.is_char('/')): 
                next0__.begin_token = t
                return next0__
        if (tok is None): 
            tok = AddressItemToken.__m_ontology.try_parse(t, TerminParseAttr.NO)
        t1 = t
        typ_ = AddressItemType.NUMBER
        house_typ = AddressHouseType.UNDEFINED
        build_typ = AddressBuildingType.UNDEFINED
        space_detail = None
        has_num_prefix = False
        tok00 = tok
        if (tok is not None): 
            if (t.is_value("УЖЕ", None)): 
                return None
            if (t.is_value("ЛИТЕРА", None)): 
                str0_ = t.get_source_text()
                if (str.isupper(str0_[len(str0_) - 1]) and str.islower(str0_[len(str0_) - 2])): 
                    return AddressItemToken._new199(AddressItemType.BUILDING, t, t, AddressBuildingType.LITER, str0_[len(str0_) - 1:])
            if (t.is_value("ПОД", None) and tok.end_token == t): 
                if (not (isinstance(t.next0_, NumberToken))): 
                    return None
            if ((tok.length_char == 1 and t.next0_ is not None and t.next0_.is_hiphen) and (isinstance(t.next0_.next0_, NumberToken))): 
                return None
            if (t.is_value("НОМЕР", None)): 
                has_num_prefix = True
            if (tok.termin.canonic_text == "ТАМ ЖЕ"): 
                cou = 0
                tt = t.previous
                first_pass3760 = True
                while True:
                    if first_pass3760: first_pass3760 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (cou > 1000): 
                        break
                    r = tt.get_referent()
                    if (r is None): 
                        continue
                    if (isinstance(r, AddressReferent)): 
                        g = Utils.asObjectOrNull(r.get_slot_value(AddressReferent.ATTR_GEO), GeoReferent)
                        if (g is not None): 
                            return AddressItemToken._new202(AddressItemType.CITY, t, tok.end_token, g)
                        break
                    elif (isinstance(r, GeoReferent)): 
                        g = Utils.asObjectOrNull(r, GeoReferent)
                        if (not g.is_state): 
                            return AddressItemToken._new202(AddressItemType.CITY, t, tok.end_token, g)
                return None
            if (isinstance(tok.termin.tag, AddressDetailType)): 
                return AddressItemToken.__try_attach_detail(t, tok)
            t1 = tok.end_token.next0_
            if ((isinstance(t1, TextToken)) and t1.term.startswith("ОБ")): 
                tok.end_token = t1
                t1 = t1.next0_
                if (t1 is not None and t1.is_char('.')): 
                    tok.end_token = t1
                    t1 = t1.next0_
            if (tok.termin.canonic_text == "НЕЖИЛОЕ"): 
                first_pass3761 = True
                while True:
                    if first_pass3761: first_pass3761 = False
                    else: t1 = t1.next0_
                    if (not (t1 is not None)): break
                    if (t1.is_char('.')): 
                        continue
                    if (t1.is_value("ВСТР", None) or t1.is_value("ВСТРОЕН", None) or t1.is_value("ВСТРОЕННЫЙ", None)): 
                        continue
                    tok2 = AddressItemToken.__m_ontology.try_parse(t1, TerminParseAttr.NO)
                    if (tok2 is None): 
                        break
                    if (tok2.termin.canonic_text == "ПОМЕЩЕНИЕ"): 
                        t1 = tok2.end_token.next0_
                    break
            if ((t1 is not None and t1.is_char('(') and (isinstance(t1.next0_, TextToken))) and t1.next0_.term.startswith("ОБ")): 
                tok.end_token = t1.next0_
                t1 = t1.next0_.next0_
                while t1 is not None:
                    if (t1.is_char_of(".)")): 
                        tok.end_token = t1
                        t1 = t1.next0_
                    else: 
                        break
            if (isinstance(tok.termin.tag, AddressItemType)): 
                if (isinstance(tok.termin.tag2, AddressHouseType)): 
                    house_typ = (Utils.valToEnum(tok.termin.tag2, AddressHouseType))
                if (isinstance(tok.termin.tag2, AddressBuildingType)): 
                    build_typ = (Utils.valToEnum(tok.termin.tag2, AddressBuildingType))
                typ_ = (Utils.valToEnum(tok.termin.tag, AddressItemType))
                if (typ_ == AddressItemType.CORPUSORFLAT and MiscLocationHelper.is_user_param_no_flats(tok)): 
                    typ_ = AddressItemType.CORPUS
                if (typ_ == AddressItemType.PLOT): 
                    if (t.previous is not None and ((t.previous.is_value("СУДЕБНЫЙ", "СУДОВИЙ") or t.previous.is_value("ИЗБИРАТЕЛЬНЫЙ", "ВИБОРЧИЙ")))): 
                        return None
                if (t1 is not None and t1.is_char_of("\\/") and AddressItemToken.__m_ontology.try_parse(t1.next0_, TerminParseAttr.NO) is not None): 
                    res_list = list()
                    res_list.append(AddressItemToken(typ_, t, t1))
                    tt = None
                    tt = t1.next0_
                    while tt is not None: 
                        tok1 = AddressItemToken.__m_ontology.try_parse(tt, TerminParseAttr.NO)
                        if (tok1 is None): 
                            break
                        if (not (isinstance(tok1.termin.tag, AddressItemType))): 
                            break
                        res_list.append(AddressItemToken(Utils.valToEnum(tok1.termin.tag, AddressItemType), tt, tok1.end_token))
                        tt = tok1.end_token
                        tt = tt.next0_
                        if (tt is None or not tt.is_char_of("\\/")): 
                            break
                        tt = tt.next0_
                    if (len(res_list) > 1 and tt is not None): 
                        i = 0
                        while i < len(res_list): 
                            nn = NumToken.try_parse(tt, GeoTokenType.TOSLASH)
                            if (nn is None): 
                                break
                            res_list[i].end_token = nn.end_token
                            res_list[i].value = nn.value
                            if (i > 0): 
                                res_list[i].begin_token = tt
                            if (i == (len(res_list) - 1)): 
                                for j in range(len(res_list) - 2, -1, -1):
                                    res_list[j].alt_typ = res_list[j + 1]
                                return res_list[0]
                            tt = nn.end_token.next0_
                            if (tt is None or not tt.is_char_of("\\/")): 
                                break
                            tt = tt.next0_
                            i += 1
                if (typ_ == AddressItemType.FLOOR and (isinstance(tok.termin.tag3, str))): 
                    return AddressItemToken._new191(typ_, t, tok.end_token, Utils.asObjectOrNull(tok.termin.tag3, str))
                if (typ_ == AddressItemType.FLOOR and (isinstance(tok.end_token.next0_, TextToken))): 
                    if (tok.end_token.next0_.is_hiphen and not tok.end_token.next0_.is_whitespace_after and (isinstance(tok.end_token.next0_.next0_, NumberToken))): 
                        return AddressItemToken._new191(typ_, t, tok.end_token.next0_.next0_, "-" + tok.end_token.next0_.next0_.value)
                    if ((tok.end_token.next0_.length_char == 1 and tok.end_token.next0_.chars.is_all_upper and (isinstance(tok.end_token.next0_.next0_, NumberToken))) and not tok.end_token.next0_.is_whitespace_after): 
                        return AddressItemToken._new191(typ_, t, tok.end_token.next0_.next0_, tok.end_token.next0_.term + tok.end_token.next0_.next0_.value)
                if (typ_ == AddressItemType.HOUSE and house_typ == AddressHouseType.SPECIAL): 
                    tt2 = tok.end_token.next0_
                    if (tt2 is not None and tt2.is_hiphen): 
                        tt2 = tt2.next0_
                    res = AddressItemToken._new207(typ_, t, tok.end_token, house_typ, Utils.ifNotNull(tok.termin.acronym, tok.termin.canonic_text))
                    num2 = NumToken.try_parse(tt2, GeoTokenType.ANY)
                    if (num2 is not None and (tt2.whitespaces_before_count < 2)): 
                        res.value = "{0}-{1}".format(res.value, num2.value)
                        res.end_token = num2.end_token
                    return res
                if (typ_ == AddressItemType.FLAT and t.is_value("КВ", None)): 
                    sit = StreetItemToken.try_parse(t, None, False, None)
                    if (sit is not None and sit.end_char > tok.end_char): 
                        return None
                if (typ_ == AddressItemType.PREFIX): 
                    first_pass3762 = True
                    while True:
                        if first_pass3762: first_pass3762 = False
                        else: t1 = t1.next0_
                        if (not (t1 is not None)): break
                        if (((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction)) and t1.whitespaces_after_count == 1): 
                            continue
                        if (t1.is_char(':')): 
                            t1 = t1.next0_
                            break
                        if (t1.is_char('(')): 
                            br = BracketHelper.try_parse(t1, BracketParseAttr.NO, 100)
                            if (br is not None and (br.length_char < 50)): 
                                t1 = br.end_token
                                continue
                        if (isinstance(t1, TextToken)): 
                            if (t1.chars.is_all_lower or (t1.whitespaces_before_count < 3)): 
                                npt = MiscLocationHelper._try_parse_npt(t1)
                                if (npt is not None and ((npt.chars.is_all_lower or npt.morph.case_.is_genitive))): 
                                    if (CityItemToken.check_keyword(npt.end_token) is None and TerrItemToken.check_keyword(npt.end_token) is None): 
                                        t1 = npt.end_token
                                        continue
                        if (t1.is_value("УКАЗАННЫЙ", None) or t1.is_value("ЕГРИП", None) or t1.is_value("ФАКТИЧЕСКИЙ", None)): 
                            continue
                        if (t1.is_comma): 
                            if (t1.next0_ is not None and t1.next0_.is_value("УКАЗАННЫЙ", None)): 
                                continue
                        break
                    if (t1 is not None): 
                        t0 = t
                        if (((t0.previous is not None and not t0.is_newline_before and t0.previous.is_char(')')) and (isinstance(t0.previous.previous, TextToken)) and t0.previous.previous.previous is not None) and t0.previous.previous.previous.is_char('(')): 
                            t = t0.previous.previous.previous.previous
                            if (t is not None and t.get_morph_class_in_dictionary().is_adjective and not t.is_newline_after): 
                                t0 = t
                        if (t0.begin_char > t1.previous.begin_char): 
                            return None
                        res = AddressItemToken(AddressItemType.PREFIX, t0, t1.previous)
                        tt = t0.previous
                        first_pass3763 = True
                        while True:
                            if first_pass3763: first_pass3763 = False
                            else: tt = tt.previous
                            if (not (tt is not None)): break
                            if (tt.newlines_after_count > 3): 
                                break
                            if (tt.is_comma_and or tt.is_char_of("().")): 
                                continue
                            if (not (isinstance(tt, TextToken))): 
                                break
                            if (((tt.is_value("ПОЧТОВЫЙ", None) or tt.is_value("ЮРИДИЧЕСКИЙ", None) or tt.is_value("ЮР", None)) or tt.is_value("ФАКТИЧЕСКИЙ", None) or tt.is_value("ФАКТ", None)) or tt.is_value("ПОЧТ", None) or tt.is_value("АДРЕС", None)): 
                                res.begin_token = tt
                            else: 
                                break
                        return res
                    else: 
                        return None
                elif ((typ_ == AddressItemType.CORPUSORFLAT and not tok.is_whitespace_before and not tok.is_whitespace_after) and tok.begin_token == tok.end_token and tok.begin_token.is_value("К", None)): 
                    if (prev is not None and prev.typ == AddressItemType.FLAT): 
                        typ_ = AddressItemType.ROOM
                    else: 
                        typ_ = AddressItemType.CORPUS
                if (typ_ == AddressItemType.DETAIL and t.is_value("У", None)): 
                    if (not MiscLocationHelper.check_geo_object_before(t, False)): 
                        return None
                if (typ_ == AddressItemType.FLAT and t.is_value("КВ", None)): 
                    if (t.get_source_text() == "кВ"): 
                        return None
                if (((typ_ == AddressItemType.FLAT or typ_ == AddressItemType.SPACE or typ_ == AddressItemType.OFFICE)) and not (isinstance(tok.end_token.next0_, NumberToken))): 
                    next0__ = AddressItemToken.__try_parse_pure_item(tok.end_token.next0_, False, None)
                    if (next0__ is not None and typ_ != AddressItemType.OFFICE and next0__.typ == AddressItemType.FLAT): 
                        next0__.begin_token = t
                        return next0__
                    if (next0__ is not None and next0__.typ == AddressItemType.BUILDING and next0__.building_type == AddressBuildingType.LITER): 
                        return AddressItemToken._new191(typ_, t, next0__.end_token, next0__.value)
                    if (next0__ is not None and ((next0__.typ == AddressItemType.CORPUS or next0__.typ == AddressItemType.HOUSE)) and next0__.begin_token.length_char == 1): 
                        return AddressItemToken._new191(typ_, t, next0__.end_token, "{0}{1}".format(("К" if next0__.typ == AddressItemType.CORPUS else "Д"), next0__.value))
                    if (next0__ is not None and typ_ == AddressItemType.OFFICE and ((next0__.typ == AddressItemType.SPACE or next0__.typ == AddressItemType.FLAT))): 
                        next0__.typ = AddressItemType.OFFICE
                        next0__.begin_token = t
                        return next0__
                    if (tok.end_token.next0_ is not None and tok.end_token.next0_.is_char('(')): 
                        tok2 = AddressItemToken.__m_ontology.try_parse(tok.end_token.next0_.next0_, TerminParseAttr.NO)
                        if (tok2 is not None and tok2.end_token.next0_ is not None and tok2.end_token.next0_.is_char(')')): 
                            t1 = tok2.end_token.next0_.next0_
                if (typ_ == AddressItemType.SPACE and tok.termin.tag3 is not None): 
                    if (prev is not None and ((prev.typ == AddressItemType.STREET or prev.typ == AddressItemType.CITY))): 
                        typ_ = AddressItemType.HOUSE
                    elif (prev is not None and ((prev.typ == AddressItemType.HOUSE or prev.typ == AddressItemType.BUILDING or prev.typ == AddressItemType.CORPUS))): 
                        pass
                    else: 
                        pass
                    if (tok.termin.tag2 is not None): 
                        space_detail = tok.termin.canonic_text
                        if (len(space_detail) > 4 or space_detail == "КАФЕ"): 
                            space_detail = space_detail.lower()
                        org1 = OrgItemToken.try_parse(t, None)
                        if (org1 is not None and org1.is_building): 
                            return AddressItemToken._new210(typ_, t, org1.end_token, space_detail, org1)
                if (typ_ == AddressItemType.SPACE): 
                    if (tok.termin.tag2 is not None): 
                        space_detail = tok.termin.canonic_text
                        if (len(space_detail) > 4 or space_detail == "КАФЕ"): 
                            space_detail = space_detail.lower()
                        org1 = OrgItemToken.try_parse(t, None)
                        if (org1 is not None and org1.is_building): 
                            return AddressItemToken._new210(typ_, t, org1.end_token, space_detail, org1)
                    next0__ = AddressItemToken.__try_parse_pure_item(tok.end_token.next0_, False, None)
                    if (next0__ is None and tok.end_token.next0_ is not None and tok.end_token.next0_.is_hiphen): 
                        next0__ = AddressItemToken.__try_parse_pure_item(tok.end_token.next0_.next0_, False, None)
                    if (next0__ is not None and ((next0__.typ == AddressItemType.SPACE or next0__.typ == AddressItemType.ROOM or next0__.typ == AddressItemType.OFFICE))): 
                        next0__.begin_token = t
                        if (next0__.detail_param is None): 
                            next0__.detail_param = space_detail
                        return next0__
                    tok2 = AddressItemToken.__m_ontology.try_parse(tok.end_token.next0_, TerminParseAttr.NO)
                    if (tok2 is None and tok.end_token.next0_ is not None and tok.end_token.next0_.is_hiphen): 
                        tok2 = AddressItemToken.__m_ontology.try_parse(tok.end_token.next0_.next0_, TerminParseAttr.NO)
                    if ((tok2 is not None and tok2.termin.tag is not None and (Utils.valToEnum(tok2.termin.tag, AddressItemType)) == AddressItemType.SPACE) and tok2.termin.tag2 is not None): 
                        space_detail = tok2.termin.canonic_text
                        if (len(space_detail) > 4): 
                            space_detail = space_detail.lower()
                        tok = tok2
                        tok.begin_token = t
                    if ((isinstance(tok.end_token.next0_, TextToken)) and tok.end_token.next0_.term == "ЗОИ"): 
                        return AddressItemToken._new212(typ_, t, tok.end_token.next0_, "3", "МОП")
                if (typ_ == AddressItemType.FLOOR and t1 is not None): 
                    next0__ = AddressItemToken.__try_parse_pure_item(t1, False, None)
                    if (next0__ is not None and next0__.typ == typ_): 
                        next0__.begin_token = t
                        return next0__
                    tt2 = t1
                    if (tt2 is not None and tt2.is_char_of("\\/")): 
                        tt2 = tt2.next0_
                    next0__ = AddressItemToken.__try_parse_pure_item(tt2, prefix_before, prev)
                    if (next0__ is not None and next0__.value == "подвал"): 
                        tt2 = next0__.end_token.next0_
                        if (tt2 is not None and tt2.is_char_of("\\/")): 
                            tt2 = tt2.next0_
                        num2 = AddressItemToken.__try_parse_pure_item(tt2, prefix_before, prev)
                        if (num2 is not None and num2.typ == AddressItemType.NUMBER and num2.value is not None): 
                            num2.typ = typ_
                            num2.begin_token = t
                            num2.value = ("-" + num2.value)
                            return num2
                if (typ_ == AddressItemType.KILOMETER or typ_ == AddressItemType.FLOOR or typ_ == AddressItemType.POTCH): 
                    if ((isinstance(tok.end_token.next0_, NumberToken)) or MiscHelper.check_number_prefix(tok.end_token.next0_) is not None): 
                        pass
                    else: 
                        return AddressItemToken(typ_, t, tok.end_token)
                if ((typ_ == AddressItemType.HOUSE or typ_ == AddressItemType.BUILDING or typ_ == AddressItemType.CORPUS) or typ_ == AddressItemType.PLOT or typ_ == AddressItemType.BOX): 
                    tt2 = t1
                    first_pass3764 = True
                    while True:
                        if first_pass3764: first_pass3764 = False
                        else: tt2 = tt2.next0_
                        if (not (tt2 is not None)): break
                        if (tt2.is_comma): 
                            continue
                        if (tt2.is_value("РАСПОЛОЖЕННЫЙ", None) or tt2.is_value("НАХОДЯЩИЙСЯ", None) or tt2.is_value("ПРИЛЕГАЮЩИЙ", None)): 
                            continue
                        if (tt2.is_value("ПОДВАЛ", None)): 
                            t1 = tt2.next0_
                            continue
                        if (tt2.morph.class0_.is_preposition): 
                            continue
                        tok2 = AddressItemToken.__m_ontology.try_parse(tt2, TerminParseAttr.NO)
                        if (tok2 is not None and (isinstance(tok2.termin.tag, AddressItemType))): 
                            typ2 = Utils.valToEnum(tok2.termin.tag, AddressItemType)
                            if (typ2 != typ_ and ((typ2 == AddressItemType.PLOT or ((typ2 == AddressItemType.HOUSE and typ_ == AddressItemType.PLOT))))): 
                                if (t.begin_char > tt2.previous.begin_char): 
                                    return None
                                return AddressItemToken._new213(typ_, t, tt2.previous, "0", house_typ)
                            if (typ_ == AddressItemType.BOX and typ2 == AddressItemType.SPACE and tok2.termin.canonic_text == "ПОДВАЛ"): 
                                tt2 = tok2.end_token
                                t1 = tt2.next0_
                                continue
                            if (typ_ == AddressItemType.CORPUS and typ2 == AddressItemType.HOUSE and (isinstance(tok2.termin.tag2, AddressHouseType))): 
                                ht = Utils.valToEnum(tok2.termin.tag2, AddressHouseType)
                                if (ht == AddressHouseType.ESTATE or ht == AddressHouseType.HOUSEESTATE): 
                                    tt2 = tok2.end_token
                                    t1 = tt2.next0_
                                    continue
                        if (isinstance(tt2, TextToken)): 
                            if (tt2.term.startswith("ДОП")): 
                                t1 = tt2.next0_
                                if (t1 is not None and t1.is_char('.')): 
                                    tt2 = tt2.next0_
                                    t1 = t1.next0_
                                continue
                        break
                    if (typ_ == AddressItemType.CORPUS): 
                        if (t1 is not None): 
                            if (t1.is_value("СЕКТОР", None) or t1.is_value("МАССИВ", None)): 
                                t1 = t1.next0_
                            elif (t1.is_value("СЕКТ", None) or t1.is_value("МАС", None)): 
                                t1 = t1.next0_
                                if (t1 is not None and t1.is_char('.')): 
                                    t1 = t1.next0_
                            else: 
                                next0__ = AddressItemToken.try_parse_pure_item(t1, None, None)
                                if (next0__ is not None and ((next0__.typ == AddressItemType.CORPUS or next0__.typ == AddressItemType.FLAT or next0__.typ == AddressItemType.CORPUSORFLAT))): 
                                    next0__.typ = AddressItemType.CORPUS
                                    next0__.begin_token = t
                                    return next0__
                                if (next0__ is not None and next0__.building_type == AddressBuildingType.LITER): 
                                    next0__.begin_token = t
                                    return next0__
                if (typ_ == AddressItemType.HOUSE and t1 is not None and t1.chars.is_letter): 
                    next0__ = AddressItemToken.try_parse_pure_item(t1, prev, None)
                    if (next0__ is not None and ((next0__.typ == typ_ or next0__.typ == AddressItemType.PLOT))): 
                        next0__.begin_token = t
                        return next0__
                if (typ_ == AddressItemType.FLAT and (isinstance(t1, TextToken)) and ((t1.is_value("М", None) or t1.is_value("M", None)))): 
                    if (isinstance(t1.next0_, NumberToken)): 
                        t1 = t1.next0_
                    elif (t1.next0_ is not None and t1.next0_.is_char('.') and (isinstance(t1.next0_.next0_, NumberToken))): 
                        t1 = t1.next0_.next0_
                if (typ_ == AddressItemType.ROOM and t1 is not None): 
                    if (t1.is_char_of("\\/")): 
                        next0__ = AddressItemToken.__try_parse_pure_item(t1.next0_, prefix_before, prev)
                        if (next0__ is not None and ((next0__.typ == AddressItemType.ROOM or next0__.typ == AddressItemType.OFFICE))): 
                            next0__.begin_token = t
                            return next0__
                    elif (t1.is_value("К", None) and not t1.is_whitespace_after and (isinstance(t1.next0_, NumberToken))): 
                        t1 = t1.next0_
                if (typ_ == AddressItemType.FIELD): 
                    nt2 = NumberHelper.try_parse_number_with_postfix(t1)
                    if (nt2 is not None and ((nt2.ex_typ == NumberExType.METER2 or nt2.ex_typ == NumberExType.GEKTAR or nt2.ex_typ == NumberExType.AR))): 
                        return AddressItemToken._new191(typ_, t, nt2.end_token, str(nt2))
                    re = AddressItemToken(typ_, t, tok.end_token)
                    nnn = io.StringIO()
                    tt = tok.end_token.next0_
                    first_pass3765 = True
                    while True:
                        if first_pass3765: first_pass3765 = False
                        else: tt = tt.next0_
                        if (not (tt is not None)): break
                        ll = NumberHelper.try_parse_roman(tt)
                        if (ll is not None and ll.int_value is not None): 
                            if (nnn.tell() > 0): 
                                print("-", end="", file=nnn)
                            print(ll.value, end="", file=nnn)
                            tt = ll.end_token
                            re.end_token = tt
                            continue
                        if (tt.is_hiphen): 
                            continue
                        if (tt.is_whitespace_before): 
                            break
                        if (isinstance(tt, NumberToken)): 
                            if (nnn.tell() > 0): 
                                print("-", end="", file=nnn)
                            print(tt.value, end="", file=nnn)
                            re.end_token = tt
                            continue
                        if ((isinstance(tt, TextToken)) and tt.chars.is_all_upper): 
                            if (nnn.tell() > 0): 
                                print("-", end="", file=nnn)
                            print(tt.term, end="", file=nnn)
                            re.end_token = tt
                            continue
                        break
                    if (nnn.tell() > 0): 
                        re.value = Utils.toStringStringIO(nnn)
                        return re
                if (typ_ == AddressItemType.NONUMBER): 
                    return AddressItemToken._new215(AddressItemType.NONUMBER, t, tok.end_token, "0", False)
                if (typ_ == AddressItemType.HOUSE or typ_ == AddressItemType.PLOT): 
                    if (t1 is not None and t1.is_value("ЛПХ", None)): 
                        t1 = t1.next0_
                if ((typ_ != AddressItemType.NUMBER and (isinstance(t1, TextToken)) and t1.chars.is_letter) and not t1.chars.is_all_upper): 
                    next0__ = AddressItemToken.try_parse_pure_item(t1, None, None)
                    if ((next0__ is not None and next0__.typ != AddressItemType.NUMBER and next0__.typ != AddressItemType.NONUMBER) and next0__.value is not None): 
                        next0__.begin_token = t
                        return next0__
                if (typ_ != AddressItemType.NUMBER): 
                    if ((((t1 is None or tok.is_newline_after)) and t.length_char > 1 and ((prev is not None or MiscLocationHelper.is_user_param_address(t)))) and not tok.is_newline_before): 
                        return AddressItemToken._new216(typ_, t, tok.end_token, house_typ, build_typ, "0", space_detail)
                if (typ_ == AddressItemType.PLOT or typ_ == AddressItemType.WELL): 
                    num1 = NumToken.try_parse(t1, GeoTokenType.HOUSE)
                    if (num1 is not None): 
                        return AddressItemToken._new191(typ_, t, num1.end_token, num1.value)
                if (typ_ == AddressItemType.PLOT): 
                    tt = t1
                    if (tt is not None): 
                        if (tt.is_value("У", None) or tt.is_value("ОКОЛО", None) or tt.is_value("ПРИ", None)): 
                            tt = tt.next0_
                    tok1 = AddressItemToken.__m_ontology.try_parse(tt, TerminParseAttr.NO)
                    if (tok1 is not None): 
                        if (isinstance(tok1.termin.tag, AddressItemType)): 
                            ty1 = Utils.valToEnum(tok1.termin.tag, AddressItemType)
                            if (ty1 == AddressItemType.HOUSE or ty1 == AddressItemType.BUILDING or ty1 == AddressItemType.CORPUS): 
                                return AddressItemToken._new191(typ_, t, tt.previous, "0")
                if (typ_ == AddressItemType.NUMBER): 
                    tok1 = AddressItemToken.__m_ontology.try_parse(tok.end_token.next0_, TerminParseAttr.NO)
                    if (tok1 is not None): 
                        if (isinstance(tok1.termin.tag, AddressItemType)): 
                            ty1 = Utils.valToEnum(tok1.termin.tag, AddressItemType)
                            if (ty1 != AddressItemType.NUMBER): 
                                typ_ = ty1
                                t1 = tok1.end_token.next0_
        if (t1 is not None and t1.is_comma): 
            if (typ_ == AddressItemType.FLAT and (isinstance(t1.next0_, NumberToken))): 
                t1 = t1.next0_
            elif ((typ_ == AddressItemType.HOUSE and (isinstance(t1.next0_, NumberToken)) and prev is not None) and prev.typ == AddressItemType.STREET): 
                t1 = t1.next0_
        if (t1 is not None and t1.is_char('.') and t1.next0_ is not None): 
            t1 = t1.next0_
            if (t1.is_newline_before and not MiscLocationHelper.is_user_param_address(t1)): 
                return None
        if (t1 is not None and t1.is_value("ЛПХ", None)): 
            t1 = t1.next0_
            if (t1 is not None and t1.is_hiphen): 
                t1 = t1.next0_
        if ((t1 is not None and t1 != t and ((t1.is_hiphen or t1.is_char_of("_:")))) and (isinstance(t1.next0_, NumberToken))): 
            t1 = t1.next0_
        if (t1 is not None and t1.is_value("МОП", None) and (isinstance(t1.next0_, NumberToken))): 
            t1 = t1.next0_
        if (t1 is not None and t1.is_value("НА", None)): 
            npt = NounPhraseHelper.try_parse(t1, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
            if (npt is not None and npt.end_token.is_value("ПЛАН", None)): 
                t1 = npt.end_token.next0_
        if (t1 is not None and t1.is_char(':')): 
            if (t1.is_newline_after and not MiscLocationHelper.is_user_param_address(t1)): 
                pass
            else: 
                t1 = t1.next0_
        tok = AddressItemToken.__m_ontology.try_parse(t1, TerminParseAttr.NO)
        if (tok is not None and (isinstance(tok.termin.tag, AddressItemType)) and (Utils.valToEnum(tok.termin.tag, AddressItemType)) == AddressItemType.NUMBER): 
            t1 = tok.end_token.next0_
        elif (tok is not None and (isinstance(tok.termin.tag, AddressItemType)) and (Utils.valToEnum(tok.termin.tag, AddressItemType)) == AddressItemType.NONUMBER): 
            re0 = AddressItemToken._new219(typ_, t, tok.end_token, "0", house_typ, build_typ)
            if (not re0.is_whitespace_after and (isinstance(re0.end_token.next0_, NumberToken))): 
                re0.end_token = re0.end_token.next0_
                re0.value = str(re0.end_token.value)
            return re0
        elif (isinstance(t1, TextToken)): 
            term = t1.term
            if (((len(term) == 7 and term.startswith("ЛИТЕРА"))) or ((len(term) == 6 and term.startswith("ЛИТЕР"))) or ((len(term) == 4 and term.startswith("ЛИТ")))): 
                txt = t1.get_source_text()
                if (((str.islower(txt[0]) and str.isupper(txt[len(txt) - 1]))) or len(term) == 7): 
                    res1 = AddressItemToken(AddressItemType.BUILDING, t, t1)
                    res1.building_type = AddressBuildingType.LITER
                    res1.value = term[len(term) - 1:]
                    return res1
            if (term.startswith("БЛОК") and len(term) > 4): 
                txt = t1.get_source_text()
                if (str.islower(txt[0]) and str.isupper(txt[4])): 
                    num1 = NumToken.try_parse(t1.next0_, GeoTokenType.ORG)
                    if (num1 is not None): 
                        res1 = AddressItemToken(AddressItemType.BLOCK, t, num1.end_token)
                        res1.value = (term[4:] + num1.value)
                        return res1
            if (typ_ == AddressItemType.FLAT and t1 is not None): 
                tok2 = AddressItemToken.__m_ontology.try_parse(t1, TerminParseAttr.NO)
                if (tok2 is None and t1.is_comma): 
                    tok2 = AddressItemToken.__m_ontology.try_parse(t1.next0_, TerminParseAttr.NO)
                if (tok2 is not None and (Utils.valToEnum(tok2.termin.tag, AddressItemType)) == AddressItemType.FLAT): 
                    t1 = tok2.end_token.next0_
            if (t1 is not None and t1.is_value2("СТРОИТЕЛЬНЫЙ", "НОМЕР")): 
                t1 = t1.next0_
            ttt = MiscHelper.check_number_prefix(t1)
            if (ttt is not None): 
                t1 = ttt
                has_num_prefix = True
                if (t1.is_hiphen or t1.is_char('_')): 
                    t1 = t1.next0_
        if (typ_ != AddressItemType.NUMBER and t1 is not None): 
            if (t1.is_char('.') and MiscLocationHelper.is_user_param_address(t1)): 
                t1 = t1.next0_
            if (t1 is not None and t1.is_char_of("\\/") and (isinstance(t1.next0_, NumberToken))): 
                t1 = t1.next0_
        if (t != t1 and (isinstance(t1, TextToken))): 
            npt = NounPhraseHelper.try_parse(t1, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
            if (npt is not None and npt.end_token.is_value("ПЛАН", None)): 
                t1 = npt.end_token.next0_
        if (t1 is None): 
            if (typ_ == AddressItemType.GENPLAN): 
                return AddressItemToken._new191(typ_, t, tok00.end_token, "0")
            return None
        if ((t1 == t and t.is_value("С", None) and (isinstance(t.next0_, NumberToken))) and MiscLocationHelper.is_user_param_address(t)): 
            typ_ = AddressItemType.BUILDING
            build_typ = AddressBuildingType.BUILDING
            t1 = t.next0_
        num = io.StringIO()
        nt = Utils.asObjectOrNull(t1, NumberToken)
        re11 = None
        if (nt is not None): 
            if (typ_ == AddressItemType.ROOM or typ_ == AddressItemType.CORPUSORFLAT): 
                nt2 = NumberHelper.try_parse_number_with_postfix(t1)
                if (nt2 is not None and nt2.ex_typ == NumberExType.METER2): 
                    return AddressItemToken._new191(AddressItemType.ROOM, t, nt2.end_token, str(nt2))
            if (typ_ == AddressItemType.FIELD or typ_ == AddressItemType.PLOT): 
                nt2 = NumberHelper.try_parse_number_with_postfix(t1)
                if (nt2 is not None and ((nt2.ex_typ == NumberExType.METER2 or nt2.ex_typ == NumberExType.GEKTAR or nt2.ex_typ == NumberExType.AR))): 
                    return AddressItemToken._new191(typ_, t, nt2.end_token, str(nt2))
            print(nt.value, end="", file=num)
            if (nt.typ == NumberSpellingType.DIGIT or nt.typ == NumberSpellingType.WORDS): 
                if (((isinstance(nt.end_token, TextToken)) and ((nt.end_token.term == "Е" or nt.end_token.term == "И")) and nt.end_token.previous == nt.begin_token) and not nt.end_token.is_whitespace_before): 
                    print(nt.end_token.term, end="", file=num)
                drob = False
                hiph = False
                lit = False
                et = nt.next0_
                if (et is not None and (((et.is_char_of("\\/") or et.is_value("ДРОБЬ", None) or et.is_value("КЛ", None)) or ((et.is_char('.') and MiscLocationHelper.is_user_param_address(et) and (isinstance(et.next0_, NumberToken))))))): 
                    next0__ = AddressItemToken.try_parse_pure_item(et.next0_, None, None)
                    if (next0__ is not None and next0__.typ != AddressItemType.NUMBER and typ_ != AddressItemType.FLAT): 
                        if (next0__.typ == typ_ and next0__.value is not None): 
                            next0__.value = "{0}/{1}".format(Utils.toStringStringIO(num), next0__.value)
                            next0__.begin_token = t
                            return next0__
                        if ((isinstance(et.next0_, NumberToken)) and et.next0_.is_whitespace_after): 
                            next2 = AddressItemToken.try_parse_pure_item(et.next0_.next0_, None, None)
                            if (next2 is not None and next2.typ != AddressItemType.NUMBER): 
                                drob = True
                                et = et.next0_
                            else: 
                                t1 = et
                        else: 
                            t1 = et
                    else: 
                        drob = True
                        et = et.next0_
                    if (drob and et is not None and et.is_char_of("\\/")): 
                        et = et.next0_
                elif (et is not None and ((et.is_hiphen or et.is_char('_')))): 
                    hiph = True
                    et = et.next0_
                elif ((et is not None and et.is_char('.') and (isinstance(et.next0_, NumberToken))) and not et.is_whitespace_after): 
                    hiph = True
                    et = et.next0_
                if (isinstance(et, NumberToken)): 
                    if (drob): 
                        next0__ = AddressItemToken.try_parse_pure_item(et, None, None)
                        if (next0__ is not None and next0__.typ == AddressItemType.NUMBER): 
                            print("/{0}".format(next0__.value), end="", file=num, flush=True)
                            t1 = next0__.end_token
                            et = t1.next0_
                            drob = False
                        else: 
                            print("/{0}".format(et.value), end="", file=num, flush=True)
                            drob = False
                            t1 = et
                            et = et.next0_
                            if (et is not None and et.is_char_of("\\/") and (isinstance(et.next0_, NumberToken))): 
                                t1 = et.next0_
                                print("/{0}".format(t1.value), end="", file=num, flush=True)
                                et = t1.next0_
                    elif ((hiph and not t1.is_whitespace_after and (isinstance(et, NumberToken))) and not et.is_whitespace_before): 
                        numm = AddressItemToken.try_parse_pure_item(et, None, None)
                        if (numm is not None and numm.typ == AddressItemType.NUMBER): 
                            merge = False
                            if ((typ_ == AddressItemType.FLAT or typ_ == AddressItemType.PLOT or typ_ == AddressItemType.SPACE) or typ_ == AddressItemType.OFFICE): 
                                if (not has_num_prefix): 
                                    merge = True
                            elif (MiscLocationHelper.is_user_param_no_flats(et)): 
                                merge = True
                            elif (typ_ == AddressItemType.HOUSE or typ_ == AddressItemType.BUILDING or typ_ == AddressItemType.CORPUS): 
                                ttt = numm.end_token.next0_
                                if (ttt is not None and ttt.is_comma): 
                                    ttt = ttt.next0_
                                numm2 = AddressItemToken.try_parse_pure_item(ttt, None, None)
                                if (numm2 is not None): 
                                    if ((numm2.typ == AddressItemType.FLAT or numm2.typ == AddressItemType.BUILDING or ((numm2.typ == AddressItemType.CORPUSORFLAT and numm2.value is not None))) or numm2.typ == AddressItemType.CORPUS): 
                                        merge = True
                            if (merge): 
                                print("/{0}".format(numm.value), end="", file=num, flush=True)
                                t1 = numm.end_token
                                et = t1.next0_
                                hiph = False
                elif (et is not None and ((et.is_hiphen or et.is_char('_') or et.is_value("НЕТ", None))) and drob): 
                    t1 = et
                ett = et
                if ((ett is not None and ett.is_char_of(",.") and (ett.whitespaces_after_count < 2)) and (isinstance(ett.next0_, TextToken))): 
                    if (BracketHelper.is_bracket(ett.next0_, False)): 
                        ett = ett.next0_
                    elif (ett.next0_.length_char == 1 and ett.next0_.chars.is_letter and ((ett.next0_.next0_ is None or ett.next0_.next0_.is_comma))): 
                        ch = AddressItemToken.__correct_char_token(ett.next0_)
                        if (ch is not None): 
                            print(ch, end="", file=num)
                            ett = ett.next0_
                            t1 = ett
                if ((BracketHelper.is_bracket(ett, False) and (isinstance(ett.next0_, TextToken)) and ett.next0_.length_char == 1) and ett.next0_.is_letters and BracketHelper.is_bracket(ett.next0_.next0_, False)): 
                    ch = AddressItemToken.__correct_char_token(ett.next0_)
                    if (ch is not None): 
                        print(ch, end="", file=num)
                        t1 = ett.next0_.next0_
                    else: 
                        ntt = NumberHelper.try_parse_roman(ett.next0_)
                        if (ntt is not None): 
                            print("/{0}".format(ntt.value), end="", file=num, flush=True)
                            t1 = ett.next0_.next0_
                elif (((BracketHelper.is_bracket(ett, False) and BracketHelper.is_bracket(ett.next0_, False) and (isinstance(ett.next0_.next0_, TextToken))) and ett.next0_.next0_.length_char == 1 and ett.next0_.next0_.is_letters) and BracketHelper.is_bracket(ett.next0_.next0_.next0_, False)): 
                    ch = AddressItemToken.__correct_char_token(ett.next0_.next0_)
                    if (ch is not None): 
                        print(ch, end="", file=num)
                        t1 = ett.next0_.next0_.next0_
                        while t1.next0_ is not None and BracketHelper.is_bracket(t1.next0_, False):
                            t1 = t1.next0_
                elif (BracketHelper.can_be_start_of_sequence(ett, True, False) and (ett.whitespaces_before_count < 2)): 
                    br = BracketHelper.try_parse(ett, BracketParseAttr.NO, 100)
                    if (br is not None and (isinstance(br.begin_token.next0_, TextToken)) and br.begin_token.next0_.next0_ == br.end_token): 
                        s = AddressItemToken.__correct_char_token(br.begin_token.next0_)
                        if (s is not None): 
                            print(s, end="", file=num)
                            t1 = br.end_token
                elif ((isinstance(et, TextToken)) and ((et.length_char == 1 or ((et.length_char == 2 and et.chars.is_all_upper and not et.is_whitespace_before)))) and et.chars.is_letter): 
                    ttt = StreetItemToken.try_parse(et, None, False, None)
                    s = AddressItemToken.__correct_char_token(et)
                    if (ttt is not None and ((ttt.typ == StreetItemType.STDNAME or ttt.typ == StreetItemType.NOUN or ttt.typ == StreetItemType.FIX))): 
                        if (not et.is_whitespace_before and et.next0_ is not None and et.next0_.is_char_of("\\/")): 
                            pass
                        else: 
                            s = (None)
                    elif (TerrItemToken.check_keyword(et) is not None): 
                        s = (None)
                    if (et.is_whitespace_before): 
                        next0__ = AddressItemToken.try_parse_pure_item(et, None, None)
                        if (next0__ is not None and next0__.value is not None): 
                            s = (None)
                        elif (et.previous is not None and et.previous.is_hiphen and et.previous.is_whitespace_before): 
                            s = (None)
                    if (s is not None): 
                        if (((s == "К" or s == "С")) and (isinstance(et.next0_, NumberToken)) and not et.is_whitespace_after): 
                            pass
                        elif ((s == "Б" and et.next0_ is not None and et.next0_.is_char_of("/\\")) and (isinstance(et.next0_.next0_, TextToken)) and et.next0_.next0_.is_value("Н", None)): 
                            et = et.next0_.next0_
                            t1 = et
                        else: 
                            ok = False
                            if (drob or hiph or lit): 
                                ok = True
                            elif (not et.is_whitespace_before or ((et.whitespaces_before_count == 1 and ((MiscLocationHelper.is_user_param_address(et) or et.chars.is_all_upper or ((et.is_newline_after or ((et.next0_ is not None and et.next0_.is_comma))))))))): 
                                ok = True
                                if (isinstance(et.next0_, NumberToken)): 
                                    if (not et.is_whitespace_before and ((et.is_whitespace_after or (isinstance(et.next0_, NumberToken))))): 
                                        pass
                                    else: 
                                        ok = False
                                if (s == "К"): 
                                    tmp = AddressItemToken(typ_, t, et.previous)
                                    next0__ = AddressItemToken.try_parse_pure_item(et, tmp, None)
                                    if (next0__ is not None and next0__.value is not None): 
                                        ok = False
                                if (s == "И"): 
                                    next0__ = AddressItemToken.try_parse_pure_item(et.next0_, prev, None)
                                    if (next0__ is not None and next0__.typ == typ_): 
                                        ok = False
                            elif (((et.next0_ is None or et.next0_.is_comma)) and (((et.whitespaces_before_count < 2) or MiscLocationHelper.is_user_param_address(et)))): 
                                ok = True
                            elif (et.is_whitespace_before and et.chars.is_all_lower and et.is_value("В", "У")): 
                                pass
                            else: 
                                ait_next = AddressItemToken.try_parse_pure_item(et.next0_, None, None)
                                if (ait_next is not None): 
                                    if ((ait_next.typ == AddressItemType.CORPUS or ait_next.typ == AddressItemType.FLAT or ait_next.typ == AddressItemType.BUILDING) or ait_next.typ == AddressItemType.OFFICE or ait_next.typ == AddressItemType.ROOM): 
                                        ok = True
                            if (ok): 
                                print(s, end="", file=num)
                                t1 = et
                                if (et.next0_ is not None and et.next0_.is_char_of("\\/") and et.next0_.next0_ is not None): 
                                    nn = NumToken.try_parse(et.next0_.next0_, GeoTokenType.STRONG)
                                    if (nn is not None): 
                                        print("/{0}".format(nn.value), end="", file=num, flush=True)
                                        et = nn.end_token
                                        t1 = et
                                    elif (isinstance(et.next0_.next0_, NumberToken)): 
                                        print("/{0}".format(et.next0_.next0_.value), end="", file=num, flush=True)
                                        et = et.next0_.next0_
                                        t1 = et
                                    elif (et.next0_.next0_.is_hiphen or et.next0_.next0_.is_char('_') or et.next0_.next0_.is_value("НЕТ", None)): 
                                        et = et.next0_.next0_
                                        t1 = et
                                if ((isinstance(et.next0_, NumberToken)) and not et.is_whitespace_after): 
                                    et = et.next0_
                                    t1 = et
                                    print(t1.value, end="", file=num)
                elif ((isinstance(et, TextToken)) and not et.is_whitespace_before): 
                    val = et.term
                    if (val == "КМ" and typ_ == AddressItemType.HOUSE): 
                        t1 = et
                        print("КМ", end="", file=num)
                    elif (val == "БН"): 
                        t1 = et
                    elif (((len(val) == 2 and val[1] == 'Б' and et.next0_ is not None) and et.next0_.is_char_of("\\/") and et.next0_.next0_ is not None) and et.next0_.next0_.is_value("Н", None)): 
                        print(val[0], end="", file=num)
                        et = et.next0_.next0_
                        t1 = et
                if (not drob and t1.next0_ is not None and t1.next0_.is_char_of("\\/")): 
                    next0__ = AddressItemToken.__try_parse_pure_item(t1.next0_.next0_, False, None)
                    if (next0__ is not None and next0__.typ == AddressItemType.NUMBER): 
                        print("/{0}".format(next0__.value), end="", file=num, flush=True)
                        t1 = next0__.end_token
        else: 
            re11 = AddressItemToken.__try_attachvch(t1, typ_)
            if ((re11) is not None): 
                re11.begin_token = t
                re11.house_type = house_typ
                re11.building_type = build_typ
                return re11
            elif (((isinstance(t1, TextToken)) and t1.length_char == 2 and t1.is_letters) and not t1.is_whitespace_before and (isinstance(t1.previous, NumberToken))): 
                src = t1.get_source_text()
                if ((src is not None and len(src) == 2 and ((src[0] == 'к' or src[0] == 'k'))) and str.isupper(src[1])): 
                    ch = AddressItemToken.correct_char(src[1])
                    if (ch != (chr(0))): 
                        return AddressItemToken._new191(AddressItemType.CORPUS, t1, t1, "{0}".format(ch))
            elif ((isinstance(t1, TextToken)) and t1.length_char == 1 and t1.is_letters): 
                if (t.is_value("САРАЙ", None)): 
                    return None
                ch = AddressItemToken.__correct_char_token(t1)
                if (ch is not None): 
                    if (typ_ == AddressItemType.NUMBER): 
                        return None
                    if (ch == "К" or ch == "С"): 
                        if (not t1.is_whitespace_after and (isinstance(t1.next0_, NumberToken))): 
                            if ((build_typ != AddressBuildingType.LITER and typ_ != AddressItemType.HOUSE and typ_ != AddressItemType.SPACE) and typ_ != AddressItemType.CARPLACE and typ_ != AddressItemType.BOX): 
                                return None
                    if (ch == "С"): 
                        num1 = NumToken.try_parse(t1.next0_, GeoTokenType.ANY)
                        if (num1 is not None and ((num1.has_prefix or num1.is_cadaster_number))): 
                            return AddressItemToken._new191(typ_, t, num1.end_token, num1.value)
                    if (ch == "Д" and typ_ == AddressItemType.PLOT): 
                        rrr = AddressItemToken.try_parse_pure_item(t1, None, None)
                        if (rrr is not None): 
                            rrr.typ = AddressItemType.PLOT
                            rrr.begin_token = t
                            return rrr
                    if (ch == "С" and t1.is_whitespace_after): 
                        next0__ = AddressItemToken.try_parse_pure_item(t1.next0_, None, None)
                        if (next0__ is not None and next0__.typ == AddressItemType.NUMBER): 
                            res1 = AddressItemToken._new225(typ_, t, next0__.end_token, next0__.value, t.morph, house_typ, build_typ)
                            return res1
                    if (prev is not None and ((prev.typ == AddressItemType.HOUSE or prev.typ == AddressItemType.NUMBER or prev.typ == AddressItemType.FLAT)) and MiscLocationHelper.is_user_param_address(t1)): 
                        if (typ_ == AddressItemType.CORPUSORFLAT and prev.typ == AddressItemType.HOUSE): 
                            typ_ = AddressItemType.CORPUS
                    else: 
                        if (t1.chars.is_all_lower and ((t1.morph.class0_.is_preposition or t1.morph.class0_.is_conjunction))): 
                            if ((t1.whitespaces_after_count < 2) and t1.next0_.chars.is_letter): 
                                if (typ_ == AddressItemType.HOUSE or typ_ == AddressItemType.PLOT or typ_ == AddressItemType.BOX): 
                                    return AddressItemToken._new191(typ_, t, t1.previous, "0")
                                return None
                        if (t.chars.is_all_upper and t.length_char == 1 and t.next0_.is_char('.')): 
                            return None
                    print(ch, end="", file=num)
                    if ((t1.next0_ is not None and ((t1.next0_.is_hiphen or t1.next0_.is_char('_'))) and not t1.is_whitespace_after) and (isinstance(t1.next0_.next0_, NumberToken)) and not t1.next0_.is_whitespace_after): 
                        nn = NumToken.try_parse(t1.next0_.next0_, GeoTokenType.HOUSE)
                        if (nn is not None): 
                            print(nn.value, end="", file=num)
                            t1 = nn.end_token
                        else: 
                            print(t1.next0_.next0_.value, end="", file=num)
                            t1 = t1.next0_.next0_
                    elif ((isinstance(t1.next0_, NumberToken)) and not t1.is_whitespace_after): 
                        nn = NumToken.try_parse(t1.next0_, GeoTokenType.HOUSE)
                        if (nn is not None): 
                            print(nn.value, end="", file=num)
                            t1 = nn.end_token
                        else: 
                            print(t1.next0_.value, end="", file=num)
                            t1 = t1.next0_
                    if (num.tell() == 1 and ((typ_ == AddressItemType.OFFICE or typ_ == AddressItemType.ROOM))): 
                        if (not MiscLocationHelper.is_user_param_address(t)): 
                            if (t.is_value("КОМ", None) and not t.next0_.is_char('.')): 
                                return None
                if ((((typ_ == AddressItemType.BOX or typ_ == AddressItemType.SPACE or typ_ == AddressItemType.PART) or typ_ == AddressItemType.CARPLACE or typ_ == AddressItemType.WELL)) and num.tell() == 0): 
                    rom = NumberHelper.try_parse_roman(t1)
                    if (rom is not None): 
                        return AddressItemToken._new191(typ_, t, rom.end_token, str(rom.value))
            elif (((BracketHelper.is_bracket(t1, False) and (isinstance(t1.next0_, TextToken)) and t1.next0_.length_char == 1) and t1.next0_.is_letters and BracketHelper.is_bracket(t1.next0_.next0_, False)) and not t1.is_whitespace_after and not t1.next0_.is_whitespace_after): 
                ch = AddressItemToken.__correct_char_token(t1.next0_)
                if (ch is None): 
                    return None
                print(ch, end="", file=num)
                t1 = t1.next0_.next0_
            elif ((isinstance(t1, TextToken)) and ((((t1.length_char == 1 and ((t1.is_hiphen or t1.is_char('_'))))) or t1.is_value("НЕТ", None) or t1.is_value("БН", None))) and (((typ_ == AddressItemType.CORPUS or typ_ == AddressItemType.CORPUSORFLAT or typ_ == AddressItemType.BUILDING) or typ_ == AddressItemType.HOUSE or typ_ == AddressItemType.FLAT))): 
                while t1.next0_ is not None and ((t1.next0_.is_hiphen or t1.next0_.is_char('_'))) and not t1.is_whitespace_after:
                    t1 = t1.next0_
                val = None
                if (not t1.is_whitespace_after and (isinstance(t1.next0_, NumberToken))): 
                    t1 = t1.next0_
                    val = str(t1.value)
                if (t1.is_value("БН", None)): 
                    val = "0"
                elif (t1.is_value("НЕТ", None)): 
                    val = "НЕТ"
                return AddressItemToken._new191(typ_, t, t1, val)
            else: 
                if (((typ_ == AddressItemType.FLOOR or typ_ == AddressItemType.KILOMETER or typ_ == AddressItemType.POTCH)) and (isinstance(t.previous, NumberToken))): 
                    return AddressItemToken(typ_, t, t1.previous)
                if ((isinstance(t1, ReferentToken)) and (isinstance(t1.get_referent(), DateReferent))): 
                    nn = AddressItemToken.try_parse_pure_item(t1.begin_token, None, None)
                    if (nn is not None and nn.end_char == t1.end_char and nn.typ == AddressItemType.NUMBER): 
                        nn.begin_token = t
                        nn.end_token = t1
                        nn.typ = typ_
                        return nn
                if ((isinstance(t1, TextToken)) and ((typ_ == AddressItemType.HOUSE or typ_ == AddressItemType.BUILDING or typ_ == AddressItemType.CORPUS))): 
                    ter = t1.term
                    if (ter == "АБ" or ter == "АБВ" or ter == "МГУ"): 
                        return AddressItemToken._new219(typ_, t, t1, ter, house_typ, build_typ)
                    ccc = AddressItemToken.__corr_number(ter)
                    if (ccc is not None): 
                        return AddressItemToken._new219(typ_, t, t1, ccc, house_typ, build_typ)
                    if (t1.chars.is_all_upper): 
                        nn = NumToken.try_parse(t1, GeoTokenType.STRONG)
                        if (nn is not None and nn.end_token != t1): 
                            t1 = nn.end_token
                            ter = nn.value
                        if (prev is not None and ((prev.typ == AddressItemType.STREET or prev.typ == AddressItemType.CITY))): 
                            return AddressItemToken._new219(typ_, t, t1, ter, house_typ, build_typ)
                        if (typ_ == AddressItemType.CORPUS and (t1.length_char < 4)): 
                            return AddressItemToken._new219(typ_, t, t1, ter, house_typ, build_typ)
                        if (typ_ == AddressItemType.BUILDING and build_typ == AddressBuildingType.LITER and (t1.length_char < 4)): 
                            return AddressItemToken._new219(typ_, t, t1, ter, house_typ, build_typ)
                if ((typ_ == AddressItemType.BOX or typ_ == AddressItemType.SPACE or typ_ == AddressItemType.PART) or typ_ == AddressItemType.CARPLACE or typ_ == AddressItemType.WELL): 
                    num1 = NumToken.try_parse(t1, GeoTokenType.ANY)
                    if (num1 is not None): 
                        return AddressItemToken._new191(typ_, t, num1.end_token, num1.value)
                if (typ_ == AddressItemType.PLOT and t1 is not None): 
                    if ((t1.is_value("ОКОЛО", None) or t1.is_value("РЯДОМ", None) or t1.is_value("НАПРОТИВ", None)) or t1.is_value("БЛИЗЬКО", None) or t1.is_value("НАВПАКИ", None)): 
                        return AddressItemToken._new191(typ_, t, t1, t1.get_source_text().lower())
                    det = AddressItemToken.__try_attach_detail(t1, None)
                    if (det is not None): 
                        return AddressItemToken._new191(typ_, t, t1.previous, "0")
                if (((typ_ != AddressItemType.NUMBER and (isinstance(t1, TextToken)) and t1.length_char <= 2) and t1.chars.is_all_upper and t1.chars.is_letter) and ((not t1.is_whitespace_after or typ_ == AddressItemType.PLOT or typ_ == AddressItemType.BOX)) and (isinstance(t1.next0_, NumberToken))): 
                    num1 = NumToken.try_parse(t1.next0_, GeoTokenType.ANY)
                    if (num1 is not None): 
                        return AddressItemToken._new191(typ_, t, num1.end_token, t1.term + num1.value)
                if (t1 is not None and t1.is_comma and prev is not None): 
                    next0__ = AddressItemToken.try_parse_pure_item(t1.next0_, None, None)
                    if (next0__ is not None): 
                        if (next0__.typ == AddressItemType.NUMBER or next0__.typ == typ_): 
                            return AddressItemToken._new191(typ_, t, next0__.end_token, next0__.value)
                        if (prev is not None and t1.previous is not None and t.begin_char <= t1.previous.begin_char): 
                            return AddressItemToken(typ_, t, t1.previous)
                if (t1 is not None and t1.is_char('(')): 
                    next0__ = AddressItemToken.try_parse_pure_item(t1.next0_, prev, None)
                    if ((next0__ is not None and next0__.typ == AddressItemType.NUMBER and next0__.end_token.next0_ is not None) and next0__.end_token.next0_.is_char(')')): 
                        next0__.typ = typ_
                        next0__.begin_token = t
                        next0__.end_token = next0__.end_token.next0_
                        return next0__
                if (MiscLocationHelper.is_user_param_address(t1) or typ_ != AddressItemType.NUMBER): 
                    nt1 = NumberHelper.try_parse_roman(t1)
                    if (nt1 is not None): 
                        return AddressItemToken._new191(typ_, t, t1, nt1.value)
                if (BracketHelper.is_bracket(t1, False) and (isinstance(t1.next0_, NumberToken))): 
                    next0__ = AddressItemToken.__try_parse_pure_item(t1.next0_, False, prev)
                    if ((next0__ is not None and next0__.typ == AddressItemType.NUMBER and next0__.end_token.next0_ is not None) and BracketHelper.is_bracket(next0__.end_token.next0_, False)): 
                        next0__.begin_token = t
                        next0__.typ = typ_
                        next0__.end_token = next0__.end_token.next0_
                        return next0__
                if (typ_ == AddressItemType.GENPLAN): 
                    return AddressItemToken._new191(typ_, t, tok00.end_token, "0")
                if (typ_ == AddressItemType.NUMBER and t.is_value("ОБЩЕЖИТИЕ", None)): 
                    num1 = NumToken.try_parse(t.next0_, GeoTokenType.ANY)
                    if (num1 is not None): 
                        return AddressItemToken._new191(AddressItemType.HOUSE, t, num1.end_token, num1.value)
                if (t.chars.is_latin_letter and not t.kit.base_language.is_en): 
                    num2 = NumberHelper.try_parse_roman(t)
                    if (num2 is not None): 
                        return AddressItemToken._new191(typ_, t, num2.end_token, num2.value)
                return None
        if (typ_ == AddressItemType.NUMBER and prepos): 
            return None
        if (t1 is None): 
            t1 = t
            while t1.next0_ is not None:
                t1 = t1.next0_
        tt = t.next0_
        while tt is not None and tt.end_char <= t1.end_char: 
            if (tt.is_newline_before and not (isinstance(tt, NumberToken))): 
                return None
            tt = tt.next0_
        if (num.tell() == 0): 
            if (t1 is not None and t1.chars.is_latin_letter and ((not t1.kit.base_language.is_en or MiscLocationHelper.is_user_param_address(t)))): 
                num2 = NumberHelper.try_parse_roman(t1)
                if (num2 is not None): 
                    return AddressItemToken._new191(typ_, t, num2.end_token, num2.value)
            return None
        res0 = AddressItemToken._new244(typ_, t, t1, Utils.toStringStringIO(num), t.morph, house_typ, build_typ, space_detail)
        t1 = t1.next0_
        if (t1 is not None and t1.is_comma): 
            t1 = t1.next0_
        if ((isinstance(t1, TextToken)) and t1.term.startswith("ОБ") and (t1.whitespaces_before_count < 2)): 
            res0.end_token = t1
            t1 = t1.next0_
            if (t1 is not None and t1.is_char('.')): 
                res0.end_token = t1
                t1 = t1.next0_
            if (res0.typ == AddressItemType.CORPUSORFLAT): 
                res0.typ = AddressItemType.FLAT
        if ((t1 is not None and t1.is_char('(') and (isinstance(t1.next0_, TextToken))) and t1.next0_.term.startswith("ОБ")): 
            res0.end_token = t1.next0_
            t1 = t1.next0_.next0_
            while t1 is not None:
                if (t1.is_char_of(".)")): 
                    res0.end_token = t1
                    t1 = t1.next0_
                else: 
                    break
            if (res0.typ == AddressItemType.CORPUSORFLAT): 
                res0.typ = AddressItemType.FLAT
        if ((typ_ == AddressItemType.NUMBER and t1 is not None and (t1.whitespaces_before_count < 3)) and t1.is_whitespace_before): 
            tok2 = AddressItemToken.__m_ontology.try_parse(t1, TerminParseAttr.NO)
            if (tok2 is not None): 
                next0__ = AddressItemToken.__try_parse_pure_item(t1, False, None)
                if ((next0__ is not None and next0__.end_token == tok2.end_token and next0__.typ != AddressItemType.NUMBER) and next0__.building_type != AddressBuildingType.LITER): 
                    if (((next0__.typ == AddressItemType.HOUSE or next0__.typ == AddressItemType.BUILDING or (next0__.typ == AddressItemType.CORPUS and next0__.typ == AddressItemType.FLOOR)) or next0__.typ == AddressItemType.FLAT or next0__.typ == AddressItemType.OFFICE) or next0__.typ == AddressItemType.PLOT): 
                        next0__.value = res0.value
                        next0__.begin_token = t
                        return next0__
        if ((((res0.typ == AddressItemType.SPACE or res0.typ == AddressItemType.FLAT or res0.typ == AddressItemType.OFFICE) or res0.typ == AddressItemType.ROOM or ((res0.typ == AddressItemType.NUMBER and has_num_prefix)))) and res0.value is not None): 
            n0 = 0
            wrapn0246 = RefOutArgWrapper(0)
            Utils.tryParseInt(Utils.ifNotNull(res0.value, ""), wrapn0246)
            n0 = wrapn0246.value
            tt = res0.end_token.next0_
            while tt is not None: 
                if (not tt.is_comma_and and not tt.is_hiphen): 
                    break
                nn = NumToken.try_parse(tt.next0_, GeoTokenType.ANY)
                if (nn is None): 
                    break
                if (nn.value.find('-') > 0): 
                    nn.value = nn.value[0:0+nn.value.find('-')]
                    nn.end_token = nn.begin_token
                tok2 = AddressItemToken.__m_ontology.try_parse(nn.end_token.next0_, TerminParseAttr.NO)
                if (tok2 is not None): 
                    break
                n = 0
                wrapn245 = RefOutArgWrapper(0)
                Utils.tryParseInt(nn.value, wrapn245)
                n = wrapn245.value
                if (tt.is_hiphen): 
                    if (n > n0 and n0 > 0 and ((n - n0) < 100)): 
                        k = n0 + 1
                        while k <= n: 
                            res0.value = "{0},{1}".format(res0.value, k)
                            k += 1
                    else: 
                        break
                else: 
                    res0.value = "{0},{1}".format(res0.value, nn.value)
                res0.end_token = nn.end_token
                if (tt.is_and): 
                    break
                tt = nn.end_token
                n0 = n
                tt = tt.next0_
        if (MiscLocationHelper.is_user_param_address(res0)): 
            tt = res0.end_token.next0_
            first_pass3766 = True
            while True:
                if first_pass3766: first_pass3766 = False
                else: tt = tt.next0_
                if (not (tt is not None)): break
                if (tt.is_value("СОГЛАСНО", None) or tt.is_value("ПО", None) or tt.length_char == 1): 
                    continue
                if (tt.is_value("ПЛ", None) or tt.is_value("БТИ", None)): 
                    res0.end_token = tt
                    continue
                npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.PARSEPREPOSITION, 0, None)
                if (npt is None): 
                    break
                if ((npt.end_token.is_value("ПЛАН", None) or npt.end_token.is_value("ПРОЕКТ", None) or npt.end_token.is_value("КОПИЯ", None)) or npt.end_token.is_value("ПАСПОРТ", None)): 
                    tt = npt.end_token
                    res0.end_token = tt
                    continue
                break
        return res0
    
    def __corr_num(self) -> None:
        if (self.end_token.is_char(')')): 
            return
        t1 = self.end_token.next0_
        if (t1 is not None and t1.is_hiphen): 
            t1 = t1.next0_
        if (t1 is None): 
            return
        if (((t1.is_char_of("\\/") or t1.is_hiphen)) and t1.next0_ is not None): 
            t1 = t1.next0_
        if (self.typ == AddressItemType.SPACE or self.typ == AddressItemType.NUMBER): 
            tok2 = AddressItemToken.__m_ontology.try_parse(t1, TerminParseAttr.NO)
            if (tok2 is None and t1 is not None and t1.is_char('(')): 
                tok2 = AddressItemToken.__m_ontology.try_parse(t1.next0_, TerminParseAttr.NO)
                if (tok2 is not None and tok2.end_token.next0_ is not None and tok2.end_token.next0_.is_char(')')): 
                    tok2.end_token = tok2.end_token.next0_
                else: 
                    tok2 = (None)
            if (tok2 is not None and tok2.termin.tag is not None and (Utils.valToEnum(tok2.termin.tag, AddressItemType)) == AddressItemType.SPACE): 
                self.end_token = tok2.end_token
                self.typ = AddressItemType.SPACE
                if (tok2.termin.tag2 is not None and self.detail_param is None): 
                    self.detail_param = tok2.termin.canonic_text
                    if (len(self.detail_param) > 4): 
                        self.detail_param = self.detail_param.lower()
                if (tok2.begin_token != t1 and self.end_token.next0_ is not None and self.end_token.next0_.is_char(')')): 
                    self.end_token = self.end_token.next0_
                t1 = self.end_token.next0_
            if (isinstance(t1, TextToken)): 
                vv = t1.term
                if (vv == "НЧ" or vv == "Н" or vv == "H"): 
                    self.value += "Н"
                    self.end_token = t1
            if (self.typ == AddressItemType.SPACE and self.value is not None and self.value.endswith("Н")): 
                self.detail_param = "нежилое"
                self.value = self.value[0:0+len(self.value) - 1]
                if (len(self.value) == 0): 
                    self.value = "0"
        elif ((self.typ == AddressItemType.HOUSE or self.typ == AddressItemType.BUILDING or self.typ == AddressItemType.CORPUS) or self.typ == AddressItemType.PLOT): 
            if (isinstance(t1, TextToken)): 
                vv = t1.term
                if (vv == "ОБЩ" or vv == "ГЛФ" or vv == "СХ"): 
                    self.end_token = t1
    
    @staticmethod
    def __try_attachvch(t : 'Token', ty : 'AddressItemType') -> 'AddressItemToken':
        if (t is None): 
            return None
        tt = t
        if ((((tt.is_value("В", None) or tt.is_value("B", None))) and tt.next0_ is not None and tt.next0_.is_char_of("./\\")) and (isinstance(tt.next0_.next0_, TextToken)) and tt.next0_.next0_.is_value("Ч", None)): 
            tt = tt.next0_.next0_
            if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                tt = tt.next0_
            tt2 = MiscHelper.check_number_prefix(tt.next0_)
            if (tt2 is not None): 
                tt = tt2
            if (tt.next0_ is not None and (isinstance(tt.next0_, NumberToken)) and (tt.whitespaces_after_count < 2)): 
                tt = tt.next0_
            return AddressItemToken._new191(ty, t, tt, "В/Ч")
        if (((tt.is_value("ВОЙСКОВОЙ", None) or tt.is_value("ВОИНСКИЙ", None))) and tt.next0_ is not None and tt.next0_.is_value("ЧАСТЬ", None)): 
            tt = tt.next0_
            tt2 = MiscHelper.check_number_prefix(tt.next0_)
            if (tt2 is not None): 
                tt = tt2
            if (tt.next0_ is not None and (isinstance(tt.next0_, NumberToken)) and (tt.whitespaces_after_count < 2)): 
                tt = tt.next0_
            return AddressItemToken._new191(ty, t, tt, "В/Ч")
        if (ty == AddressItemType.FLAT or ty == AddressItemType.SPACE): 
            if (tt.whitespaces_before_count > 1): 
                return None
            if (not (isinstance(tt, TextToken))): 
                return None
            if (tt.term.startswith("ОБЩ") or tt.term.startswith("ВЕД") or tt.term.startswith("МОП")): 
                if (tt.next0_ is not None and tt.next0_.is_char('.')): 
                    tt = tt.next0_
                re = AddressItemToken.__try_attachvch(tt.next0_, ty)
                if (re is not None): 
                    return re
                return AddressItemToken._new191(ty, t, tt, "0")
            if (tt.chars.is_all_upper and tt.length_char > 1): 
                if (NumberHelper.try_parse_roman(tt) is None): 
                    re = AddressItemToken._new191(ty, t, tt, tt.term)
                    if ((tt.whitespaces_after_count < 2) and (isinstance(tt.next0_, TextToken)) and tt.next0_.chars.is_all_upper): 
                        tt = tt.next0_
                        re.end_token = tt
                        re.value += tt.term
                    return re
        return None
    
    @staticmethod
    def __out_doube_km(n1 : 'NumberToken', n2 : 'NumberToken') -> str:
        if (n1.int_value is None or n2.int_value is None): 
            return "{0}+{1}".format(n1.value, n2.value)
        v = n1.real_value + ((n2.real_value / (1000)))
        return NumberHelper.double_to_string(round(v, 3))
    
    @staticmethod
    def __try_attach_detail_range(t : 'Token') -> 'AddressItemToken':
        t1 = t.next0_
        if (t1 is not None and t1.is_char('.')): 
            t1 = t1.next0_
        if (not (isinstance(t1, NumberToken))): 
            return None
        if (t1.next0_ is None or not t1.next0_.is_char('+') or not (isinstance(t1.next0_.next0_, NumberToken))): 
            return None
        res = AddressItemToken._new251(AddressItemType.DETAIL, t, t1.next0_.next0_, AddressDetailType.RANGE)
        res.value = "км{0}".format(AddressItemToken.__out_doube_km(Utils.asObjectOrNull(t1, NumberToken), Utils.asObjectOrNull(t1.next0_.next0_, NumberToken)))
        t1 = t1.next0_.next0_.next0_
        if (t1 is not None and t1.is_hiphen): 
            t1 = t1.next0_
        if (t1 is not None and t1.is_value("КМ", None)): 
            t1 = t1.next0_
            if (t1 is not None and t1.is_char('.')): 
                t1 = t1.next0_
        if (not (isinstance(t1, NumberToken))): 
            return None
        if (t1.next0_ is None or not t1.next0_.is_char('+') or not (isinstance(t1.next0_.next0_, NumberToken))): 
            return None
        res.value = "{0}-км{1}".format(res.value, AddressItemToken.__out_doube_km(Utils.asObjectOrNull(t1, NumberToken), Utils.asObjectOrNull(t1.next0_.next0_, NumberToken)))
        res.end_token = t1.next0_.next0_
        return res
    
    @staticmethod
    def __try_attach_detail(t : 'Token', tok : 'TerminToken') -> 'AddressItemToken':
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        if (t is None or (isinstance(t, ReferentToken))): 
            return None
        if (t.is_value("КМ", None)): 
            ran = AddressItemToken.__try_attach_detail_range(t)
            if (ran is not None): 
                return ran
        tt = t
        if (t.chars.is_capital_upper and not t.morph.class0_.is_preposition): 
            return None
        if (tok is None): 
            tok = AddressItemToken.__m_ontology.try_parse(t, TerminParseAttr.NO)
        if (tok is None and t.morph.class0_.is_preposition and t.next0_ is not None): 
            tt = t.next0_
            if (isinstance(tt, NumberToken)): 
                pass
            else: 
                if (tt.chars.is_capital_upper and not tt.morph.class0_.is_preposition): 
                    return None
                tok = AddressItemToken.__m_ontology.try_parse(tt, TerminParseAttr.NO)
        res = None
        first_num = False
        if (tok is not None and tok.termin.tag2 is not None and (isinstance(tok.termin.tag, AddressDetailType))): 
            res = AddressItemToken(AddressItemType.DETAIL, t, tok.end_token)
            res.detail_type = (Utils.valToEnum(tok.termin.tag, AddressDetailType))
            res.detail_param = "часть"
            return res
        if (tok is None): 
            mc = tt.get_morph_class_in_dictionary()
            if (mc.is_verb): 
                next0__ = AddressItemToken.__try_attach_detail(tt.next0_, tok)
                if (next0__ is not None): 
                    next0__.begin_token = t
                    return next0__
            if (isinstance(tt, NumberToken)): 
                first_num = True
                nex = NumberHelper.try_parse_number_with_postfix(tt)
                if (nex is not None and ((nex.ex_typ == NumberExType.METER or nex.ex_typ == NumberExType.KILOMETER))): 
                    res = AddressItemToken(AddressItemType.DETAIL, t, nex.end_token)
                    tyy = NumberExType.METER
                    wraptyy252 = RefOutArgWrapper(tyy)
                    res.detail_meters = (math.floor(nex.normalize_value(wraptyy252)))
                    tyy = wraptyy252.value
                    tt2 = res.end_token.next0_
                    if (tt2 is not None and tt2.is_hiphen): 
                        tt2 = tt2.next0_
                    nex2 = NumberHelper.try_parse_number_with_postfix(tt2)
                    if (nex2 is not None and nex2.ex_typ == NumberExType.METER and nex2.int_value is not None): 
                        res.end_token = nex2.end_token
                        res.detail_meters += nex2.int_value
            if (res is None): 
                return None
        else: 
            if (not (isinstance(tok.termin.tag, AddressDetailType))): 
                return None
            if (t.is_value("У", None)): 
                if (t.next0_ is None or t.next0_.is_char_of(",.;")): 
                    return None
            res = AddressItemToken._new251(AddressItemType.DETAIL, t, tok.end_token, Utils.valToEnum(tok.termin.tag, AddressDetailType))
        tt = res.end_token.next0_
        first_pass3767 = True
        while True:
            if first_pass3767: first_pass3767 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (isinstance(tt, ReferentToken)): 
                break
            if (not tt.morph.class0_.is_preposition): 
                if (tt.chars.is_capital_upper or tt.chars.is_all_upper): 
                    break
            tok = AddressItemToken.__m_ontology.try_parse(tt, TerminParseAttr.NO)
            if (tok is not None and (isinstance(tok.termin.tag, AddressDetailType))): 
                ty = Utils.valToEnum(tok.termin.tag, AddressDetailType)
                if (ty != AddressDetailType.UNDEFINED): 
                    if (ty == AddressDetailType.NEAR and res.detail_type != AddressDetailType.UNDEFINED and res.detail_type != ty): 
                        pass
                    else: 
                        res.detail_type = ty
                tt = tok.end_token
                res.end_token = tt
                continue
            npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
            if (npt is not None): 
                tt = npt.end_token
            if (((tt.is_value("ОРИЕНТИР", None) or tt.is_value("НАПРАВЛЕНИЕ", None) or tt.is_value("ОТ", None)) or tt.is_value("В", None) or tt.is_value("УСАДЬБА", None)) or tt.is_value("ДВОР", None)): 
                res.end_token = tt
                continue
            if (tt.is_value("ЗДАНИЕ", None) or tt.is_value("СТРОЕНИЕ", None) or tt.is_value("ДОМ", None)): 
                ait = AddressItemToken.try_parse_pure_item(tt, None, None)
                if (ait is not None and ait.value is not None): 
                    break
                if (OrgItemToken.try_parse(tt.next0_, None) is not None): 
                    break
                res.end_token = tt
                continue
            if (npt is not None and npt.internal_noun is not None): 
                tt = npt.end_token
                res.end_token = tt
                continue
            if (((tt.is_value("ГРАНИЦА", None) or tt.is_value("ПРЕДЕЛ", None))) and tt.next0_ is not None): 
                if (tt.next0_.is_value("УЧАСТОК", None)): 
                    tt = tt.next0_
                    res.end_token = tt
                    continue
            mc = tt.get_morph_class_in_dictionary()
            if (mc.is_verb and not mc.is_noun): 
                continue
            if ((tt.is_comma or mc.is_preposition or tt.is_hiphen) or tt.is_char(':')): 
                continue
            if ((isinstance(tt, NumberToken)) and tt.next0_ is not None): 
                nex = NumberHelper.try_parse_number_with_postfix(tt)
                if (nex is not None and ((nex.ex_typ == NumberExType.METER or nex.ex_typ == NumberExType.KILOMETER))): 
                    tt = nex.end_token
                    res.end_token = tt
                    tyy = NumberExType.METER
                    wraptyy254 = RefOutArgWrapper(tyy)
                    res.detail_meters = (math.floor(nex.normalize_value(wraptyy254)))
                    tyy = wraptyy254.value
                    continue
            break
        if (first_num and res.detail_type == AddressDetailType.UNDEFINED): 
            return None
        if (res is not None and res.end_token.next0_ is not None and res.end_token.next0_.morph.class0_.is_preposition): 
            if (res.end_token.whitespaces_after_count == 1 and res.end_token.next0_.whitespaces_after_count == 1): 
                res.end_token = res.end_token.next0_
        if (res is not None and res.end_token.next0_ is not None): 
            if (res.end_token.next0_.is_hiphen or res.end_token.next0_.is_char(':')): 
                res.end_token = res.end_token.next0_
        return res
    
    @staticmethod
    def try_parse_list(t : 'Token', max_count : int=20) -> typing.List['AddressItemToken']:
        if (t is None): 
            return None
        ad = GeoAnalyzer._get_data(t)
        if (ad is not None): 
            if (ad.level > 0): 
                return None
            ad.level += 1
        res = AddressItemToken.__try_parse_list_int(t, max_count)
        if (ad is not None): 
            ad.level -= 1
        if (res is not None and len(res) == 0): 
            return None
        return res
    
    @staticmethod
    def __try_parse_list_int(t : 'Token', max_count : int=20) -> typing.List['AddressItemToken']:
        from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
        from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        if (isinstance(t, NumberToken)): 
            if (t.int_value is None): 
                return None
            v = t.int_value
            if ((v < 100000) or v >= 10000000): 
                if (t.typ == NumberSpellingType.DIGIT and not t.morph.class0_.is_adjective): 
                    if (t.next0_ is None or (isinstance(t.next0_, NumberToken))): 
                        if (t.previous is None or not t.previous.morph.class0_.is_preposition): 
                            return None
        it = AddressItemToken.try_parse(t, False, None, None)
        if (it is None): 
            return None
        if (it.typ == AddressItemType.NUMBER): 
            return None
        if (it.detail_type == AddressDetailType.ORG or ((it.is_house and it.value == "0"))): 
            if (not MiscLocationHelper.is_user_param_address(it)): 
                return None
        if (it.typ == AddressItemType.KILOMETER and (isinstance(it.begin_token.previous, NumberToken))): 
            it = it.clone()
            it.begin_token = it.begin_token.previous
            it.value = str(it.begin_token.value)
            if (it.begin_token.previous is not None and it.begin_token.previous.morph.class0_.is_preposition): 
                it.begin_token = it.begin_token.previous
        if (it.typ == AddressItemType.STREET and it.ref_token is not None and not MiscLocationHelper.is_user_param_address(it)): 
            return None
        res = list()
        res.append(it)
        while it.alt_typ is not None:
            res.append(it.alt_typ)
            it = it.alt_typ
        pref = it.typ == AddressItemType.PREFIX
        t = it.end_token.next0_
        first_pass3768 = True
        while True:
            if first_pass3768: first_pass3768 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (max_count > 0 and len(res) >= max_count): 
                break
            last = res[len(res) - 1]
            if (len(res) > 1): 
                if (last.is_newline_before and res[len(res) - 2].typ != AddressItemType.PREFIX): 
                    i = 0
                    i = 0
                    first_pass3769 = True
                    while True:
                        if first_pass3769: first_pass3769 = False
                        else: i += 1
                        if (not (i < (len(res) - 1))): break
                        if (res[i].typ == last.typ): 
                            if (i == (len(res) - 2) and ((last.typ == AddressItemType.CITY or last.typ == AddressItemType.REGION))): 
                                jj = 0
                                jj = 0
                                while jj < i: 
                                    if ((res[jj].typ != AddressItemType.PREFIX and res[jj].typ != AddressItemType.ZIP and res[jj].typ != AddressItemType.REGION) and res[jj].typ != AddressItemType.COUNTRY): 
                                        break
                                    jj += 1
                                if (jj >= i): 
                                    continue
                            break
                    if ((i < (len(res) - 1)) or last.typ == AddressItemType.ZIP): 
                        res.remove(last)
                        break
            if (t.is_table_control_char): 
                break
            if (t.is_char(',') or t.is_char('|')): 
                continue
            if (t.is_value("ДУБЛЬ", None)): 
                continue
            if (t.is_char_of("\\/")): 
                if (t.is_newline_before or t.is_newline_after): 
                    break
                if (t.previous is not None and t.previous.is_comma): 
                    continue
                if (last.typ == AddressItemType.STREET and last.is_doubt): 
                    break
                it = AddressItemToken._new251(AddressItemType.DETAIL, t, t, AddressDetailType.CROSS)
                res.append(it)
                continue
            if (t.is_char(':') and MiscLocationHelper.is_user_param_address(t)): 
                continue
            if (t.is_char(';') and MiscLocationHelper.is_user_param_address(t) and not MiscLocationHelper.is_user_param_gar_address(t)): 
                continue
            if (BracketHelper.is_bracket(t, False) and t.next0_ is not None and t.next0_.is_comma): 
                continue
            if (t.is_char('.')): 
                if (MiscLocationHelper.is_user_param_address(t)): 
                    continue
                if (t.is_newline_after): 
                    if (last.typ == AddressItemType.CITY): 
                        next0__ = AddressItemToken.try_parse(t.next0_, False, None, None)
                        if (next0__ is not None and next0__.typ == AddressItemType.STREET): 
                            continue
                    break
                if (t.previous is not None and t.previous.is_char('.')): 
                    if (t.previous.previous is not None and t.previous.previous.is_char('.')): 
                        break
                continue
            if (t.is_hiphen or t.is_char('_')): 
                if (((it.typ == AddressItemType.NUMBER or it.typ == AddressItemType.STREET)) and (isinstance(t.next0_, NumberToken))): 
                    continue
                if (MiscLocationHelper.is_user_param_address(it)): 
                    continue
                if (it.typ == AddressItemType.CITY): 
                    continue
            if (it.typ == AddressItemType.DETAIL and it.detail_type == AddressDetailType.CROSS): 
                str1 = AddressItemToken.try_parse(t, True, None, None)
                if (str1 is not None and str1.typ == AddressItemType.STREET): 
                    if (str1.end_token.next0_ is not None and ((str1.end_token.next0_.is_and or str1.end_token.next0_.is_hiphen))): 
                        str2 = AddressItemToken.try_parse(str1.end_token.next0_.next0_, True, None, None)
                        if (str2 is None or str2.typ != AddressItemType.STREET): 
                            str2 = StreetDefineHelper._try_parse_second_street(str1.begin_token, str1.end_token.next0_.next0_)
                            if (str2 is not None and str2.is_doubt): 
                                str2 = str2.clone()
                                str2.is_doubt = False
                        if (str2 is not None and str2.typ == AddressItemType.STREET): 
                            res.append(str1)
                            res.append(str2)
                            t = str2.end_token
                            it = str2
                            continue
            pre = pref
            if (it.typ == AddressItemType.KILOMETER or ((it.typ == AddressItemType.HOUSE and it.value is not None and ((len(res) == 1 or res[len(res) - 2].typ != AddressItemType.STREET))))): 
                if (not t.is_newline_before): 
                    pre = True
            it0 = AddressItemToken.try_parse(t, pre, it, None)
            if (it0 is None): 
                hous = False
                wraphous257 = RefOutArgWrapper(False)
                tt = AddressItemToken.goto_end_of_address(t.previous, wraphous257)
                hous = wraphous257.value
                if (tt is not None and tt.end_char >= t.end_char and tt.next0_ is not None): 
                    if (tt.next0_.is_comma): 
                        tt = tt.next0_
                    it0 = AddressItemToken.try_parse(tt.next0_, pre, it, None)
                    if (it0 is None and hous and it.typ == AddressItemType.STREET): 
                        res.append(AddressItemToken._new191(AddressItemType.HOUSE, t, tt, "0"))
                if (it.typ == AddressItemType.CITY): 
                    sit = StreetItemToken.try_parse(t, None, False, None)
                    if (sit is not None and sit.typ == StreetItemType.NOUN and sit.termin.canonic_text == "УЛИЦА"): 
                        if (AddressItemToken.check_house_after(sit.end_token.next0_, False, False)): 
                            t = sit.end_token
                            continue
            if (it0 is None and t.get_morph_class_in_dictionary().is_preposition and (t.whitespaces_after_count < 3)): 
                it0 = AddressItemToken.try_parse(t.next0_, pre, it, None)
                if (it0 is not None): 
                    if (it0.typ == AddressItemType.NUMBER): 
                        it0 = (None)
                    elif (it0.typ == AddressItemType.BUILDING and t.next0_.is_value("СТ", None)): 
                        it0 = (None)
                    else: 
                        it0 = it0.clone()
                        it0.begin_token = t
            if (it0 is None): 
                if (BracketHelper.can_be_end_of_sequence(t, True, None, False) and last.typ == AddressItemType.STREET): 
                    continue
                if (t.is_char_of("\\/") and last.typ == AddressItemType.STREET): 
                    continue
            if (((it0 is None and t.is_char('(') and (isinstance(t.next0_, ReferentToken))) and (isinstance(t.next0_.get_referent(), GeoReferent)) and t.next0_.next0_ is not None) and t.next0_.next0_.is_char(')')): 
                it0 = AddressItemToken.try_parse(t.next0_, pre, it, None)
                if (it0 is not None): 
                    it0 = it0.clone()
                    it0.begin_token = t
                    it0.end_token = it0.end_token.next0_
                    geo0 = Utils.asObjectOrNull(t.next0_.get_referent(), GeoReferent)
                    if (geo0.higher is None): 
                        for kk in range(len(res) - 1, -1, -1):
                            if (res[kk].typ == AddressItemType.CITY and (isinstance(res[kk].referent, GeoReferent))): 
                                if (GeoOwnerHelper.can_be_higher(Utils.asObjectOrNull(res[kk].referent, GeoReferent), geo0, None, None) or ((geo0.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None and res[kk].referent.find_slot(GeoReferent.ATTR_TYPE, "город", True) is not None))): 
                                    geo0.higher = Utils.asObjectOrNull(res[kk].referent, GeoReferent)
                                    break
            if (it0 is None): 
                if (t.newlines_before_count > 2): 
                    break
                if (it.typ == AddressItemType.POSTOFFICEBOX): 
                    break
                if (t.is_hiphen and t.next0_ is not None and t.next0_.is_comma): 
                    continue
                if (t.is_hiphen and (isinstance(t.next0_, NumberToken)) and MiscLocationHelper.is_user_param_address(t)): 
                    continue
                if (t.is_value("НЕТ", None) or t.is_value("ТЕР", None) or t.is_value("ТЕРРИТОРИЯ", None)): 
                    continue
                if (MiscLocationHelper.is_user_param_address(t)): 
                    if ((t.is_value("РАСПОЛОЖЕННЫЙ", None) or t.is_value("НЕЖИЛОЙ", None) or t.is_value("ЗДАНИЕ", None)) or t.is_value("ЧАСТЬ", None)): 
                        continue
                    if (((t.is_value("ПЛ", None) or t.is_value("ПЛОЩАДЬ", None) or t.is_value("ПЛОЩ", None))) and t.next0_ is not None): 
                        nn = NumberHelper.try_parse_number_with_postfix((t.next0_ if isinstance(t.next0_, NumberToken) else t.next0_.next0_))
                        if (nn is not None and nn.ex_typ == NumberExType.METER2): 
                            t = nn.end_token
                            continue
                tt1 = StreetItemToken.check_std_name(t)
                if (tt1 is not None): 
                    t = tt1
                    continue
                if (t.morph.class0_.is_preposition): 
                    it0 = AddressItemToken.try_parse(t.next0_, False, it, None)
                    if (it0 is not None and it0.typ == AddressItemType.BUILDING and it0.begin_token.is_value("СТ", None)): 
                        it0 = (None)
                        break
                    if (it0 is not None): 
                        if ((it0.typ == AddressItemType.DETAIL and it.typ == AddressItemType.CITY and it.detail_meters > 0) and it.detail_type == AddressDetailType.UNDEFINED): 
                            it.detail_type = it0.detail_type
                            it.end_token = it0.end_token
                            t = it.end_token
                            continue
                        if ((it0.typ == AddressItemType.HOUSE or it0.typ == AddressItemType.BUILDING or it0.typ == AddressItemType.CORPUS) or it0.typ == AddressItemType.STREET or it0.typ == AddressItemType.DETAIL): 
                            it = it0
                            res.append(it)
                            t = it.end_token
                            continue
                if (it.typ == AddressItemType.HOUSE or it.typ == AddressItemType.BUILDING or it.typ == AddressItemType.NUMBER): 
                    if ((not t.is_whitespace_before and t.length_char == 1 and t.chars.is_letter) and not t.is_whitespace_after and (isinstance(t.next0_, NumberToken))): 
                        ch = AddressItemToken.__correct_char_token(t)
                        if (ch == "К" or ch == "С"): 
                            it0 = AddressItemToken._new191((AddressItemType.CORPUS if ch == "К" else AddressItemType.BUILDING), t, t.next0_, str(t.next0_.value))
                            it = it0
                            res.append(it)
                            t = it.end_token
                            tt = t.next0_
                            if (((tt is not None and not tt.is_whitespace_before and tt.length_char == 1) and tt.chars.is_letter and not tt.is_whitespace_after) and (isinstance(tt.next0_, NumberToken))): 
                                ch = AddressItemToken.__correct_char_token(tt)
                                if (ch == "К" or ch == "С"): 
                                    it = AddressItemToken._new191((AddressItemType.CORPUS if ch == "К" else AddressItemType.BUILDING), tt, tt.next0_, str(tt.next0_.value))
                                    res.append(it)
                                    t = it.end_token
                            continue
                if (t.morph.class0_.is_preposition): 
                    if ((((t.is_value("У", None) or t.is_value("ВОЗЛЕ", None) or t.is_value("НАПРОТИВ", None)) or t.is_value("НА", None) or t.is_value("В", None)) or t.is_value("ВО", None) or t.is_value("ПО", None)) or t.is_value("ОКОЛО", None)): 
                        if (it0 is not None and it0.typ == AddressItemType.NUMBER): 
                            break
                        continue
                if (t.morph.class0_.is_noun): 
                    if ((t.is_value("ДВОР", None) or t.is_value("ПОДЪЕЗД", None) or t.is_value("КРЫША", None)) or t.is_value("ПОДВАЛ", None)): 
                        continue
                if (t.is_value("ТЕРРИТОРИЯ", "ТЕРИТОРІЯ")): 
                    continue
                if (t.is_char('(') and t.next0_ is not None): 
                    it0 = AddressItemToken.try_parse(t.next0_, pre, None, None)
                    if (it0 is not None and it0.end_token.next0_ is not None and it0.end_token.next0_.is_char(')')): 
                        it0 = it0.clone()
                        it0.begin_token = t
                        it0.end_token = it0.end_token.next0_
                        it = it0
                        res.append(it)
                        t = it.end_token
                        continue
                    li0 = AddressItemToken.__try_parse_list_int(t.next0_, 3)
                    if ((li0 is not None and len(li0) > 1 and li0[0].typ != AddressItemType.DETAIL) and li0[len(li0) - 1].end_token.next0_ is not None and li0[len(li0) - 1].end_token.next0_.is_char(')')): 
                        li0[0] = li0[0].clone()
                        li0[0].begin_token = t
                        li0[len(li0) - 1] = li0[len(li0) - 1].clone()
                        li0[len(li0) - 1].end_token = li0[len(li0) - 1].end_token.next0_
                        res.extend(li0)
                        it = li0[len(li0) - 1]
                        t = it.end_token
                        continue
                    br = BracketHelper.try_parse(t, BracketParseAttr.NO, 100)
                    if (br is not None and (br.length_char < 100)): 
                        if (t.next0_.is_value("БЫВШИЙ", None) or t.next0_.is_value("БЫВШ", None)): 
                            it = AddressItemToken(AddressItemType.DETAIL, t, br.end_token)
                            res.append(it)
                        t = br.end_token
                        continue
                check_kv = False
                if (t.is_value("КВ", None) or t.is_value("KB", None)): 
                    if (it.typ == AddressItemType.NUMBER and len(res) > 1 and res[len(res) - 2].typ == AddressItemType.STREET): 
                        check_kv = True
                    elif ((it.typ == AddressItemType.HOUSE or it.typ == AddressItemType.BUILDING or it.typ == AddressItemType.CORPUS) or it.typ == AddressItemType.CORPUSORFLAT): 
                        for jj in range(len(res) - 2, -1, -1):
                            if (res[jj].typ == AddressItemType.STREET or res[jj].typ == AddressItemType.CITY): 
                                check_kv = True
                    if (check_kv): 
                        tt2 = t.next0_
                        if (tt2 is not None and tt2.is_char('.')): 
                            tt2 = tt2.next0_
                        it22 = AddressItemToken.try_parse_pure_item(tt2, None, None)
                        if (it22 is not None and it22.typ == AddressItemType.NUMBER): 
                            it22 = it22.clone()
                            it22.begin_token = t
                            it22.typ = AddressItemType.FLAT
                            res.append(it22)
                            t = it22.end_token
                            continue
                if (res[len(res) - 1].typ == AddressItemType.CITY): 
                    if (((t.is_hiphen or t.is_char('_') or t.is_value("НЕТ", None))) and t.next0_ is not None and t.next0_.is_comma): 
                        att = AddressItemToken.try_parse_pure_item(t.next0_.next0_, None, None)
                        if (att is not None): 
                            if (att.typ == AddressItemType.HOUSE or att.typ == AddressItemType.BUILDING or att.typ == AddressItemType.CORPUS): 
                                it = AddressItemToken(AddressItemType.STREET, t, t)
                                res.append(it)
                                continue
                if (t.length_char == 2 and (isinstance(t, TextToken)) and t.chars.is_all_upper): 
                    term = t.term
                    if (not Utils.isNullOrEmpty(term) and term[0] == 'Р'): 
                        continue
                break
            if (t.whitespaces_before_count > 15): 
                if (it0.typ == AddressItemType.STREET and last.typ == AddressItemType.CITY): 
                    pass
                else: 
                    break
            if (t.is_newline_before and it0.typ == AddressItemType.STREET and it0.ref_token is not None): 
                if (not it0.ref_token_is_gsk): 
                    break
            if (it0.typ == AddressItemType.STREET and t.is_value("КВ", None)): 
                if (it is not None): 
                    if (it.typ == AddressItemType.HOUSE or it.typ == AddressItemType.BUILDING or it.typ == AddressItemType.CORPUS): 
                        it2 = AddressItemToken.try_parse_pure_item(t, None, None)
                        if (it2 is not None and it2.typ == AddressItemType.FLAT): 
                            it0 = it2
            if (it0.typ == AddressItemType.PREFIX): 
                break
            if (it0.typ == AddressItemType.NUMBER): 
                if (Utils.isNullOrEmpty(it0.value)): 
                    break
                if (not str.isdigit(it0.value[0])): 
                    break
                if (it0.is_newline_before and not MiscLocationHelper.is_user_param_address(it0) and res[len(res) - 1].typ != AddressItemType.STREET): 
                    break
                if (it0.begin_token.is_value("НОМЕР", None)): 
                    pass
                else: 
                    cou = 0
                    for i in range(len(res) - 1, -1, -1):
                        if (res[i].typ == AddressItemType.NUMBER): 
                            cou += 1
                        else: 
                            break
                    if (cou > 5): 
                        break
                    if (it.is_doubt and t.is_newline_before): 
                        break
            if (it0.typ == AddressItemType.CORPUSORFLAT and it is not None and it.typ == AddressItemType.FLAT): 
                it0.typ = AddressItemType.ROOM
            if ((it0.alt_typ is None and (((it0.typ == AddressItemType.FLOOR or it0.typ == AddressItemType.POTCH or it0.typ == AddressItemType.BLOCK) or it0.typ == AddressItemType.KILOMETER)) and Utils.isNullOrEmpty(it0.value)) and it.typ == AddressItemType.NUMBER and it.end_token.next0_ == it0.begin_token): 
                it = it.clone()
                res[len(res) - 1] = it
                it.typ = it0.typ
                it.end_token = it0.end_token
            elif ((it0.alt_typ is None and ((it.typ == AddressItemType.FLOOR or it.typ == AddressItemType.POTCH)) and Utils.isNullOrEmpty(it.value)) and it0.typ == AddressItemType.NUMBER and it.end_token.next0_ == it0.begin_token): 
                it = it.clone()
                res[len(res) - 1] = it
                it.value = it0.value
                it.end_token = it0.end_token
            else: 
                it = it0
                res.append(it)
                while it.alt_typ is not None:
                    res.append(it.alt_typ)
                    it = it.alt_typ
            t = it.end_token
        if ((len(res) > 1 and res[0].typ == AddressItemType.DETAIL and res[0].detail_type == AddressDetailType.CROSS) and res[1].typ != AddressItemType.STREET): 
            return None
        if (len(res) > 0): 
            it = res[len(res) - 1]
            it0 = (res[len(res) - 2] if len(res) > 1 else None)
            if (it.typ == AddressItemType.NUMBER and it0 is not None and it0.ref_token is not None): 
                for s in it0.ref_token.referent.slots: 
                    if (s.type_name == "TYPE"): 
                        ss = Utils.asObjectOrNull(s.value, str)
                        if ("гараж" in ss or ((ss[0] == 'Г' and ss[len(ss) - 1] == 'К'))): 
                            if (it0.ref_token.referent.find_slot("NAME", "РОСАТОМ", True) is not None): 
                                break
                            it.typ = AddressItemType.BOX
                            break
            if (it.typ == AddressItemType.NUMBER or it.typ == AddressItemType.ZIP): 
                del0_ = False
                if (it.begin_token.previous is not None and it.begin_token.previous.morph.class0_.is_preposition): 
                    del0_ = True
                elif (it.morph.class0_.is_noun and not MiscLocationHelper.is_user_param_address(it)): 
                    del0_ = True
                if ((not del0_ and it.end_token.whitespaces_after_count == 1 and it.whitespaces_before_count > 0) and it.typ == AddressItemType.NUMBER): 
                    npt = MiscLocationHelper._try_parse_npt(it.end_token.next0_)
                    if (npt is not None): 
                        del0_ = True
                if (del0_): 
                    del res[len(res) - 1]
                elif ((it.typ == AddressItemType.NUMBER and it0 is not None and it0.typ == AddressItemType.STREET) and it0.ref_token is None): 
                    if (it.begin_token.previous.is_char(',') or it.is_newline_after): 
                        it = it.clone()
                        res[len(res) - 1] = it
                        it.typ = AddressItemType.HOUSE
                        it.is_doubt = True
        if (len(res) == 0): 
            return None
        if ((len(res) == 1 and res[0].typ == AddressItemType.STREET and res[0].chars.is_latin_letter) and not MiscLocationHelper.is_user_param_address(res[0])): 
            return None
        for r in res: 
            if (r.typ == AddressItemType.CITY or r.typ == AddressItemType.STREET): 
                ty = AddressItemToken.__find_addr_typ(r.begin_token, r.end_char, 0)
                if (ty is not None): 
                    if (r.detail_type == AddressDetailType.UNDEFINED): 
                        r.detail_type = ty.detail_type
                    if (ty.detail_meters > 0): 
                        r.detail_meters = ty.detail_meters
                    if (ty.detail_param is not None): 
                        r.detail_param = ty.detail_param
        i = 0
        while i < (len(res) - 2): 
            if (res[i].typ == AddressItemType.STREET and res[i + 1].typ == AddressItemType.NUMBER): 
                if ((res[i + 2].typ == AddressItemType.BUILDING or res[i + 2].typ == AddressItemType.CORPUS or res[i + 2].typ == AddressItemType.OFFICE) or res[i + 2].typ == AddressItemType.FLAT): 
                    res[i + 1] = res[i + 1].clone()
                    res[i + 1].typ = AddressItemType.HOUSE
            i += 1
        i = 0
        first_pass3770 = True
        while True:
            if first_pass3770: first_pass3770 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if (res[i].typ == AddressItemType.STREET and res[i + 1].typ == AddressItemType.CITY and (isinstance(res[i].referent, StreetReferent))): 
                sr = Utils.asObjectOrNull(res[i].referent, StreetReferent)
                if (len(sr.slots) != 2 or sr.kind != StreetKind.AREA or len(sr.typs) != 1): 
                    continue
                if (i == 0 and MiscLocationHelper.is_user_param_address(res[0])): 
                    pass
                elif (i > 0 and res[i - 1].typ == AddressItemType.CITY): 
                    pass
                else: 
                    continue
                tt = res[i + 1].begin_token
                if (isinstance(tt, ReferentToken)): 
                    tt = tt.begin_token
                npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                if (npt is not None and npt.end_char == res[i + 1].end_char): 
                    res[i].end_token = res[i + 1].end_token
                    sr.add_slot(StreetReferent.ATTR_NAME, npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False), False, 0)
                    del res[i + 1]
                    break
        i = 0
        while i < (len(res) - 1): 
            if (res[i].typ == AddressItemType.BUILDING and res[i].begin_token == res[i].end_token and res[i].begin_token.length_char == 1): 
                if (res[i + 1].typ == AddressItemType.CITY): 
                    del res[i]
                    i -= 1
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if (res[i].typ == AddressItemType.FLAT and res[i + 1].typ == AddressItemType.STREET and (isinstance(res[i + 1].ref_token, OrgItemToken))): 
                str0_ = str(res[i + 1].ref_token).upper()
                if ("ЛЕСНИЧ" in str0_): 
                    res[i + 1].begin_token = res[i].begin_token
                    res[i + 1].referent.add_slot("NUMBER", res[i].value, False, 0)
                    del res[i]
                    break
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if ((res[i].typ == res[i + 1].typ and (((res[i].typ == AddressItemType.ROOM or res[i].typ == AddressItemType.FLAT or res[i].typ == AddressItemType.SPACE) or res[i].typ == AddressItemType.OFFICE)) and res[i].value is not None) and res[i + 1].value is not None): 
                res[i] = res[i].clone()
                if (res[i].value != res[i + 1].value): 
                    res[i].value = "{0},{1}".format(res[i].value, res[i + 1].value)
                res[i].end_token = res[i + 1].end_token
                del res[i + 1]
                i -= 1
            elif ((res[i].typ == AddressItemType.SPACE and res[i].value is not None and res[i + 1].typ == AddressItemType.BUILDING) and res[i + 1].building_type == AddressBuildingType.LITER): 
                res[i] = res[i].clone()
                res[i].value = "{0}{1}".format(res[i].value, res[i + 1].value)
                res[i].end_token = res[i + 1].end_token
                del res[i + 1]
                i -= 1
            i += 1
        i = 0
        first_pass3771 = True
        while True:
            if first_pass3771: first_pass3771 = False
            else: i += 1
            if (not (i < (len(res) - 1))): break
            if ((res[i].typ == AddressItemType.STREET and (isinstance(res[i].referent, StreetReferent)) and res[i + 1].typ == AddressItemType.STREET) and (isinstance(res[i + 1].ref_token, OrgItemToken))): 
                ss = Utils.asObjectOrNull(res[i].referent, StreetReferent)
                if (ss.numbers is None or len(ss.names) > 0): 
                    continue
                if (not "квартал" in str(ss)): 
                    continue
                str0_ = str(res[i + 1].ref_token).upper()
                if (not "ЛЕСНИЧ" in str0_): 
                    continue
                res[i + 1].begin_token = res[i].begin_token
                res[i + 1].referent.add_slot("NUMBER", ss.numbers, False, 0)
                del res[i]
                break
        i = 0
        while i < (len(res) - 1): 
            if ((res[i].typ == AddressItemType.STREET and res[i + 1].typ == AddressItemType.KILOMETER and (isinstance(res[i].referent, StreetReferent))) and res[i].referent.numbers is None): 
                res[i] = res[i].clone()
                res[i].referent.numbers = res[i + 1].value + "км"
                res[i].end_token = res[i + 1].end_token
                del res[i + 1]
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if ((res[i + 1].typ == AddressItemType.STREET and res[i].typ == AddressItemType.KILOMETER and (isinstance(res[i + 1].referent, StreetReferent))) and res[i + 1].referent.numbers is None): 
                res[i + 1] = res[i + 1].clone()
                res[i + 1].referent.numbers = res[i].value + "км"
                res[i + 1].begin_token = res[i].begin_token
                del res[i]
                break
            i += 1
        i = 0
        while i < (len(res) - 1): 
            if (res[i].typ == AddressItemType.BUILDING and res[i + 1].typ == AddressItemType.BUILDING and (isinstance(res[i].begin_token, TextToken))): 
                if (res[i].begin_token.term.startswith("ЗД")): 
                    res[i] = res[i].clone()
                    res[i].typ = AddressItemType.HOUSE
            i += 1
        i = 0
        first_pass3772 = True
        while True:
            if first_pass3772: first_pass3772 = False
            else: i += 1
            if (not (i < len(res))): break
            if (res[i].typ == AddressItemType.PART): 
                if (i > 0 and ((res[i - 1].typ == AddressItemType.HOUSE or res[i - 1].typ == AddressItemType.PLOT))): 
                    continue
                if (((i + 1) < len(res)) and ((res[i + 1].typ == AddressItemType.HOUSE or res[i + 1].typ == AddressItemType.PLOT))): 
                    continue
                if (i == 0): 
                    return None
                del res[i:i+len(res) - i]
                break
            elif ((res[i].typ == AddressItemType.NONUMBER and i == (len(res) - 1) and i > 0) and res[i - 1].typ == AddressItemType.CITY): 
                res[i] = res[i].clone()
                res[i].typ = AddressItemType.HOUSE
        i = 0
        while i < len(res): 
            if (res[i].area_terr is not None): 
                ter = Utils.asObjectOrNull(res[i].area_terr.referent, GeoReferent)
                if ((ter.is_region and i > 0 and res[i - 1].typ == AddressItemType.CITY) and ter.higher is None): 
                    ter.higher = Utils.asObjectOrNull(res[i - 1].referent, GeoReferent)
                res.insert(i, res[i].area_terr)
                i += 1
            i += 1
        if (len(res) > 0 and MiscLocationHelper.is_user_param_address(res[0])): 
            i = 0
            while i < (len(res) - 1): 
                j = i + 1
                while j < len(res): 
                    if (res[j].is_newline_before): 
                        break
                    if (res[i].typ == res[j].typ and (isinstance(res[i].referent, GeoReferent)) and res[j].referent == res[i].referent): 
                        del res[j]
                        j -= 1
                    j += 1
                i += 1
        i = 1
        first_pass3773 = True
        while True:
            if first_pass3773: first_pass3773 = False
            else: i += 1
            if (not (i < len(res))): break
            if (res[i].typ == AddressItemType.POTCH and res[i].value is not None): 
                ok = False
                if (res[i - 1].typ == AddressItemType.STREET): 
                    ok = True
                elif (((i + 1) < len(res)) and res[i + 1].typ == AddressItemType.STREET): 
                    ok = True
                if (not ok): 
                    continue
                it = res[i]
                rr = AddressItemToken(AddressItemType.STREET, it.begin_token, it.end_token)
                sr = StreetReferent()
                sr._add_typ("подъезд")
                sr.add_slot(StreetReferent.ATTR_NUMBER, it.value, False, 0)
                rr.referent = (sr)
                res[i] = rr
        for i in range(len(res) - 1, 0, -1):
            if (res[i].typ == AddressItemType.NUMBER and res[i].value is not None and res[i].begin_token.is_value("НОМЕР", None)): 
                if (res[i - 1].typ == AddressItemType.SPACE or res[i - 1].typ == AddressItemType.FLAT): 
                    res[i].typ = AddressItemType.ROOM
                elif ((res[i - 1].typ == AddressItemType.FLOOR or res[i - 1].typ == AddressItemType.HOUSE or res[i - 1].typ == AddressItemType.CORPUS) or res[i - 1].typ == AddressItemType.BUILDING): 
                    res[i].typ = AddressItemType.FLAT
        while len(res) > 0:
            last = res[len(res) - 1]
            if (last.detail_type == AddressDetailType.ORG and not MiscLocationHelper.is_user_param_address(it)): 
                del res[len(res) - 1]
                continue
            if (last.typ == AddressItemType.DETAIL and last.detail_type == AddressDetailType.CROSS and last.length_char == 1): 
                del res[len(res) - 1]
                continue
            if (last.typ == AddressItemType.CITY and len(res) > 4): 
                ok = False
                for ii in range(3):
                    if (res[ii].typ == AddressItemType.CITY): 
                        geo1 = Utils.asObjectOrNull(last.referent, GeoReferent)
                        geo0 = Utils.asObjectOrNull(res[ii].referent, GeoReferent)
                        if ((geo1 is not None and geo0 is not None and geo0.higher is None) and GeoOwnerHelper.can_be_higher(geo1, geo0, None, None)): 
                            break
                        ok = True
                if (ok): 
                    del res[len(res) - 1]
                    continue
            if (last.typ != AddressItemType.STREET or not (isinstance(last.ref_token, OrgItemToken))): 
                break
            if (last.ref_token.is_gsk or last.ref_token.has_terr_keyword): 
                break
            if (MiscLocationHelper.is_user_param_address(last)): 
                break
            del res[len(res) - 1]
        if (len(res) > 2 and MiscLocationHelper.is_user_param_address(res[0])): 
            i = 1
            first_pass3774 = True
            while True:
                if first_pass3774: first_pass3774 = False
                else: i += 1
                if (not (i < len(res))): break
                if (((res[i - 1].typ == AddressItemType.STREET or res[i - 1].typ == AddressItemType.CITY)) and res[i].typ == AddressItemType.STREET): 
                    sr = Utils.asObjectOrNull(res[i].referent, StreetReferent)
                    if (sr is None): 
                        continue
                    if ((sr.numbers is None or len(sr.names) > 0 or len(sr.typs) != 1) or sr.typs[0] != "улица"): 
                        continue
                    if ((i + 1) < len(res)): 
                        continue
                    if (res[i - 1].typ == AddressItemType.CITY): 
                        geo = Utils.asObjectOrNull(res[i - 1].referent, GeoReferent)
                        if (geo is None): 
                            continue
                        if ("город" in geo.typs): 
                            continue
                    res[i] = res[i].clone()
                    res[i].typ = AddressItemType.HOUSE
                    res[i].value = sr.numbers
                    res[i].referent = (None)
        i = 0
        while i < (len(res) - 2): 
            if (res[i].typ == AddressItemType.REGION and res[i + 1].typ == AddressItemType.NUMBER and res[i + 2].typ == AddressItemType.CITY): 
                ok = False
                j = i + 3
                while j < len(res): 
                    if (res[j].typ == AddressItemType.STREET or res[j].value is not None): 
                        ok = True
                    j += 1
                if (ok): 
                    del res[i + 1]
                    break
            i += 1
        return res
    
    def __init__(self, typ_ : 'AddressItemType', begin : 'Token', end : 'Token') -> None:
        super().__init__(begin, end, None)
        self.__m_typ = AddressItemType.PREFIX
        self.value = None;
        self.referent = None;
        self.ref_token = None;
        self.referent2 = None;
        self.ref_token2 = None;
        self.ref_token_is_gsk = False
        self.ref_token_is_massive = False
        self.is_doubt = False
        self.is_genplan = False
        self.detail_type = AddressDetailType.UNDEFINED
        self.building_type = AddressBuildingType.UNDEFINED
        self.house_type = AddressHouseType.UNDEFINED
        self.detail_meters = 0
        self.detail_param = None;
        self.orto_terr = None;
        self.area_terr = None;
        self.alt_typ = None;
        self.typ = typ_
    
    @property
    def typ(self) -> 'AddressItemType':
        return self.__m_typ
    @typ.setter
    def typ(self, value_) -> 'AddressItemType':
        self.__m_typ = value_
        if (value_ == AddressItemType.HOUSE): 
            pass
        return value_
    
    def clone(self) -> 'AddressItemToken':
        res = AddressItemToken(self.typ, self.begin_token, self.end_token)
        res.morph = self.morph
        res.value = self.value
        res.referent = self.referent
        res.ref_token = self.ref_token
        res.referent2 = self.referent2
        res.ref_token2 = self.ref_token2
        res.ref_token_is_gsk = self.ref_token_is_gsk
        res.ref_token_is_massive = self.ref_token_is_massive
        res.is_doubt = self.is_doubt
        res.detail_type = self.detail_type
        res.building_type = self.building_type
        res.house_type = self.house_type
        res.detail_meters = self.detail_meters
        res.detail_param = self.detail_param
        res.is_genplan = self.is_genplan
        if (self.orto_terr is not None): 
            res.orto_terr = self.orto_terr.clone()
        if (self.area_terr is not None): 
            res.area_terr = self.area_terr.clone()
        if (self.alt_typ is not None): 
            res.alt_typ = self.alt_typ.clone()
        return res
    
    @property
    def is_street_road(self) -> bool:
        if (self.typ != AddressItemType.STREET): 
            return False
        if (not (isinstance(self.referent, StreetReferent))): 
            return False
        return self.referent.kind == StreetKind.ROAD
    
    @property
    def is_street_detail(self) -> bool:
        if (self.typ != AddressItemType.STREET): 
            return False
        if (not (isinstance(self.referent, StreetReferent))): 
            return False
        for s in self.referent.get_string_values("MISC"): 
            if ("бизнес" in s or "делов" in s or "офис" in s): 
                return True
        return False
    
    @property
    def is_digit(self) -> bool:
        if (self.value == "Б/Н" or self.value == "НЕТ"): 
            return True
        if (Utils.isNullOrEmpty(self.value)): 
            return False
        if (str.isdigit(self.value[0]) or self.value[0] == '-'): 
            return True
        if (len(self.value) > 1): 
            if (str.isalpha(self.value[0]) and str.isdigit(self.value[1])): 
                return True
        if (len(self.value) != 1 or not str.isalpha(self.value[0])): 
            return False
        if (not self.begin_token.chars.is_all_lower): 
            return False
        return True
    
    @property
    def is_house(self) -> bool:
        return (self.typ == AddressItemType.HOUSE or self.typ == AddressItemType.PLOT or self.typ == AddressItemType.BOX) or self.typ == AddressItemType.BUILDING or self.typ == AddressItemType.CORPUS
    
    def __str__(self) -> str:
        res = io.StringIO()
        print("{0} {1}".format(Utils.enumToString(self.typ), Utils.ifNotNull(self.value, "")), end="", file=res, flush=True)
        if (self.referent is not None): 
            print(" <{0}>".format(str(self.referent)), end="", file=res, flush=True)
        if (self.referent2 is not None): 
            print(" / <{0}>".format(str(self.referent2)), end="", file=res, flush=True)
        if (self.detail_type != AddressDetailType.UNDEFINED or self.detail_meters > 0): 
            print(" [{0}, {1}]".format(Utils.enumToString(self.detail_type), self.detail_meters), end="", file=res, flush=True)
        if (self.orto_terr is not None): 
            print(" TERR: {0}".format(self.orto_terr), end="", file=res, flush=True)
        if (self.area_terr is not None): 
            print(" AREA: {0}".format(self.area_terr), end="", file=res, flush=True)
        if (self.alt_typ is not None): 
            print(" ALT: {0}".format(self.alt_typ), end="", file=res, flush=True)
        if (self.ref_token is not None): 
            print(" REFTOKEN: {0}".format(str(self.ref_token)), end="", file=res, flush=True)
        if (self.ref_token2 is not None): 
            print(" REFTOKEN2: {0}".format(str(self.ref_token2)), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def __find_addr_typ(t : 'Token', max_char : int, lev : int=0) -> 'AddressItemToken':
        if (t is None or t.end_char > max_char): 
            return None
        if (lev > 5): 
            return None
        if (isinstance(t, ReferentToken)): 
            geo = Utils.asObjectOrNull(t.get_referent(), GeoReferent)
            if (geo is not None): 
                for s in geo.slots: 
                    if (s.type_name == GeoReferent.ATTR_TYPE): 
                        ty = s.value
                        if ("район" in ty): 
                            return None
            tt = t.begin_token
            first_pass3775 = True
            while True:
                if first_pass3775: first_pass3775 = False
                else: tt = tt.next0_
                if (not (tt is not None and tt.end_char <= t.end_char)): break
                if (tt.end_char > max_char): 
                    break
                if (tt.is_value("У", None)): 
                    if (geo.find_slot(GeoReferent.ATTR_TYPE, "улус", True) is not None): 
                        continue
                ty = AddressItemToken.__find_addr_typ(tt, max_char, lev + 1)
                if (ty is not None): 
                    if (ty.begin_token == ty.end_token and tt.is_value("РАЙОН", None)): 
                        if (tt.end_char == t.end_char): 
                            continue
                        if (tt.next0_ is not None and tt.next0_.is_comma): 
                            continue
                    return ty
        else: 
            ai = AddressItemToken.__try_attach_detail(t, None)
            if (ai is not None): 
                if (ai.detail_type != AddressDetailType.UNDEFINED or ai.detail_meters > 0): 
                    return ai
        return None
    
    @staticmethod
    def try_parse(t : 'Token', prefix_before : bool=False, prev : 'AddressItemToken'=None, ad : 'GeoAnalyzerData'=None) -> 'AddressItemToken':
        if (t is None): 
            return None
        if (ad is None): 
            ad = GeoAnalyzer._get_data(t)
        if (ad is None): 
            return None
        if (ad.alevel > 1): 
            return None
        ad.alevel += 1
        res = AddressItemToken.__try_parse(t, prefix_before, prev, ad)
        ad.alevel -= 1
        if ((res is None and t.is_value("З", None) and (isinstance(t.next0_, NumberToken))) and prev is not None and prev.typ == AddressItemType.STREET): 
            num = AddressItemToken.try_parse_pure_item(t.next0_, None, None)
            if (num is not None and num.typ == AddressItemType.NUMBER): 
                res = AddressItemToken._new191(AddressItemType.HOUSE, t, num.end_token, num.value)
        if (((res is not None and not res.is_whitespace_after and res.end_token.next0_ is not None) and ((res.end_token.next0_.is_hiphen or res.end_token.next0_.is_char_of("\\/"))) and not res.end_token.next0_.is_whitespace_after) and res.value is not None): 
            if ((res.typ == AddressItemType.HOUSE or res.typ == AddressItemType.BUILDING or res.typ == AddressItemType.CORPUS) or res.typ == AddressItemType.PLOT): 
                tt = res.end_token.next0_.next0_
                next0__ = AddressItemToken.try_parse_pure_item(tt, None, None)
                if (next0__ is not None and next0__.typ == AddressItemType.NUMBER): 
                    res = res.clone()
                    res.value = "{0}{1}{2}".format(res.value, ("-" if res.end_token.next0_.is_hiphen else "/"), next0__.value)
                    res.end_token = next0__.end_token
                    tt = res.end_token.next0_
                    if ((tt is not None and ((tt.is_hiphen or tt.is_char_of("\\/"))) and not tt.is_whitespace_before) and not tt.is_whitespace_after): 
                        next0__ = AddressItemToken.try_parse_pure_item(tt.next0_, None, None)
                        if (next0__ is not None and next0__.typ == AddressItemType.NUMBER): 
                            res.value = "{0}{1}{2}".format(res.value, ("-" if tt.is_hiphen else "/"), next0__.value)
                            res.end_token = next0__.end_token
                elif ((isinstance(tt, TextToken)) and tt.length_char == 1 and tt.chars.is_all_upper): 
                    res.value = "{0}-{1}".format(res.value, tt.term)
                    res.end_token = tt
        return res
    
    @staticmethod
    def __try_parse(t : 'Token', prefix_before : bool, prev : 'AddressItemToken', ad : 'GeoAnalyzerData') -> 'AddressItemToken':
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        from pullenti.ner.address.internal.StreetDefineHelper import StreetDefineHelper
        if (t is None): 
            return None
        if (isinstance(t, ReferentToken)): 
            rt = Utils.asObjectOrNull(t, ReferentToken)
            ty = None
            geo = Utils.asObjectOrNull(rt.referent, GeoReferent)
            if ((geo is not None and t.next0_ is not None and t.next0_.is_hiphen) and MiscLocationHelper.is_user_param_address(t)): 
                sit = StreetItemToken._try_parse_spec(t, None)
                if (sit is not None and sit[0].typ == StreetItemType.NAME): 
                    geo = (None)
                elif (t.next0_.next0_ is not None and (isinstance(t.next0_.next0_.get_referent(), GeoReferent))): 
                    geo = (None)
            if (geo is not None): 
                if (geo.is_city): 
                    ty = AddressItemType.CITY
                elif (geo.is_state): 
                    ty = AddressItemType.COUNTRY
                else: 
                    ty = AddressItemType.REGION
                res = AddressItemToken._new202(ty, t, t, rt.referent)
                if (ty != AddressItemType.CITY): 
                    return res
                tt = t.begin_token
                first_pass3776 = True
                while True:
                    if first_pass3776: first_pass3776 = False
                    else: tt = tt.next0_
                    if (not (tt is not None and tt.end_char <= t.end_char)): break
                    if (isinstance(tt, ReferentToken)): 
                        if (tt.get_referent() == geo): 
                            res1 = AddressItemToken.__try_parse(tt, False, prev, ad)
                            if (res1 is not None and ((res1.detail_meters > 0 or res1.detail_type != AddressDetailType.UNDEFINED))): 
                                res1.begin_token = res1.end_token = t
                                return res1
                        continue
                    det = AddressItemToken.__try_parse_pure_item(tt, False, None)
                    if (det is not None): 
                        if (tt.is_value("У", None) and geo.find_slot(GeoReferent.ATTR_TYPE, "улус", True) is not None): 
                            pass
                        else: 
                            if (det.detail_type != AddressDetailType.UNDEFINED and res.detail_type == AddressDetailType.UNDEFINED): 
                                res.detail_type = det.detail_type
                            if (det.detail_meters > 0): 
                                res.detail_meters = det.detail_meters
                return res
        kvart = False
        if (prev is not None): 
            if (t.is_value("КВ", None) or t.is_value("КВАРТ", None)): 
                if ((((prev.typ == AddressItemType.HOUSE or prev.typ == AddressItemType.NUMBER or prev.typ == AddressItemType.BUILDING) or prev.typ == AddressItemType.FLOOR or prev.typ == AddressItemType.POTCH) or prev.typ == AddressItemType.CORPUS or prev.typ == AddressItemType.CORPUSORFLAT) or prev.typ == AddressItemType.DETAIL): 
                    return AddressItemToken.try_parse_pure_item(t, prev, None)
                kvart = True
        if (prev is not None and ((t.is_value("П", None) or t.is_value("ПОЗ", None) or t.is_value("ПОЗИЦИЯ", None)))): 
            if (((MiscLocationHelper.is_user_param_address(t) or prev.typ == AddressItemType.STREET or prev.typ == AddressItemType.CITY) or prev.typ == AddressItemType.GENPLAN or prev.typ == AddressItemType.PLOT) or prev.typ == AddressItemType.CITY): 
                tt = t.next0_
                if (tt is not None and tt.is_char('.')): 
                    tt = tt.next0_
                next0__ = AddressItemToken.try_parse_pure_item(tt, None, None)
                if (next0__ is not None and ((next0__.typ == AddressItemType.NUMBER or next0__.typ == AddressItemType.GENPLAN))): 
                    next0__ = next0__.clone()
                    next0__.begin_token = t
                    next0__.is_genplan = True
                    next0__.typ = AddressItemType.NUMBER
                    return next0__
        pure = AddressItemToken.try_parse_pure_item(t, prev, ad)
        if ((pure is not None and pure.typ != AddressItemType.NUMBER and pure.typ != AddressItemType.KILOMETER) and pure.value is not None): 
            if (t.is_value("СТ", None) and OrgItemToken.try_parse(t, None) is not None): 
                pass
            elif (kvart): 
                ttt = pure.end_token.next0_
                if (ttt is not None and ttt.is_comma): 
                    ttt = ttt.next0_
                next0__ = AddressItemToken.try_parse_pure_item(ttt, None, None)
                if (next0__ is not None and next0__.typ == AddressItemType.PLOT): 
                    pass
                else: 
                    return pure
            else: 
                return pure
        tt2 = MiscLocationHelper.check_territory(t)
        if (tt2 is not None): 
            next0__ = AddressItemToken.try_parse(tt2.next0_, False, None, None)
            if (next0__ is not None and next0__.typ == AddressItemType.STREET): 
                ss = Utils.asObjectOrNull(next0__.referent, StreetReferent)
                if (ss.kind == StreetKind.ROAD or ss.kind == StreetKind.RAILWAY): 
                    next0__.begin_token = t
                    return next0__
        if (t.is_value("ТРК", None)): 
            pass
        sli = StreetItemToken.try_parse_list(t, 10, ad)
        if (sli is not None): 
            rt = StreetDefineHelper._try_parse_street(sli, prefix_before or ((prev is not None and prev.detail_type == AddressDetailType.CROSS)), False, prev is not None and prev.typ == AddressItemType.STREET, None)
            if (rt is None and sli[0].typ != StreetItemType.FIX): 
                org0_ = OrgItemToken.try_parse(t, None)
                if (org0_ is not None and not org0_.is_building): 
                    si = StreetItemToken._new262(t, org0_.end_token, StreetItemType.FIX, org0_)
                    sli.clear()
                    sli.append(si)
                    rt = StreetDefineHelper._try_parse_street(sli, prefix_before or prev is not None, False, False, None)
                elif (len(sli) == 1 and sli[0].typ == StreetItemType.NOUN and not sli[0].is_newline_after): 
                    org0_ = OrgItemToken.try_parse(sli[0].end_token.next0_, None)
                    if (org0_ is not None): 
                        typ_ = sli[0].termin.canonic_text.lower()
                        si = StreetItemToken._new262(t, org0_.end_token, StreetItemType.FIX, org0_)
                        sli.clear()
                        sli.append(si)
                        rt = StreetDefineHelper._try_parse_street(sli, prefix_before or prev is not None, False, False, None)
                        if (rt is not None): 
                            sr = Utils.asObjectOrNull(rt.referent, StreetReferent)
                            sr.add_slot(StreetReferent.ATTR_TYPE, None, True, 0)
                            sr._add_typ(typ_)
                            sr.kind = StreetKind.UNDEFINED
                    elif ((prev is not None and prev.typ == AddressItemType.CITY and (isinstance(sli[0].end_token.next0_, ReferentToken))) and (isinstance(sli[0].end_token.next0_.get_referent(), GeoReferent))): 
                        rt0 = Utils.asObjectOrNull(sli[0].end_token.next0_, ReferentToken)
                        st1 = StreetItemToken.try_parse(rt0.begin_token, sli[0], False, None)
                        if (st1 is not None and st1.end_char == rt0.end_char): 
                            sli1 = list()
                            sli1.append(sli[0])
                            sli1.append(st1)
                            rt = StreetDefineHelper._try_parse_street(sli1, prefix_before, False, (prev is not None and prev.typ == AddressItemType.STREET), None)
                            if (rt is not None): 
                                rt.end_token = rt0
            if ((rt is None and prev is not None and prev.typ == AddressItemType.CITY) and MiscLocationHelper.is_user_param_address(sli[0])): 
                if (len(sli) == 1 and (((sli[0].typ == StreetItemType.NAME or sli[0].typ == StreetItemType.STDNAME or sli[0].typ == StreetItemType.STDADJECTIVE) or ((sli[0].typ == StreetItemType.NUMBER and sli[0].begin_token.morph.class0_.is_adjective))))): 
                    rt = StreetDefineHelper._try_parse_street(sli, True, False, False, None)
            if (((rt is None and prev is not None and prev.typ == AddressItemType.STREET) and len(sli) == 1 and sli[0].typ == StreetItemType.NAME) and MiscLocationHelper.is_user_param_address(sli[0])): 
                ok1 = False
                if (prev.ref_token is not None): 
                    ok1 = True
                elif ((isinstance(prev.referent, StreetReferent)) and prev.referent.kind == StreetKind.AREA): 
                    ok1 = True
                elif (AddressItemToken.check_house_after(sli[0].end_token.next0_, False, False)): 
                    ok1 = True
                if (ok1): 
                    rt = StreetDefineHelper._try_parse_street(sli, True, False, False, None)
            if (rt is not None): 
                if (len(sli) > 2): 
                    pass
                if (rt.begin_char > sli[0].begin_char): 
                    return None
                crlf = False
                ttt = rt.begin_token
                while ttt != rt.end_token and (ttt.end_char < rt.end_char): 
                    if (ttt.is_newline_after): 
                        crlf = True
                        break
                    ttt = ttt.next0_
                if (crlf): 
                    ttt = rt.begin_token.previous
                    first_pass3777 = True
                    while True:
                        if first_pass3777: first_pass3777 = False
                        else: ttt = ttt.previous
                        if (not (ttt is not None)): break
                        if (ttt.morph.class0_.is_preposition or ttt.is_comma): 
                            continue
                        if (isinstance(ttt.get_referent(), GeoReferent)): 
                            crlf = False
                        break
                    if (sli[0].typ == StreetItemType.NOUN and "ДОРОГА" in sli[0].termin.canonic_text): 
                        crlf = False
                if (crlf): 
                    tt33 = rt.end_token.next0_
                    if (tt33 is not None and tt33.is_comma): 
                        tt33 = tt33.next0_
                    aat = AddressItemToken.try_parse_pure_item(tt33, None, None)
                    if (aat is None): 
                        return None
                    if (aat.typ != AddressItemType.HOUSE): 
                        return None
                if (rt.end_token.next0_ is not None and rt.end_token.next0_.is_char_of("\\/")): 
                    if (not AddressItemToken.check_house_after(rt.end_token.next0_.next0_, False, False)): 
                        sli2 = StreetItemToken.try_parse_list(rt.end_token.next0_.next0_, 10, ad)
                        if (sli2 is not None and len(sli2) > 0): 
                            rt2 = StreetDefineHelper._try_parse_street(sli2, prefix_before, False, True, Utils.asObjectOrNull(rt.referent, StreetReferent))
                            if (rt2 is not None): 
                                rt.end_token = rt2.end_token
                                rt.referent2 = rt2.referent
                return rt
            if (len(sli) == 1 and sli[0].typ == StreetItemType.NOUN): 
                tt = sli[0].end_token.next0_
                if (tt is not None and ((tt.is_hiphen or tt.is_char('_') or tt.is_value("НЕТ", None)))): 
                    ttt = tt.next0_
                    if (ttt is not None and ttt.is_comma): 
                        ttt = ttt.next0_
                    att = AddressItemToken.try_parse_pure_item(ttt, None, None)
                    if (att is not None): 
                        if (att.typ == AddressItemType.HOUSE or att.typ == AddressItemType.CORPUS or att.typ == AddressItemType.BUILDING): 
                            return AddressItemToken(AddressItemType.STREET, t, tt)
            if ((len(sli) == 1 and sli[0].typ == StreetItemType.NAME and prev is not None) and prev.typ == AddressItemType.CITY and MiscLocationHelper.is_user_param_address(sli[0])): 
                tt3 = sli[0].end_token.next0_
                while tt3 is not None: 
                    if (not tt3.is_char_of(",.")): 
                        break
                    tt3 = tt3.next0_
                if (AddressItemToken.check_street_after(tt3, False)): 
                    rr = GeoReferent()
                    rr.add_slot(GeoReferent.ATTR_NAME, MiscHelper.get_text_value_of_meta_token(sli[0], GetTextAttr.NO), False, 0)
                    rr.higher = Utils.asObjectOrNull(prev.referent, GeoReferent)
                    return AddressItemToken._new264(AddressItemType.REGION, sli[0].begin_token, sli[0].end_token, rr, ReferentToken(rr, sli[0].begin_token, sli[0].end_token))
        if (t is None or pure is not None): 
            return pure
        if ((t.length_char == 1 and t.chars.is_letter and prev is not None) and prev.typ == AddressItemType.CITY and MiscLocationHelper.is_user_param_address(t)): 
            tt = t.next0_
            if (tt is not None and tt.is_hiphen): 
                tt = tt.next0_
            ch = AddressItemToken.__correct_char_token(t)
            if ((isinstance(tt, NumberToken)) and ch is not None): 
                micr = StreetReferent()
                micr._add_typ("микрорайон")
                micr.add_slot(StreetReferent.ATTR_NUMBER, "{0}{1}".format(tt.value, ch), False, 0)
                micr.kind = StreetKind.AREA
                return AddressItemToken._new264(AddressItemType.STREET, t, tt, micr, ReferentToken(micr, t, tt))
        return None
    
    SPEED_REGIME = False
    
    @staticmethod
    def _prepare_all_data(t0 : 'Token') -> None:
        if (not AddressItemToken.SPEED_REGIME): 
            return
        ad = GeoAnalyzer._get_data(t0)
        if (ad is None): 
            return
        ad.aregime = False
        t = t0
        while t is not None: 
            d = Utils.asObjectOrNull(t.tag, GeoTokenData)
            prev = None
            kk = 0
            tt = t.previous
            first_pass3778 = True
            while True:
                if first_pass3778: first_pass3778 = False
                else: tt = tt.previous; kk += 1
                if (not (tt is not None and (kk < 10))): break
                dd = Utils.asObjectOrNull(tt.tag, GeoTokenData)
                if (dd is None): 
                    continue
                if (dd.street is not None): 
                    if (dd.street.end_token.next0_ == t): 
                        prev = dd.addr
                    elif (t.previous is not None and t.previous.is_comma and dd.street.end_token.next0_ == t.previous): 
                        prev = dd.addr
                elif (dd.addr is not None and (((dd.addr.typ == AddressItemType.HOUSE or dd.addr.typ == AddressItemType.FLAT or dd.addr.typ == AddressItemType.CORPUS) or dd.addr.typ == AddressItemType.BUILDING))): 
                    if (dd.addr.end_token.next0_ == t): 
                        prev = dd.addr
                    elif (t.previous is not None and t.previous.is_comma and dd.addr.end_token.next0_ == t.previous): 
                        prev = dd.addr
            str0_ = AddressItemToken.try_parse_pure_item(t, prev, None)
            if (str0_ is not None): 
                if (d is None): 
                    d = GeoTokenData(t)
                d.addr = str0_
            t = t.next0_
        ad.aregime = True
    
    @staticmethod
    def check_street_after(t : 'Token', check_this_and_not_next : bool=False) -> bool:
        from pullenti.ner.geo.internal.OrgItemToken import OrgItemToken
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.") or t.is_hiphen or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        ait = AddressItemToken.try_parse(t, False, None, None)
        if (ait is None or ait.typ != AddressItemType.STREET): 
            return False
        if (ait.ref_token is not None): 
            if (not ait.ref_token_is_gsk): 
                return False
            oo = Utils.asObjectOrNull(ait.ref_token, OrgItemToken)
            if (oo is not None and oo.is_doubt): 
                return False
        if (not check_this_and_not_next): 
            return True
        if (t.next0_ is None or ait.end_char <= t.end_char): 
            return True
        ait2 = AddressItemToken.try_parse(t.next0_, False, None, None)
        if (ait2 is None): 
            return True
        aits1 = AddressItemToken.try_parse_list(t, 20)
        aits2 = AddressItemToken.try_parse_list(t.next0_, 20)
        if (aits1 is not None and aits2 is not None): 
            if (aits2[len(aits2) - 1].end_char > aits1[len(aits1) - 1].end_char): 
                return False
        return True
    
    @staticmethod
    def check_house_after(t : 'Token', leek : bool=False, pure_house : bool=False) -> bool:
        if (t is None): 
            return False
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.") or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        if (t.is_newline_before and t.previous is not None): 
            return False
        ait = AddressItemToken.try_parse_pure_item(t, None, None)
        if (ait is not None): 
            if (ait.typ == AddressItemType.NONUMBER): 
                return True
            if (ait.value is None or ait.value == "0"): 
                return False
            if (pure_house): 
                return ait.typ == AddressItemType.HOUSE or ait.typ == AddressItemType.PLOT
            if (((ait.typ == AddressItemType.HOUSE or ait.typ == AddressItemType.FLOOR or ait.typ == AddressItemType.OFFICE) or ait.typ == AddressItemType.FLAT or ait.typ == AddressItemType.PLOT) or ait.typ == AddressItemType.ROOM or ait.typ == AddressItemType.CORPUS): 
                if (((isinstance(t, TextToken)) and t.chars.is_all_upper and t.next0_ is not None) and t.next0_.is_hiphen and (isinstance(t.next0_.next0_, NumberToken))): 
                    return False
                if ((isinstance(t, TextToken)) and t.next0_ == ait.end_token and t.next0_.is_hiphen): 
                    return False
                return True
            if (leek): 
                if (ait.typ == AddressItemType.NUMBER): 
                    return True
            if (ait.typ == AddressItemType.NUMBER): 
                t1 = t.next0_
                while t1 is not None and t1.is_char_of(".,"):
                    t1 = t1.next0_
                ait = AddressItemToken.try_parse_pure_item(t1, None, None)
                if (ait is not None and ((((ait.typ == AddressItemType.BUILDING or ait.typ == AddressItemType.CORPUS or ait.typ == AddressItemType.FLAT) or ait.typ == AddressItemType.FLOOR or ait.typ == AddressItemType.OFFICE) or ait.typ == AddressItemType.ROOM))): 
                    return True
        return False
    
    @staticmethod
    def check_km_after(t : 'Token') -> bool:
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.") or t.morph.class0_.is_preposition): 
                pass
            else: 
                break
            t = t.next0_; cou += 1
        if (t is None): 
            return False
        km = AddressItemToken.try_parse_pure_item(t, None, None)
        if (km is not None and km.typ == AddressItemType.KILOMETER): 
            return True
        if (not (isinstance(t, NumberToken)) or t.next0_ is None): 
            return False
        if (t.next0_.is_value("КИЛОМЕТР", None) or t.next0_.is_value("МЕТР", None) or t.next0_.is_value("КМ", None)): 
            return True
        return False
    
    @staticmethod
    def check_km_before(t : 'Token') -> bool:
        cou = 0
        while t is not None and (cou < 4): 
            if (t.is_char_of(",.")): 
                pass
            elif (t.is_value("КМ", None) or t.is_value("КИЛОМЕТР", None) or t.is_value("МЕТР", None)): 
                return True
            t = t.previous; cou += 1
        return False
    
    @staticmethod
    def correct_char(v : 'char') -> 'char':
        if (v == 'A' or v == 'А'): 
            return 'А'
        if (v == 'Б' or v == 'Г'): 
            return v
        if (v == 'B' or v == 'В'): 
            return 'В'
        if (v == 'C' or v == 'С'): 
            return 'С'
        if (v == 'D' or v == 'Д'): 
            return 'Д'
        if (v == 'E' or v == 'Е'): 
            return 'Е'
        if (v == 'H' or v == 'Н'): 
            return 'Н'
        if (v == 'K' or v == 'К'): 
            return 'К'
        return chr(0)
    
    @staticmethod
    def __correct_char_token(t : 'Token') -> str:
        tt = Utils.asObjectOrNull(t, TextToken)
        if (tt is None): 
            return None
        v = tt.term
        if (len(v) == 1): 
            corr = AddressItemToken.correct_char(v[0])
            if (corr != (chr(0))): 
                return "{0}".format(corr)
            if (t.chars.is_cyrillic_letter): 
                return v
        if (len(v) == 2): 
            if (t.chars.is_cyrillic_letter): 
                return v
            corr = AddressItemToken.correct_char(v[0])
            corr2 = AddressItemToken.correct_char(v[1])
            if (corr != (chr(0)) and corr2 != (chr(0))): 
                return "{0}{1}".format(corr, corr2)
        return None
    
    @staticmethod
    def __corr_number(num : str) -> str:
        if (Utils.isNullOrEmpty(num)): 
            return None
        if (num[0] != 'З'): 
            return None
        res = "3"
        i = 0
        i = 1
        while i < len(num): 
            if (num[i] == 'З'): 
                res += "3"
            elif (num[i] == 'О'): 
                res += "0"
            else: 
                break
            i += 1
        if (i == len(num)): 
            return res
        if ((i + 1) < len(num)): 
            return None
        if (num[i] == 'А' or num[i] == 'Б' or num[i] == 'В'): 
            return "{0}{1}".format(res, num[i])
        return None
    
    @staticmethod
    def create_address(txt : str) -> 'ReferentToken':
        from pullenti.ner.address.internal.AddressDefineHelper import AddressDefineHelper
        ar = None
        try: 
            ar = ProcessorService.get_empty_processor().process(SourceOfAnalysis._new266(txt, "ADDRESS"), None, None)
        except Exception as ex: 
            return None
        if (ar is None): 
            return None
        AddressItemToken._prepare_all_data(ar.first_token)
        li = list()
        t = ar.first_token
        first_pass3779 = True
        while True:
            if first_pass3779: first_pass3779 = False
            else: t = t.next0_
            if (not (t is not None)): break
            if (t.is_char_of(",.")): 
                continue
            ait = AddressItemToken.try_parse_pure_item(t, (li[len(li) - 1] if len(li) > 0 else None), None)
            if (ait is None): 
                break
            li.append(ait)
            t = ait.end_token
        if (li is None or len(li) == 0): 
            return None
        rt = AddressDefineHelper.try_define(li, ar.first_token, None, True)
        return Utils.asObjectOrNull(rt, ReferentToken)
    
    @staticmethod
    def _new191(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        return res
    
    @staticmethod
    def _new199(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressBuildingType', _arg5 : str) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.building_type = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new202(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        return res
    
    @staticmethod
    def _new207(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressHouseType', _arg5 : str) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.house_type = _arg4
        res.value = _arg5
        return res
    
    @staticmethod
    def _new210(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'ReferentToken') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.detail_param = _arg4
        res.ref_token2 = _arg5
        return res
    
    @staticmethod
    def _new212(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : str) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.detail_param = _arg5
        return res
    
    @staticmethod
    def _new213(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'AddressHouseType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.house_type = _arg5
        return res
    
    @staticmethod
    def _new215(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : bool) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.is_doubt = _arg5
        return res
    
    @staticmethod
    def _new216(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressHouseType', _arg5 : 'AddressBuildingType', _arg6 : str, _arg7 : str) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.house_type = _arg4
        res.building_type = _arg5
        res.value = _arg6
        res.detail_param = _arg7
        return res
    
    @staticmethod
    def _new219(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'AddressHouseType', _arg6 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.house_type = _arg5
        res.building_type = _arg6
        return res
    
    @staticmethod
    def _new225(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'MorphCollection', _arg6 : 'AddressHouseType', _arg7 : 'AddressBuildingType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.morph = _arg5
        res.house_type = _arg6
        res.building_type = _arg7
        return res
    
    @staticmethod
    def _new244(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : str, _arg5 : 'MorphCollection', _arg6 : 'AddressHouseType', _arg7 : 'AddressBuildingType', _arg8 : str) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.value = _arg4
        res.morph = _arg5
        res.house_type = _arg6
        res.building_type = _arg7
        res.detail_param = _arg8
        return res
    
    @staticmethod
    def _new251(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'AddressDetailType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.detail_type = _arg4
        return res
    
    @staticmethod
    def _new264(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent', _arg5 : 'ReferentToken') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        res.ref_token = _arg5
        return res
    
    @staticmethod
    def _new269(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'Referent', _arg5 : bool) -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.referent = _arg4
        res.is_doubt = _arg5
        return res
    
    @staticmethod
    def _new289(_arg1 : 'AddressItemType', _arg2 : 'Token', _arg3 : 'Token', _arg4 : 'ReferentToken', _arg5 : 'AddressDetailType') -> 'AddressItemToken':
        res = AddressItemToken(_arg1, _arg2, _arg3)
        res.ref_token = _arg4
        res.detail_type = _arg5
        return res