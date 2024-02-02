from tkinter import messagebox

import numpy as np

from classes.ImageOperation import ImageOperation
from PIL import Image


class Binary(ImageOperation):
    def negate_operation(self):
        image = self.preprocess_image(self.image)
        pixel_data = np.array(image)
        negated_array = np.invert(pixel_data)
        negated_image = Image.fromarray(negated_array)
        return negated_image

    def and_operation(self, image_2):
        if not self.check_are_images_compatible(image_2):
            messagebox.showerror("Error", "Images must be of same size and type")
            return
        image = self.preprocess_image(self.image)
        image_2 = self.preprocess_image(image_2)
        pixel_data = np.array(image)
        pixel_data2 = np.array(image_2)
        and_array = np.bitwise_and(pixel_data, pixel_data2)
        and_image = Image.fromarray(and_array)
        return and_image

    def or_operation(self, image_2):
        if not self.check_are_images_compatible(image_2):
            messagebox.showerror("Error", "Images must be of same size and type")
            return
        image = self.preprocess_image(self.image)
        image_2 = self.preprocess_image(image_2)
        pixel_data = np.array(image)
        pixel_data2 = np.array(image_2)
        or_array = np.bitwise_or(pixel_data, pixel_data2)
        or_image = Image.fromarray(or_array)
        return or_image

    def xor_operation(self, image_2):
        if not self.check_are_images_compatible(image_2):
            messagebox.showerror("Error", "Images must be of same size and type")
            return
        image = self.preprocess_image(self.image)
        image_2 = self.preprocess_image(image_2)
        pixel_data = np.array(image)
        pixel_data2 = np.array(image_2)
        or_array = np.bitwise_xor(pixel_data, pixel_data2)
        or_image = Image.fromarray(or_array)
        return or_image

    def convert_to_binary_mask(self, threshold=128):
        image = self.preprocess_image(self.image)

        binary_mask = image.point(lambda x: 255 if x > threshold else 0).convert('L')

        return binary_mask

    def convert_to_8bit(self):
        if self.is_binary:
            return self.image
        image = self.preprocess_image(self.image)
        eight_bit_image = image.point(lambda x: x * 255)

        return eight_bit_image
