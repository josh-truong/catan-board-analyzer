import tkinter as tk
from image_collection import ImageCollection
from catan_tile_shape_detector import CatanTileShapeDetector
from PIL import ImageTk, Image
from typing import Optional
import cv2

class ImageGalleryApp:
    def __init__(self, image_collection: ImageCollection):
        self.image_collection = image_collection
        self.current_image_path: Optional[str] = None

        self.root = tk.Tk()
        self.root.title("Image Gallery")

        self.side_by_side_label = tk.Label(self.root)
        self.side_by_side_label.pack()

        self.previous_button = tk.Button(self.root, text="Previous", command=self.load_previous_image)
        self.previous_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.root, text="Next", command=self.load_next_image)
        self.next_button.pack(side=tk.LEFT)

        self.load_next_image()

    def load_image(self, image_path: str) -> None:
        self.root.title(f"Image Gallery - {image_path}")
        detector = CatanTileShapeDetector()
        shape = detector.run_detection(image_path)

        img_with_contours = shape.get_image_with_contours()
        cropped_image = shape.get_cropped_image()

        if img_with_contours is not None and cropped_image is not None:
            img_with_contours = Image.fromarray(cv2.cvtColor(img_with_contours, cv2.COLOR_BGR2RGB))
            cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

            # Resize the images if needed
            max_width = max(img_with_contours.width, cropped_image.width)
            max_height = max(img_with_contours.height, cropped_image.height)
            img_with_contours = img_with_contours.resize((max_width, max_height))
            cropped_image = cropped_image.resize((max_width, max_height))

            # Create a new blank image with double width to display side by side
            side_by_side_image = Image.new('RGB', (max_width * 2, max_height))
            side_by_side_image.paste(img_with_contours, (0, 0))
            side_by_side_image.paste(cropped_image, (max_width, 0))

            # Convert the side-by-side image to PhotoImage
            photo = ImageTk.PhotoImage(side_by_side_image)

            # Update the side-by-side label with the new image
            self.side_by_side_label.configure(image=photo)
            self.side_by_side_label.image = photo

            self.current_image_path = image_path

    def load_previous_image(self) -> None:
        image_path = self.image_collection.previous_image()
        if image_path:
            self.load_image(image_path)

    def load_next_image(self) -> None:
        image_path = self.image_collection.next_image()
        if image_path:
            self.load_image(image_path)

    def run(self) -> None:
        initial_image_path = self.image_collection.get_current_image_path()
        if initial_image_path:
            self.load_image(initial_image_path)
        self.root.mainloop()


# image_collection = ImageCollection("../data/game_pieces/number_tokens/", ".jpg")
image_collection = ImageCollection("../data/game_pieces/terrain_hexes/", ".jpg")
app = ImageGalleryApp(image_collection)
app.run()
