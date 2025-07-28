import cv2
import numpy as np
from PIL import Image

PILimage = Image.Image

def convert_pil_to_cv(image: PILimage) -> np.ndarray:
    """Конвертирует в массив numpy"""
    return np.array(image)

def convert_cv_to_pill(image: np.ndarray) -> PILimage:
    """Конвертирует в PIL изображение"""
    return Image.fromarray(image)

def grayscale(image: np.ndarray) -> np.ndarray:
    """Конвертирует изображение в оттенки серого"""
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)

def remove_nested_rectangles(rectangles: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    """
    Удаляет вложенные прямоугольники из списка.

    Если прямоугольник A полностью содержится в прямоугольнике B, A будет удален.
    Функция также удаляет дубликаты.

    :param rectangles: Список прямоугольников в формате (x, y, w, h).
    :return: Отфильтрованный список прямоугольников.
    """
    # Сначала удаляем полные дубликаты, чтобы упростить логику
    unique_rects = sorted(list(set(rectangles)))
    
    if not unique_rects:
        return []

    # Создаем список для хранения индексов прямоугольников, которые нужно удалить
    rects_to_remove = set()

    # Сравниваем каждую пару прямоугольников
    for i, rect1 in enumerate(unique_rects):
        x1, y1, w1, h1 = rect1
        for j, rect2 in enumerate(unique_rects):
            if i == j:
                continue
            
            x2, y2, w2, h2 = rect2

            # Проверяем, находится ли rect1 полностью внутри rect2
            is_nested = (x1 >= x2) and (y1 >= y2) and (x1 + w1 <= x2 + w2) and (y1 + h1 <= y2 + h2)

            if is_nested:
                # Если rect1 внутри rect2, помечаем rect1 на удаление
                rects_to_remove.add(i)
                break # Можно переходить к следующему rect1

    # Создаем итоговый список, исключая вложенные прямоугольники
    filtered_rects = [rect for i, rect in enumerate(unique_rects) if i not in rects_to_remove]
    
    return filtered_rects

