import cv2
import numpy as np
import logging
from PIL import Image

class ImageQualityMetrics:
    """Метрики качества изображения для выбора стратегии обработки"""
    
    @staticmethod
    def estimate_dpi(gray: np.ndarray) -> float:
        """Оценивает примерное разрешение по размеру текстовых элементов"""
        # Находим края
        edges = cv2.Canny(gray, 50, 150)
        
        # Находим горизонтальные линии (примерная высота строк)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        detect_horizontal = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
        
        # Считаем количество строк
        contours, _ = cv2.findContours(detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            heights = [cv2.boundingRect(c)[3] for c in contours if cv2.boundingRect(c)[3] > 5]
            if heights:
                avg_line_height = np.median(heights)
                # Типичная высота строки при 300 dpi = 40-50 пикселей
                # При 150 dpi = 20-25 пикселей
                estimated_dpi = (avg_line_height / 45) * 300
                return max(75, min(300, estimated_dpi))
        
        return 150  # Значение по умолчанию

    @staticmethod
    def measure_text_contrast(gray: np.ndarray) -> float:
        """Измеряет контраст текста относительно фона"""
        # Применяем морфологические операции для выделения текста
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        gradient = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
        
        # Находим области с текстом
        _, text_mask = cv2.threshold(gradient, 10, 255, cv2.THRESH_BINARY)
        
        if np.sum(text_mask > 0) < 100:  # Слишком мало текста
            return 0
        
        # Измеряем разницу между текстом и фоном
        text_pixels = gray[text_mask > 0]
        background_pixels = gray[text_mask == 0]
        
        if len(background_pixels) == 0:
            return 0
        
        text_mean = np.mean(text_pixels)
        background_mean = np.mean(background_pixels)
        
        contrast = abs(background_mean - text_mean)
        return contrast

    @staticmethod
    def detect_noise_level(gray: np.ndarray) -> float:
        """Определяет уровень шума (зерна) на изображении"""
        # Используем высокочастотный фильтр для детекции шума
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        noise = cv2.absdiff(gray, blur)
        
        # Нормализуем по яркости
        noise_level = np.mean(noise) / (np.std(gray) + 1e-6)
        return noise_level

    @staticmethod
    def check_broken_characters(gray: np.ndarray) -> float:
        """Проверяет наличие разрывов в буквах"""
        # Бинаризация
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Находим компоненты связности
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
        
        # Анализируем размеры компонент
        if num_labels < 2:
            return 0
        
        areas = stats[1:, cv2.CC_STAT_AREA]  # Пропускаем фон
        small_components = np.sum(areas < 50)  # Очень мелкие компоненты
        
        # Высокий процент мелких компонент указывает на разрывы
        broken_ratio = small_components / len(areas) if len(areas) > 0 else 0
        return broken_ratio


class AdaptiveImageProcessing:
    def __init__(self):
        self.logger = logging.getLogger("app." + __class__.__name__)
        self.metrics = ImageQualityMetrics()

    def analyze_image_quality(self, gray: np.ndarray) -> dict:
        """Анализирует качество изображения"""
        metrics = {
            'dpi': self.metrics.estimate_dpi(gray),
            'contrast': self.metrics.measure_text_contrast(gray),
            'noise': self.metrics.detect_noise_level(gray),
            'broken_chars': self.metrics.check_broken_characters(gray)
        }
        
        self.logger.debug(f"Image metrics: DPI≈{metrics['dpi']:.0f}, "
                         f"Contrast={metrics['contrast']:.1f}, "
                         f"Noise={metrics['noise']:.3f}, "
                         f"Broken={metrics['broken_chars']:.2%}")
        
        return metrics

    def process(self, gray: np.ndarray) -> np.ndarray:
        """Адаптивная обработка на основе анализа качества"""

        # Анализируем качество
        metrics = self.analyze_image_quality(gray)
        # Image metrics: DPI≈75, Contrast=82.2, Noise=0.024, Broken=51.22% "bad/РИР-САЗ.pdf" 
        # Image metrics: DPI≈150, Contrast=119.9, Noise=0.073, Broken=31.69% "bad/scan_v1.pdf"
        # Image metrics: DPI≈150, Contrast=120.4, Noise=0.061, Broken=32.83% "bad/Браз-Юнигрин Пауэр.pdf"

        # Image metrics: DPI≈150, Contrast=114.0, Noise=0.054, Broken=17.64% "bad/АС РУ- ВОСЬМОЙ ВЕТРОПАРК.pdf"  стандартный режим
       
        if self._has_broken_characters(metrics) and not self._is_low_contrast(metrics):
            self.logger.info("Detected broken characters - applying closing")
            binary = self._process_high_quality(gray)
        elif self._is_low_contrast(metrics):
            self.logger.info("Detected low contrast - enhancing")
            binary = self._process_low_contrast(gray, metrics)
        else:
            self.logger.info("Using standard processing")
            binary = self._process_standard(gray)
        
        return binary

    def _is_high_quality(self, metrics: dict) -> bool:
        """Проверяет, является ли скан высокого качества"""
        return (metrics['contrast'] > 80 and 
                metrics['noise'] < 0.05 and 
                metrics['broken_chars'] < 0.15 and
                metrics['dpi'] > 200)

    def _is_low_dpi(self, metrics: dict) -> bool:
        """Проверяет низкое разрешение"""
        return metrics['dpi'] < 150

    def _has_broken_characters(self, metrics: dict) -> bool:
        """Проверяет наличие разрывов в буквах"""
        return metrics['broken_chars'] > 0.25

    def _is_low_contrast(self, metrics: dict) -> bool:
        """Проверяет низкий контраст"""
        return metrics['contrast'] < 100

    def _process_high_quality(self, gray: np.ndarray) -> np.ndarray:
        """Минимальная обработка для качественных сканов"""
        # Только легкое сглаживание шума
        cleaned = cv2.medianBlur(gray, 3)
        binary = cv2.adaptiveThreshold(cleaned, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY, 25, 15)
        
        # # Простая бинаризация
        # _, binary = cv2.threshold(cleaned, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return binary

    def _process_low_dpi(self, gray: np.ndarray, metrics: dict) -> np.ndarray:
        """Обработка низкого разрешения"""
        # Увеличиваем изображение
        scale = 300 / metrics['dpi']
        h, w = gray.shape
        if scale > 1.5:
            gray = cv2.resize(gray, (int(w * scale), int(h * scale)), 
                            interpolation=cv2.INTER_CUBIC)
        
        # Усиливаем края
        sharpening_kernel = np.array([[-1,-1,-1],
                                     [-1, 9,-1],
                                     [-1,-1,-1]])
        sharpened = cv2.filter2D(gray, -1, sharpening_kernel)
        
        # Адаптивная бинаризация для разного освещения
        binary = cv2.adaptiveThreshold(
            sharpened, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            blockSize=151, 
            C=10
        )
        # cleaned = cv2.medianBlur(binary, 3)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        # cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=1)

        cleaned_resized = cv2.resize(binary, (w, h), interpolation=cv2.INTER_AREA)
        return cleaned_resized

    def _process_broken_chars(self, gray: np.ndarray, metrics: dict) -> np.ndarray:
        """Обработка разрывов в буквах"""
        # Сначала улучшаем контраст если нужно
        
        # Бинаризация
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Инвертируем для морфологии
        binary_inv = cv2.bitwise_not(binary)
        
        # Соединяем разрывы небольшим closing
        kernel_size = 2 if metrics['dpi'] < 300 else 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        closed = cv2.morphologyEx(binary_inv, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        # Возвращаем обратно
        result = cv2.bitwise_not(closed)
        
        return result

    def _process_low_contrast(self, gray: np.ndarray, metrics: dict) -> np.ndarray:
        """Обработка низкого контраста (тусклый текст)"""

        alpha = 0.2
        beta = (1.0 - alpha)
        gamma = 0
        adjusted = cv2.addWeighted(gray, alpha=alpha, src2=gray, beta=beta, gamma=gamma)
        
        clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8,8))
        enhanced = clahe.apply(adjusted)
        
        # # Если есть шум, сначала убираем его
        
        
        # # # Адаптивная бинаризация работает лучше для неравномерного освещения
        binary = cv2.adaptiveThreshold(
            adjusted, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=25,
            C=15
        )

        return enhanced

    def _clean_lines_binary(self, binary: np.ndarray) -> np.ndarray:
        """Удаляет линии с БИНАРНОГО изображения"""
        
        # Инвертируем (линии и текст становятся белыми)
        binary_inv = cv2.bitwise_not(binary)
        
        # Удаляем горизонтальные линии
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (70, 1))
        horizontal_lines = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        binary_inv = cv2.subtract(binary_inv, horizontal_lines)
        
        # Удаляем вертикальные линии
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 70))
        vertical_lines = cv2.morphologyEx(binary_inv, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        binary_inv = cv2.subtract(binary_inv, vertical_lines)
        
        # Возвращаем обратно
        cleaned = cv2.bitwise_not(binary_inv)
        
        return cleaned

    def _process_standard(self, gray: np.ndarray) -> np.ndarray:
        """Стандартная обработка среднего качества"""
        # # Легкое размытие для шума
        cleaned = cv2.medianBlur(gray, 3)
        
        # Умеренное усиление контраста
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cleaned = clahe.apply(cleaned)

        binary = cv2.adaptiveThreshold(
            cleaned, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=21, 
            C=10 
        )
       
        return binary