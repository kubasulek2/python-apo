from tkinter import messagebox

from PIL import Image
import numpy as np
from classes.ImageOperation import ImageOperation


class MultiArgument(ImageOperation):

    def addImage(self, image_2, limitSaturation=False):
        if not self.check_are_images_compatible(image_2):
            messagebox.showerror("Error", "Images must be of same size and type.")
            return
        image = self.image
        image_2 = self.preprocess_image(image_2)
        if limitSaturation:
            image = self.reduce_grayscale_levels(image)
            image_2 = self.reduce_grayscale_levels(image_2)
        pixel_values = list(image.getdata())
        pixel_values2 = list(image_2.getdata())
        added_values = [np.clip(value + value2, 0, 255) for value, value2 in zip(pixel_values, pixel_values2)]

        added_image = Image.new('L', self.image.size)
        added_image.putdata(added_values)
        return added_image

    def sub_image(self, image_2):
        if not self.check_are_images_compatible(image_2):
            messagebox.showerror("Error", "Images must be of same size and type.")
            return
        image = self.preprocess_image(self.image)
        image_2 = self.preprocess_image(image_2)

        pixel_values = list(image.getdata())
        pixel_values2 = list(image_2.getdata())
        sub_values = [abs(value - value2) for value, value2 in zip(pixel_values, pixel_values2)]

        sub_image = Image.new('L', self.image.size)
        sub_image.putdata(sub_values)
        return sub_image

    def operate_on_image(self, value=1, operand="+", ):
        pixel_values = list(self.image.getdata())
        if operand == "+":
            new_pixel_values = [np.clip(pixel_value + value, 0, 255) for pixel_value in pixel_values]
        elif operand == "-":
            new_pixel_values = [np.clip(pixel_value - value, 0, 255) for pixel_value in pixel_values]
        elif operand == "*":
            new_pixel_values = [np.clip(pixel_value * value, 0, 255) for pixel_value in pixel_values]
        elif operand == "/":
            new_pixel_values = [np.clip(int(pixel_value / value), 0, 255) for pixel_value in pixel_values]

        new_image = Image.new('L', self.image.size)
        new_image.putdata(new_pixel_values)
        return new_image

    def reduce_grayscale_levels(self, image):
        pixel_values = list(image.getdata())
        new_pixel_values = [np.clip(int(value / 2), 1, 127) for value in pixel_values]

        new_image = Image.new('L', image.size)
        new_image.putdata(new_pixel_values)
        return new_image
