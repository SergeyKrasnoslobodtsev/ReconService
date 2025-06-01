import logging

from pullenti.Sdk import Sdk

logger = logging.getLogger(__name__)

def test_initialization():
    """
    Тест инициализации Pullenti SDK.
    """
    logger.info('Начинаем тест инициализации Pullenti SDK')
    Sdk.initialize_all()
    logger.info('Pullenti SDK успешно инициализирован')
    v = Sdk.get_version()
    logger.info(f'Версия Pullenti SDK получена: {v}')

    assert v is not None, "Версия Pullenti SDK не должна быть None"