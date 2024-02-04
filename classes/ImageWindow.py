import csv
import os
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk

from .Binary import Binary
from .HistogramWindow import HistogramWindow
from .Lab5 import Lab5
from .LutWindow import LutWindow
from .Morphology import Morphology
from .MultiArgument import MultiArgument
from .Neighbour import Neighbour
from .Window import Window
from .Histogram import Histogram
from .SingleArgument import SingleArgument
import tkinter as tk


class ImageWindow(Window):
    def __init__(self, image, path, parent):
        self.image_path = path
        self.image = image
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_window = tk.Toplevel(parent.tkWindow)
        self.image_window.minsize(700, 500)
        self.image_window.maxsize(1400, 1200)
        self.image_window.title("Edit Image: " + path)

        self.create_menu()

        # Create the bottom panel for the image
        self.bottom_panel = tk.Frame(self.image_window, width=700)
        self.bottom_panel.pack(fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(self.bottom_panel, image=self.photo)
        self.image_label.photo = self.photo
        self.image_label.pack(fill=tk.BOTH, expand=True)

        super().__init__(self.image_window, parent)

    def create_menu(self):
        # Create the top panel with buttons
        top_panel = tk.Frame(self.image_window, height=50, width=700)
        top_panel.pack(fill=tk.BOTH)

        # Create a menu button
        menu_button = tk.Menubutton(top_panel, text="File", underline=0, padx=5)
        menu_button.pack(side=tk.LEFT)

        # Create a menu
        menu = tk.Menu(menu_button, tearoff=0)
        menu_button.configure(menu=menu)

        # Add options to the menu
        menu.add_command(label="Open", command=self.load_new_image)
        menu.add_command(label="Open new window", command=self.open_new_image)
        menu.add_command(label="Save", command=self.save_image)
        menu.add_command(label="Duplicate", command=self.duplicate_image)
        menu.add_command(label="Mirror", command=self.mirror_image)
        menu.add_command(label="Close", command=self.close)

        # Create a menu button
        menu_button = tk.Menubutton(top_panel, text="Hist", underline=0, padx=5)
        menu_button.pack(side=tk.LEFT)

        # Create a menu
        menu = tk.Menu(menu_button, tearoff=0)
        menu_button.configure(menu=menu)

        # Add options to the menu
        menu.add_command(label="Histogram", command=self.show_histogram)
        menu.add_command(label="Lut", command=self.show_lut_table)
        menu.add_command(label="Linear Stretching", command=self.show_linear_stretch)
        menu.add_command(label="Nonlinear Stretching", command=self.show_nonlinear_stretch)
        menu.add_command(label="Equalization", command=self.show_equalization)
        menu.add_command(label="p1-p2 to q3-q4 Stretching", command=self.show_histogram_stretching)

        menu_button = tk.Menubutton(top_panel, text="Single-arg", underline=0, padx=5)
        menu_button.pack(side=tk.LEFT)

        # Create a menu
        menu = tk.Menu(menu_button, tearoff=0)
        menu_button.configure(menu=menu)

        # Add options to the menu
        menu.add_command(label="Negate", command=self.show_negation)
        menu.add_command(label="Binary Threshold", command=self.show_threshold)
        menu.add_command(label="Reduce Grayscale", command=self.show_reduce_grayscale)
        menu.add_command(label="Threshold Preserve", command=self.show_threshold_preserve)

        menu_button = tk.Menubutton(top_panel, text="Multi-arg", underline=0, padx=5)
        menu_button.pack(side=tk.LEFT)

        # Create a menu
        menu = tk.Menu(menu_button, tearoff=0)
        menu_button.configure(menu=menu)

        # Add options to the menu
        menu.add_command(label="Add Image", command=self.show_add_image)
        menu.add_command(label="Subtract Image Absolute", command=self.show_sub_image)
        menu.add_command(label="Add Number", command=self.show_add)
        menu.add_command(label="Subtract Number", command=self.show_subtract)
        menu.add_command(label="Multiply Number", command=self.show_multiply)
        menu.add_command(label="Divide Number", command=self.show_divide)

        menu_button = tk.Menubutton(top_panel, text="Binary", underline=0, padx=5)
        menu_button.pack(side=tk.LEFT)

        # Create a menu
        menu = tk.Menu(menu_button, tearoff=0)
        menu_button.configure(menu=menu)

        # Add options to the menu
        menu.add_command(label="NOT", command=self.show_binary_not)
        menu.add_command(label="AND", command=self.show_binary_add)
        menu.add_command(label="OR", command=self.show_binary_or)
        menu.add_command(label="XOR", command=self.show_binary_xor)
        menu.add_command(label="Binary Mask", command=self.show_binary_mask)
        menu.add_command(label="8bit Mask", command=self.show_8bit_mask)

        menu_button = tk.Menubutton(top_panel, text="Neighbour", underline=0, padx=5)
        menu_button.pack(side=tk.LEFT)

        # Create a menu
        menu = tk.Menu(menu_button, tearoff=0)
        menu_button.configure(menu=menu)

        # Add options to the menu
        menu.add_command(label="Linear smoothing", command=self.show_linear_smoothing)
        menu.add_command(label="Linear sharpening", command=self.show_linear_sharpening)
        menu.add_command(label="Directional Edge detection", command=lambda: self.show_edge_detection("Directional"))
        menu.add_command(label="Sobel Edge detection", command=lambda: self.show_edge_detection("Sobel"))
        menu.add_command(label="Prewitt Edge detection", command=lambda: self.show_edge_detection("Prewitt"))
        menu.add_command(label="Median operation", command=self.show_median)

        menu_button = tk.Menubutton(top_panel, text="Lab 5", underline=0, padx=5)
        menu_button.pack(side=tk.LEFT)

        # Create a menu
        menu = tk.Menu(menu_button, tearoff=0)
        menu_button.configure(menu=menu)

        # Add options to the menu
        menu.add_command(label="Canny", command=self.show_canny)
        menu.add_command(label="Segmentation: User threshold", command=self.show_user_threshold)
        menu.add_command(label="Segmentation: Otsu", command=self.show_otsu)
        menu.add_command(label="Segmentation: Adaptive threshold", command=self.show_adaptive)

        menu_button = tk.Menubutton(top_panel, text="Morph", underline=0, padx=5)
        menu_button.pack(side=tk.LEFT)

        # Create a menu
        menu = tk.Menu(menu_button, tearoff=0)
        menu_button.configure(menu=menu)

        # Add options to the menu
        menu.add_command(label="Erode", command=self.show_erosion)
        menu.add_command(label="Dilate", command=self.show_dilation)
        menu.add_command(label="Open", command=self.show_open)
        menu.add_command(label="Close", command=self.show_close)
        menu.add_command(label="Binary vector", command=self.show_features)

        menu_button = tk.Menubutton(top_panel, text="Project", underline=0, padx=5)
        menu_button.pack(side=tk.LEFT)

        # Create a menu
        menu = tk.Menu(menu_button, tearoff=0)
        menu_button.configure(menu=menu)

        # Add options to the menu
        menu.add_command(label="Hough Transformation", command=self.op_fallback)


    def load_new_image(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            self.image_path = file_path
            image = Image.open(file_path)
            self.update_image(image)

    def show_histogram(self):
        hist_window = HistogramWindow(parent=self, path=self.image_path, image=self.image)
        self.add_child(hist_window)

    def show_lut_table(self):
        lut_window = LutWindow(parent=self, path=self.image_path, image=self.image)
        self.add_child(lut_window)

    def duplicate_image(self):
        copied_image = self.image.copy()
        copied_image_window = ImageWindow(parent=self, path=self.image_path, image=copied_image)
        self.add_child(copied_image_window)

    def mirror_image(self):
        mirrored_img = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.update_image(mirrored_img)

    def open_new_image(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            new_image = Image.open(file_path)
            new_image_window = ImageWindow(parent=self, path=file_path, image=new_image)
            self.add_child(new_image_window)

    def save_image(self):
        _, file_extension = os.path.splitext(self.image_path)
        file_path = filedialog.asksaveasfilename(initialfile=self.image_path)

        if file_path:
            self.image.save(file_path)

    def update_image(self, image):
        self.image = image
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.photo)
        self.image_label.photo = self.photo

    def show_linear_stretch(self):
        histogram = Histogram(self.image)
        image = histogram.linear_histogram_stretching()
        self.update_image(image)

    def show_nonlinear_stretch(self):
        histogram = Histogram(self.image)
        gamma = simpledialog.askfloat("Gamma", "Select gamma value:", minvalue=0.1, maxvalue=10.0)

        saturation = messagebox.askyesno("Limit saturation", "Limit saturation?")

        image = histogram.nonlinear_stretch_image(gamma, saturation)
        self.update_image(image)

    def show_equalization(self):
        histogram = Histogram(self.image)
        image = histogram.histogram_equalization()
        self.update_image(image)

    def show_histogram_stretching(self):
        histogram = Histogram(self.image)

        q3 = simpledialog.askfloat("Linear Stretching", "Choose value q3 (0-255):", minvalue=0, maxvalue=255)
        if q3 is None:
            return
        q4 = simpledialog.askfloat("Linear Stretching", "Choose value q4 (0-255):", minvalue=0, maxvalue=255)
        if q4 is None:
            return
        image = histogram.histogram_stretching(q3, q4)
        self.update_image(image)

    def show_negation(self):
        binary = SingleArgument(self.image)
        image = binary.negate()
        self.update_image(image)

    def show_threshold(self):
        binary = SingleArgument(self.image)
        threshold = simpledialog.askfloat("Threshold", "Select threshold value:", minvalue=1, maxvalue=255)
        image = binary.threshold(threshold)
        self.update_image(image)

    def show_threshold_preserve(self):
        binary = SingleArgument(self.image)
        threshold = simpledialog.askfloat("Threshold", "Select threshold value:", minvalue=1, maxvalue=255)
        image = binary.threshold(threshold, preserve=True)
        self.update_image(image)

    def show_reduce_grayscale(self):
        binary = SingleArgument(self.image)
        levels = simpledialog.askfloat("Reduce Grayscale levels", "Select number of levels (1-20):", minvalue=1,
                                       maxvalue=20)
        image = binary.reduce_grayscale_levels(levels)
        self.update_image(image)

    def show_add_image(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            saturation = messagebox.askyesno("Limit saturation", "Limit saturation?")
            image = Image.open(file_path)
            multi = MultiArgument(self.image)
            image = multi.addImage(image, saturation)
            self.update_image(image)

    def show_sub_image(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            image = Image.open(file_path)
            multi = MultiArgument(self.image)
            image = multi.sub_image(image)
            self.update_image(image)

    def show_add(self):
        multi = MultiArgument(self.image)
        value = simpledialog.askfloat("Add", "Choose value to add:", minvalue=1, maxvalue=255)
        image = multi.operate_on_image(value, "+")
        self.update_image(image)

    def show_subtract(self):
        multi = MultiArgument(self.image)
        value = simpledialog.askfloat("Subtract", "Choose value to subtract:", minvalue=1, maxvalue=255)
        image = multi.operate_on_image(value, "-")
        self.update_image(image)

    def show_multiply(self):
        multi = MultiArgument(self.image)
        value = simpledialog.askfloat("Multiply", "Choose value to multiply:", minvalue=1, maxvalue=255)
        image = multi.operate_on_image(value, "*")
        self.update_image(image)

    def show_divide(self):
        multi = MultiArgument(self.image)
        value = simpledialog.askfloat("Divide", "Choose value to divide:", minvalue=1, maxvalue=255)
        image = multi.operate_on_image(value, "/")
        self.update_image(image)

    def show_binary_not(self):
        binary = Binary(self.image)
        image = binary.negate_operation()
        self.update_image(image)

    def show_binary_add(self):
        binary = Binary(self.image)
        file_path = filedialog.askopenfilename()
        if file_path:
            new_image = Image.open(file_path)
            image = binary.and_operation(new_image)
            self.update_image(image)

    def show_binary_or(self):
        binary = Binary(self.image)
        file_path = filedialog.askopenfilename()
        if file_path:
            new_image = Image.open(file_path)
            image = binary.or_operation(new_image)
            self.update_image(image)

    def show_binary_xor(self):
        binary = Binary(self.image)
        file_path = filedialog.askopenfilename()
        if file_path:
            new_image = Image.open(file_path)
            image = binary.xor_operation(new_image)
            self.update_image(image)

    def show_binary_mask(self):
        binary = Binary(self.image)
        image = binary.convert_to_binary_mask()
        self.update_image(image)

    def show_8bit_mask(self):
        binary = Binary(self.image)
        image = binary.convert_to_8bit()
        self.update_image(image)

    def show_linear_smoothing(self):
        types = ["Regular", "Weighted", "Gaussian"]
        user_choice = simpledialog.askinteger("Linear Smoothing",
                                              "Choose smoothing type  1 -  Regular, 2 - Weighted,  3- Gaussian):")
        i = user_choice - 1
        neighbour = Neighbour(self.image)
        if 0 <= i < len(types):
            image = neighbour.linear_smoothing(type=types[i])
            self.update_image(image)

    def show_linear_sharpening(self):
        masks = [
            [[0, -1, 0], [-1, 4, -1], [0, -1, 0]],
            [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]],
            [[1, -2, 1], [-2, 4, -2], [1, -2, 1]],
        ]
        user_choice = simpledialog.askinteger("Laplacian Mask", "Choose Mask  1, 2, 3")
        i = user_choice - 1
        neighbour = Neighbour(self.image)
        if 0 <= i < len(masks):
            image = neighbour.linear_sharpening(mask=masks[i])
            self.update_image(image)

    def show_edge_detection(self, type):
        neighbour = Neighbour(self.image)
        image = neighbour.edge_detection(type)
        self.update_image(image)

    def show_median(self):
        neighbour = Neighbour(self.image)
        kernel_size = simpledialog.askinteger("Kernel Size", "Choose kernel size (3, 5, 7, 9)")
        if kernel_size is None:
            return
        if kernel_size not in [3, 5, 7, 9]:
            messagebox.showerror("Error", "Invalid kernel size")
            return
        image = neighbour.median_filter(kernel_size)
        self.update_image(image)

    def show_canny(self):
        threshold_1 = simpledialog.askfloat("Threshold", "Select threshold value:", minvalue=1, maxvalue=255)
        threshold_2 = simpledialog.askfloat("Threshold", "Select threshold value:", minvalue=1, maxvalue=255)
        if threshold_1 is None or threshold_2 is None:
            return
        lab5 = Lab5(self.image)
        image = lab5.canny(threshold_1, threshold_2)
        self.update_image(image)

    def show_otsu(self):
        lab5 = Lab5(self.image)
        image, thresh = lab5.segmentation_otsu()
        self.update_image(image)
        messagebox.showinfo("Threshold", "Threshold value: " + str(thresh))

    def show_adaptive(self):
        block_size = simpledialog.askinteger("Block size", "Select block-size odd value:", minvalue=1, maxvalue=25)
        threshold_2 = simpledialog.askinteger("C constant", "Select C constant value:", minvalue=1, maxvalue=10)
        method = simpledialog.askinteger("Method", "Select method: 1 - MEAN, 2 - GAUSSIAN")

        if block_size is None or threshold_2 is None or block_size % 2 == 0 or method not in [1, 2]:
            return

        lab5 = Lab5(self.image)
        image = lab5.segmentation_adaptive(block_size, method)
        self.update_image(image)

    def show_user_threshold(self):
        threshold_1 = simpledialog.askfloat("Threshold", "Select threshold value:", minvalue=1, maxvalue=255)
        threshold_2 = simpledialog.askfloat("Threshold", "Select threshold value:", minvalue=1, maxvalue=255)
        if threshold_1 is None or threshold_2 is None:
            return
        lab5 = Lab5(self.image)
        res_low, res_up, image = lab5.segmentation_user_threshold(threshold_1, threshold_2)
        self.update_image(image)
        # messagebox.showinfo("Return values", "Lower threshold: " + str(res_low) + "\nUpper threshold: " + str(res_up))

    def show_dilation(self):
        method = simpledialog.askinteger("Method", "Select shape: 1 - disk, 2 - cross")
        if method is None or method not in [1, 2]:
            print("error")
            return
        morph = Morphology(self.image)
        image = morph.dilate(method)
        self.update_image(image)

    def show_erosion(self):
        method = simpledialog.askinteger("Method", "Select shape: 1 - disk, 2 - cross")
        if method is None or method not in [1, 2]:
            print("error")
            return
        morph = Morphology(self.image)
        image = morph.erode(method)
        self.update_image(image)

    def show_open(self):
        method = simpledialog.askinteger("Method", "Select shape: 1 - disk, 2 - cross")
        if method is None or method not in [1, 2]:
            print("error")
            return
        morph = Morphology(self.image)
        image = morph.opening(method)
        self.update_image(image)

    def show_close(self):
        method = simpledialog.askinteger("Method", "Select shape: 1 - disk, 2 - cross")
        if method is None or method not in [1, 2]:
            print("error")
            return
        morph = Morphology(self.image)
        image = morph.closing(method)
        self.update_image(image)

    def show_features(self):
        morph = Morphology(self.image)
        features = morph.calculate_features_from_image()
        # save features array as csv file
        # use system dialog to save csv file under path chosen by user
        file_path = filedialog.asksaveasfilename(initialfile="features.csv")
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                fieldnames = ['Area', 'Moments', 'Perimeter', 'AspectRatio', 'Extent', 'Solidity',
                              'EquivalentDiameter']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for feature in features:
                    writer.writerow(feature)

    def op_fallback(self):
        pass
