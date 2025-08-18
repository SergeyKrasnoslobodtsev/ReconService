import cv2
import numpy as np
import logging

from PIL import Image

class AdaptiveImageProcessing:
    def __init__(self):
        self.logger = logging.getLogger("app." + __class__.__name__)

    def _analyze_image_quality(self, gray: np.ndarray) -> dict:
        """Анализирует качество изображения и возвращает метрики"""
        h, w = gray.shape
        
        # 1. Контрастность (стандартное отклонение)
        contrast = np.std(gray)
        
        # 2. Средняя яркость
        brightness = np.mean(gray)
        
        # 3. Гистограмма для анализа распределения яркости
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_norm = hist.flatten() / (h * w)
        
        # 4. Процент белых пикселей (фон)
        white_ratio = np.sum(gray > 240) / (h * w)
        
        # 5. Процент очень темных пикселей (текст)
        black_ratio = np.sum(gray < 50) / (h * w)
        
        # 6. Резкость (вариация Лапласа)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        return {
            'contrast': contrast,
            'brightness': brightness,
            'white_ratio': white_ratio,
            'black_ratio': black_ratio,
            'sharpness': laplacian_var,
            'hist': hist_norm
        }

    def _is_high_quality_scan(self, metrics: dict) -> bool:
        """Проверяет, является ли скан высокого качества"""
        # Хороший документ: contrast=57.8, brightness=238.3, white_ratio=0.908, black_ratio=0.037
        return (metrics['contrast'] > 55 and 
                metrics['brightness'] < 240 and  # Важно: хорошие документы имеют меньшую яркость
                metrics['white_ratio'] > 0.85 and 
                metrics['black_ratio'] > 0.035)

    def _is_low_contrast_scan(self, metrics: dict) -> bool:
        """Проверяет, является ли скан низкоконтрастным/бледным"""
        # Проблемный документ: contrast=46.3, brightness=244.0, white_ratio=0.932, black_ratio=0.029
        return (metrics['contrast'] < 48 or 
                metrics['brightness'] > 243.5 or  # Бледные документы очень яркие
                metrics['black_ratio'] < 0.030)

    def _is_medium_quality_with_grain(self, metrics: dict) -> bool:
        """Проверяет, является ли скан среднего качества с зерном"""
        # Документ с зерном: contrast=57.9, brightness=241.1, white_ratio=0.946, black_ratio=0.054
        return (metrics['contrast'] > 55 and 
                240 <= metrics['brightness'] <= 242 and
                metrics['black_ratio'] > 0.050)

    # Удалите дублирующий метод process и оставьте только этот:
    def process(self, gray: np.ndarray) -> np.ndarray:
        """Простая обработка с проверкой результата"""
        self.logger.debug("Starting image processing")
        # Сначала попробуйте вашу старую рабочую версию
        cleaned = cv2.medianBlur(gray, 3)
        # cleaned = cv2.bilateralFilter(cleaned, 3, 7, 7)
        
        # cleaned = cv2.adaptiveThreshold(cleaned, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        #                                 cv2.THRESH_BINARY, 21, 10)
        # bilateral = cv2.bilateralFilter(cleaned, 15, 75, 75)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        # erosion = cv2.erode(cleaned, kernel, iterations=1)
        # dilation = cv2.dilate(erosion, kernel, iterations=1)
        # # Проверим, достаточно ли контраста в результате
        # contrast = np.std(cleaned)
        # if contrast < 100:  # Если результат слишком однородный
        #     self.logger.debug(f"Контраст слишком низкий {contrast}, пробуем CLAHE")
        #     # Попробуйте более агрессивную обработку
        #     clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(2,2))
        #     enhanced = clahe.apply(gray)
        #     cleaned = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        #                                 cv2.THRESH_BINARY, 15, 10)
        Image.fromarray(cleaned).show()
        return cleaned

    def _process_low_contrast(self, gray: np.ndarray, metrics: dict) -> np.ndarray:
        """Обработка низкоконтрастных/бледных сканов"""
        self.logger.debug("Using low-contrast processing")
        
        # Более агрессивная обработка для серого текста
        # 1. Сильное увеличение контраста
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # 2. Гамма-коррекция для затемнения серого текста
        gamma = 0.6  # Затемнить
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
        enhanced = cv2.LUT(enhanced, table)
        
        # 3. Морфологические операции для усиления текста
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        enhanced = cv2.morphologyEx(enhanced, cv2.MORPH_CLOSE, kernel)
        # 4. Удаление линий (если есть)
        cleaned = cv2.medianBlur(enhanced, 3)
        # 5. Адаптивная бинаризация с более агрессивными параметрами
        cleaned = cv2.adaptiveThreshold(cleaned, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                    cv2.THRESH_BINARY, 51, 8)

        
        
        return cleaned

    def _process_medium_quality_with_grain(self, gray: np.ndarray) -> np.ndarray:
        """Обработка сканов среднего качества с зерном"""
        self.logger.debug("Using medium-quality processing with grain removal")
        
        # 1. Медианное размытие для удаления зерна (как вы упоминали)
        cleaned = cv2.medianBlur(gray, 3)  
        
        # 2. Легкое улучшение контраста
        # Используем CLAHE для улучшения контраста
        # clipLimit = 1.5 для умеренного улучшения
        # tileGridSize = (8,8) для сохранения мелких деталей
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(2,2))
        cleaned = clahe.apply(cleaned)
        
        # 3. Бинаризация Otsu
        # _, cleaned = cv2.threshold(cleaned, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return cleaned

    def _process_high_quality(self, gray: np.ndarray) -> np.ndarray:
        """Обработка высококачественных сканов - минимальная обработка"""
        self.logger.debug("Using high-quality processing")
        # Минимальная обработка для отличного качества
        cleaned = cv2.medianBlur(gray, 3)
        _, cleaned = cv2.threshold(cleaned, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cleaned

    def _process_medium_quality(self, gray: np.ndarray) -> np.ndarray:
        """Обработка сканов среднего качества (fallback)"""
        self.logger.debug("Using default medium-quality processing")
        
        # Стандартная обработка
        cleaned = cv2.medianBlur(gray, 3)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cleaned = clahe.apply(cleaned)
        _, cleaned = cv2.threshold(cleaned, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return cleaned