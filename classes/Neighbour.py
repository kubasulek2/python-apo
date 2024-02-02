from tkinter import simpledialog, messagebox

import numpy as np
from PIL import Image

from classes.ImageOperation import ImageOperation
import cv2


class Neighbour(ImageOperation):
    def linear_smoothing(self, type="Regular"):

        if type == "Gaussian":
            return self.gaussian_smoothing()
        elif type == "Weighted":
            return self.linear_smoothing_regular(use_weights=True)
        else:
            return self.linear_smoothing_regular()

    def linear_smoothing_regular(self, use_weights=False):
        kernel_size = (3, 3)
        weights = self.ask_for_weights() if use_weights else None

        # Read the image
        image_array = self.prepare_image()

        if weights is None:
            smoothed_image = cv2.blur(image_array, kernel_size)
        else:
            smoothed_image = cv2.filter2D(image_array, -1, weights)

        smoothed_image = self.remove_border(smoothed_image)
        return Image.fromarray(smoothed_image)

    def gaussian_smoothing(self, kernel_size=(5, 5), sigma_x=0):
        image_array = self.prepare_image()
        # Grayscale image: apply Gaussian smoothing directly
        smoothed_image_array = cv2.GaussianBlur(
            image_array, kernel_size, sigma_x
        )

        # Convert the smoothed image back to a PIL Image
        smoothed_image_array = self.remove_border(smoothed_image_array)
        smoothed_image_pil = Image.fromarray(np.uint8(smoothed_image_array))
        return smoothed_image_pil

    def linear_sharpening(self, mask):
        # Read the image
        image_array = self.prepare_image()
        # Apply the custom mask using filter2D
        custom_filter = np.array(mask, dtype=np.float32)
        sharpened = cv2.filter2D(image_array, -1, custom_filter)
        # sharpened_image = self.remove_border(image_array)
        # sharpened_image = np.clip(self.image + sharpened_image, 0, 255).astype(np.uint8)
        # Linear sharpening: add the sharpened result to the original image
        # sharpened_image = cv2.addWeighted(image_array, 1.5, sharpened, -0.5, 0)
        return Image.fromarray(sharpened)

    def edge_detection(self, type):
        if type == "Directional":
            user_choice = simpledialog.askstring("Laplacian Mask", "Choose Mask  E, NE, N, NW, W, SW, S, SE")
            if user_choice:
                user_choice = user_choice.upper()
                if user_choice not in ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]:
                    messagebox.showerror("Error", "Invalid choice")
                    return
            return self.sobel_directional(user_choice)
        elif type == "Sobel":
            return self.sobel()
        elif type == "Prewitt":
            return self.prewitt()

    def sobel_directional(self, mask_choice):
        # Convert image to grayscale
        gray = self.prepare_image()
        # Define Sobel masks based on user choice
        sobel_masks = {
            'E': np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]),
            'SE': np.array([[2, 1, 0], [1, 0, -1], [0, -1, -2]]),
            'S': np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]),
            'WS': np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]),
            'W': np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
            'WN': np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]),
            'N': np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
            'NE': np.array([[0, -1, -2], [1, 0, -1], [2, 1, 0]])
        }

        # Check if the user's choice is valid
        if mask_choice not in sobel_masks:
            print("Invalid Sobel mask choice. Please choose from (E, SE, S, WS, W, WN, N, NE).")
            return

        # Apply the selected Sobel mask
        selected_mask = sobel_masks[mask_choice]

        gX = cv2.filter2D(gray, 6, selected_mask)
        gY = cv2.filter2D(gray, 6, - selected_mask)
        gX = cv2.convertScaleAbs(gX)
        gY = cv2.convertScaleAbs(gY)
        # combine the gradient representations into a single image
        combined = cv2.addWeighted(gX, 0.5, gY, 0.5, 0)
        combined = self.remove_border(combined)
        return Image.fromarray(combined)

    def sobel(self):
        image_array = self.prepare_image()

        # Apply the selected Sobel mask
        gX = cv2.Sobel(image_array, 6, 1, 0)
        gY = cv2.Sobel(image_array, 6, 0, 1)
        gX = cv2.convertScaleAbs(gX)
        gY = cv2.convertScaleAbs(gY)
        # combine the gradient representations into a single image
        combined = cv2.addWeighted(gX, 0.5, gY, 0.5, 0)
        combined = self.remove_border(combined)
        return Image.fromarray(combined)

    def prewitt(self):
        gray = self.prepare_image()
        # Apply the selected Sobel mask
        gX = cv2.Sobel(gray, 6, 1, 0)
        gY = cv2.Sobel(gray, 6, 0, 1)
        # Calculate gradient magnitude
        magnitude = np.sqrt(gX ** 2 + gY ** 2)

        # Convert the gradient magnitude to unsigned 8-bit integer for display
        magnitude = self.remove_border(magnitude)
        magnitude = cv2.convertScaleAbs(magnitude)
        return Image.fromarray(magnitude)

    def median_filter(self, kernel_size):
        image_array = self.prepare_image()
        median_filtered_image = cv2.medianBlur(image_array, kernel_size)

        median_filtered_image = self.remove_border(median_filtered_image)
        return Image.fromarray(median_filtered_image)

    def ask_for_weights(self):
        user_input = simpledialog.askinteger("Weights Input", "Enter weight value:")
        if user_input:
            return np.array([[1, 1, 1], [1, int(user_input), 1], [1, 1, 1]], dtype=np.float32) / (8 + int(
                user_input))
        return None

    def ask_for_border(self):
        user_input = simpledialog.askstring("Border Input", "choose border value: 1 - CONSTANT, 2 - REFLECT, 3 - WRAP")
        if user_input:
            if user_input == "2":
                return cv2.BORDER_REFLECT
            elif user_input == "3":
                return cv2.BORDER_WRAP
            else:
                return cv2.BORDER_CONSTANT

    def apply_border(self, image, border):
        if border == cv2.BORDER_CONSTANT:
            borderValue = simpledialog.askinteger("Border value", "Enter border value from 0 - 255")
            if borderValue < 0 or borderValue > 255:
                messagebox.showerror("Error", "Invalid value")
                raise ValueError("Invalid value")
            borderValue = int(borderValue)
            return cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_CONSTANT,
                                      value=(borderValue, borderValue, borderValue))
        else:
            return cv2.copyMakeBorder(image, 1, 1, 1, 1, borderType=border)

    def remove_border(self, image):
        return image
        # return image[1:-1, 1:-1]

    def prepare_image(self):
        image_array = np.array(self.image)
        if len(image_array.shape) == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        border = self.ask_for_border()
        image_array = self.apply_border(image_array, border)
        return image_array
