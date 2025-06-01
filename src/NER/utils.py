import re
import typing
import datetime

from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.Referent import Referent
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.date.DateAnalyzer import DateAnalyzer
from pullenti.ner.date.DateRangeReferent import DateRangeReferent
from pullenti.ner.date.DateReferent import DateReferent


_QUARTER_PATTERNS = [
    r"(?P<quarter_num>[1-4РIIVX]{1,3})\s*[-й]*(?:й|ого|му|го|м)?\s*(?:кв\.|квартал[а-яё]*)\b",
    r"\b(?P<quarter_word>перв(?:ый|ого|ому)|втор(?:ой|ого|ому)|трет(?:ий|ьего|ьему)|четверт(?:ый|ого|ому))\s*[-й]*(?:й|ого|му|го|м)?\s*(?:кв\.|квартал[а-яё]*)\b"
]
_QUARTER_MAP_ROMAN = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4}
_QUARTER_MAP_DIGIT_SUFFIX = {'1':1, '2':2, '3':3, '4':4, '1-й':1, '2-й':2, '3-й':3, '4-й':4, '1й':1, '2й':2, '3й':3, '4й':4}
_QUARTER_MAP_WORDS = {'перв': 1, 'втор': 2, 'трет': 3, 'четверт': 4}

def extract_quarter_via_regex(txt: str, context_year: int) -> typing.Optional[dict]:
    """Извлекает дату конца квартала из текста с помощью регулярных выражений."""
    if not (context_year and context_year > 0):
        return None

    for pattern in _QUARTER_PATTERNS:
        match = re.search(pattern, txt, re.IGNORECASE)
        if match:
            q_num = 0
            if match.groupdict().get('quarter_num'):
                q_str = match.group('quarter_num').lower()
                q_num = _QUARTER_MAP_ROMAN.get(q_str) or \
                        _QUARTER_MAP_DIGIT_SUFFIX.get(q_str) or \
                        (int(q_str) if q_str.isdigit() and 1 <= int(q_str) <= 4 else 0)
            elif match.groupdict().get('quarter_word'):
                q_word_part = match.group('quarter_word').lower()[:4]
                q_num = _QUARTER_MAP_WORDS.get(q_word_part, 0)

            if q_num > 0:
                quarter_end_dt = get_quarter_end_date(context_year, q_num)
                if quarter_end_dt:
                    return {
                        'day': quarter_end_dt.day, 
                        'month': quarter_end_dt.month, 
                        'year': quarter_end_dt.year, 
                        'type': 'quarter_end_regex'
                    }
            # Если нашли совпадение по одному паттерну, но не смогли определить квартал,
            # можно либо продолжить с другими паттернами, либо выйти.
            # В текущей логике оригинала, если match есть, но q_num=0, то он перейдет к следующему паттерну.
            # Если q_num > 0 и quarter_end_dt есть, то break был в оригинале, здесь return.
    return None

def parse_pullenti_date_referent(date_ref: DateReferent) -> typing.Optional[dict]:
    """Обрабатывает DateReferent от Pullenti."""
    p_day = date_ref.day if date_ref.day > 0 else 0
    p_month = date_ref.month if date_ref.month > 0 else 0
    p_year = date_ref.year if date_ref.year > 0 else 0
    
    date_info = None
    if p_month > 0: # Месяц обязателен для какой-либо осмысленной даты
        if p_year > 0:
            if p_day > 0:
                date_info = {'day': p_day, 'month': p_month, 'year': p_year, 'type': 'full_dmy_pullenti'}
            else: # Год и месяц есть, дня нет
                date_info = {'day': 1, 'month': p_month, 'year': p_year, 'type': 'month_year_pullenti'}
        else: # Года нет
            if p_day > 0: # Есть день и месяц
                date_info = {'day': p_day, 'month': p_month, 'year': None, 'type': 'day_month_only_pullenti'}
            else: # Есть только месяц
                date_info = {'day': 1, 'month': p_month, 'year': None, 'type': 'month_only_pullenti'}
    return date_info

