import pytest
import datetime
from unittest.mock import patch, MagicMock

from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.date.DateRangeReferent import DateRangeReferent
from pullenti.ner.date.DateAnalyzer import DateAnalyzer
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.ProcessorService import ProcessorService


from src.NER.utils import (
    get_quarter_end_date,
    extract_quarter_via_regex,
    parse_pullenti_date_referent,
    parse_pullenti_date_range_referent,
    extract_dates_via_pullenti,
    select_best_date_candidate,
    format_currency_value
)


class MockDateReferent:
    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return f"MockDateReferent(d={self.day}, m={self.month}, y={self.year})"

class MockDateRangeReferent:
    def __init__(self, quarter=0, date_from=None, date_to=None):
        self.quarter = quarter
        self.date_from = date_from
        self.date_to = date_to

    def __str__(self):
        return f"MockDateRangeReferent(q={self.quarter}, from={self.date_from}, to={self.date_to})"


class TestGetQuarterEndDate:
    @pytest.mark.parametrize("year, quarter, expected_date_tuple", [
        (2023, 1, (2023, 3, 31)),
        (2023, 2, (2023, 6, 30)),
        (2023, 3, (2023, 9, 30)),
        (2023, 4, (2023, 12, 31)),
        (2024, 1, (2024, 3, 31)), # високосный год, но на эти даты не влияет
    ])
    def test_valid_quarters(self, year, quarter, expected_date_tuple):
        expected = datetime.date(expected_date_tuple[0], expected_date_tuple[1], expected_date_tuple[2])
        assert get_quarter_end_date(year, quarter) == expected

    @pytest.mark.parametrize("year, quarter", [
        (2023, 0),
        (2023, 5),
        (0, 1),
        (-1, 1),
    ])
    def test_invalid_input(self, year, quarter):
        assert get_quarter_end_date(year, quarter) is None


class TestExtractQuarterViaRegex:
    @pytest.mark.parametrize("text, year, expected_result_dict", [
        ("1 квартал 2023", 2023, {'day': 31, 'month': 3, 'year': 2023, 'type': 'quarter_end_regex'}),
        ("отчет за II-й квартал", 2024, {'day': 30, 'month': 6, 'year': 2024, 'type': 'quarter_end_regex'}),
        ("4-й квартал", 2023, {'day': 31, 'month': 12, 'year': 2023, 'type': 'quarter_end_regex'}),
        ("Первый квартал", 2023, {'day': 31, 'month': 3, 'year': 2023, 'type': 'quarter_end_regex'}),
    ])
    def test_found_quarter(self, text, year, expected_result_dict):
        assert extract_quarter_via_regex(text, year) == expected_result_dict

    @pytest.mark.parametrize("text, year", [
        ("5 квартал", 2023),
        ("не квартал", 2023),
        ("1 квартал", 0), # Невалидный год
        ("1 квартал", None),
    ])
    def test_not_found_quarter(self, text, year):
        assert extract_quarter_via_regex(text, year) is None

    def test_no_context_year(self):
        assert extract_quarter_via_regex("1 квартал", None) is None


class TestParsePullentiDateReferent:
    def test_full_dmy(self):
        ref = MockDateReferent(day=15, month=7, year=2023)
        assert parse_pullenti_date_referent(ref) == {'day': 15, 'month': 7, 'year': 2023, 'type': 'full_dmy_pullenti'}

    def test_month_year(self):
        ref = MockDateReferent(month=7, year=2023) # day=0
        assert parse_pullenti_date_referent(ref) == {'day': 1, 'month': 7, 'year': 2023, 'type': 'month_year_pullenti'}

    def test_day_month_only(self):
        ref = MockDateReferent(day=15, month=7) # year=0
        assert parse_pullenti_date_referent(ref) == {'day': 15, 'month': 7, 'year': None, 'type': 'day_month_only_pullenti'}

    def test_month_only(self):
        ref = MockDateReferent(month=7) # day=0, year=0
        assert parse_pullenti_date_referent(ref) == {'day': 1, 'month': 7, 'year': None, 'type': 'month_only_pullenti'}
    
    def test_no_month(self):
        ref = MockDateReferent(day=15, year=2023) # month=0
        assert parse_pullenti_date_referent(ref) is None

    def test_empty_referent(self):
        ref = MockDateReferent()
        assert parse_pullenti_date_referent(ref) is None


