from .Window import Window
from .Histogram import Histogram
import tkinter as tk


class LutWindow(Window):
    def __init__(self, image, path, parent):
        self.image = image
        self.path = path
        self.histogram = Histogram(image)
        hist_window = self.show_LUT(parent.tkWindow)

        super().__init__(hist_window, parent)

    def show_LUT(self, parent_window):
        lut_window = tk.Toplevel(parent_window)
        lut_window.title("LUT Table")
        lut_list = tk.Listbox(lut_window, height=20, width=40)
        lut_list.pack()
        lut_list.insert(tk.END, "Value\t|\tPixel Count\n")
        lut_list.insert(tk.END, "-" * 24 + "\n")

        histogram = self.histogram.calculate_histogram()

        if self.histogram.is_gray_scale:
            self.print_LUT_channel(histogram[0], lut_list)
        else:
            r, g, b = histogram
            self.print_LUT_channel(r, lut_list, "Red")
            self.print_LUT_channel(g, lut_list, "Green")
            self.print_LUT_channel(b, lut_list, "Blue")

        lut_scroll = tk.Scrollbar(lut_window, orient="vertical")
        lut_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        lut_list.config(yscrollcommand=lut_scroll.set)
        lut_scroll.config(command=lut_list.yview)

        return lut_window

    def print_LUT_channel(self, data, lut_list, label=None):

        if label is not None:
            lut_list.insert(tk.END, "\n")
            lut_list.insert(tk.END, label)
            lut_list.insert(tk.END, "\n")

        lut_arr = [0] * 256

        for index in range(0, 256):
            lut_arr[index] = data[index]

        for i in range(len(lut_arr)):
            lut_list.insert(tk.END, f"{i}\t|\t{lut_arr[i]}\n")
