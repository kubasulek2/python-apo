from classes.ImageOperation import ImageOperation
import cv2
import numpy as np
from PIL import Image
from skimage.measure import regionprops, label


class Morphology(ImageOperation):
    def prepare_image(self):
        image_array = np.array(self.image)
        if len(image_array.shape) == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        return image_array

    def dilate(self, size=3, shape_type=1):
        image_array = self.prepare_image()
        kernel = self.get_kernel(size, shape_type)
        dilation = cv2.dilate(image_array, kernel)
        return Image.fromarray(dilation)

    def erode(self, size=3, shape_type=1):
        image_array = self.prepare_image()
        kernel = self.get_kernel(size, shape_type)
        erosion = cv2.erode(image_array, kernel)
        return Image.fromarray(erosion)

    def opening(self, size=3, shape_type=1):
        image_array = self.prepare_image()
        kernel = self.get_kernel(size, shape_type)
        opening = cv2.morphologyEx(image_array, cv2.MORPH_OPEN, kernel)
        return Image.fromarray(opening)

    def closing(self, size=3, shape_type=1):
        image_array = self.prepare_image()
        kernel = self.get_kernel(size, shape_type)
        closing = cv2.morphologyEx(image_array, cv2.MORPH_CLOSE, kernel)
        return Image.fromarray(closing)

    def calculate_features_from_image(self):
        image_array = self.prepare_image()

        labeled_image, num_features = label(image_array, return_num=True)

        feature_vector = []

        for region in regionprops(labeled_image):
            moments = region.moments_central

            area = region.area
            perimeter = region.perimeter

            aspectRatio = region.major_axis_length / region.minor_axis_length
            extent = region.extent
            solidity = region.solidity
            equivalentDiameter = region.equivalent_diameter

            feature_vector.append({
                "Area": area,
                "Moments": moments,
                "Perimeter": perimeter,
                "AspectRatio": aspectRatio,
                "Extent": extent,
                "Solidity": solidity,
                "EquivalentDiameter": equivalentDiameter
            })

        return feature_vector

    def get_kernel(self, size=3, shape_type=1):
        if shape_type == 1:
            return np.array([[3, 3, 3], [3, 3, 3], [3, 3, 3]], np.uint8)
        else:
            return np.array([[0, 3, 0], [3, 3, 3], [0, 3, 0]], np.uint8)
