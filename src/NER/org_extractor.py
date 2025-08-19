import re
import logging
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

from pullenti.ner.ExtOntology import ExtOntology
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.AnalysisResult import AnalysisResult
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
from pullenti.ner.org.OrganizationReferent import OrganizationReferent

# ---- Доменные сущности
@dataclass(frozen=True)
class Org:
    name: str     # "ЕВРОСИБЭНЕРГО"
    otype: str    # "АО"

@dataclass(frozen=True)
class Roles:
    seller: Org
    buyer: Org

# ---- Контракты стратегий

class IOrgExtractor:
    def extract(self, text: str) -> Optional[Org]:
        raise NotImplementedError

class IRoleAssigner:
    def assign(self, text: str) -> Optional[Roles]:
        raise NotImplementedError

ORG_TYPES = {
            'АО': 'акционерное общество', 
            'ОАО': 'открытое акционерное общество',
            'ЗАО': 'закрытое акционерное общество',
            'ООО': 'общество с ограниченной ответственностью',
            'ИП': 'индивидуальный предприниматель', 
            'ПАО': 'публичное акционерное общество',
            'ОО': 'общественная организация',
            'НП': 'некоммерческое партнерство',
            'ГУП': 'государственное унитарное предприятие',
            'МУП': 'муниципальное унитарное предприятие',
            'ФГУП': 'федеральное государственное унитарное предприятие',
        }

