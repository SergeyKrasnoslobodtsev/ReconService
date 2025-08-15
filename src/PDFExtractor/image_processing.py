import cv2
import numpy as np

from PIL import Image

def detected_text_blocks_lines(gray:np.ndarray)->np.ndarray:
    blur = cv2.blur(gray, (3, 3))
    binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel_width = 15 # Ширина ядра (подбирается)
    kernel_height = 3 # Высота ядра (подбирается)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_width, kernel_height))
    dilated_text = cv2.dilate(binary, kernel, iterations=1) # Количество итераций тоже можно менять

    # Можно добавить операцию замыкания (closing) для заполнения небольших разрывов внутри блоков
    kernel_closing = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    closed_text = cv2.morphologyEx(dilated_text, cv2.MORPH_CLOSE, kernel_closing, iterations=1)
    # return closed_text

    return closed_text

def remove_lines_by_mask(gray: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Удаляет из серого изображения все пиксели, где в маске mask == 255,
    заменяя их белым (255).
    mask: 8-битное, 0 — фон, 255 — линии.
    """
    # Убедимся, что оба массива одного размера и типа
    assert gray.shape == mask.shape, "gray и mask должны быть одинакового размера"

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.dilate(mask.astype(np.uint8), kernel, iterations=1)

    if gray.dtype != np.uint8:
        gray = gray.astype(np.uint8)
    if mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)

    # Инвертируем маску: линии → 0, фон → 255
    inv_mask = cv2.bitwise_not(mask)

    # Применяем побитовое И — оставляем только фон по маске
    cleaned = cv2.bitwise_and(gray, inv_mask)

    # Опционально: там, где были линии (mask==255), заливаем белым,
    # чтобы нечёткие края получили идеальный фон
    cleaned[mask == 255] = 255

    return cleaned

def detected_text(roi_image: np.ndarray, vk: int=100, hk=50) -> np.ndarray:
    # Адаптивная бинаризация (текст становится белым на чёрном фоне)
    binary = cv2.threshold(roi_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # Склейка слов в строки
    horiz_k = cv2.getStructuringElement(cv2.MORPH_RECT, (vk, 1))
    closed_h = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, horiz_k, iterations=2)
    # Склейка строк в параграфы
    vert_k = cv2.getStructuringElement(cv2.MORPH_RECT, (1, hk))
    closed_p = cv2.morphologyEx(closed_h, cv2.MORPH_CLOSE, vert_k, iterations=2)

    return closed_p

def find_max_contours(mask: np.ndarray, max: int = 10) -> list:
        """Находит контуры таблиц на изображении."""
        contours, __ = cv2.findContours(
            mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        # Удаляем контуры, которые слишком малы
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:max]
        
        cont = []
        for c in contours:
            c_poly = cv2.approxPolyDP(c, 3, True)
            if len(c_poly) < 4:
                continue
            x, y, w, h = cv2.boundingRect(c_poly)
            if w < 500 or h < 50:
                continue
            cont.append((x, y, w, h))
        # Сортируем контуры по y-координате
        cont = sorted(cont, key=lambda c: c[1])
        return cont

def extract_strong_lines(mask: np.ndarray, orientation: str, length: int) -> np.ndarray:
    """
    Извлекает только настоящие линии заданной ориентации,
    убирая короткие штрихи (буквы и шум).
    orientation: 'vert' или 'horiz'
    length: минимальная длина линии в пикселях
    """
    if orientation == 'vert':
        # узкий и длинный вертикальный kernel, ширина=1, высота=length
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, length))
    else:
        # широкая и плоская горизонтальная «щётка»
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (length, 1))
    # открытие: сначала эрозия (уберёт всё меньше заданной длины), потом дилатация
    clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return clean


def find_lines(gray: np.ndarray, scale: int = 50) -> np.ndarray:
    """Находит длинные линии на изображении."""
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    
    _, img_bin = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img_bin = 255-img_bin
    vertical_element, _ = create_structuring_element(img_bin, scale + 150, type=0)
    horizontal_element, _ = create_structuring_element(img_bin, scale, type=1)

    vertical_lines = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, vertical_element, iterations=1)
    horizontal_lines = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, horizontal_element, iterations=2)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    v_fixed = cv2.morphologyEx(vertical_lines, cv2.MORPH_CLOSE, kernel, iterations=1)
    h_fixed = cv2.morphologyEx(horizontal_lines, cv2.MORPH_CLOSE, kernel, iterations=1)

    v_fixed = cv2.dilate(v_fixed, cv2.getStructuringElement(cv2.MORPH_RECT,(1,5)), 2)
    h_fixed = cv2.dilate(h_fixed, cv2.getStructuringElement(cv2.MORPH_RECT,(5,1)), 2)

     # Инициализируем итоговые отфильтрованные маски
    h_filtered_final = np.zeros_like(h_fixed)
    v_filtered_final = np.zeros_like(v_fixed)

    # Создаем маску для поиска кандидатов в таблицы
    # Объединяем горизонтальные и вертикальные линии, чтобы выделить области с сеткой
    table_candidate_mask = cv2.bitwise_or(h_fixed, v_fixed)
    # Image.fromarray(table_candidate_mask).show()


    table_regions = find_max_contours(table_candidate_mask, max=4)

    if not table_regions: # Если регионы таблиц не найдены, применяем фильтрацию ко всему изображению (как раньше)
        print("Регионы таблиц не найдены, фильтрация ко всему изображению.")
        intersec_full = cv2.bitwise_and(v_fixed, h_fixed)
        h_filtered_final = filter_small_and_isolated(h_fixed.copy(), intersec_full, min_length=1, min_intersections=1)
        v_filtered_final = filter_small_and_isolated(v_fixed.copy(), intersec_full, min_length=50, min_intersections=1) # min_length для вертикальных можно подбирать
        return h_filtered_final, v_filtered_final

    for (x, y, w, h) in table_regions:
        # Вырезаем ROI из h_fixed, v_fixed и создаем локальную маску пересечений
        roi_h_fixed = h_fixed[y:y+h, x:x+w]
        roi_v_fixed = v_fixed[y:y+h, x:x+w]
        
        if roi_h_fixed.size == 0 or roi_v_fixed.size == 0: # Пропускаем пустые ROI
            continue

        roi_intersec = cv2.bitwise_and(roi_v_fixed, roi_h_fixed)

        # Применяем фильтрацию к ROI
        # Параметры min_length и min_intersections могут требовать корректировки для ROI
        filtered_roi_h = filter_small_and_isolated(roi_h_fixed.copy(), roi_intersec, min_length=1, min_intersections=1)
        filtered_roi_v = filter_small_and_isolated(roi_v_fixed.copy(), roi_intersec, min_length=max(10, h // 100), min_intersections=1)

        # Вставляем отфильтрованные ROI обратно в итоговые маски
        # Используем np.maximum, чтобы корректно обработать возможные перекрытия ROI (хотя RETR_EXTERNAL должен их минимизировать)
        h_filtered_final[y:y+h, x:x+w] = np.maximum(h_filtered_final[y:y+h, x:x+w], filtered_roi_h)
        v_filtered_final[y:y+h, x:x+w] = np.maximum(v_filtered_final[y:y+h, x:x+w], filtered_roi_v)
    

    return h_filtered_final, v_filtered_final

def filter_small_and_isolated(mask: np.ndarray, intersec: np.ndarray, min_length:int = 120, min_intersections: int = 1):
    """
    Удаляет из mask все компоненты (линии), 
    у которых длина (число пикселей) < min_length
    или число пересечений <= min_intersections.
    """
    
    num_mask_labels, labels_mask, stats_mask, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), connectivity=8) 
    
    output_mask = np.zeros_like(mask, dtype=np.uint8)

    for lbl in range(1, num_mask_labels): # Начинаем с 1, чтобы пропустить фон (метка 0)
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

def create_structuring_element(image: np.ndarray, scale: int, type: int = 0):
    """Создает структурный элемент для морфологических операций."""
    if type == 0:
        size = image.shape[0] // scale
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, size))
    elif type == 1:
        size = image.shape[1] // scale
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (size, 1))
    else:
        raise ValueError("Ожидается 0 или 1 для типа структурного элемента")
    
    return element, size