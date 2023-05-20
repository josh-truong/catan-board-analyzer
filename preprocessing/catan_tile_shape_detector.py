import cv2
import numpy as np
import matplotlib.pyplot as plt
from shapes import Shape, Hexagon, Circle
from typing import Union

class CatanTileShapeDetector:
    def __init__(self):
        pass

    def resize_image(self, img: Union[np.ndarray, cv2.Mat], scale_percent=20):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        return img

    def detect_circle(self, img: Union[np.ndarray, cv2.Mat], gray: Union[np.ndarray, cv2.Mat]) -> Shape:
        blurred = cv2.medianBlur(gray, 5)
        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, minDist=30, param1=50, param2=95, minRadius=70, maxRadius=185)
        best_circle = Circle(None, None)
        if circles is not None:
            circles = np.round(circles[0, :]).astype(int)
            largest_circle = max(circles, key=lambda x: x[2])
            best_circle = Circle(largest_circle, img)
        return best_circle
            
    def detect_hexagon(self, img: Union[np.ndarray, cv2.Mat], gray: Union[np.ndarray, cv2.Mat]) -> Shape:
        bestagon = Hexagon(None, None)
        _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i, contour in enumerate(contours):
            if i == 0:
                continue
            
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 6:
                area = cv2.contourArea(contour)

                if area > bestagon.area():
                    bestagon = Hexagon(contour, img)
        return bestagon

    def detect_shapes(self, img: Union[np.ndarray, cv2.Mat]) -> Shape:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        shapes = []
        shapes.append(self.detect_hexagon(img, gray))
        shapes.append(self.detect_circle(img, gray))
        largest_shape = max(shapes, key=lambda shape: shape.area())
        return largest_shape
        

    def run_detection(self, image_path: str) -> Shape:
        img = cv2.imread(image_path)
        if img is None:
            print("Error loading image:", image_path)
            return
        img = self.resize_image(img)
        return self.detect_shapes(img)


if __name__ == "__main__":
    detector = CatanTileShapeDetector()
    # shape = detector.run_detection("../data/game_pieces/terrain_hexes/20230519_133159.jpg")
    
    shape = detector.run_detection("../data/game_pieces/number_tokens/20230520_120836.jpg")
    plt.imshow(shape.get_cropped_image())
    plt.show()
    