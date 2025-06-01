from abc import ABC
import enum
import os
from typing import List, Optional, Tuple

import cv2
import numpy as np
import pytesseract

from PIL import Image

from .image_processing import detected_text_blocks_lines
class OcrEngine(enum.Enum):
    TESSERACT = 0
    EASYOCR = 1
    PADDLEOCR = 2



class Engine(ABC):
    def extract_text(self, image: np.ndarray) -> Tuple[str, List[Tuple[int, int, int, int]]]:
        ...     
    def detected_text(self, image: np.ndarray):
        blobs = detected_text_blocks_lines(image)
        cnts, hierarchy = cv2.findContours(blobs, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        if cnts is not None and hierarchy is not None:
            if hierarchy.ndim == 3 and hierarchy.shape[0] == 1 and hierarchy.shape[1] == len(cnts):
                for i, cnt in enumerate(cnts):
                    # Внешние контуры не имеют родителя, поэтому их родительский индекс равен -1.
                    if hierarchy[0][i][3] == -1:
                        x, y, w, h = cv2.boundingRect(cnt)
                        if w > 15 and h > 15: # Отфильтровываем очень маленькие контуры
                            boxes.append((x, y, w, h))
        
        boxes = sorted(boxes, key=lambda b: (b[1], b[0]))
        return boxes

    def preprocess(self, gray: np.ndarray) -> np.ndarray:

        # h, w = gray.shape

        # _, thresh = cv2.threshold(
        #     gray, 
        #     0, 255, 
        #     cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
        # )  


        # clean = cv2.bitwise_not(thresh)
        border = 10
        gray = cv2.copyMakeBorder(
            gray, border, border, border, border,
            borderType=cv2.BORDER_CONSTANT,
            value=255
        )
        # blur = cv2.medianBlur(clean, 3)

        return gray

class TesseractEngine(Engine):
    def __init__(self):
        self.cfg = r'--oem 1 --psm 4 -l rus+eng'

    def extract_text(self, image: np.ndarray) -> Tuple[str, List[Tuple[int, int, int, int]]]:
        image = self.preprocess(image)
        data = pytesseract.image_to_data(image, config=self.cfg, output_type=pytesseract.Output.DICT)
        
        words = []
        # Собираем все распознанные слова
        # Фильтруем пустые строки и строки с низкой уверенностью (conf < 0 это обычно пропуски)
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > -1 and data['text'][i].strip() != '':
                words.append(data['text'][i])
        
        # Объединяем все слова в одну строку через пробел
        text = " ".join(words)

        boxes = self.detected_text(image) # Ваш метод для получения bounding boxes блоков
        return (text, boxes)
    

class EasyOcrEngine(Engine):
    def __init__(self):
        os.environ["KMP_DEVICE_THREAD_LIMIT"] = "4"
        os.environ["OMP_THREAD_LIMIT"] = "4"
        import easyocr
        
        self.reader = easyocr.Reader(['ru', 'en'], gpu=False)

    def extract_text(self, image: np.ndarray) -> Tuple[str, List[Tuple[int, int, int, int]]]:
        image = self.preprocess(image)
        result = self.reader.readtext(image)
        text = " ".join([res[1] for res in result])
        if text != '':
            boxes = self.detected_text(image)
        return text, boxes

class PaddleOcrEngine(Engine):
    def __init__(self):
        os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
        from paddleocr import PaddleOCR
        self.reader = PaddleOCR(use_angle_cls=True, lang='ru')
    
    def extract_text(self, image: np.ndarray) -> Tuple[str, List[Tuple[int, int, int, int]]]:
        image = self.preprocess(image)
        result = self.reader.ocr(image, cls=False)
        text = " ".join([res[1][0] for res in result])
        if text != '':
                boxes = self.detected_text(image)
        return text, boxes

class OCR:
    def __init__(self, ocr_engine:Optional[OcrEngine]):
        match(ocr_engine):
            case ocr_engine.EASYOCR:
                self.ocr = EasyOcrEngine()
            case ocr_engine.PADDLEOCR:
                self.ocr = PaddleOcrEngine()
            case _: 
                self.ocr = TesseractEngine()

    def extract(self, image: np.ndarray) -> Tuple[str, List[Tuple[int, int, int, int]]]:
        return self.ocr.extract_text(image)
    