class TestParsePullentiDateRangeReferent:
    def test_quarter_with_year_from_date_to(self):
        date_to_ref = MockDateReferent(year=2023)
        range_ref = MockDateRangeReferent(quarter=1, date_to=date_to_ref)
        assert parse_pullenti_date_range_referent(range_ref, 2022) == \
               {'day': 31, 'month': 3, 'year': 2023, 'type': 'quarter_end_pullenti'}

    def test_quarter_with_year_from_date_from(self):
        date_from_ref = MockDateReferent(year=2023)
        range_ref = MockDateRangeReferent(quarter=2, date_from=date_from_ref)
        assert parse_pullenti_date_range_referent(range_ref, 2022) == \
               {'day': 30, 'month': 6, 'year': 2023, 'type': 'quarter_end_pullenti'}

    def test_quarter_with_context_year(self):
        range_ref = MockDateRangeReferent(quarter=3)
        assert parse_pullenti_date_range_referent(range_ref, 2023) == \
               {'day': 30, 'month': 9, 'year': 2023, 'type': 'quarter_end_pullenti'}

    def test_quarter_no_year_available(self):
        range_ref = MockDateRangeReferent(quarter=4)
        assert parse_pullenti_date_range_referent(range_ref, None) is None

    def test_not_quarter_delegates_to_date_from(self):
        date_from_ref = MockDateReferent(day=10, month=5, year=2023)
        range_ref = MockDateRangeReferent(date_from=date_from_ref)
        expected = parse_pullenti_date_referent(date_from_ref)
        assert parse_pullenti_date_range_referent(range_ref, 2023) == expected
    
    def test_empty_range_referent(self):
        range_ref = MockDateRangeReferent()
        assert parse_pullenti_date_range_referent(range_ref, 2023) is None

class TestSelectBestDateCandidate:
    def test_priority_quarter_regex(self):
        dates = [
            {'day': 1, 'month': 1, 'year': 2023, 'type': 'full_dmy_pullenti'},
            {'day': 31, 'month': 3, 'year': 2023, 'type': 'quarter_end_regex'}
        ]
        assert select_best_date_candidate(dates, 2023) == dates[1]

    def test_priority_quarter_pullenti_over_full_dmy(self):
        dates = [
            {'day': 1, 'month': 1, 'year': 2023, 'type': 'full_dmy_pullenti'},
            {'day': 30, 'month': 6, 'year': 2023, 'type': 'quarter_end_pullenti'}
        ]
        assert select_best_date_candidate(dates, 2023) == dates[1]

    def test_priority_full_dmy_over_month_year(self):
        dates = [
            {'day': 1, 'month': 7, 'year': 2023, 'type': 'month_year_pullenti'},
            {'day': 15, 'month': 7, 'year': 2023, 'type': 'full_dmy_pullenti'}
        ]
        assert select_best_date_candidate(dates, 2023) == dates[1]
    
    def test_context_year_day_month_only(self):
        dates = [
            {'day': 20, 'month': 8, 'year': None, 'type': 'day_month_only_pullenti'}
        ]
        expected = {'day': 20, 'month': 8, 'year': 2024, 'type': 'day_month_only_context_applied'}
        assert select_best_date_candidate(dates, 2024) == expected

    def test_context_year_month_only(self):
        dates = [
            {'day': 1, 'month': 9, 'year': None, 'type': 'month_only_pullenti'}
        ]
        expected = {'day': 1, 'month': 9, 'year': 2024, 'type': 'month_only_context_applied'}
        assert select_best_date_candidate(dates, 2024) == expected

    def test_no_suitable_candidate(self):
        dates = [
            {'day': 10, 'month': 10, 'year': None, 'type': 'day_month_only_pullenti'}
        ]
        assert select_best_date_candidate(dates, None) is None
        assert select_best_date_candidate([], 2023) is None

    def test_candidate_without_year_not_selected_if_not_contextual(self):
        dates = [
            {'day': 1, 'month': 1, 'year': None, 'type': 'day_month_only_pullenti'}
        ]
        # Этот тип требует контекстного года, но он не будет выбран, если приоритетные типы с годом отсутствуют
        # и контекстный год не применяется (например, если он None)
        assert select_best_date_candidate(dates, None) is None


class TestFormatCurrencyValue:
    @pytest.mark.parametrize("input_str, expected_str", [
        # Основные случаи
        ("123456789", "1234567,89"),
        ("12345", "123,45"),
        ("123", "1,23"),
        ("12", "0,12"),
        ("1", "0,01"),
        
        # С различными разделителями и символами
        ("1.234.567,89", "1234567,89"),
        ("1,234,567.89", "1234567,89"),
        ("1 234 567,89", "1234567,89"),
        ("1.234.567,89руб.", "1234567,89"),
        ("1,234,567.89..", "1234567,89"),  # Ваш проблемный случай
        
        # С символами валюты и специальными символами
        ("$12345", "123,45"),
        ("€12345", "123,45"),
        ("¥12345", "123,45"),
        ("12345 руб.", "123,45"),
        (";12345/[<]", "123,45"),
        ("|;12345|", "123,45"),


        # Отрицательные числа (знак минус игнорируется)
        ("-12345", "123,45"),
        
        # Граничные случаи
        ("0", "0,00"),
        ("00", "0,00"),
        ("000", "0,00"),
        ("100", "1,00"),
        ("1000", "10,00"),
        ("10000", "100,00"),
        
    ])
    def test_valid_normalizations(self, input_str, expected_str):
        assert format_currency_value(input_str) == expected_str

    @pytest.mark.parametrize("input_str", [
        "abc",
        "123a.45",
        "",
        "   ",
        "только текст",
        ".",
        ",",
    ])
    def test_invalid_strings(self, input_str):
        assert format_currency_value(input_str) is None



