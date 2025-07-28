import logging
import cv2
import numpy as np

from PIL import Image

from ..utils import convert_pil_to_cv, grayscale, convert_cv_to_pill


try:
    from cv2.ximgproc import niBlackThreshold, BINARIZATION_SAUVOLA
except ImportError:
    niBlackThreshold = None
    BINARIZATION_SAUVOLA = None
    logging.warning("Модуль cv2.ximgproc не найден. Для использования бинаризации Сауволы, установите: pip install opencv-contrib-python")


PILimage = Image.Image

logger = logging.getLogger(__name__)

class ImageProcessor:
    
    def process(self, image: PILimage) -> np.ndarray:

        logger.info("Начало продвинутой предобработки изображения.")

        cv_image = convert_pil_to_cv(image)
        
        
        gray_image = grayscale(cv_image)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
        contrast_enhanced_image = clahe.apply(gray_image)
        logger.debug("Контраст изображения улучшен с помощью CLAHE.")

        denoised_image = cv2.medianBlur(contrast_enhanced_image, 3)
        logger.debug("Шум удален с помощью medianBlur.")
        binary_image = cv2.adaptiveThreshold(
                denoised_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
        # ИСПРАВЛЕНО: Проверяем наличие и функции, и константы
        # if niBlackThreshold is not None and BINARIZATION_SAUVOLA is not None:
        #     binary_image = niBlackThreshold(
        #         denoised_image, 
        #         maxValue=255, 
        #         type=cv2.THRESH_BINARY, 
        #         blockSize=21,
        #         k=0.2,
        #         # ИСПРАВЛЕНО: Используем правильный флаг
        #         binarizationMethod=BINARIZATION_SAUVOLA
        #     )
        #     logger.info("Изображение бинаризовано методом Сауволы.")
        # else:
        #     logger.warning("Используется стандартная адаптивная бинаризация (модуль ximgproc недоступен).")
        #     binary_image = cv2.adaptiveThreshold(
        #         denoised_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        #     )
        convert_cv_to_pill(binary_image).show()
        return binary_image

   