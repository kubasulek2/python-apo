from classes.ImageOperation import ImageOperation
import cv2
import numpy as np
from PIL import Image


class Lab5(ImageOperation):
    def canny(self, threshold_1=100, threshold_2=200):
        image_array = self.prepare_image()

        edges = cv2.Canny(image_array, threshold_1, threshold_2)
        return Image.fromarray(edges)

    def segmentation_otsu(self):
        image_array = self.prepare_image()
        # this way
        # ret, thresh = cv2.threshold(image_array, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # or that way
        thresh, ret = cv2.threshold(image_array, 0, 255, cv2.THRESH_OTSU)
        return Image.fromarray(ret), thresh

    def segmentation_adaptive(self, block_size=3, c=1, method=1):
        thresh = cv2.ADAPTIVE_THRESH_MEAN_C if method == 1 else cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        image_array = self.prepare_image()
        result = cv2.adaptiveThreshold(image_array, 255, thresh, cv2.THRESH_BINARY, block_size,
                                       c)
        return Image.fromarray(result)

    def segmentation_user_threshold(self, lower_thresh, upper_thresh):
        image_array = self.prepare_image()
        ret_low, lower = cv2.threshold(image_array, lower_thresh, 255, cv2.THRESH_BINARY)
        ret_up, upper = cv2.threshold(image_array, upper_thresh, 255, cv2.THRESH_BINARY_INV)
        combined = cv2.bitwise_and(lower, upper)
        return ret_low, ret_up, Image.fromarray(combined)

    def prepare_image(self):
        image_array = np.array(self.image)
        if len(image_array.shape) == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        return image_array
