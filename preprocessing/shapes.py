import cv2
import math
import numpy as np
from typing import Union
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def get_cropped_image(self):
        pass

    @abstractmethod
    def get_image_with_contours(self):
        pass

class Hexagon(Shape):
    def __init__(self, contour, original_img):
        self.contour = contour
        self.img = original_img

    def area(self) -> float:
        if (self.contour is None): return -1.0
        return cv2.contourArea(self.contour)
    
    def get_cropped_image(self):
        if self.contour is None: return None
        if self.img is None: return None

        epsilon = 0.008 * cv2.arcLength(self.contour, True)
        smoothed_contour = cv2.approxPolyDP(self.contour, epsilon, True)
        mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [smoothed_contour], 0, 255, -1)
        result = cv2.bitwise_and(self.img, self.img, mask=mask)
        return result
    
    def get_image_with_contours(self):
        if self.contour is None: return None
        if self.img is None: return None

        img_copy = self.img.copy()
        cv2.drawContours(img_copy, [self.contour], 0, (255, 0, 0), 2)
        return img_copy

class Circle(Shape):
    def __init__(self, circle: np.ndarray, original_img: Union[np.ndarray, cv2.Mat]):
        self.circle = circle
        self.img = original_img

    def area(self) -> float:
        if (self.circle is None): return -1.0
        (_, _, r) = self.circle
        return math.pi * (r ** 2)
    
    def get_cropped_image(self):
        if self.circle is None: return None
        if self.img is None: return None

        (x, y, r) = self.circle
        mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
        result = cv2.bitwise_and(self.img, self.img, mask=mask)
        return result

    def get_image_with_contours(self):
        if self.circle is None: return None
        if self.img is None: return None

        (x, y, r) = self.circle
        img_copy = self.img.copy()
        cv2.circle(img_copy, (x, y), r, (255, 0, 0), 2)
        return img_copy