from PIL import Image
from classes.ImageOperation import ImageOperation


class SingleArgument(ImageOperation):

    def negate(self):
        image = self.preprocess_image(self.image)
        pixel_values = list(image.getdata())
        negated_values = [255 - value for value in pixel_values]
        negated_image = Image.new('L', self.image.size)
        negated_image.putdata(negated_values)
        return negated_image

    def threshold(self, threshold_value, preserve=False):
        image = self.preprocess_image(self.image)
        pixel_values = list(image.getdata())
        threshold_values = [0 if value < threshold_value else 255 if not preserve else value for value in pixel_values]
        threshold_image = Image.new('L', self.image.size)
        threshold_image.putdata(threshold_values)
        return threshold_image

    def reduce_grayscale_levels(self, levels):
        image = self.preprocess_image(self.image)
        pixel_values = list(image.getdata())
        new_pixel_values = [int(value / 255 * levels) * (255 // (levels - 1)) for value in pixel_values]
        new_image = Image.new('L', self.image.size)
        new_image.putdata(new_pixel_values)
        return new_image