def parse_pullenti_date_range_referent(
    date_range_ref: DateRangeReferent,
    context_year: typing.Optional[int]
) -> typing.Optional[dict]:
    """Обрабатывает DateRangeReferent от Pullenti, фокусируясь на кварталах."""
    if date_range_ref.quarter > 0:
        quarter_num_pullenti = date_range_ref.quarter
        quarter_year_candidate_pullenti = 0
        if date_range_ref.date_to and date_range_ref.date_to.year > 0:
            quarter_year_candidate_pullenti = date_range_ref.date_to.year
        elif date_range_ref.date_from and date_range_ref.date_from.year > 0:
            quarter_year_candidate_pullenti = date_range_ref.date_from.year
        
        year_for_quarter_pullenti = quarter_year_candidate_pullenti if quarter_year_candidate_pullenti > 0 else context_year
        
        if year_for_quarter_pullenti and year_for_quarter_pullenti > 0:
            quarter_end_dt_pullenti = get_quarter_end_date(year_for_quarter_pullenti, quarter_num_pullenti)
            if quarter_end_dt_pullenti:
                print(f"Pullenti обнаружил квартал Q{quarter_num_pullenti} для года {year_for_quarter_pullenti}, дата конца: {quarter_end_dt_pullenti}")
                return {
                    'day': quarter_end_dt_pullenti.day, 
                    'month': quarter_end_dt_pullenti.month, 
                    'year': quarter_end_dt_pullenti.year, 
                    'type': 'quarter_end_pullenti'
                }
    # Если это не квартал, но есть date_from, можно попробовать его распарсить как DateReferent
    elif date_range_ref.date_from:
        return parse_pullenti_date_referent(date_range_ref.date_from)
    return None

def extract_dates_via_pullenti(txt: str, context_year: typing.Optional[int]) -> typing.List[dict]:
    """Извлекает даты из текста с помощью Pullenti."""
    potential_dates = []
    if not txt:
        return potential_dates

    try:
        with ProcessorService.create_specific_processor(DateAnalyzer.ANALYZER_NAME) as proc:
            analysis_result = proc.process(SourceOfAnalysis(txt))
            entities: typing.List[Referent] = analysis_result.entities
            
            print(f"Анализ текста '{txt}' дал {len(entities)} сущностей Pullenti.")
            for i, entity in enumerate(entities):
                print(f"  Сущность {i}: {type(entity).__name__} - '{str(entity)}'")
                parsed_date_info = None
                if isinstance(entity, DateRangeReferent):
                    parsed_date_info = parse_pullenti_date_range_referent(entity, context_year)
                elif isinstance(entity, DateReferent):
                    parsed_date_info = parse_pullenti_date_referent(entity)
                
                if parsed_date_info:
                    potential_dates.append(parsed_date_info)
    except Exception as e_pullenti:
        print(f"Ошибка при обработке текста '{txt}' с Pullenti: {e_pullenti}")
    return potential_dates


_DATE_TYPE_PREFERENCE_ORDER = [
    'quarter_end_regex',
    'quarter_end_pullenti',
    'full_dmy_pullenti',
    'month_year_pullenti'
]

_CONTEXT_DATE_TYPE_PREFERENCE_ORDER = [
        'day_month_only_pullenti', 
    'month_only_pullenti'
]

def select_best_date_candidate(
    potential_dates: typing.List[dict], 
    context_year: typing.Optional[int]
) -> typing.Optional[dict]:
    """Выбирает наилучший кандидат даты на основе приоритетов."""
    best_date_components = None

    for date_type in _DATE_TYPE_PREFERENCE_ORDER:
        for pd_info in potential_dates:
            if pd_info['type'] == date_type and pd_info.get('year') is not None: # Убедимся, что год есть для основных типов
                best_date_components = pd_info
                print(f"Выбран кандидат по типу '{date_type}': {best_date_components}")
                return best_date_components # Возвращаем первый лучший найденный

    # Если не нашли с годом, и есть контекстный год, ищем даты без года
    if not best_date_components and context_year and context_year > 0:
        for date_type_ctx in _CONTEXT_DATE_TYPE_PREFERENCE_ORDER:
            for pd_info in potential_dates:
                # Ищем только те, где год изначально не был определен
                if pd_info['type'] == date_type_ctx and pd_info.get('year') is None:
                    best_date_components = {
                        'day': pd_info['day'], 
                        'month': pd_info['month'], 
                        'year': context_year, 
                        'type': pd_info['type'].replace('_pullenti', '_context_applied') # Обновляем тип
                    }
                    print(f"Применен контекстный год {context_year} к кандидату типа '{pd_info['type']}': {best_date_components}")
                    return best_date_components # Возвращаем первый лучший найденный с контекстом
    
    if best_date_components: # Если что-то выбрали на предыдущих шагах
         return best_date_components

    # Если ничего не подошло под строгие критерии, но есть хоть какие-то даты с годом
    # (например, если в _DATE_TYPE_PREFERENCE_ORDER были типы, где год мог быть None, но это не наш случай сейчас)
    # Можно добавить еще один проход по всем potential_dates, если нужна менее строгая логика.
    # В текущей логике, если ничего не выбрано, вернется None.
    print(f"Не удалось выбрать приоритетного кандидата из: {potential_dates} с контекстным годом {context_year}")
    return None