class _OrgExtractor(IOrgExtractor):
    def __init__(self):
        self.logger = logging.getLogger("app." + __class__.__name__)
    
    def extract(self, text: str) -> Optional[Org]:
        conf_ontology = self._configure_org_ontology()
        conf_ontology.initialize()

        with ProcessorService.create_specific_processor(OrganizationAnalyzer.ANALYZER_NAME) as proc:
            ar: AnalysisResult = proc.process(SourceOfAnalysis(text), conf_ontology)
        candidates: List[Org] = []
        for e0_ in ar.entities:

            if not isinstance(e0_, OrganizationReferent):
                continue
            best_name = self.select_best_org_name_and_type(e0_, text)
            candidates.append(Org(name=best_name['name'], otype=best_name['type']))
        if len(candidates) > 1: 
            candidates = candidates[:2]
        return candidates


    def select_best_org_name_and_type(self, org: OrganizationReferent, full_text: str):
        """
        Приоритет:
        1) Самая длинная «поверхность» по NAME-слотам, найденная в тексте (с дефисами/тире).
        2) Лучшая «поверхность» из occurrence (если 1) не сработал).
        3) Фоллбэк: самая длинная валидная NAME-строка из слотов.
        Везде обрезаем юр-формы по краям и хвосты реквизитов.
        """
        # 1) кандидаты из NAME, реально найденные в тексте
        name_surfaces: list[str] = []
        for s in org.slots:
            if s.type_name != OrganizationReferent.ATTR_NAME:
                continue
            raw = str(s.value).strip()
            if not _looks_valid_org_name(raw):
                continue
            core = _strip_legal_form_edges(raw)
            if not core:
                continue
            surface = _match_surface_in_text_preserve_punct(core, full_text)
            if surface and _looks_valid_org_name(surface):
                name_surfaces.append(surface)

        best_name = ""
        if name_surfaces:
            # Берём самую «содержательную» по длине нормализованного текста
            best_name = max(name_surfaces, key=lambda s: len(_normalize_text(s)))

        # 2) occurrence как резерв
        if not best_name:
            occ = self._best_surface_from_occurrence(org, full_text)
            if _looks_valid_org_name(occ):
                best_name = occ

        # 3) фоллбэк — самая длинная валидная NAME-строка
        if not best_name:
            max_len = 0
            for s in org.slots:
                if s.type_name == OrganizationReferent.ATTR_NAME:
                    raw = _strip_trailing_props(_strip_legal_form_edges(str(s.value).strip().upper()))
                    if _looks_valid_org_name(raw) and len(raw) > max_len:
                        best_name, max_len = raw, len(raw)

        # Тип по словарю
        best_type = ""
        for s in org.slots:
            if s.type_name == OrganizationReferent.ATTR_TYPE:
                type_value = str(s.value).upper()
                if type_value in ORG_TYPES:
                    best_type = type_value
                    break

        # финальная подчистка кавычек/пробелов
        best_name = best_name.strip().strip('«»"“”„\'')
        return {"name": best_name, "type": best_type}
    
    @staticmethod
    def _best_surface_from_occurrence(org: OrganizationReferent, full_text: str) -> str:
        """Возвращает самую длинную форму из фактических вхождений в тексте (сохраняем дефисы), без юр-форм по краям."""
        occs = getattr(org, 'occurrence', None)
        if not occs:
            return ""
        spans = []
        for occ in occs:
            b = getattr(occ, 'begin_char', None)
            e = getattr(occ, 'end_char', None)
            if isinstance(b, int) and isinstance(e, int) and 0 <= b <= e < len(full_text):
                spans.append(full_text[b:e+1])

        if not spans:
            return ""

        # Берём самую «содержательную» (по длине после нормализации)
        surface = max(spans, key=lambda s: len(_normalize_text(s)))
        surface = _strip_legal_form_edges(surface)
        surface = _strip_trailing_props(surface) 
        surface = re.sub(r'\s+', ' ', surface).strip()
        return surface.upper()
    
    @staticmethod
    def _configure_org_ontology() -> ExtOntology:
        """Настраивает онтологию организаций с предопределенными организациями"""
        org_ontos = ExtOntology()
        map_orgs = {
            'РУСАЛ НОВОКУЗНЕЦКИЙ АЛЮМИНИЕВЫЙ ЗАВОД': 'АО',
            'РУСАЛ АЧИНСКИЙ ГЛИНОЗЕМНЫЙ КОМБИНАТ': 'АО',
            'ОК РУСАЛ ТД': 'АО', 
            'РОССИЙСКИЕ ЖЕЛЕЗНЫЕ ДОРОГИ (РЖД)': 'ОАО', 
            'РЖД': 'ОАО'
        }
        org_id_counter = 0
        for org_full_name, org_type in map_orgs.items():
            ontology_item_ref = OrganizationReferent()
            names_to_add_to_ontology = set()
            org_full_name_upper = org_full_name.upper()
            words = org_full_name_upper.split()
            names_to_add_to_ontology.add(org_full_name_upper)
            if len(words) > 1 and words[0] == "РУСАЛ":
                names_to_add_to_ontology.add(" ".join(words[1:]))
            if len(words) > 1:
                current_prefix_parts = []
                for i in range(len(words) - 1):
                    current_prefix_parts.append(words[i])
                    prefix_variant = " ".join(current_prefix_parts)
                    if not (prefix_variant == "РУСАЛ" and words[0] == "РУСАЛ" and len(words) > 1):
                        names_to_add_to_ontology.add(prefix_variant)
            if org_full_name_upper == "РУСАЛ": 
                names_to_add_to_ontology.add("РУСАЛ")
            
            for name_variant in names_to_add_to_ontology:
                ontology_item_ref.add_slot(OrganizationReferent.ATTR_NAME, name_variant, False)
            ontology_item_ref.add_slot(OrganizationReferent.ATTR_TYPE, org_type.upper(), False)
            org_ontos.add_referent(f"org_{org_id_counter}", ontology_item_ref)
            org_id_counter += 1
        return org_ontos

