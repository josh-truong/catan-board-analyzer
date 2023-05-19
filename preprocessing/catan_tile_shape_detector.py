import cv2
import numpy as np
from typing import Union

class CatanTileShapeDetector:
    def __init__(self):
        self.max_hexagon_area = 0
        self.max_hexagon_contour = None
        self.image_with_contours = None
        self.cropped_image = None

    def resize_image(self, img: Union[np.ndarray, cv2.Mat], scale_percent=20):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        return img

    def detect_shapes(self, img: Union[np.ndarray, cv2.Mat]):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i, contour in enumerate(contours):
            if i == 0:
                continue
            
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 6:
                area = cv2.contourArea(contour)

                if area > self.max_hexagon_area:
                    self.max_hexagon_area = area
                    self.max_hexagon_contour = contour
                    self.image_with_contours = self.get_image_with_contours(img)
                    self.cropped_image = self.get_cropped_image(img)

    def get_image_with_contours(self, img):
        if self.max_hexagon_contour is not None:
            img_copy = img.copy()
            cv2.drawContours(img_copy, [self.max_hexagon_contour], 0, (255, 0, 0), 2)
            return img_copy

    def get_cropped_image(self, img):
        if self.max_hexagon_contour is not None:
            epsilon = 0.008 * cv2.arcLength(self.max_hexagon_contour, True)
            smoothed_contour = cv2.approxPolyDP(self.max_hexagon_contour, epsilon, True)
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, [smoothed_contour], 0, 255, -1)
            result = cv2.bitwise_and(img, img, mask=mask)
            return result

    def run_detection(self, image_path: str):
        img = cv2.imread(image_path)
        if img is None:
            print("Error loading image:", image_path)
            return
        img = self.resize_image(img)
        self.detect_shapes(img)