def get_quarter_end_date(year: int, quarter: int) -> typing.Optional[datetime.date]:
    """Возвращает последний день указанного квартала."""
    if not (1 <= quarter <= 4) or year <= 0:
        return None
    
    if quarter == 1:
        return datetime.date(year, 3, 31)
    elif quarter == 2:
        return datetime.date(year, 6, 30)
    elif quarter == 3:
        return datetime.date(year, 9, 30)
    elif quarter == 4:
        return datetime.date(year, 12, 31)
    return None

def _normalize_currency_string(value: str) -> typing.Optional[str]:
    """Предварительно обрабатывает и нормализует строку для парсинга валюты."""
    text_to_process = value.strip()
    if not text_to_process:
        return None
    
    if not any(char.isdigit() for char in text_to_process):
        return None 
    
    if any(char.isalpha() for char in text_to_process):
        return None

    s = text_to_process.replace(" ", "")
    s = s.replace(',', '.')

    if not s: 
        return None

    # *** Условие для "двух точек" ***
    # Если после замены запятых на точки в строке есть ".." (две точки подряд),
    # считаем это невалидным форматом для дальнейшей нормализации.
    # _normalize_currency_string вернет None, и format_currency_value вернет исходную строку.
    if ".." in s:
        return None 
    
    # Обработка нескольких точек, которые НЕ идут подряд (например, разделители тысяч "1.234.56")
    if s.count('.') > 1:
        parts = s.split('.')
        integer_part_str = "".join(parts[:-1])
        decimal_part_str = parts[-1]
        
        # Простая валидация для частей (можно усложнить при необходимости)
        is_valid_integer_part = (
            not integer_part_str or 
            integer_part_str == '-' or 
            (integer_part_str.startswith('-') and integer_part_str[1:].isdigit()) or
            integer_part_str.isdigit()
        )
        is_valid_decimal_part = (not decimal_part_str or decimal_part_str.isdigit())

        if not (is_valid_integer_part and is_valid_decimal_part):
            return None 
        
        if integer_part_str == "-" and not decimal_part_str: # Избегаем просто "-"
            return None

        s = f"{integer_part_str}.{decimal_part_str}"
        if s == ".": # Если исходная строка была, например, " . . "
            return None
    
    # Пост-обработка для одиночной точки или нормализованных нескольких точек
    if not s or s == "-": 
        return None

        
    return s

def format_currency_value(value: str) -> str:
    """Форматирует строку, представляющую денежное значение, к виду 'ЧИСЛО,ДД'."""
    original_value_to_return = value 

    normalized_s = _normalize_currency_string(value)
    
    if normalized_s is None:
        return original_value_to_return

    # Паттерн для целого числа с опциональной дробной частью (1 или 2 знака)
    # Позволяет отрицательные числа
    match = re.fullmatch(r"(-?\d+)(\.(\d{1,2}))?", normalized_s)

    if match:
        integer_part = match.group(1)
        # group(2) это точка с дробной частью, group(3) это сама дробная часть
        decimal_digits_str = match.group(3) 

        if decimal_digits_str:
            # Дополняем нулем, если только одна цифра после точки (например, 123.5 -> 123,50)
            formatted_decimal = f"{decimal_digits_str}0" if len(decimal_digits_str) == 1 else decimal_digits_str
            return f"{integer_part},{formatted_decimal}"
        else:
            # Если дробной части нет, добавляем ",00"
            return f"{integer_part},00"
    else:
        # Если строка не соответствует ожидаемому формату после нормализации
        return original_value_to_return