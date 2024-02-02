from .Window import Window
from .Histogram import Histogram
import tkinter as tk


class HistogramWindow(Window):
    def __init__(self, image, path, parent):
        self.image = image
        self.histogram = Histogram(image)
        self.path = path
        self.hist_window = tk.Toplevel(parent.tkWindow)
        self.create_histogram()

        super().__init__(self.hist_window, parent)

    def create_histogram(self):
        result = self.histogram.calculate_histogram()
        if self.histogram.is_gray_scale:
            r = result[0]
        else:
            r, g, b = result
        self.hist_window.title("Histogram")
        canvas = None

        if self.histogram.is_gray_scale:
            canvas = self.create_scrollableCanvas(850)
            max_value = max(r)
            for i in range(256):
                value = r[i]
                if value > 0:
                    canvas.create_line(50 + i * 3, 550, 50 + i * 3, 550 - (value * 500 / max_value),
                                       fill="black")
            # Add labels for every 10th value
            for i in range(0, 256, 10):
                canvas.create_text(50 + i * 3, 570, anchor=tk.N, text=str(i), fill="black")

        else:
            canvas = self.create_scrollableCanvas(2500)
            max_value = max(max(r), max(g), max(b))

            colors = [["red", 0], ["green", 1], ["blue", 2]]

            for [color, position] in colors:
                for i in range(256):
                    shift = 0 if position == 0 else 60 + (255 * 3) * position
                    value = r[i] if color == "red" else (g[i] if color == "green" else b[i])
                    if value > 0:
                        canvas.create_line(shift + 50 + i * 3, 550, shift + 50 + i * 3, 550 - (value * 500 / max_value),
                                           fill=color)

                # Add labels for every 10th value
                for i in range(0, 256, 10):
                    canvas.create_text(shift + 50 + i * 3, 570, anchor=tk.N, text=str(i), fill="black")

                # Add labels for every 10th max_value
            for i in range(0, max_value + 1, int(max_value / 10)):
                canvas.create_text(50, 550 - (i * 500 / max_value), anchor=tk.E, text=str(i), fill="black")

        canvas.update()  # Update the canvas to ensure the display is refreshed

        def display_value(event):
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)
            val = max_value - int((y - 50) / 500 * max_value)
            canvas.delete("value_text")
            canvas.create_text(x, y - 10, anchor=tk.S, text=str(val), tag="value_text", fill="black")

        canvas.bind("<Motion>", display_value)

        return self.hist_window

    def create_scrollableCanvas(self, width):
        # Internal width

        # Create a canvas with the desired internal width
        canvas = tk.Canvas(self.hist_window, width=850, height=600, bg='gray', scrollregion=(0, 0, width, 600))

        # Create a horizontal scrollbar
        scrollbar = tk.Scrollbar(self.hist_window, orient="horizontal", command=canvas.xview)
        scrollbar.pack(side="bottom", fill="x")

        # Configure the canvas to use the scrollbar
        canvas.config(xscrollcommand=scrollbar.set)
        canvas.pack(expand=tk.YES, fill=tk.BOTH)
        canvas.config(scrollregion=canvas.bbox("all"))
        return canvas
