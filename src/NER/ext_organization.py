from enum import Enum
from typing import Optional
import logging
from dataclasses import dataclass, field
import re

from pydantic import BaseModel

from pullenti.ner.org.OrganizationReferent import OrganizationReferent
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.org.OrganizationAnalyzer import OrganizationAnalyzer
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.AnalysisResult import AnalysisResult
from pullenti.ner.MorphCollection import MorphLang

class Role(Enum):
    SELLER = "продавец"
    BUYER = "покупатель"
    UNKNOWN = "неизвестно"

class Organization(BaseModel):
    """Финальная, публичная модель организации."""
    name: str
    type: list[str]
    type_abbr: Optional[str] = None  # Добавляем поле для аббревиатуры
    name_raw: str
    role: Role

@dataclass(order=True)
class _PotentialOrganization:
    """
    Внутренняя, строго типизированная структура для хранения
    и сортировки потенциальных организаций-кандидатов.
    Сортировка происходит по позиции в тексте, а затем по убыванию длины.
    """
    sort_index: tuple[int, int] = field(init=False, repr=False)
    
    # Поля ниже не участвуют в сравнении для сортировки
    start: int = field(compare=False)
    end: int = field(compare=False)
    name_raw: str = field(compare=False)
    ref: OrganizationReferent = field(compare=False)
    types: list[str] = field(compare=False)

    def __post_init__(self):
        # Задаем поля для сортировки: сначала по позиции, потом по убыванию длины
        self.sort_index = (self.start, -len(self.name_raw))

