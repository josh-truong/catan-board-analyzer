from image_collection import ImageCollection
from catan_tile_shape_detector import CatanTileShapeDetector


image_collection = ImageCollection("../data/tiles/", ".jpg")
detector = CatanTileShapeDetector()
cropped_images = []

for i in range(len(image_collection)):
    detector.run_detection(image_collection.next_image())
    cropped_image = detector.cropped_image
    cropped_images.append(cropped_image)