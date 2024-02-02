class ImageOperation:
    def __init__(self, image):
        self.image = image
        unique_colors = set(self.image.getdata())
        self.is_gray_scale = True if len(unique_colors) <= 256 else False
        self.is_binary = True if len(unique_colors) == 2 else False

    def preprocess_image(self, image):
        image = image if image.mode == "L" else image.convert("L")
        return image

    def check_are_images_compatible(self, image_2):
        if self.image.size != image_2.size:
            return False
        elif self.image.mode != image_2.mode:
            return False
        return True