class RegexRoleExtractor(IRoleAssigner):
    def __init__(self):
        self.logger = logging.getLogger("app." + __class__.__name__)
        self.extractor = _OrgExtractor()
    seller_key_words = ['продавец', 'с одной стороны', 'между', 'от продавца']
    buyer_key_words  = ['покупатель', 'с другой стороны', 'от покупателя']

    def assign(self, text: str) -> Optional[Roles]:
        """
        Извлекает организации и назначает роли продавца и покупателя.
        Возвращает Roles с заполненными полями seller и buyer.
        """
        orgs = self.extractor.extract(text)
        roles = self.assign_roles_from_candidates(text, orgs, self.seller_key_words, self.buyer_key_words)
        if not roles:
            return None
        seller_org = next((o for o in orgs if o.name == roles['seller']), None)
        buyer_org = next((o for o in orgs if o.name == roles['buyer']), None)

        seller = Org(name=roles['seller'], otype=seller_org.otype if seller_org else "")
        buyer  = Org(name=roles['buyer'],  otype=buyer_org.otype if buyer_org else "")
        
        if seller.name == 'РОССИЙСКИЕ ЖЕЛЕЗНЫЕ ДОРОГИ':
            seller = Org(name="РОССИЙСКИЕ ЖЕЛЕЗНЫЕ ДОРОГИ (РЖД)", otype=seller.otype)
        
        return Roles(seller=seller, buyer=buyer)

    def assign_roles_from_candidates(self,
        text: str,
        orgs: list[Org],  # [{'name': str, 'type': str}, ...] — возьмём только первые 2
        seller_key_words: list[str],
        buyer_key_words: list[str],
    ) -> dict:
        """
        Возвращает {'seller': <name>, 'buyer': <name>} по правилам:
        1) 'РУСАЛ' -> покупатель
        2) иначе — по близости ключевых слов
        3) иначе — фолбэк: [0]=seller, [1]=buyer
        """
        result = {'seller': '', 'buyer': ''}


        cand = [o.name for o in orgs]
        if not cand:
            return result
        if len(cand) == 1:
            # Если только одна компания, без двусмысленности ставим её как продавца (можно поменять под ваш кейс)
            result['seller'] = cand[0]
            return result

        A, B = cand[0], cand[1]

        # Правило 1: "РУСАЛ" — покупатель
        a_is_rusal = self._contains_rusal(A)
        b_is_rusal = self._contains_rusal(B)
        if a_is_rusal ^ b_is_rusal:
            result['buyer']  = A if a_is_rusal else B
            result['seller'] = B if a_is_rusal else A
            return result
        elif a_is_rusal and b_is_rusal:
            # Оба содержат 'РУСАЛ': покупателем делаем более длинное имя (менее амбигуно)
            if len(_normalize_text(A)) >= len(_normalize_text(B)):
                result['buyer'], result['seller'] = A, B
            else:
                result['buyer'], result['seller'] = B, A
            return result

        # Правило 2: по ключевым словам (ищем ближайшие)
        norm_text = _normalize_text(text)

        # Пытаемся взять "поверхность" имен из текста, чтобы точнее найти позицию
        A_surface = _match_surface_in_text_preserve_punct(A, text) or A
        B_surface = _match_surface_in_text_preserve_punct(B, text) or B

        posA = self._norm_index_of_phrase(A_surface, norm_text)
        posB = self._norm_index_of_phrase(B_surface, norm_text)

        buyer_pos = self._keyword_positions(norm_text, buyer_key_words)
        seller_pos = self._keyword_positions(norm_text, seller_key_words)

        A_b = _nearest_distance(posA, buyer_pos)
        B_b = _nearest_distance(posB, buyer_pos)
        A_s = _nearest_distance(posA, seller_pos)
        B_s = _nearest_distance(posB, seller_pos)

        # Если вообще нет ключевых слов — фолбэк
        if all(d == float('inf') for d in (A_b, B_b, A_s, B_s)):
            result['seller'], result['buyer'] = A, B
            return result

        # Покупателем считаем того, кто ближе к "buyer"-ключам (при равенстве — тот, кто ДАЛЬШЕ от "seller"-ключей)
        if (A_b < B_b) or (A_b == B_b and A_s > B_s):
            result['buyer'], result['seller'] = A, B
        elif (B_b < A_b) or (A_b == B_b and B_s > A_s):
            result['buyer'], result['seller'] = B, A
        else:
            # Если всё равно неоднозначно — смотрим "seller"-близость
            if A_s < B_s:
                result['seller'], result['buyer'] = A, B
            elif B_s < A_s:
                result['seller'], result['buyer'] = B, A
            else:
                # финальный фолбэк
                result['seller'], result['buyer'] = A, B

        return result

    @staticmethod
    def _contains_rusal(name: str) -> bool:
        """Проверка 'РУСАЛ' в названии с нормализацией."""
        return 'русал' in _normalize_text(name)
    
    @staticmethod
    def _norm_index_of_phrase(phrase: str, norm_text: str) -> int:
        """Ищем индекс фразы в НОРМАЛИЗОВАННОМ тексте."""
        if not phrase:
            return -1
        norm_phrase = _normalize_text(phrase)
        return norm_text.find(norm_phrase)
    
    @staticmethod
    def _keyword_positions(norm_text: str, keywords: list[str]) -> list[int]:
        """Собираем позиции ключевых слов в НОРМАЛИЗОВАННОМ тексте (с поддержкой окончаний)."""
        positions = []
        for kw in keywords:
            kw_norm = _normalize_text(kw)
            # Лёгкая лемматизация по корню для покупатель/продавец
            if kw_norm == 'покупатель':
                pattern = r'\bпокупател\w*\b'
            elif kw_norm == 'продавец':
                pattern = r'\bпродавц\w*\b'
            else:
                pattern = r'\b' + re.escape(kw_norm) + r'\b'
            positions.extend(m.start() for m in re.finditer(pattern, norm_text, flags=re.IGNORECASE))
        return positions


