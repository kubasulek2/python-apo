from classes.ImageOperation import ImageOperation
import cv2
import numpy as np
from PIL import Image


class Hough(ImageOperation):
    def transform(self, threshold=100):
        img, edges = self.prepare_image()
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)
        if lines is None:
            return Image.fromarray(img)

        for line in lines:
            for rho, theta in line:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * -b)
                y1 = int(y0 + 1000 * a)
                x2 = int(x0 - 1000 * -b)
                y2 = int(y0 - 1000 * a)
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
        return Image.fromarray(img)

    def transform_p(self, threshold=100, min_line_length=100, max_line_gap=10):
        img, edges = self.prepare_image()
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold, minLineLength=min_line_length,
                                maxLineGap=max_line_gap)
        if lines is None:
            return Image.fromarray(img)
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)

        return Image.fromarray(img)

    def prepare_image(self):
        img = np.array(self.image)
        if len(img.shape) == 3:
            print("Converting to gray")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        return img, edges
