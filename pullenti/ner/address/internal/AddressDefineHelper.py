# SDK Pullenti Lingvo, version 4.29, march 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.address.StreetKind import StreetKind
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.ReferentsEqualType import ReferentsEqualType
from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.address.AddressReferent import AddressReferent
from pullenti.ner.Referent import Referent
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.geo.internal.TerrItemToken import TerrItemToken
from pullenti.ner.geo.GeoReferent import GeoReferent
from pullenti.ner.Token import Token
from pullenti.ner.address.internal.AddressItemType import AddressItemType
from pullenti.ner.geo.internal.MiscLocationHelper import MiscLocationHelper
from pullenti.ner.geo.internal.GeoOwnerHelper import GeoOwnerHelper
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.address.StreetReferent import StreetReferent
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.address.AddressDetailType import AddressDetailType
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken

class AddressDefineHelper:
    
    @staticmethod
    def try_define(li : typing.List['AddressItemToken'], t : 'Token', ad : 'AnalyzerData', ignore_street : bool=False) -> 'Token':
        if (li is None or len(li) == 0): 
            return None
        empty = True
        not_empty = False
        bad_org = False
        has_geo = False
        has_street = False
        ii = 0
        first_pass3751 = True
        while True:
            if first_pass3751: first_pass3751 = False
            else: ii += 1
            if (not (ii < len(li))): break
            v = li[ii]
            if (v.typ == AddressItemType.SPACE and (len(li) < 3) and not MiscLocationHelper.is_user_param_address(v)): 
                return None
            if (v.typ == AddressItemType.DETAIL): 
                continue
            if ((v.typ == AddressItemType.SPACE and ii == 0 and ((ii + 1) < len(li))) and ((li[ii + 1].typ == AddressItemType.CITY or li[ii + 1].typ == AddressItemType.COUNTRY))): 
                return None
            if ((v.typ == AddressItemType.STREET and v.ref_token_is_gsk and len(li) == 2) and not MiscLocationHelper.is_user_param_address(v)): 
                if ("АЭРОПОРТ" in str(v).upper()): 
                    if (ii == 0 and li[1].typ == AddressItemType.CITY): 
                        return None
                    if (ii == 1 and li[0].typ == AddressItemType.CITY): 
                        return None
            if (((v.typ == AddressItemType.REGION and not v.is_newline_after and ((ii + 2) < len(li))) and li[ii + 1].typ == AddressItemType.STREET and not li[ii + 1].is_newline_after) and li[ii + 2].typ == AddressItemType.CITY): 
                vv = li[ii + 1]
                li[ii + 1] = li[ii + 2]
                li[ii + 2] = vv
            elif ((v.typ == AddressItemType.CITY and ((ii + 2) < len(li)) and li[ii + 1].typ == AddressItemType.STREET) and li[ii + 2].typ == AddressItemType.CITY): 
                if (GeoOwnerHelper.can_be_higher(Utils.asObjectOrNull(v.referent, GeoReferent), Utils.asObjectOrNull(li[ii + 2].referent, GeoReferent), None, None)): 
                    li[ii + 2].referent.higher = Utils.asObjectOrNull(v.referent, GeoReferent)
                    vv = li[ii + 1]
                    li[ii + 1] = li[ii + 2]
                    li[ii + 2] = vv
            if (v.detail_type == AddressDetailType.ORG and (len(li) < 4) and not MiscLocationHelper.is_user_param_address(v)): 
                return None
            if (v.typ == AddressItemType.BUILDING and (ii < 2) and ((ii + 1) < len(li))): 
                if (li[ii].is_doubt or li[ii].typ == AddressItemType.BUILDING): 
                    ok = False
                    if (ii > 0 and li[ii - 1].typ == AddressItemType.CITY): 
                        ok = True
                    jj = ii + 1
                    while jj < len(li): 
                        if (li[jj].typ != AddressItemType.STREET): 
                            ok = False
                        jj += 1
                    if (not ok): 
                        return None
            if ((v.building_type == AddressBuildingType.LITER and v.length_char == 1 and ((ii + 1) < len(li))) and li[ii + 1].typ == AddressItemType.STREET): 
                del li[ii]
                ii -= 1
                continue
            if (v.typ == AddressItemType.NUMBER or v.typ == AddressItemType.ZIP or v.typ == AddressItemType.DETAIL): 
                pass
            elif (v.typ == AddressItemType.HOUSE and ((v.is_doubt or v.house_type == AddressHouseType.SPECIAL))): 
                pass
            elif (v.typ != AddressItemType.STREET): 
                empty = False
                if (v.typ != AddressItemType.CITY and v.typ != AddressItemType.COUNTRY and v.typ != AddressItemType.REGION): 
                    not_empty = True
                if (v.typ == AddressItemType.CITY or v.typ == AddressItemType.REGION or v.typ == AddressItemType.COUNTRY): 
                    has_geo = True
            elif ((isinstance(v.referent, StreetReferent)) and str(v.referent) != "улица"): 
                has_street = True
                if (MiscLocationHelper.is_user_param_address(v)): 
                    empty = False
                    not_empty = True
                    continue
                s = Utils.asObjectOrNull(v.referent, StreetReferent)
                if (s.kind == StreetKind.RAILWAY and s.numbers is None): 
                    pass
                elif (s.kind == StreetKind.ORG or v.ref_token is not None): 
                    if (v.is_doubt and v.ref_token is not None and not v.ref_token_is_gsk): 
                        bad_org = True
                    if (bad_org): 
                        if (v == li[0]): 
                            return None
                        elif (li[0].typ == AddressItemType.PREFIX and v == li[1]): 
                            return None
                elif (s.kind == StreetKind.AREA): 
                    has_street = True
                else: 
                    if ((v.is_doubt and v == li[0] and not v.is_street_road) and not MiscLocationHelper.is_user_param_address(v)): 
                        ok = False
                        if (len(li) > 1 and li[1].typ == AddressItemType.CITY): 
                            ok = True
                        elif (v.referent is not None and ad is not None): 
                            for r in ad.referents: 
                                if (v.referent.can_be_equals(r, ReferentsEqualType.WITHINONETEXT)): 
                                    ok = True
                                    break
                        if (not ok): 
                            return None
                    has_street = True
                    empty = False
                    not_empty = True
        if (ignore_street): 
            pass
        else: 
            if (empty): 
                return None
            if (not not_empty): 
                for v in li: 
                    if (v != li[0] and v.is_newline_before): 
                        return None
                if (bad_org and not MiscLocationHelper.is_user_param_address(li[0])): 
                    return None
                if (li[0].typ == AddressItemType.STREET and li[0].referent.kind == StreetKind.ORG): 
                    return None
                if (len(li) == 1 and li[0].typ != AddressItemType.STREET): 
                    if (li[0].detail_type != AddressDetailType.UNDEFINED and MiscLocationHelper.is_user_param_address(li[0])): 
                        pass
                    elif (li[0].detail_meters > 0): 
                        pass
                    else: 
                        return None
                if (len(li) == 2): 
                    if (li[0].typ == AddressItemType.DETAIL and li[1].typ != AddressItemType.CITY): 
                        return None
                    if (li[1].typ == AddressItemType.DETAIL and li[0].typ != AddressItemType.CITY): 
                        return None
            if (not has_geo and not has_street): 
                return None
        if ((len(li) > 3 and li[0].typ == AddressItemType.CITY and li[1].typ == AddressItemType.STREET) and li[2].typ == AddressItemType.CITY and li[3].typ == AddressItemType.STREET): 
            if (li[1].referent.kind == StreetKind.RAILWAY or li[1].referent.kind == StreetKind.ROAD): 
                geo = Utils.asObjectOrNull(li[2].referent, GeoReferent)
                if (geo is not None and geo.higher is None and GeoOwnerHelper.can_be_higher(Utils.asObjectOrNull(li[0].referent, GeoReferent), geo, None, None)): 
                    geo.higher = Utils.asObjectOrNull(li[0].referent, GeoReferent)
                    li[2] = li[2].clone()
                    li[2].begin_token = li[0].begin_token
                    del li[0:0+2]
        if (len(li) >= 2 and li[0].typ == AddressItemType.BLOCK and li[1].typ == AddressItemType.STREET): 
            return None
        if (len(li) >= 2 and li[0].typ == AddressItemType.CITY and li[1].typ == AddressItemType.BUILDING): 
            if (li[1].begin_token.is_value("СТР", None) and not MiscLocationHelper.is_user_param_address(li[1])): 
                return None
        if (li[0].typ == AddressItemType.STREET and not MiscLocationHelper.is_user_param_address(li[0])): 
            if (li[0].ref_token is not None): 
                if (not li[0].ref_token_is_gsk or li[0].referent.kind == StreetKind.AREA): 
                    return None
        if (li[0].typ == AddressItemType.STREET and MiscLocationHelper.is_user_param_address(li[0])): 
            ok = True
            for it in li: 
                if ((it.typ == AddressItemType.ZIP or it.typ == AddressItemType.REGION or it.typ == AddressItemType.CITY) or it.typ == AddressItemType.COUNTRY): 
                    ok = False
            if (ok): 
                tt = li[len(li) - 1].end_token.next0_
                while tt is not None:
                    if (tt.is_comma): 
                        tt = tt.next0_
                    else: 
                        break
                ter = TerrItemToken.try_parse(tt, None, None)
                if (ter is not None and ter.termin_item is None and ter.onto_item is None): 
                    tt2 = ter.end_token.next0_
                    while tt2 is not None:
                        if (tt2.is_comma): 
                            tt2 = tt2.next0_
                        else: 
                            break
                    if (tt2 is not None and (isinstance(tt2.get_referent(), GeoReferent)) and tt2.get_referent().is_city): 
                        li2 = AddressItemToken.try_parse_list(tt2, 20)
                        if (li2 is not None): 
                            li.extend(li2)
        if (len(li) >= 6): 
            ii = 2
            first_pass3752 = True
            while True:
                if first_pass3752: first_pass3752 = False
                else: ii += 1
                if (not (ii < (len(li) - 1))): break
                if (li[ii].begin_token.previous.is_char(';')): 
                    has_city = False
                    has_house = MiscLocationHelper.is_user_param_address(li[ii])
                    jj = 0
                    while jj < ii: 
                        v = li[jj]
                        if (v.typ == AddressItemType.REGION or v.typ == AddressItemType.CITY): 
                            has_city = True
                        elif ((v.typ == AddressItemType.HOUSE or v.typ == AddressItemType.STREET or v.typ == AddressItemType.BUILDING) or v.typ == AddressItemType.CORPUS): 
                            has_house = True
                        jj += 1
                    if (not has_city or not has_house): 
                        continue
                    has_city = False
                    has_house = MiscLocationHelper.is_user_param_address(li[ii])
                    jj = ii
                    while jj < len(li): 
                        v = li[jj]
                        if (v.typ == AddressItemType.REGION or v.typ == AddressItemType.CITY): 
                            has_city = True
                        elif ((v.typ == AddressItemType.HOUSE or v.typ == AddressItemType.STREET or v.typ == AddressItemType.BUILDING) or v.typ == AddressItemType.CORPUS): 
                            has_house = True
                        jj += 1
                    if (not has_city or not has_house): 
                        continue
                    del li[ii:ii+len(li) - ii]
                    break
        addr = AddressReferent()
        streets = list()
        i = 0
        j = 0
        metro = None
        details = list()
        district = None
        geos = None
        err = False
        cross = False
        has_genplan = False
        i = 0
        while i < len(li): 
            if ((li[i].typ == AddressItemType.DETAIL and li[i].detail_type == AddressDetailType.CROSS and ((i + 2) < len(li))) and li[i + 1].typ == AddressItemType.STREET and li[i + 2].typ == AddressItemType.STREET): 
                cross = True
                streets.append(li[i + 1])
                streets.append(li[i + 2])
                li[i + 1].end_token = li[i + 2].end_token
                li[i].tag = (addr)
                li[i + 1].tag = (addr)
                del li[i + 2]
                break
            elif (li[i].typ == AddressItemType.STREET): 
                if (((li[i].ref_token is not None and not li[i].ref_token_is_gsk)) and len(streets) == 0): 
                    if (i > 0 and li[i].is_newline_before): 
                        err = True
                        del li[i:i+len(li) - i]
                        break
                    elif ((i + 1) == len(li)): 
                        err = len(details) == 0
                    elif (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.NUMBER): 
                        err = True
                    if (err and geos is not None): 
                        for ii in range(i - 1, -1, -1):
                            if (li[ii].typ == AddressItemType.ZIP or li[ii].typ == AddressItemType.PREFIX): 
                                err = False
                    if (err and not MiscLocationHelper.is_user_param_address(li[i])): 
                        break
                if (li[i].detail_type != AddressDetailType.UNDEFINED): 
                    details.append(li[i])
                li[i].tag = (addr)
                streets.append(li[i])
                if (li[i].referent2 is not None): 
                    cross = True
                if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.STREET): 
                    pass
                elif ((((i + 2) < len(li)) and li[i + 2].typ == AddressItemType.STREET and li[i + 1].is_house) and (i + 3) == len(li) and not li[i + 2].ref_token_is_gsk): 
                    i += 1
                elif (((((i + 4) < len(li)) and ((li[i + 1].typ == AddressItemType.HOUSE or li[i + 1].typ == AddressItemType.NUMBER)) and li[i + 2].typ == AddressItemType.DETAIL) and li[i + 2].detail_type == AddressDetailType.CROSS and li[i + 3].typ == AddressItemType.STREET) and ((li[i + 4].typ == AddressItemType.HOUSE or li[i + 4].typ == AddressItemType.NUMBER))): 
                    cross = True
                    li[i + 2].tag = (addr)
                    streets.append(li[i + 3])
                    li[i + 3].tag = (addr)
                    li[i + 4] = li[i + 4].clone()
                    li[i + 4].value = "{0}/{1}".format(li[i + 1].value, li[i + 4].value)
                    del li[i + 1]
                    i -= 1
                    break
                else: 
                    break
            elif (li[i].typ == AddressItemType.CITY or li[i].typ == AddressItemType.REGION or li[i].typ == AddressItemType.COUNTRY): 
                if (geos is None): 
                    geos = list()
                geo = Utils.asObjectOrNull(li[i].referent, GeoReferent)
                if (li[i].detail_type != AddressDetailType.UNDEFINED): 
                    details.append(li[i])
                    if (len(geos) == 0): 
                        if (geo.higher is not None): 
                            if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.STREET and (isinstance(li[i + 1].referent, StreetReferent))): 
                                sr = Utils.asObjectOrNull(li[i + 1].referent, StreetReferent)
                                if (sr.kind == StreetKind.UNDEFINED): 
                                    geos.append(geo)
                                else: 
                                    geos.append(geo.higher)
                            else: 
                                geos.append(geo.higher)
                        else: 
                            geos.append(geo)
                elif ((len(geos) > 0 and geo.higher == geos[len(geos) - 1] and li[i].typ == AddressItemType.REGION) and li[i - 1].typ == AddressItemType.CITY): 
                    district = li[i]
                else: 
                    geos.insert(0, geo)
                li[i].tag = (addr)
            elif (li[i].typ == AddressItemType.DETAIL): 
                details.append(li[i])
                li[i].tag = (addr)
            elif (li[i].typ == AddressItemType.GENPLAN): 
                has_genplan = True
            i += 1
        if ((i >= len(li) and metro is None and len(details) == 0) and not cross and not ignore_street): 
            i = 0
            first_pass3753 = True
            while True:
                if first_pass3753: first_pass3753 = False
                else: i += 1
                if (not (i < len(li))): break
                cit = False
                if (li[i].typ == AddressItemType.CITY): 
                    cit = True
                elif (li[i].typ == AddressItemType.REGION): 
                    for s in li[i].referent.slots: 
                        if (s.type_name == GeoReferent.ATTR_TYPE): 
                            ss = Utils.asObjectOrNull(s.value, str)
                            if ("посел" in ss or "сельск" in ss or "почтовое отделение" in ss): 
                                cit = True
                if (cit): 
                    if (((i + 1) < len(li)) and (((((((li[i + 1].typ == AddressItemType.HOUSE or li[i + 1].typ == AddressItemType.BLOCK or li[i + 1].typ == AddressItemType.SPACE) or li[i + 1].typ == AddressItemType.PLOT or li[i + 1].typ == AddressItemType.FIELD) or li[i + 1].typ == AddressItemType.BUILDING or li[i + 1].typ == AddressItemType.CORPUS) or li[i + 1].typ == AddressItemType.POSTOFFICEBOX or li[i + 1].typ == AddressItemType.DELIVERYAREA) or li[i + 1].typ == AddressItemType.PART or li[i + 1].typ == AddressItemType.CSP) or li[i + 1].typ == AddressItemType.GENPLAN))): 
                        break
                    if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.NUMBER): 
                        if (li[i].end_token.next0_.is_comma): 
                            if ((isinstance(li[i].referent, GeoReferent)) and not li[i].referent.is_big_city and li[i].referent.is_city): 
                                li[i + 1].typ = AddressItemType.HOUSE
                                li[i + 1].is_doubt = True
                                break
                    if (li[0].typ == AddressItemType.ZIP or li[0].typ == AddressItemType.PREFIX): 
                        break
                    if (MiscLocationHelper.is_user_param_address(li[0])): 
                        break
                    continue
                if (li[i].typ == AddressItemType.REGION): 
                    if ((isinstance(li[i].referent, GeoReferent)) and li[i].referent.higher is not None and li[i].referent.higher.is_city): 
                        if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.HOUSE): 
                            break
            if (i >= len(li)): 
                return None
        if (err and not MiscLocationHelper.is_user_param_address(li[0])): 
            return None
        i0 = i
        if (i > 0 and li[i - 1].typ == AddressItemType.HOUSE and li[i - 1].is_digit): 
            addr.add_slot(AddressReferent.ATTR_HOUSE, li[i - 1].value, False, 0).tag = li[i - 1]
            if (li[i - 1].house_type != AddressHouseType.UNDEFINED): 
                addr.house_type = li[i - 1].house_type
            li[i - 1].tag = (addr)
        elif ((i > 0 and li[i - 1].typ == AddressItemType.KILOMETER and li[i - 1].is_digit) and (i < len(li)) and li[i].is_street_road): 
            addr.add_slot(AddressReferent.ATTR_KILOMETER, li[i - 1].value, False, 0).tag = li[i - 1]
            li[i - 1].tag = (addr)
        else: 
            if (i >= len(li)): 
                i = -1
            i = 0
            first_pass3754 = True
            while True:
                if first_pass3754: first_pass3754 = False
                else: i += 1
                if (not (i < len(li))): break
                if (li[i].tag is not None): 
                    continue
                if (li[i].typ == AddressItemType.CITY or li[i].typ == AddressItemType.REGION or li[i].typ == AddressItemType.COUNTRY): 
                    if (geos is None): 
                        geos = list()
                    if (li[i].is_newline_before): 
                        if (len(geos) > 0): 
                            if ((i > 0 and li[i - 1].typ != AddressItemType.CITY and li[i - 1].typ != AddressItemType.REGION) and li[i - 1].typ != AddressItemType.ZIP and li[i - 1].typ != AddressItemType.PREFIX): 
                                break
                        if (((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.STREET and i > i0): 
                            break
                    if (li[i].detail_type != AddressDetailType.UNDEFINED): 
                        details.append(li[i])
                        li[i].tag = (addr)
                        if (len(geos) > 0): 
                            continue
                    if (len(geos) > 0): 
                        if (li[i].referent.higher == geos[0]): 
                            del geos[0]
                    ii = 0
                    ii = 0
                    while ii < len(geos): 
                        if (geos[ii].is_city): 
                            break
                        ii += 1
                    if (ii >= len(geos)): 
                        geos.append(Utils.asObjectOrNull(li[i].referent, GeoReferent))
                    elif (i > 0 and li[i].is_newline_before and i > i0): 
                        jj = 0
                        jj = 0
                        while jj < i: 
                            if ((li[jj].typ != AddressItemType.PREFIX and li[jj].typ != AddressItemType.ZIP and li[jj].typ != AddressItemType.REGION) and li[jj].typ != AddressItemType.COUNTRY and li[jj].typ != AddressItemType.CITY): 
                                break
                            jj += 1
                        if (jj < i): 
                            break
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.STREET): 
                    if (len(streets) > 0): 
                        if (li[i].is_newline_before): 
                            break
                        if (MiscHelper.can_be_start_of_sentence(li[i].begin_token) and not li[i].begin_token.is_char('(')): 
                            break
                    if (i == (len(li) - 1)): 
                        pass
                    elif (li[i].ref_token is None and i > 0 and li[i - 1].typ != AddressItemType.STREET): 
                        if (li[i - 1].typ == AddressItemType.HOUSE and li[i - 1].house_type == AddressHouseType.SPECIAL): 
                            pass
                        elif (MiscLocationHelper.is_user_param_address(li[i])): 
                            pass
                        else: 
                            break
                    if (len(streets) > 0): 
                        ss = Utils.asObjectOrNull(li[i].referent, StreetReferent)
                        if (ss.kind == StreetKind.ORG and li[i].is_street_detail): 
                            details.append(li[i])
                            li[i].tag = (addr)
                            continue
                    if (len(streets) > 1): 
                        break
                    streets.append(li[i])
                    li[i].tag = (addr)
                elif (li[i].typ == AddressItemType.DETAIL): 
                    if ((i + 1) == len(li) and li[i].detail_type == AddressDetailType.NEAR): 
                        break
                    if (li[i].detail_type == AddressDetailType.NEAR and ((i + 1) < len(li)) and li[i + 1].typ == AddressItemType.CITY): 
                        details.append(li[i])
                        li[i].tag = (addr)
                        i += 1
                    if (li[i].length_char == 1 and li[i].detail_type == AddressDetailType.CROSS and ((((i + 1) == len(li) or li[i + 1].typ != AddressItemType.STREET or i == 0) or li[i - 1].typ != AddressItemType.STREET))): 
                        pass
                    else: 
                        details.append(li[i])
                    li[i].tag = (addr)
                else: 
                    wrapi66 = RefOutArgWrapper(i)
                    inoutres67 = AddressDefineHelper.__add_address_attrs(addr, li, wrapi66, i0, ignore_street, has_genplan)
                    i = wrapi66.value
                    if (inoutres67): 
                        if (i >= len(li) or li[i].tag is not None): 
                            continue
                    elif (i > i0): 
                        if (((li[i].typ == AddressItemType.REGION and li[i0].typ == AddressItemType.STREET and ((i + 1) < len(li))) and li[i + 1].typ != AddressItemType.STREET and li[i + 1].typ != AddressItemType.REGION) and li[i + 1].typ != AddressItemType.CITY): 
                            pass
                        else: 
                            break
        if (len(streets) == 1 and streets[0].orto_terr is not None): 
            streets.insert(0, streets[0].orto_terr)
        typs = list()
        for s in addr.slots: 
            if (not s.type_name in typs): 
                typs.append(s.type_name)
        if (len(streets) == 1 and not streets[0].is_doubt and streets[0].ref_token is None): 
            pass
        elif (len(li) > 2 and li[0].typ == AddressItemType.ZIP and ((li[1].typ == AddressItemType.COUNTRY or li[1].typ == AddressItemType.REGION))): 
            pass
        elif (ignore_street): 
            pass
        elif ((len(typs) + len(streets)) < 2): 
            if (len(typs) > 0): 
                if ((((((typs[0] != AddressReferent.ATTR_STREET and typs[0] != AddressReferent.ATTR_POSTOFFICEBOX and typs[0] != AddressReferent.ATTR_DELIVERYAREA) and metro is None and typs[0] != AddressReferent.ATTR_HOUSE) and typs[0] != AddressReferent.ATTR_HOUSEORPLOT and typs[0] != AddressReferent.ATTR_CORPUS) and typs[0] != AddressReferent.ATTR_BUILDING and typs[0] != AddressReferent.ATTR_PLOT) and typs[0] != AddressReferent.ATTR_DETAIL and typs[0] != AddressReferent.ATTR_ZIP) and len(details) == 0 and not cross): 
                    return None
            elif (len(streets) == 0 and len(details) == 0 and not cross): 
                if ((i > 0 and li[i - 1].typ == AddressItemType.CITY and i > 2) and li[i - 2].typ == AddressItemType.ZIP): 
                    pass
                else: 
                    return None
            elif ((i == len(li) and len(streets) == 1 and (isinstance(streets[0].referent, StreetReferent))) and streets[0].referent.find_slot(StreetReferent.ATTR_TYPE, "квартал", True) is not None and not MiscLocationHelper.is_user_param_address(li[0])): 
                return None
            if (geos is None): 
                has_geo2 = False
                tt = li[0].begin_token.previous
                first_pass3755 = True
                while True:
                    if first_pass3755: first_pass3755 = False
                    else: tt = tt.previous
                    if (not (tt is not None)): break
                    if (tt.morph.class0_.is_preposition or tt.is_comma): 
                        continue
                    r = tt.get_referent()
                    if (r is None): 
                        break
                    if (r.type_name == "DATE" or r.type_name == "DATERANGE"): 
                        continue
                    if (isinstance(r, GeoReferent)): 
                        if (not r.is_state): 
                            if (geos is None): 
                                geos = list()
                            geos.append(Utils.asObjectOrNull(r, GeoReferent))
                            has_geo2 = True
                    break
                if (not has_geo2 and not MiscLocationHelper.is_user_param_address(li[0])): 
                    if (len(streets) > 0 and streets[0].ref_token_is_gsk and streets[0].ref_token is not None): 
                        pass
                    else: 
                        return None
        i = 0
        first_pass3756 = True
        while True:
            if first_pass3756: first_pass3756 = False
            else: i += 1
            if (not (i < len(li))): break
            if (li[i].typ == AddressItemType.PREFIX): 
                li[i].tag = (addr)
            elif (li[i].tag is None): 
                if (li[i].is_newline_before and i > i0): 
                    stop = False
                    j = (i + 1)
                    while j < len(li): 
                        if (li[j].typ == AddressItemType.STREET): 
                            stop = True
                            break
                        j += 1
                    if (stop): 
                        break
                if (li[i].typ == AddressItemType.COUNTRY or li[i].typ == AddressItemType.REGION or li[i].typ == AddressItemType.CITY): 
                    if (geos is None): 
                        geos = list()
                    if (not Utils.asObjectOrNull(li[i].referent, GeoReferent) in geos): 
                        geos.append(Utils.asObjectOrNull(li[i].referent, GeoReferent))
                    if (li[i].typ != AddressItemType.COUNTRY): 
                        if (li[i].detail_type != AddressDetailType.UNDEFINED and addr.detail == AddressDetailType.UNDEFINED): 
                            addr.add_slot(AddressReferent.ATTR_DETAIL, Utils.enumToString(li[i].detail_type).upper(), False, 0).tag = li[i]
                            if (li[i].detail_meters > 0): 
                                addr.add_slot(AddressReferent.ATTR_DETAILPARAM, "{0}м".format(li[i].detail_meters), False, 0)
                    li[i].tag = (addr)
                    continue
                wrapi68 = RefOutArgWrapper(i)
                inoutres69 = AddressDefineHelper.__add_address_attrs(addr, li, wrapi68, i0, ignore_street, has_genplan)
                i = wrapi68.value
                if (not inoutres69): 
                    break
                if (i >= len(li) or li[i].tag is not None): 
                    continue
        t0 = None
        t1 = None
        i = 0
        while i < len(li): 
            if (li[i].tag is not None): 
                t0 = li[i].begin_token
                break
            i += 1
        for i in range(len(li) - 1, -1, -1):
            if (li[i].tag is not None): 
                t1 = li[i].end_token
                break
        else: i = -1
        if (t0 is None or t1 is None): 
            return None
        if (li[len(li) - 1].tag is None and MiscLocationHelper.is_user_param_address(li[0])): 
            ok = True
            for i in range(len(li) - 1, -1, -1):
                if (li[i].tag is not None): 
                    break
                ii = 0
                ii = 0
                while ii < i: 
                    if (str(li[ii]) == str(li[i]) and li[ii].tag is not None): 
                        break
                    ii += 1
                if (ii >= i): 
                    ok = False
                    break
            else: i = -1
            if (ok): 
                t1 = li[len(li) - 1].end_token
        if (geos is not None and len(geos) > 1 and MiscLocationHelper.is_user_param_address(t0)): 
            if (geos[0].higher is None and geos[1].higher is not None): 
                hi = geos[1].higher
                geos[1].higher = None
                if (GeoOwnerHelper.can_be_higher(geos[0], geos[1], None, None) and GeoOwnerHelper.can_be_higher(hi, geos[0], None, None)): 
                    geos[0].higher = hi
                    geos[1].higher = geos[0]
                    del geos[0]
                else: 
                    geos[1].higher = hi
        if (len(addr.slots) == 0): 
            pure_streets = 0
            gsks = 0
            for s in streets: 
                if (s.ref_token is not None and s.ref_token_is_gsk): 
                    gsks += 1
                elif (s.ref_token is None): 
                    pure_streets += 1
            if ((pure_streets + gsks) == 0 and len(streets) > 0): 
                if (((len(details) > 0 or cross)) and geos is not None): 
                    pass
                else: 
                    addr = (None)
            elif (len(streets) < 2): 
                if ((len(streets) == 1 and geos is not None and len(geos) > 0) and ((streets[0].ref_token is None or streets[0].ref_token_is_gsk))): 
                    pass
                elif (len(details) > 0 and geos is not None and len(streets) == 0): 
                    pass
                else: 
                    addr = (None)
        if (addr is not None): 
            if (cross): 
                if (len(streets) > 1 or ((len(streets) == 1 and streets[0].referent2 is not None))): 
                    addr.detail = AddressDetailType.CROSS
            elif (len(details) > 0): 
                ty = AddressDetailType.UNDEFINED
                par = None
                for v in details: 
                    if ((isinstance(v.referent, StreetReferent)) and v.referent.kind == StreetKind.ORG): 
                        org0_ = Utils.asObjectOrNull(v.referent.get_slot_value(StreetReferent.ATTR_REF), Referent)
                        if (org0_ is not None and org0_.type_name == "ORGANIZATION"): 
                            addr.add_slot(AddressReferent.ATTR_DETAILREF, org0_, False, 0)
                            v.referent.move_ext_referent(addr, org0_)
                    elif (v.referent is not None): 
                        addr.add_slot(AddressReferent.ATTR_DETAILREF, v.referent, False, 0)
                        if (v.ref_token is not None): 
                            addr.add_ext_referent(v.ref_token)
                        gg = Utils.asObjectOrNull(v.referent, GeoReferent)
                        if (gg is not None and gg.higher is None and geos is not None): 
                            if (len(geos) > 0 and GeoOwnerHelper.can_be_higher(geos[0], gg, None, None)): 
                                gg.higher = geos[0]
                    elif (v.detail_type == AddressDetailType.ORG and v.ref_token is not None): 
                        addr.add_slot(AddressReferent.ATTR_DETAILREF, v.ref_token.referent, False, 0)
                        addr.add_ext_referent(v.ref_token)
                    if (v.detail_type == AddressDetailType.CROSS and (len(streets) < 2)): 
                        continue
                    if (ty == AddressDetailType.UNDEFINED or v.detail_meters > 0): 
                        if (v.detail_meters > 0): 
                            par = "{0}м".format(v.detail_meters)
                        ty = v.detail_type
                    if (ty == AddressDetailType.UNDEFINED or v.detail_type == AddressDetailType.RANGE): 
                        ty = v.detail_type
                        par = v.value
                    if (v.detail_param is not None): 
                        ty = v.detail_type
                        par = v.detail_param
                if (ty != AddressDetailType.UNDEFINED): 
                    addr.detail = ty
                if (par is not None): 
                    addr.add_slot(AddressReferent.ATTR_DETAILPARAM, par, False, 0)
                else: 
                    for v in li: 
                        if (v.tag is not None and v.detail_meters > 0): 
                            addr.add_slot(AddressReferent.ATTR_DETAILPARAM, "{0}м".format(v.detail_meters), False, 0)
                            break
        if (geos is None and len(streets) > 0 and not streets[0].is_street_road): 
            cou = 0
            tt = t0.previous
            while tt is not None and (cou < 200): 
                if (tt.is_newline_after): 
                    cou += 10
                r = tt.get_referent()
                if ((isinstance(r, GeoReferent)) and not r.is_state): 
                    geos = list()
                    geos.append(Utils.asObjectOrNull(r, GeoReferent))
                    break
                if (isinstance(r, StreetReferent)): 
                    ggg = r.geos
                    if (len(ggg) > 0): 
                        geos = list(ggg)
                        break
                if (isinstance(r, AddressReferent)): 
                    ggg = r.geos
                    if (len(ggg) > 0): 
                        geos = list(ggg)
                        break
                tt = tt.previous; cou += 1
        rt = None
        sr0 = None
        ii = 0
        first_pass3757 = True
        while True:
            if first_pass3757: first_pass3757 = False
            else: ii += 1
            if (not (ii < len(streets))): break
            if ((district is not None and geos is not None and len(geos) == 1) and district.referent is not None and district.ref_token is not None): 
                district.referent.add_slot(GeoReferent.ATTR_TYPE, "район", False, 0)
                distr = Utils.asObjectOrNull(ad.register_referent(district.referent), GeoReferent)
                geos.clear()
                geos.append(distr)
            s = streets[ii]
            sr = Utils.asObjectOrNull(s.referent, StreetReferent)
            if (sr is None or len(sr.slots) == 0): 
                continue
            nam = sr.get_string_value(StreetReferent.ATTR_NAME)
            if (nam is not None): 
                if (nam.startswith("НЕ УКАЗАН") or nam.startswith("НЕ ЗАДАН")): 
                    continue
            if ((s.area_terr is not None and geos is not None and len(geos) == 1) and s.area_terr.referent.higher == geos[0]): 
                geos.clear()
                geos.append(Utils.asObjectOrNull(s.area_terr.referent, GeoReferent))
            if (geos is not None and sr is not None and len(sr.geos) == 0): 
                for gr in geos: 
                    if (gr.is_city or ((gr.higher is not None and gr.higher.is_city)) or ((gr.is_region and sr.kind != StreetKind.UNDEFINED))): 
                        sr.add_slot(StreetReferent.ATTR_GEO, gr, True, 0)
                        if (isinstance(s.referent2, StreetReferent)): 
                            s.referent2.add_slot(StreetReferent.ATTR_GEO, gr, True, 0)
                        if (li[0].referent == gr): 
                            streets[0].begin_token = li[0].begin_token
                        jj = ii + 1
                        while jj < len(streets): 
                            if (isinstance(streets[jj].referent, StreetReferent)): 
                                streets[jj].referent.add_slot(StreetReferent.ATTR_GEO, gr, False, 0)
                            jj += 1
                        geos.remove(gr)
                        break
                    elif (gr.is_region): 
                        ok = False
                        if ((sr.kind == StreetKind.RAILWAY or sr.kind == StreetKind.ROAD or sr.kind == StreetKind.AREA) or sr.kind == StreetKind.SPEC): 
                            ok = True
                        else: 
                            for v in gr.typs: 
                                if (v == "муниципальный округ" or v == "городской округ"): 
                                    ok = True
                        if (ok): 
                            if (li[0].referent == gr): 
                                streets[0].begin_token = li[0].begin_token
                            sr.add_slot(StreetReferent.ATTR_GEO, gr, True, 0)
                            geos.remove(gr)
                            break
            is_reverce = False
            if (sr is not None and len(sr.geos) == 0): 
                if (sr0 is not None): 
                    for g in sr0.geos: 
                        sr.add_slot(StreetReferent.ATTR_GEO, g, False, 0)
                sr0 = sr
            if (s.referent is not None and s.referent.find_slot(StreetReferent.ATTR_NAME, "НЕТ", True) is not None): 
                for ss in s.referent.slots: 
                    if (ss.type_name == StreetReferent.ATTR_GEO): 
                        if (addr is not None): 
                            addr.add_referent(Utils.asObjectOrNull(ss.value, Referent))
            else: 
                if ((sr is not None and ii > 0 and (isinstance(streets[ii - 1].referent, StreetReferent))) and not cross): 
                    sr00 = Utils.asObjectOrNull(streets[ii - 1].referent, StreetReferent)
                    ki = sr00.kind
                    ok2 = False
                    if (ki != sr.kind or ki == StreetKind.AREA or ki == StreetKind.ORG): 
                        if ((sr.kind == StreetKind.AREA or ki == StreetKind.AREA or ki == StreetKind.RAILWAY) or ki == StreetKind.ROAD or ((ki == StreetKind.ORG and sr.kind == StreetKind.UNDEFINED))): 
                            ok2 = True
                    if (ki == StreetKind.ORG and streets[ii - 1].ref_token_is_massive): 
                        ok2 = True
                    if (ki == StreetKind.UNDEFINED and ((sr.kind == StreetKind.ORG or sr.kind == StreetKind.AREA))): 
                        ok2 = True
                    if ((sr.kind == StreetKind.ROAD and sr00.numbers is not None and sr00.numbers.endswith("км")) and sr.numbers is None): 
                        ok2 = True
                        is_reverce = True
                    if (sr.find_slot(StreetReferent.ATTR_NAME, "ОЛИМПИЙСКАЯ ДЕРЕВНЯ", True) is not None): 
                        ok2 = True
                        is_reverce = True
                    if (((not ok2 and len(streets) == 2 and MiscLocationHelper.is_user_param_address(streets[0])) and sr.kind == StreetKind.UNDEFINED and sr00.kind == StreetKind.UNDEFINED) and not sr.can_be_equals(sr00, ReferentsEqualType.WITHINONETEXT)): 
                        ok2 = True
                    if (ok2): 
                        if (sr.kind == StreetKind.AREA or sr.kind == StreetKind.ORG): 
                            if (ki == StreetKind.UNDEFINED): 
                                is_reverce = True
                        if (is_reverce): 
                            streets[ii - 1].end_token = streets[ii].end_token
                            streets[ii - 1].referent.higher = sr
                            streets[ii - 1].referent.add_slot(StreetReferent.ATTR_GEO, None, True, 0)
                        else: 
                            sr.higher = Utils.asObjectOrNull(streets[ii - 1].referent, StreetReferent)
                            sr.add_slot(StreetReferent.ATTR_GEO, None, True, 0)
                            if (addr is not None): 
                                slo = addr.find_slot(AddressReferent.ATTR_STREET, None, True)
                                if (slo is not None): 
                                    addr.slots.remove(slo)
                            s.begin_token = t0
                if (addr is not None): 
                    addr.move_ext_referent(s.referent, None)
                    if (s.referent2 is not None): 
                        addr.move_ext_referent(s.referent2, None)
                hi = ii > 0 and (isinstance(streets[ii - 1].referent, StreetReferent)) and streets[ii - 1].referent.higher == s.referent
                s.referent = ad.register_referent(s.referent)
                if (hi): 
                    streets[ii - 1].referent.higher = Utils.asObjectOrNull(s.referent, StreetReferent)
                if (addr is not None and not is_reverce): 
                    addr.add_referent(s.referent)
                if (s.referent2 is not None): 
                    s.referent2 = ad.register_referent(s.referent2)
                    if (addr is not None and not is_reverce): 
                        addr.add_referent(s.referent2)
                tt = s.begin_token.previous
                first_pass3758 = True
                while True:
                    if first_pass3758: first_pass3758 = False
                    else: tt = tt.previous
                    if (not (tt is not None and tt.begin_char >= t0.begin_char)): break
                    g = Utils.asObjectOrNull(tt.get_referent(), GeoReferent)
                    if (g is None or sr is None): 
                        continue
                    for gg in sr.geos: 
                        if (gg.top_higher == g.top_higher): 
                            s.begin_token = tt
                rt = ReferentToken(s.referent, s.begin_token, s.end_token)
                t = (rt)
                t.kit.embed_token(rt)
                if (is_reverce and (isinstance(t.previous, ReferentToken))): 
                    rt = ReferentToken(t.previous.get_referent(), t.previous, t)
                    t.kit.embed_token(rt)
                    t = (rt)
                if (s.begin_char == t0.begin_char): 
                    t0 = (rt)
                if (s.end_char == t1.end_char): 
                    t1 = (rt)
        if (addr is not None): 
            ok = False
            for s in addr.slots: 
                if (s.type_name != AddressReferent.ATTR_DETAIL): 
                    ok = True
            if ((len(streets) > 0 and streets[0].referent is not None and len(streets[0].referent.slots) == 0) and geos is not None and len(geos) > 0): 
                ok = True
            if (not ok): 
                addr = (None)
        if (addr is None): 
            return t
        if (geos is not None and len(geos) > 0): 
            if ((len(geos) == 1 and geos[0].is_region and len(streets) == 1) and streets[0].ref_token is not None): 
                pass
            if (len(streets) == 1 and streets[0].referent is not None): 
                for s in streets[0].referent.slots: 
                    if (s.type_name == StreetReferent.ATTR_GEO and (isinstance(s.value, GeoReferent))): 
                        k = 0
                        gg = Utils.asObjectOrNull(s.value, GeoReferent)
                        while gg is not None and (k < 5): 
                            for ii in range(len(geos) - 1, -1, -1):
                                if (geos[ii] == gg): 
                                    del geos[ii]
                                    break
                            gg = (Utils.asObjectOrNull(gg.parent_referent, GeoReferent)); k += 1
            while len(geos) >= 2:
                if (geos[1].higher is None and GeoOwnerHelper.can_be_higher(geos[0], geos[1], None, None)): 
                    geos[1].higher = geos[0]
                    del geos[0]
                elif (geos[0].higher is None and GeoOwnerHelper.can_be_higher(geos[1], geos[0], None, None)): 
                    geos[0].higher = geos[1]
                    del geos[1]
                elif (geos[1].higher is not None and geos[1].higher.higher is None and GeoOwnerHelper.can_be_higher(geos[0], geos[1].higher, None, None)): 
                    geos[1].higher.higher = geos[0]
                    del geos[0]
                elif (geos[0].higher is not None and geos[0].higher.higher is None and GeoOwnerHelper.can_be_higher(geos[1], geos[0].higher, None, None)): 
                    geos[0].higher.higher = geos[1]
                    del geos[1]
                else: 
                    break
            for g in geos: 
                addr.add_referent(g)
        ok1 = False
        for s in addr.slots: 
            if (s.type_name != AddressReferent.ATTR_STREET): 
                ok1 = True
                break
        if (not ok1): 
            return t
        if (addr.house is not None and addr.corpus is None and addr.find_slot(AddressReferent.ATTR_STREET, None, True) is None): 
            if (geos is not None and len(geos) > 0 and geos[0].find_slot(GeoReferent.ATTR_NAME, "ЗЕЛЕНОГРАД", True) is not None): 
                addr.corpus = addr.house
                addr.house = None
        for ii in range(len(addr.slots) - 1, -1, -1):
            if (isinstance(addr.slots[ii].value, str)): 
                if ((Utils.asObjectOrNull(addr.slots[ii].value, str)) == "НЕТ"): 
                    del addr.slots[ii]
        if (MiscLocationHelper.is_user_param_address(t1)): 
            hous = False
            wraphous70 = RefOutArgWrapper(False)
            t1 = AddressItemToken.goto_end_of_address(t1, wraphous70)
            hous = wraphous70.value
            if ((hous and addr.house is None and addr.building is None) and addr.house_or_plot is None and addr.corpus is None): 
                addr.house = "0"
        if (ad is not None): 
            addr = (Utils.asObjectOrNull(ad.register_referent(addr), AddressReferent))
        rt = ReferentToken(addr, t0, t1)
        t.kit.embed_token(rt)
        t = (rt)
        if ((t.next0_ is not None and ((t.next0_.is_comma or t.next0_.is_char(';'))) and (t.next0_.whitespaces_after_count < 2)) and (isinstance(t.next0_.next0_, NumberToken))): 
            last = None
            for ll in li: 
                if (ll.tag is not None): 
                    last = ll
            attr_name = None
            if (last is None): 
                return t
            if (last.typ == AddressItemType.HOUSE): 
                attr_name = AddressReferent.ATTR_HOUSE
            elif (last.typ == AddressItemType.CORPUS): 
                attr_name = AddressReferent.ATTR_CORPUS
            elif (last.typ == AddressItemType.BUILDING): 
                attr_name = AddressReferent.ATTR_BUILDING
            elif (last.typ == AddressItemType.FLAT): 
                attr_name = AddressReferent.ATTR_FLAT
            elif (last.typ == AddressItemType.PAVILION): 
                attr_name = AddressReferent.ATTR_PAVILION
            elif (last.typ == AddressItemType.PLOT): 
                attr_name = AddressReferent.ATTR_PLOT
            elif (last.typ == AddressItemType.FIELD): 
                attr_name = AddressReferent.ATTR_FIELD
            elif (last.typ == AddressItemType.GENPLAN): 
                attr_name = AddressReferent.ATTR_GENPLAN
            elif (last.typ == AddressItemType.BOX): 
                attr_name = AddressReferent.ATTR_BOX
            elif (last.typ == AddressItemType.WELL): 
                attr_name = AddressReferent.ATTR_WELL
            elif (last.typ == AddressItemType.CARPLACE): 
                attr_name = AddressReferent.ATTR_CARPLACE
            elif (last.typ == AddressItemType.PART): 
                attr_name = AddressReferent.ATTR_PART
            elif (last.typ == AddressItemType.SPACE): 
                attr_name = AddressReferent.ATTR_SPACE
            elif (last.typ == AddressItemType.POTCH): 
                attr_name = AddressReferent.ATTR_PORCH
            elif (last.typ == AddressItemType.BLOCK): 
                attr_name = AddressReferent.ATTR_BLOCK
            elif (last.typ == AddressItemType.OFFICE): 
                attr_name = AddressReferent.ATTR_OFFICE
            elif (last.typ == AddressItemType.ROOM): 
                attr_name = AddressReferent.ATTR_ROOM
            if (attr_name is not None): 
                t = t.next0_.next0_
                while t is not None: 
                    if (not (isinstance(t, NumberToken))): 
                        break
                    nt = Utils.asObjectOrNull(t, NumberToken)
                    if (nt.int_value is None or nt.int_value > 1000): 
                        break
                    addr1 = Utils.asObjectOrNull(addr.clone(), AddressReferent)
                    addr1.occurrence.clear()
                    addr1.add_slot(attr_name, str(t.value), True, 0)
                    if (ad is not None): 
                        addr1 = (Utils.asObjectOrNull(ad.register_referent(addr1), AddressReferent))
                    rt = ReferentToken(addr1, t, t)
                    t.kit.embed_token(rt)
                    t = (rt)
                    if ((t.next0_ is not None and ((t.next0_.is_comma or t.next0_.is_char(';'))) and (t.next0_.whitespaces_after_count < 2)) and (isinstance(t.next0_.next0_, NumberToken))): 
                        pass
                    else: 
                        break
                    t = t.next0_
        return t
    
    @staticmethod
    def __add_address_attrs(addr : 'AddressReferent', li : typing.List['AddressItemToken'], i : int, i0 : int, ignore_street : bool, has_genplan : bool) -> bool:
        if (li[i.value].typ == AddressItemType.HOUSE): 
            if (addr.house is not None): 
                return False
            if (li[i.value].value is not None or MiscLocationHelper.is_user_param_address(li[i.value])): 
                attr = AddressReferent.ATTR_HOUSE
                if (li[i.value].is_doubt): 
                    attr = AddressReferent.ATTR_HOUSEORPLOT
                    if (((i.value + 1) < len(li)) and (((li[i.value + 1].typ == AddressItemType.FLAT or li[i.value + 1].typ == AddressItemType.POTCH or li[i.value + 1].typ == AddressItemType.FLOOR) or li[i.value + 1].typ == AddressItemType.NUMBER))): 
                        attr = AddressReferent.ATTR_HOUSE
                addr.add_slot(attr, Utils.ifNotNull(li[i.value].value, "0"), False, 0).tag = li[i.value]
                if (li[i.value].house_type != AddressHouseType.UNDEFINED): 
                    addr.house_type = li[i.value].house_type
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.KILOMETER and li[i.value].is_digit and (((i0 < len(li)) and li[i0].is_street_road))): 
            if (addr.kilometer is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_KILOMETER, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.PLOT): 
            if (addr.plot is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_PLOT, Utils.ifNotNull(li[i.value].value, "0"), False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.FIELD): 
            if (addr.field is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_FIELD, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.GENPLAN): 
            if (addr.genplan is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_GENPLAN, Utils.ifNotNull(li[i.value].value, "0"), False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.BOX): 
            if (addr.box is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_BOX, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.WELL): 
            if (addr.well is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_WELL, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.CARPLACE): 
            if (addr.carplace is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_CARPLACE, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.PART and li[i.value].is_digit): 
            if (addr.part is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_PART, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.SPACE): 
            if (addr.space is None): 
                s = addr.add_slot(AddressReferent.ATTR_SPACE, li[i.value].value, False, 0)
                if (s is not None): 
                    s.tag = li[i.value]
                li[i.value].tag = (addr)
            elif (li[i.value].detail_param is None or li[i.value].value is not None): 
                return False
            if (li[i.value].detail_param is not None): 
                dp = li[i.value].detail_param
                addr.add_slot(AddressReferent.ATTR_SPACETYPE, dp, False, 0)
                li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.BLOCK and li[i.value].value is not None): 
            if (addr.block is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_BLOCK, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.CORPUS): 
            if (addr.corpus is not None): 
                return False
            if (li[i.value].value is not None): 
                s = addr.add_slot(AddressReferent.ATTR_CORPUS, li[i.value].value, False, 0)
                if (s is not None): 
                    s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.BUILDING): 
            if (addr.building is not None): 
                return False
            if (li[i.value].value is not None): 
                s = addr.add_slot(AddressReferent.ATTR_BUILDING, li[i.value].value, False, 0)
                if (s is not None): 
                    s.tag = li[i.value]
                if (li[i.value].building_type != AddressBuildingType.UNDEFINED): 
                    addr.building_type = li[i.value].building_type
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.FLOOR and li[i.value].value is not None): 
            if (addr.floor0_ is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_FLOOR, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.POTCH): 
            if (addr.potch is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_PORCH, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.FLAT): 
            if (addr.flat is not None): 
                return False
            if (li[i.value].value is not None): 
                addr.add_slot(AddressReferent.ATTR_FLAT, li[i.value].value, False, 0).tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.PAVILION): 
            if (addr.pavilion is not None): 
                return False
            addr.add_slot(AddressReferent.ATTR_PAVILION, Utils.ifNotNull(li[i.value].value, "0"), False, 0).tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.OFFICE): 
            if (addr.office is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_OFFICE, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.ROOM): 
            if (addr.room is not None): 
                return False
            s = addr.add_slot(AddressReferent.ATTR_ROOM, li[i.value].value, False, 0)
            if (s is not None): 
                s.tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.ZIP): 
            if (addr.zip0_ is not None): 
                return False
            addr.add_slot(AddressReferent.ATTR_ZIP, li[i.value].value, False, 0).tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.CORPUSORFLAT and ((li[i.value].is_digit or li[i.value].value is None))): 
            j = 0
            j = (i.value + 1)
            while j < len(li): 
                if (li[j].is_digit): 
                    if ((((li[j].typ == AddressItemType.FLAT or li[j].typ == AddressItemType.CORPUSORFLAT or li[j].typ == AddressItemType.OFFICE) or li[j].typ == AddressItemType.FLOOR or li[j].typ == AddressItemType.POTCH) or li[j].typ == AddressItemType.DELIVERYAREA or li[j].typ == AddressItemType.POSTOFFICEBOX) or li[j].typ == AddressItemType.BUILDING or li[j].typ == AddressItemType.PAVILION): 
                        break
                j += 1
            if (li[i.value].value is not None): 
                if ((j < len(li)) and addr.corpus is None): 
                    addr.add_slot(AddressReferent.ATTR_CORPUS, li[i.value].value, False, 0).tag = li[i.value]
                elif (addr.corpus is not None): 
                    addr.add_slot(AddressReferent.ATTR_FLAT, li[i.value].value, False, 0).tag = li[i.value]
                elif ((i.value + 2) == len(li) and li[i.value + 1].typ == AddressItemType.NUMBER): 
                    addr.add_slot(AddressReferent.ATTR_CORPUS, li[i.value].value, False, 0).tag = li[i.value]
                    i.value += 1
                    addr.add_slot(AddressReferent.ATTR_FLAT, li[i.value].value, False, 0).tag = li[i.value]
                else: 
                    addr.add_slot(AddressReferent.ATTR_CORPUSORFLAT, li[i.value].value, False, 0).tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.NUMBER and li[i.value].is_digit and ((((not li[i.value].is_newline_before and i.value > 0 and li[i.value - 1].typ == AddressItemType.STREET)) or ignore_street or li[i.value].is_genplan))): 
            v = 0
            wrapv80 = RefOutArgWrapper(0)
            inoutres81 = Utils.tryParseInt(li[i.value].value, wrapv80)
            v = wrapv80.value
            if (not inoutres81): 
                wrapv71 = RefOutArgWrapper(0)
                inoutres72 = Utils.tryParseInt(li[i.value].value[0:0+len(li[i.value].value) - 1], wrapv71)
                v = wrapv71.value
                if (not inoutres72): 
                    if (not "/" in li[i.value].value): 
                        return False
            if (v > 500 and not MiscLocationHelper.is_user_param_address(li[0]) and not ignore_street): 
                return False
            attr = AddressReferent.ATTR_HOUSEORPLOT
            ii = i.value + 1
            if ((ii < len(li)) and li[ii].typ == AddressItemType.DETAIL): 
                ii += 1
            if ((ii < len(li)) and (((((li[ii].typ == AddressItemType.FLAT or li[ii].typ == AddressItemType.CORPUSORFLAT or li[ii].typ == AddressItemType.POTCH) or li[ii].typ == AddressItemType.CORPUS or li[ii].typ == AddressItemType.BUILDING) or li[ii].typ == AddressItemType.FLOOR or li[ii].typ == AddressItemType.NUMBER) or li[ii].typ == AddressItemType.SPACE or ((li[ii].typ == AddressItemType.STREET and li[ii].ref_token_is_gsk))))): 
                attr = AddressReferent.ATTR_HOUSE
            addr.add_slot(attr, li[i.value].value, False, 0).tag = li[i.value]
            if (li[i.value].is_genplan): 
                if (addr.genplan is None): 
                    addr.add_slot(AddressReferent.ATTR_GENPLAN, "0", False, 0)
            li[i.value].tag = (addr)
            if (((i.value + 1) < len(li)) and ((li[i.value + 1].typ == AddressItemType.NUMBER or li[i.value + 1].typ == AddressItemType.FLAT or li[i.value + 1].typ == AddressItemType.CORPUSORFLAT)) and not li[i.value + 1].is_newline_before): 
                wrapv78 = RefOutArgWrapper(0)
                inoutres79 = Utils.tryParseInt(li[i.value + 1].value, wrapv78)
                v = wrapv78.value
                if (inoutres79): 
                    if (v > 500 and not MiscLocationHelper.is_user_param_address(li[0])): 
                        if (((i.value + 2) < len(li)) and li[i.value + 2].typ == AddressItemType.CITY): 
                            pass
                        else: 
                            return False
                i.value += 1
                if ((((li[i.value].typ == AddressItemType.NUMBER or li[i.value].typ == AddressItemType.CORPUSORFLAT)) and li[i.value].value is not None and (i.value + 1) == (len(li) - 1)) and ((li[i.value + 1].typ == AddressItemType.NUMBER or li[i.value + 1].typ == AddressItemType.FLAT))): 
                    addr.add_slot(AddressReferent.ATTR_CORPUS, li[i.value].value, False, 0).tag = li[i.value]
                    li[i.value].tag = (addr)
                    i.value += 1
                    if (li[i.value].value is not None): 
                        addr.add_slot(AddressReferent.ATTR_FLAT, li[i.value].value, False, 0).tag = li[i.value]
                        li[i.value].tag = (addr)
                    return True
                if ((((i.value + 1) < len(li)) and li[i.value + 1].typ == AddressItemType.BUILDING and not li[i.value + 1].is_newline_before) and li[i.value + 1].building_type == AddressBuildingType.LITER): 
                    addr.add_slot(AddressReferent.ATTR_CORPUS, li[i.value].value, False, 0).tag = li[i.value]
                    li[i.value].tag = (addr)
                    return True
                if ((li[i.value].typ == AddressItemType.NUMBER and li[i.value].end_token.next0_ is not None and li[i.value].end_token.next0_.is_comma) and li[i.value].begin_token.previous.is_comma): 
                    if (((i.value + 1) < len(li)) and ((li[i.value + 1].typ == AddressItemType.CORPUS or li[i.value + 1].typ == AddressItemType.CORPUSORFLAT))): 
                        addr.add_slot(AddressReferent.ATTR_BUILDING, li[i.value].value, False, 0).tag = li[i.value]
                        li[i.value].tag = (addr)
                        return True
                    else: 
                        if (li[i.value].begin_token.previous.is_comma and li[i.value].begin_token.previous.previous is not None and li[i.value].begin_token.previous.previous.is_comma): 
                            addr.add_slot(AddressReferent.ATTR_FLAT, li[i.value].value, False, 0).tag = li[i.value]
                        else: 
                            vv = 0
                            wrapvv74 = RefOutArgWrapper(0)
                            inoutres75 = Utils.tryParseInt(Utils.ifNotNull(li[i.value - 1].value, ""), wrapvv74)
                            vv = wrapvv74.value
                            if (not inoutres75): 
                                addr.add_slot(AddressReferent.ATTR_CORPUSORFLAT, li[i.value].value, False, 0).tag = li[i.value]
                            else: 
                                wrapvv73 = RefOutArgWrapper(0)
                                Utils.tryParseInt(Utils.ifNotNull(li[i.value].value, ""), wrapvv73)
                                vv = wrapvv73.value
                                addr.add_slot((AddressReferent.ATTR_CORPUSORFLAT if i.value == (len(li) - 1) and vv > 0 else AddressReferent.ATTR_CORPUS), li[i.value].value, False, 0).tag = li[i.value]
                        li[i.value].tag = (addr)
                        return True
                if ((((i.value + 1) < len(li)) and li[i.value + 1].typ == AddressItemType.NUMBER and not li[i.value + 1].is_newline_before) and (v < 5) and li[i.value].value is not None): 
                    wrapv76 = RefOutArgWrapper(0)
                    inoutres77 = Utils.tryParseInt(li[i.value + 1].value, wrapv76)
                    v = wrapv76.value
                    if (inoutres77): 
                        if ((v < 500) or MiscLocationHelper.is_user_param_address(li[0])): 
                            addr.add_slot(AddressReferent.ATTR_CORPUS, li[i.value].value, False, 0).tag = li[i.value]
                            li[i.value].tag = (addr)
                            i.value += 1
                if ((li[i.value].begin_token.previous.is_hiphen or addr.find_slot(AddressReferent.ATTR_CORPUS, None, True) is not None or li[i.value].value is None) or ((li[i.value].begin_token.previous.is_comma and li[i.value].begin_token.previous.previous is not None and li[i.value].begin_token.previous.previous.is_comma))): 
                    addr.add_slot(AddressReferent.ATTR_FLAT, Utils.ifNotNull(li[i.value].value, ""), False, 0).tag = li[i.value]
                else: 
                    addr.add_slot(AddressReferent.ATTR_CORPUSORFLAT, li[i.value].value, False, 0).tag = li[i.value]
                li[i.value].tag = (addr)
            return True
        if (((not li[i.value].is_newline_before and li[i.value].typ == AddressItemType.NUMBER and li[i.value].is_digit) and li[i.value].value is not None and i.value > 0) and (((li[i.value - 1].typ == AddressItemType.NUMBER or li[i.value - 1].typ == AddressItemType.HOUSE or li[i.value - 1].typ == AddressItemType.BUILDING) or li[i.value - 1].typ == AddressItemType.CORPUS))): 
            if (addr.flat is not None): 
                return False
            if (addr.house is None and addr.building is None and addr.corpus is None): 
                return False
            v = 0
            wrapv82 = RefOutArgWrapper(0)
            inoutres83 = Utils.tryParseInt(li[i.value].value, wrapv82)
            v = wrapv82.value
            if (inoutres83): 
                if (v > 1000): 
                    return False
            if (((i.value + 1) < len(li)) and ((li[i.value + 1].typ == AddressItemType.NUMBER or li[i.value + 1].typ == AddressItemType.FLAT))): 
                addr.add_slot(AddressReferent.ATTR_CORPUS, li[i.value].value, False, 0).tag = li[i.value]
                li[i.value].tag = (addr)
                i.value += 1
                if (li[i.value].value is not None): 
                    addr.add_slot(AddressReferent.ATTR_FLAT, li[i.value].value, False, 0).tag = li[i.value]
                li[i.value].tag = (addr)
            else: 
                addr.add_slot(AddressReferent.ATTR_FLAT, li[i.value].value, False, 0).tag = li[i.value]
                li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.POSTOFFICEBOX): 
            if (addr.post_office_box is not None): 
                return False
            addr.add_slot(AddressReferent.ATTR_POSTOFFICEBOX, Utils.ifNotNull(li[i.value].value, ""), False, 0).tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.DELIVERYAREA): 
            if (addr.delivery_area is not None): 
                return False
            addr.add_slot(AddressReferent.ATTR_DELIVERYAREA, Utils.ifNotNull(li[i.value].value, ""), False, 0).tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (li[i.value].typ == AddressItemType.CSP): 
            if (addr.csp is not None): 
                return False
            addr.add_slot(AddressReferent.ATTR_CSP, li[i.value].value, False, 0).tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if ((li[i.value].typ == AddressItemType.NONUMBER and addr.house is None and addr.plot is None) and addr.house_or_plot is None): 
            addr.add_slot(AddressReferent.ATTR_HOUSEORPLOT, li[i.value].value, False, 0).tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if (((li[i.value].typ == AddressItemType.NUMBER and addr.house is None and addr.corpus is None) and addr.building is None and addr.plot is None) and addr.house_or_plot is None and (((MiscLocationHelper.is_user_param_address(li[i.value]) or has_genplan or ((i.value > 0 and li[i.value - 1].typ == AddressItemType.SPACE))) or i.value == (len(li) - 1)))): 
            if (addr.space is not None and addr.space != "подвал"): 
                addr.add_slot(AddressReferent.ATTR_HOUSE, li[i.value].value, False, 0).tag = li[i.value]
            elif ((i.value + 2) == len(li) and li[i.value + 1].typ == AddressItemType.NUMBER): 
                addr.add_slot(AddressReferent.ATTR_HOUSE, li[i.value].value, False, 0).tag = li[i.value]
                addr.add_slot(AddressReferent.ATTR_FLAT, li[i.value + 1].value, False, 0).tag = li[i.value + 1]
                li[i.value + 1].tag = (addr)
            else: 
                addr.add_slot(AddressReferent.ATTR_HOUSEORPLOT, li[i.value].value, False, 0).tag = li[i.value]
            li[i.value].tag = (addr)
            return True
        if ((li[i.value].typ == AddressItemType.NUMBER and (((addr.house is not None or addr.building is not None or addr.corpus is not None) or addr.house_or_plot is not None)) and i.value > 0) and li[i.value - 1].typ == AddressItemType.SPACE and not li[i.value - 1].is_digit): 
            addr.space = li[i.value].value
            li[i.value].tag = (addr)
            return True
        if ((li[i.value].typ == AddressItemType.NUMBER and i.value > 0 and li[i.value - 1].typ == AddressItemType.FLOOR) and addr.flat is None): 
            addr.flat = li[i.value].value
            li[i.value].tag = (addr)
            return True
        return False