# ---- Утилита вывода в нужном формате "Название, Тип"
def to_label(o: Org) -> str:
    return f"{o.name}, {o.otype}"


_LAT2CYR = str.maketrans({
    'A':'А','B':'В','C':'С','E':'Е','H':'Н','K':'К','M':'М','O':'О','P':'Р','T':'Т','X':'Х','Y':'У',
    'a':'а','c':'с','e':'е','o':'о','p':'р','x':'х','y':'у','k':'к','m':'м','h':'н','b':'в','t':'т',
    'R':'Р','r':'р','V':'В','v':'в'
})

def _normalize_text(text: str) -> str:
    """Нормализует текст: лат->кир гомоглифы, нижний регистр, 'ё'->'е', убирает пунктуацию, схлопывает пробелы."""
    if not text:
        return ""
    # Сначала переводим вероятные латинские буквы в кириллицу (важно до нижнего регистра)
    text = text.translate(_LAT2CYR)
    text = text.lower().replace('ё', 'е')
    # Удаляем пунктуацию (оставляем буквы/цифры/пробелы)
    text = re.sub(r'[^\w\s]', ' ', text, flags=re.UNICODE)
    # Схлопываем все виды пробельных в 1 пробел
    text = re.sub(r'\s+', ' ', text, flags=re.UNICODE)
    return text.strip()

def _normalize_for_match(text: str) -> str:
    """Нормализация для поиска: только лат->кир (без лоуеркейса/удаления пунктуации)."""
    return text.translate(_LAT2CYR)

def _charflex(token: str) -> str:
    """
    Разрешить разрывы внутри слова: 'КОМБИНАТ' -> 'к\\s*о\\s*м\\s*б\\s*и\\s*н\\s*а\\s*т'
    Работает поверх _normalize_text(token).
    """
    t = _normalize_text(token)
    parts = [re.escape(ch) + r'\s*' for ch in t]
    return ''.join(parts).rstrip(r'\s*')

def _expand_to_nearest_quotes(full_text: str, start: int, end: int) -> tuple[int, int]:
    """
    Если match попал внутрь кавычек — расширяем до ближайшей парной кавычки.
    Возвращаем (s, e) в координатах исходного текста. Если кавычек нет — исходный span.
    """
    left = max(full_text.rfind('«', 0, start), full_text.rfind('"', 0, start))
    right_1 = full_text.find('»', end)
    right_2 = full_text.find('"', end)
    rights = [i for i in (right_1, right_2) if i != -1]
    right = min(rights) if rights else -1

    if left != -1 and right != -1 and left < start < end < right + 1:
        # включим сами кавычки
        return left, right + 1
    return start, end