class ExtOrganization:

    def __init__(self):
        self.logger = logging.getLogger('app.' + __class__.__name__)
        # Паттерн для удаления мусора в конце названия организации
        self._clean_pattern = re.compile(r'[,]?\s*\(?ИНН/КПП.*|\s*\(?ИНН.*', re.IGNORECASE)
        # Словарь префиксов организаций
        self.ORG_PREFIXES = {
            'ооо', 'оао', 'зао', 'пао', 'ао', 'ип',
            'общество с ограниченной ответственностью',
            'открытое акционерное общество',
            'закрытое акционерное общество',
            'публичное акционерное общество',
            'акционерное общество',
            'индивидуальный предприниматель'
        }
        # Добавляем шаблон для нормализации пробелов и переносов строк
        self._normalize_pattern = re.compile(r'\s+')

    def _get_abbr_type(self, types: list[str]) -> Optional[str]:
        """Находит самую короткую аббревиатуру в списке типов."""
        if not types:
            return None
        # Убираем точки и приводим к нижнему регистру для сравнения
        cleaned_types = [t.replace('.', '').lower() for t in types]
        # Находим самую короткую строку, которая скорее всего и есть аббревиатура
        return min(cleaned_types, key=len).upper()

    def _clean_raw_name(self, raw_name: str) -> str:
        """Удаляет из сырого названия организации лишние части (ИНН, КПП и т.д.)."""
        return self._clean_pattern.sub('', raw_name).strip()
    
    def _normalize_text(self, text: str) -> str:
        """Нормализует текст, заменяя множественные пробелы и переносы строк одним пробелом."""
        return self._normalize_pattern.sub(' ', text).strip()

    def extract(self, text: str) -> list[Organization]:
        """
        Извлекает все организации из текста, используя строго типизированный
        подход для фильтрации и объединения результатов для повышения точности.

        Args:
            text: Исходный текст для анализа.

        Returns:
            Список извлеченных организаций.
        """
        # Создаем дополнительную версию текста с нормализованными пробелами для поиска
        normalized_text = self._normalize_text(text)
        
        with ProcessorService.create_specific_processor(OrganizationAnalyzer.ANALYZER_NAME) as processor:
            result = processor.process(SourceOfAnalysis(text))
            # Для поиска дополнительных организаций используем нормализованный текст
            normalized_result = processor.process(SourceOfAnalysis(normalized_text))

        self.logger.debug(f"Результат анализа: {result}")
        
        # Собрать всех кандидатов из обоих вариантов текста
        potential_orgs = self._collect_potential_organizations(text, result)
        normalized_orgs = self._collect_potential_organizations(normalized_text, normalized_result, is_normalized=True)
        
        # Объединяем результаты, избегая дубликатов
        all_potential_orgs = []
        seen_names = set()
        
        for org in potential_orgs:
            clean_name = self._normalize_text(self._clean_raw_name(org.name_raw))
            if clean_name not in seen_names:
                seen_names.add(clean_name)
                all_potential_orgs.append(org)
        
        for org in normalized_orgs:
            clean_name = self._normalize_text(self._clean_raw_name(org.name_raw))
            if clean_name not in seen_names:
                seen_names.add(clean_name)
                all_potential_orgs.append(org)
                
        if not all_potential_orgs:
            return []

        # Отсортировать кандидатов
        all_potential_orgs.sort()

        # Отфильтровать вложенные сущности, оставив только самые полные
        return self._filter_nested_organizations(all_potential_orgs)

    def _collect_potential_organizations(self, text: str, result: AnalysisResult, is_normalized: bool = False) -> list[_PotentialOrganization]:
        """Собирает всех кандидатов в организации из результатов анализа."""
        candidates = []
        for org_ref in result.entities:
            if isinstance(org_ref, OrganizationReferent) and org_ref.occurrence:
                first_occurrence = org_ref.occurrence[0]
                raw_name_from_text = text[first_occurrence.begin_char : first_occurrence.end_char + 1].strip()
                
                # Проверяем, является ли кандидат валидной организацией
                is_valid_org = False
                # 1. Проверка на наличие кавычек
                if '"' in raw_name_from_text or '«' in raw_name_from_text:
                    is_valid_org = True
                # 2. Проверка на наличие префикса
                else:
                    normalized_name = self._normalize_text(raw_name_from_text.lower())
                    for prefix in self.ORG_PREFIXES:
                        if normalized_name.startswith(prefix):
                            is_valid_org = True
                            break
                # 3. Проверка на наличие аббревиатуры организации в начале
                if not is_valid_org and re.match(r'^[А-ЯA-Z]{2,4}\s+"', raw_name_from_text):
                    is_valid_org = True
                    
                if not is_valid_org:
                    self.logger.debug(f"Пропускаем невалидного кандидата: '{raw_name_from_text}'")
                    continue

                candidates.append(_PotentialOrganization(
                    ref=org_ref,
                    name_raw=raw_name_from_text,
                    types=org_ref.get_string_values(OrganizationReferent.ATTR_TYPE),
                    start=first_occurrence.begin_char,
                    end=first_occurrence.end_char
                ))
                
                # Для нормализованного текста нам может понадобиться исходное имя
                if is_normalized:
                    # Ищем в исходном тексте все вхождения нормализованного имени организации
                    # Этот шаг помогает найти организации с разрывами строк в исходном тексте
                    alt_names = self._find_alternative_names_in_text(text, raw_name_from_text)
                    for alt_name in alt_names:
                        if alt_name != raw_name_from_text:
                            candidates.append(_PotentialOrganization(
                                ref=org_ref,
                                name_raw=alt_name,
                                types=org_ref.get_string_values(OrganizationReferent.ATTR_TYPE),
                                start=text.find(alt_name),  # Примерная позиция
                                end=text.find(alt_name) + len(alt_name)  # Примерная позиция
                            ))
        return candidates
    
    def _find_alternative_names_in_text(self, original_text: str, normalized_name: str) -> list[str]:
        """
        Находит альтернативные написания организации в исходном тексте,
        учитывая разрывы строк и особенности форматирования.
        """
        result = []
        # Разбиваем нормализованное имя на части, которые можно искать в тексте
        parts = normalized_name.split()
        if not parts:
            return []
            
        # Ищем первую часть в тексте
        first_part = parts[0]
        positions = []
        start_pos = 0
        while start_pos < len(original_text):
            pos = original_text.find(first_part, start_pos)
            if pos == -1:
                break
            positions.append(pos)
            start_pos = pos + len(first_part)
            
        # Для каждой найденной позиции пытаемся собрать полное имя организации
        for start_pos in positions:
            remaining_parts = parts[1:]
            current_pos = start_pos + len(first_part)
            found_all = True
            
            # Максимальная длина текста для поиска следующей части
            search_window = 200
            
            for part in remaining_parts:
                # Ищем следующую часть в ограниченном окне текста
                window_text = original_text[current_pos:current_pos + search_window]
                part_pos = window_text.find(part)
                
                if part_pos == -1:
                    found_all = False
                    break
                
                current_pos += part_pos + len(part)
            
            if found_all:
                # Извлекаем фрагмент текста от начала до конца найденной организации
                extracted_name = original_text[start_pos:current_pos].strip()
                # Проверяем, что извлеченное имя включает все части
                if all(part in extracted_name for part in parts):
                    result.append(extracted_name)
                    
        return result

    def _filter_nested_organizations(self, sorted_orgs: list[_PotentialOrganization]) -> list[Organization]:
        """Отсеивает вложенные организации, оставляя только самые внешние и полные."""
        final_orgs: list[Organization] = []
        last_end_pos = -1
        seen_names = set()  # Для отслеживания уже добавленных организаций

        for org_candidate in sorted_orgs:
            if org_candidate.start < last_end_pos:
                self.logger.debug(f"Пропускаем вложенную/дублирующую организацию: '{org_candidate.name_raw}'")
                continue
            
            clean_name_raw = self._clean_raw_name(org_candidate.name_raw)
            normalized_name = self._normalize_text(clean_name_raw)
            
            # Избегаем дубликатов по нормализованному имени
            if normalized_name in seen_names:
                continue
                
            seen_names.add(normalized_name)
            abbr_type = self._get_abbr_type(org_candidate.types)

            self.logger.debug(f"Финальная организация: '{clean_name_raw}' (Тип: {abbr_type})")
            
            final_orgs.append(Organization(
                name=org_candidate.ref.to_string_ex(MorphLang.RU, 0),
                type=org_candidate.types,
                type_abbr=abbr_type,
                name_raw=clean_name_raw,
                role=Role.UNKNOWN
            ))
            last_end_pos = org_candidate.end
            
        return final_orgs




