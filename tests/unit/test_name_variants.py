#!/usr/bin/env python3
"""Тестирование генерации вариантов названий организаций"""

import pytest
from src.NER.ext_organization import generate_organization_name_variants, generate_partial_matches


class TestPartialMatches:
    """Тесты для генерации частичных совпадений"""
    
    def test_partial_matches_basic(self):
        """Тест базовой генерации частичных совпадений"""
        text = "РУСАЛ НОВОКУЗНЕЦКИЙ АЛЮМИНИЕВЫЙ ЗАВОД"
        result = generate_partial_matches(text)
        
        expected = [
            "РУСАЛ НОВОКУЗНЕЦКИЙ",
            "РУСАЛ НОВОКУЗНЕЦКИЙ АЛЮМИНИЕВЫЙ",
            "РУСАЛ НОВОКУЗНЕЦКИЙ АЛЮМИНИЕВЫЙ ЗАВОД"
        ]
        print(f"\nОтладка test_partial_matches_basic:")
        print(f"Входной текст: '{text}'")
        print(f"Фактический результат: {result}")
        print(f"Ожидаемый результат: {expected}")
        print(f"Типы: {type(result)}, {type(expected)}")
        assert result == expected
    
    def test_partial_matches_two_words(self):
        """Тест с двумя словами"""
        text = "ОК РУСАЛ"
        result = generate_partial_matches(text)
        
        expected = ["ОК РУСАЛ"]
        assert result == expected
    
    def test_partial_matches_single_word(self):
        """Тест с одним словом"""
        text = "РУСАЛ"
        result = generate_partial_matches(text)
        
        expected = []
        assert result == expected


class TestOrganizationNameVariants:
    """Тесты для генерации вариантов названий организаций"""
    
    def test_rusal_organization_variants(self):
        """Тест вариантов для организации РУСАЛ"""
        org_name = "РУСАЛ НОВОКУЗНЕЦКИЙ АЛЮМИНИЕВЫЙ ЗАВОД"
        variants = generate_organization_name_variants(org_name)
        
        expected_variants = {
            "НОВОКУЗНЕЦКИЙ АЛЮМИНИЕВЫЙ ЗАВОД",
            "РУСАЛ НОВОКУЗНЕЦКИЙ АЛЮМИНИЕВЫЙ ЗАВОД", 
            "РУСАЛ НОВОКУЗНЕЦКИЙ",                    
            "РУСАЛ НОВОКУЗНЕЦКИЙ АЛЮМИНИЕВЫЙ"        
        }
        
        assert variants == expected_variants
    
    def test_rusal_short_organization_variants(self):
        """Тест вариантов для короткой организации РУСАЛ"""
        org_name = "ОК РУСАЛ ТД"
        variants = generate_organization_name_variants(org_name)
        
        expected_variants = {
            "ОК РУСАЛ ТД",    # полное название
            "ОК РУСАЛ"        # частичное
        }
        
        assert variants == expected_variants
    
    def test_non_rusal_organization_variants(self):
        """Тест вариантов для не-РУСАЛ организации"""
        org_name = "СИБИРСКАЯ ЭНЕРГЕТИЧЕСКАЯ КОМПАНИЯ"
        variants = generate_organization_name_variants(org_name)
        
        expected_variants = {
            "СИБИРСКАЯ ЭНЕРГЕТИЧЕСКАЯ КОМПАНИЯ",   # полное название
            "СИБИРСКАЯ ЭНЕРГЕТИЧЕСКАЯ"             # частичное
        }
        
        assert variants == expected_variants


def test_integration_example():
    """Интеграционный тест с выводом для визуальной проверки"""
    test_cases = [
        "РУСАЛ НОВОКУЗНЕЦКИЙ АЛЮМИНИЕВЫЙ ЗАВОД",
        "РУСАЛ АЧИНСКИЙ ГЛИНОЗЕМНЫЙ КОМБИНАТ", 
        "ОК РУСАЛ ТД"
    ]
    
    for org_name in test_cases:
        variants = generate_organization_name_variants(org_name)
        print(f"\nОрганизация: {org_name}")
        print("Варианты названий:")
        for i, variant in enumerate(sorted(variants), 1):
            print(f"  {i}. {variant}")
        
        # Базовая проверка, что варианты не пустые
        assert len(variants) > 0
        assert org_name in variants  # полное название всегда должно быть включено