def _match_surface_in_text_preserve_punct(name: str, full_text: str) -> str:
    """
    Ищем NAME в тексте, разрешая:
    - пробелы/дефисы между токенами,
    - пробелы ВНУТРИ слов (OCR-разрывы),
    - лат<->кир гомоглифы.
    Возвращаем форму из исходного текста (с дефисами/кавычками), срезав юр-формы и хвосты реквизитов.
    """
    if not name:
        return ""
    tokens = _normalize_text(name).split()
    if not tokens:
        return ""

    # Готовим шаблон: внутри слова — \s*, между словами — (пробел|дефис)+
    token_patterns = [_charflex(tok) for tok in tokens]
    sep = r'(?:\s|[-–—])+'
    pattern = r'\b' + sep.join(token_patterns) + r'\b'

    text4match = _normalize_for_match(full_text)
    m = re.search(pattern, text4match, flags=re.IGNORECASE | re.UNICODE)
    if not m:
        return ""

    # Базовый span по нормализованному тексту → те же индексы в исходном тексте
    s, e = m.start(), m.end()

    # Если внутри кавычек — аккуратно расширим до границ кавычек
    s, e = _expand_to_nearest_quotes(full_text, s, e)

    surface = full_text[s:e]
    surface = _strip_legal_form_edges(surface)
    surface = _strip_trailing_props(surface)
    surface = re.sub(r'\s+', ' ', surface).strip()
    return surface.upper()

def _strip_legal_form_edges(text: str) -> str:
    """Удаляет юр-формы (из ORG_TYPES: и сокращения, и полные фразы) только с краёв строки."""
    if not text:
        return ""
    # Альтернативы из ORG_TYPES: ключи (АО, ООО, ...) + значения (полные фразы)
    alts = [re.escape(k) for k in ORG_TYPES.keys()]
    alts += [re.escape(v) for v in ORG_TYPES.values() if v]
    if not alts:
        return text.strip()

    ALT = r'(?:' + '|'.join(sorted(alts, key=len, reverse=True)) + r')'
    s = text.strip()

    # Нормализуем латиницу в кириллицу (индексы не меняются — посимвольная замена)
    s = s.translate(_LAT2CYR)

    # Срез слева (итеративно)
    while True:
        m = re.match(r'^(?:[«"\(\']*\s*)' + ALT + r'(?:\s+|\s*[-–—]\s*)', s, flags=re.IGNORECASE)
        if not m:
            break
        s = s[m.end():].lstrip()

    # Срез справа (итеративно)
    while True:
        m = re.search(r'(?:\s+|\s*[-–—]\s*)' + ALT + r'(?:[»"\)\']*\s*)$', s, flags=re.IGNORECASE)
        if not m:
            break
        s = s[:m.start()].rstrip()

    return s.strip()

_MISC_TAIL_RE = re.compile(
    r'[\s,]*\(?\s*(?:ИНН|КПП|ОГРН|ОКПО)\s*[:№]?\s*[\d/\-\s]+\)?\s*$',
    flags=re.IGNORECASE | re.UNICODE
)

def _strip_trailing_props(s: str) -> str:
    """Убирает с конца '(... ИНН ...)', ', ИНН:...', 'КПП ...' и т.п. Повторяет до полного удаления."""
    if not s:
        return s
    out = s
    while True:
        new = _MISC_TAIL_RE.sub('', out)
        if new == out:
            break
        out = new
    # подчистим висящие кавычки/знаки после удаления хвоста
    out = out.strip().strip('«»"“”„\' ,;:')
    return out

_CYRILLIC_RE = re.compile(r'[а-яё]', flags=re.IGNORECASE)

def _looks_valid_org_name(name: str) -> bool:
    n = (name or "").strip()
    if len(n) < 3:
        return False
    # Наличие кириллицы (после твоей лат->кир нормализации это надёжный фильтр от AO/OT и пр.)
    if not _CYRILLIC_RE.search(n):
        return False
    return True


def _nearest_distance(pos: int, positions: list[int]) -> float:
    if pos < 0 or not positions:
        return float('inf')
    return min(abs(pos - p) for p in positions)