import os

class ImageCollection:
    def __init__(self, directory_name: str, file_ext: str = ".jpg") -> None:
        self.directory_name = directory_name
        self.file_ext = file_ext
        self.image_file_path = []
        self.num_imgs = 0
        self.current_index = -1

        self._load_image_paths()

    def __len__(self):
        return self.num_imgs

    def _load_image_paths(self) -> None:
        self.image_file_path = []
        for file in os.listdir(self.directory_name):
            if file.endswith(self.file_ext):
                self.image_file_path.append(os.path.join(self.directory_name, file))
        self.num_imgs = len(self.image_file_path)

        if (self.num_imgs == 0):
            raise Exception(f"No files with '{self.file_ext}' extension found in '{self.directory_name}' directory.")

    def get_current_image_path(self) -> str:
        if 0 <= self.current_index < self.num_imgs:
            print(self.current_index, self.image_file_path[self.current_index])
            return self.image_file_path[self.current_index]
        return None

    def next_image(self) -> str:
        if self.num_imgs == 0: return None
        self.current_index = (self.current_index + 1) % self.num_imgs
        return self.get_current_image_path()

    def previous_image(self) -> str:
        if self.num_imgs == 0: return None
        self.current_index = (self.current_index - 1) % self.num_imgs
        return self.get_current_image_path()


