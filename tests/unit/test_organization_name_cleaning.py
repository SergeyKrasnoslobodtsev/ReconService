import pytest
from src.NER.organization_processor import OrganizationProcessor


class TestOrganizationNameCleaning:
    """Тестирование очистки названий организаций от ИНН/КПП"""
    
    def setup_method(self):
        self.processor = OrganizationProcessor()
    
    def test_clean_organization_name_inn_kpp(self):
        """Тест очистки названия с ИНН/КПП"""
        raw_name = 'ООО "РН-Карт", ИНН/КПП 7743529527/772501001'
        expected = 'ООО "РН-Карт"'
        result = self.processor._clean_organization_name(raw_name)
        assert result == expected
    
    def test_clean_organization_name_inn_only(self):
        """Тест очистки названия с ИНН в скобках"""
        raw_name = 'Общество с ограниченной ответственностью "НОВАЯ ЭНЕРГОСБЫТОВАЯ КОМПАНИЯ" (ИНН 7730674566'
        expected = 'Общество с ограниченной ответственностью "НОВАЯ ЭНЕРГОСБЫТОВАЯ КОМПАНИЯ"'
        result = self.processor._clean_organization_name(raw_name)
        assert result == expected
    
    def test_clean_organization_name_inn_with_closing_bracket(self):
        """Тест очистки названия с ИНН в полных скобках"""
        raw_name = 'АО "РУСАЛ САЯНАЛ" (ИНН 1902015920)'
        expected = 'АО "РУСАЛ САЯНАЛ"'
        result = self.processor._clean_organization_name(raw_name)
        assert result == expected
    
    def test_clean_organization_name_inn_comma_format(self):
        """Тест очистки названия с ИНН через запятую"""
        raw_name = 'ООО "Тест", ИНН 1234567890'
        expected = 'ООО "Тест"'
        result = self.processor._clean_organization_name(raw_name)
        assert result == expected
    
    def test_clean_organization_name_no_inn(self):
        """Тест, что название без ИНН остается без изменений"""
        raw_name = 'ООО "Чистое название"'
        expected = 'ООО "Чистое название"'
        result = self.processor._clean_organization_name(raw_name)
        assert result == expected
    
    def test_clean_organization_name_multiple_spaces(self):
        """Тест удаления лишних пробелов"""
        raw_name = '  ООО "Тест"  , ИНН 1234567890  '
        expected = 'ООО "Тест"'
        result = self.processor._clean_organization_name(raw_name)
        assert result == expected
    
    def test_clean_organization_name_unclosed_quotes(self):
        """Тест исправления незакрытых кавычек"""
        raw_name = 'Публичное акционерное общество "Федеральная гидрогенерирующая компания - РусГидро'
        expected = 'Публичное акционерное общество "Федеральная гидрогенерирующая компания - РусГидро"'
        result = self.processor._clean_organization_name(raw_name)
        assert result == expected
    
    def test_clean_organization_name_unclosed_quotes_with_inn(self):
        """Тест исправления незакрытых кавычек с ИНН"""
        raw_name = 'Акционерное общество "Объединенная компания РУСАЛ Уральский Алюминий (ИНН 1234567890)'
        expected = 'Акционерное общество "Объединенная компания РУСАЛ Уральский Алюминий"'
        result = self.processor._clean_organization_name(raw_name)
        assert result == expected
    
    def test_fix_quotes_method(self):
        """Тест метода исправления кавычек"""
        # Одна открывающая кавычка
        result = self.processor._fix_quotes('ООО "Тест')
        assert result == 'ООО "Тест"'
        
        # Парные кавычки (не трогаем)
        result = self.processor._fix_quotes('ООО "Тест"')
        assert result == 'ООО "Тест"'
        
        # Нет кавычек (не трогаем)
        result = self.processor._fix_quotes('ООО Тест')
        assert result == 'ООО Тест'
        
        # Три кавычки (добавляем четвертую)
        result = self.processor._fix_quotes('ООО "Тест" и "Еще')
        assert result == 'ООО "Тест" и "Еще"'
