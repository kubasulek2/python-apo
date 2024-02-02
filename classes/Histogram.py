from PIL import Image, ImageOps, ImageEnhance
import numpy as np


class Histogram:
    def __init__(self, image):
        self.image = image
        unique_colors = set(self.image.getdata())
        self.is_gray_scale = True if len(unique_colors) <= 256 else False

    def calculate_histogram(self):
        if self.is_gray_scale:  # Check if the image is in grayscale mode
            histogram = self.image.histogram()
            return histogram, None, None  # Return grayscale histogram only

        else:  # Check if the image is in color mode
            histogram = self.image.histogram()
            r = histogram[0:256]
            g = histogram[256:512]
            b = histogram[512:768]
            return r, g, b

    def linear_histogram_stretching(self):
        pixel_values = list(self.image.getdata())
        if self.is_gray_scale:  # Check if the image is in grayscale mode
            # Get the pixel values as a list

            stretched_values = self.linear_stretch_channel(pixel_values)

            # Create a new image with the stretched values
            stretched_image = Image.new('L', self.image.size)
            stretched_image.putdata(stretched_values)
            return stretched_image
        else:
            # Separate the pixel values into individual color channels
            red_channel, green_channel, blue_channel = zip(*pixel_values)

            # Perform linear histogram stretching for each color channel
            stretched_red = self.linear_stretch_channel(red_channel)
            stretched_green = self.linear_stretch_channel(green_channel)
            stretched_blue = self.linear_stretch_channel(blue_channel)
            stretched_red_image = Image.new('L', self.image.size)
            stretched_red_image.putdata(stretched_red)
            stretched_green_image = Image.new('L', self.image.size)
            stretched_green_image.putdata(stretched_green)
            stretched_blue_image = Image.new('L', self.image.size)
            stretched_blue_image.putdata(stretched_blue)

            # Combine the stretched color channels into a new image
            stretched_image = Image.merge('RGB', (stretched_red_image, stretched_green_image, stretched_blue_image))
            return stretched_image

    def nonlinear_stretch_image(self, gamma, sat=False):
        pixel_values = list(self.image.getdata())
        if self.is_gray_scale:  # Check if the image is in grayscale mode
            # Get the pixel value

            stretched_values = self.nonlinear_stretch_channel(pixel_values, gamma)

            # Create a new image with the stretched values
            stretched_image = Image.new('L', self.image.size)
            stretched_image.putdata(stretched_values)

        else:
            # Separate the pixel values into individual color channels
            red_channel, green_channel, blue_channel = zip(*pixel_values)

            # Perform linear histogram stretching for each color channel
            stretched_red = self.nonlinear_stretch_channel(red_channel, gamma)
            stretched_green = self.nonlinear_stretch_channel(green_channel, gamma)
            stretched_blue = self.nonlinear_stretch_channel(blue_channel, gamma)
            stretched_red_image = Image.new('L', self.image.size)
            stretched_red_image.putdata(stretched_red)
            stretched_green_image = Image.new('L', self.image.size)
            stretched_green_image.putdata(stretched_green)
            stretched_blue_image = Image.new('L', self.image.size)
            stretched_blue_image.putdata(stretched_blue)

            # Combine the stretched color channels into a new image
            stretched_image = Image.merge('RGB', (stretched_red_image, stretched_green_image, stretched_blue_image))

        if sat:
            img_data = np.array(stretched_image)
            low_percentile, high_percentile = np.percentile(img_data, [2.5, 97.5])
            img_data = np.interp(img_data, (low_percentile, high_percentile), (0, 255))
            stretched_image = Image.fromarray(np.uint8(img_data))

        return stretched_image

    def histogram_equalization(self):
        img_data = np.array(self.image)
        if self.image.mode in ["RGB", "RGBA"]:
            for channel in range(3):
                img_data[..., channel] = self.equalize_channel(img_data[..., channel])
        else:
            img_data = self.equalize_channel(img_data)
        return Image.fromarray(img_data)

    def histogram_stretching(self, q3, q4):
        img_data = np.array(self.image)
        if self.image.mode == "RGB":
            for channel in range(3):
                p1 = min(img_data[..., channel].flatten())
                p2 = max(img_data[..., channel].flatten())
                img_data[..., channel] = np.interp(img_data[..., channel], (p1, p2), (q3, q4))
        else:
            p1 = min(img_data.flatten())
            p2 = max(img_data.flatten())
            img_data = np.interp(img_data, (p1, p2), (q3, q4))
        return Image.fromarray(np.uint8(img_data))

    def equalize_channel(self, img_channel):
        hist, bins = np.histogram(img_channel.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalized = cdf / cdf[-1]  # Normalize the CDF
        img_equalized = np.interp(img_channel, bins[:-1], cdf_normalized * 255).astype('uint8')

        return img_equalized

    def linear_stretch_channel(self, channel):
        # Calculate the minimum and maximum pixel values for the channel
        min_value = min(channel)
        max_value = max(channel)

        # Perform linear histogram stretching for the channel
        stretched_values = [
            int((pixel - min_value) / (max_value - min_value) * 255)
            for pixel in channel
        ]

        return stretched_values

    def nonlinear_stretch_channel(self, channel, gamma):
        stretched_values = [
            max(0, min(255, int(round(255.0 * pow(pixel / 255.0, 1.0 / gamma)))))
            for pixel in channel
        ]
        return stretched_values