class TestExtractDatesViaPullenti:
    @patch('src.NER.utils.parse_pullenti_date_range_referent')
    @patch('src.NER.utils.parse_pullenti_date_referent')
    @patch('src.NER.utils.ProcessorService')
    def test_empty_text(self, mock_proc_service, mock_parse_date, mock_parse_range):
        result = extract_dates_via_pullenti("", 2023)
        assert result == []
        mock_proc_service.create_specific_processor.assert_not_called()

    @patch('src.NER.utils.parse_pullenti_date_range_referent')
    @patch('src.NER.utils.parse_pullenti_date_referent')
    @patch('src.NER.utils.ProcessorService')
    def test_no_dates_found_by_pullenti(self, mock_proc_service, mock_parse_date, mock_parse_range):
        mock_analysis_result = MagicMock()
        mock_analysis_result.entities = []
        
        mock_proc_instance = MagicMock()
        mock_proc_instance.process.return_value = mock_analysis_result
        mock_proc_service.create_specific_processor.return_value.__enter__.return_value = mock_proc_instance

        result = extract_dates_via_pullenti("текст без дат", 2023)
        
        assert result == []
        mock_proc_service.create_specific_processor.assert_called_once_with(DateAnalyzer.ANALYZER_NAME)
        mock_proc_instance.process.assert_called_once()
        call_args, _ = mock_proc_instance.process.call_args
        assert isinstance(call_args[0], SourceOfAnalysis)
        assert call_args[0].text == "текст без дат"
        mock_parse_date.assert_not_called()
        mock_parse_range.assert_not_called()

    @patch('src.NER.utils.parse_pullenti_date_range_referent')
    @patch('src.NER.utils.parse_pullenti_date_referent')
    @patch('src.NER.utils.ProcessorService')
    def test_single_date_referent(self, mock_proc_service, mock_parse_date, mock_parse_range):
        mock_entity_date = MagicMock(spec=DateReferent)
        
        mock_analysis_result = MagicMock()
        mock_analysis_result.entities = [mock_entity_date]
        
        mock_proc_instance = MagicMock()
        mock_proc_instance.process.return_value = mock_analysis_result
        mock_proc_service.create_specific_processor.return_value.__enter__.return_value = mock_proc_instance
        
        expected_parsed_date = {'day': 10, 'month': 1, 'year': 2023, 'type': 'full_dmy_pullenti'}
        mock_parse_date.return_value = expected_parsed_date
        mock_parse_range.return_value = None # На случай, если логика в utils будет пытаться парсить как оба типа

        result = extract_dates_via_pullenti("10 января 2023", 2023)
        
        assert result == [expected_parsed_date]
        mock_parse_date.assert_called_once_with(mock_entity_date)
        # В зависимости от реализации цикла в utils, mock_parse_range может быть вызван или нет.
        # Если есть четкое if/elif isinstance, то не будет. Если просто последовательные вызовы, то будет.
        # Предполагаем if/elif, поэтому mock_parse_range.assert_not_called() или mock_parse_range.return_value = None

    @patch('src.NER.utils.parse_pullenti_date_range_referent')
    @patch('src.NER.utils.parse_pullenti_date_referent')
    @patch('src.NER.utils.ProcessorService')
    def test_single_date_range_referent(self, mock_proc_service, mock_parse_date, mock_parse_range):
        mock_entity_range = MagicMock(spec=DateRangeReferent)

        mock_analysis_result = MagicMock()
        mock_analysis_result.entities = [mock_entity_range]

        mock_proc_instance = MagicMock()
        mock_proc_instance.process.return_value = mock_analysis_result
        mock_proc_service.create_specific_processor.return_value.__enter__.return_value = mock_proc_instance

        expected_parsed_range = {'day': 31, 'month': 3, 'year': 2023, 'type': 'quarter_end_pullenti'}
        mock_parse_range.return_value = expected_parsed_range
        mock_parse_date.return_value = None

        context_year = 2023
        result = extract_dates_via_pullenti("1 квартал 2023", context_year)

        assert result == [expected_parsed_range]
        mock_parse_range.assert_called_once_with(mock_entity_range, context_year)
        # mock_parse_date.assert_not_called() or mock_parse_date.return_value = None

    @patch('src.NER.utils.parse_pullenti_date_range_referent')
    @patch('src.NER.utils.parse_pullenti_date_referent')
    @patch('src.NER.utils.ProcessorService')
    def test_mixed_entities(self, mock_proc_service, mock_parse_date, mock_parse_range):
        mock_entity_date = MagicMock(spec=DateReferent)
        mock_entity_range = MagicMock(spec=DateRangeReferent)

        mock_analysis_result = MagicMock()
        mock_analysis_result.entities = [mock_entity_date, mock_entity_range]

        mock_proc_instance = MagicMock()
        mock_proc_instance.process.return_value = mock_analysis_result
        mock_proc_service.create_specific_processor.return_value.__enter__.return_value = mock_proc_instance

        parsed_date = {'day': 5, 'month': 5, 'year': 2022, 'type': 'full_dmy_pullenti'}
        parsed_range = {'day': 30, 'month': 6, 'year': 2022, 'type': 'quarter_end_pullenti'}
        
        # Настройка side_effect, чтобы возвращать разные значения для разных вызовов/аргументов
        def parse_date_side_effect(entity):
            if entity == mock_entity_date:
                return parsed_date
            return None
        
        def parse_range_side_effect(entity, year):
            if entity == mock_entity_range:
                return parsed_range
            return None

        mock_parse_date.side_effect = parse_date_side_effect
        mock_parse_range.side_effect = parse_range_side_effect
        
        context_year = 2022
        result = extract_dates_via_pullenti("смешанный текст", context_year)

        assert len(result) == 2
        assert parsed_date in result
        assert parsed_range in result
        
        mock_parse_date.assert_any_call(mock_entity_date)
        mock_parse_range.assert_any_call(mock_entity_range, context_year)

    @patch('src.NER.utils.parse_pullenti_date_range_referent')
    @patch('src.NER.utils.parse_pullenti_date_referent')
    @patch('src.NER.utils.ProcessorService')
    def test_parser_returns_none(self, mock_proc_service, mock_parse_date, mock_parse_range):
        mock_entity_date = MagicMock(spec=DateReferent)
        
        mock_analysis_result = MagicMock()
        mock_analysis_result.entities = [mock_entity_date]
        
        mock_proc_instance = MagicMock()
        mock_proc_instance.process.return_value = mock_analysis_result
        mock_proc_service.create_specific_processor.return_value.__enter__.return_value = mock_proc_instance
        
        mock_parse_date.return_value = None
        mock_parse_range.return_value = None

        result = extract_dates_via_pullenti("непонятная дата", 2023)
        
        assert result == []
        mock_parse_date.assert_called_once_with(mock_entity_date)

    @patch('builtins.print')
    @patch('src.NER.utils.parse_pullenti_date_range_referent')
    @patch('src.NER.utils.parse_pullenti_date_referent')
    @patch('src.NER.utils.ProcessorService')
    def test_pullenti_exception(self, mock_proc_service, mock_parse_date, mock_parse_range, mock_print):
        mock_proc_service.create_specific_processor.side_effect = Exception("Pullenti Service Error")

        result = extract_dates_via_pullenti("текст вызывающий ошибку", 2023)
        
        assert result == []
        mock_parse_date.assert_not_called()
        mock_parse_range.assert_not_called()
        mock_print.assert_called_once_with("Ошибка при обработке текста \'текст вызывающий ошибку\' с Pullenti: Pullenti Service Error")

    @patch('src.NER.utils.parse_pullenti_date_range_referent')
    @patch('src.NER.utils.parse_pullenti_date_referent')
    @patch('src.NER.utils.ProcessorService')
    def test_no_context_year_for_range(self, mock_proc_service, mock_parse_date, mock_parse_range):
        mock_entity_range = MagicMock(spec=DateRangeReferent)

        mock_analysis_result = MagicMock()
        mock_analysis_result.entities = [mock_entity_range]

        mock_proc_instance = MagicMock()
        mock_proc_instance.process.return_value = mock_analysis_result
        mock_proc_service.create_specific_processor.return_value.__enter__.return_value = mock_proc_instance

        expected_parsed_range = {'day': 31, 'month': 3, 'year': 2023, 'type': 'quarter_end_pullenti'} 
        mock_parse_range.return_value = expected_parsed_range
        mock_parse_date.return_value = None
        
        # Вызов с context_year = None
        result = extract_dates_via_pullenti("1 квартал", None)

        assert result == [expected_parsed_range]
        mock_parse_range.assert_called_once_with(mock_entity_range, None)
