
import numpy as np
import pytesseract

from .TableDetector.table import BBox


class OcrEngine:

    def __init__(self):
        
        self.cfg = r'--oem 1 --psm 6 -l rus+eng'

    def extract_text(self, image: np.ndarray) -> tuple[str, list[BBox]]:
        data = pytesseract.image_to_data(image, config=self.cfg, output_type=pytesseract.Output.DICT)
        
        words = []
        boxes: list[BBox] = []

        for i in range(len(data['text'])):
            if data['text'][i].strip() != '':
                words.append(data['text'][i])
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                boxes.append(BBox(x=x, y=y, width=w, height=h))

        text = " ".join(words)
 
        return (text, boxes)