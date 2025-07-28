import logging
import cv2
import numpy as np
from ...LayoutAnalisis.TableDetector.table import BBox, Cell
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)


class FindTableCadidates:

    def find(self, image: np.ndarray):

        binary = cv2.threshold(image, 0, 255, 1)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(binary, kernel, iterations=1)
        # Image.fromarray(dilated).show()
        v_lines = self._find_vertical_lines(dilated)
        h_lines = self._find_horizontal_lines(dilated)
        mask = v_lines + h_lines
        # Image.fromarray(mask).show()
        cnts = self._find_contours(mask)
        
        
        roi_intersec = cv2.bitwise_and(v_lines, h_lines)
        for bbox in cnts:
            filtered_v_lines = self._filter_small_and_isolated(v_lines[bbox.roi], roi_intersec[bbox.roi], min_length=max(10, bbox.height // 100), min_intersections=1)
            filtered_h_lines = self._filter_small_and_isolated(h_lines[bbox.roi], roi_intersec[bbox.roi], min_length=1, min_intersections=1)
            # утолщаем линии чтоб удалить полностью с изображения
            # раньше нельзя утолщать так как обработка связанных компонентов будет выполняться долго
            filtered_v_lines = cv2.dilate(filtered_v_lines, kernel, iterations=2)
            filtered_h_lines = cv2.dilate(filtered_h_lines, kernel, iterations=2)
            mask = filtered_v_lines + filtered_h_lines
            # Image.fromarray(mask).show()
            data = self._extract_table_structure(filtered_v_lines, filtered_h_lines)
            logger.debug(data)
            # удаляем сетку таблицы перед распознаванием
            # region = image[bbox.roi].copy()
            # region[filtered_h_lines == 255] = 255
            # region[filtered_v_lines == 255] = 255

        
        logger.debug("Done!")
        return cnts
    
    @staticmethod
    def _extract_table_structure(v_lines: np.ndarray, h_lines: np.ndarray) -> list[Cell]:

        """
        Извлекает структуру таблицы, включая объединенные ячейки.
        Возвращает список строк, где каждая строка - это список ячеек.
        Каждая ячейка - это словарь с изображением, координатами, rowspan и colspan.
        """
        # 1. Находим контуры ячеек
        grid_mask = v_lines + h_lines
        inverted_mask = cv2.bitwise_not(grid_mask)
        # Image.fromarray(inverted_mask).show()
        contours = cv2.findContours(inverted_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        from ..utils import sort_contours, remove_nested_rectangles
        sort_cnts, bboxs = sort_contours(contours)
        print(bboxs)

        
        logger.debug(f'Lenght cells {len(bboxs)}')

        return []


    @staticmethod
    def _filter_small_and_isolated(mask: np.ndarray, intersec: np.ndarray, min_length:int = 120, min_intersections: int = 1):
        """
        Удаляет из mask все компоненты (линии), у которых длина (число пикселей) < min_length
        или число пересечений <= min_intersections.
        """
        
        num_mask_labels, labels_mask, stats_mask, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8) 
        
        output_mask = np.zeros_like(mask, dtype=np.uint8)

        for lbl in range(1, num_mask_labels): 
            length = stats_mask[lbl, cv2.CC_STAT_AREA]

            if length < min_length:
                continue 

            comp_boolean_mask = (labels_mask == lbl) 
            
            current_comp_intersections_map_bool = comp_boolean_mask & (intersec > 0)
            
            if not np.any(current_comp_intersections_map_bool): 
                crosses = 0
            else:
                num_intersection_blobs, _ = cv2.connectedComponents(current_comp_intersections_map_bool.astype(np.uint8), connectivity=8)
                crosses = num_intersection_blobs - 1 
            
            if crosses > min_intersections: 
                output_mask[comp_boolean_mask] = 255 
                
        return output_mask

    @staticmethod
    def _find_contours(mask_img: np.ndarray, max_cnts: int = 5):
        """Находит контуры на изображении"""
        contours = cv2.findContours(mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        # Удаляем контуры, которые слишком малы
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:max_cnts]
        
        cont: list[BBox] = []
        for c in contours:
            c_poly = cv2.approxPolyDP(c, 3, True)
            area = cv2.contourArea(c)
            if area < 30000:
                continue
            if len(c_poly) < 4:
                continue
            x, y, w, h = cv2.boundingRect(c_poly)

            cont.append(BBox(x=x, y=y, width=w, height=h))
        # Сортируем контуры по y-координате
        cont = sorted(cont, key=lambda c: c.y)
        logger.debug(f'Найдено кандидатов-таблиц: {len(cont)}')
        return cont

    @staticmethod
    def _find_vertical_lines(binary: np.ndarray):
        """Находит вертикальные линии в бинарном изображении."""
        if binary.shape[0] > binary.shape[1]:
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(binary.shape[0] / 150)))
        else:
            vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(binary.shape[1] / 150)))

        vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=1)

        return vertical_lines
    
    @staticmethod
    def _find_horizontal_lines(binary: np.ndarray):
        """Находит горизонтальные линии в бинарном изображении."""
        if binary.shape[0] > binary.shape[1]:
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(binary.shape[0] / 20), 1))
        else:
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(binary.shape[1] / 20), 1))

        horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)

        return horizontal_lines