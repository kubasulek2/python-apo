from tkinter import *
from tkinter import filedialog
from PIL import Image

from .Window import Window
from .ImageWindow import ImageWindow


class MainWindow(Window):
    def __init__(self):
        rootWindow = Tk()
        rootWindow.title("APO editor")
        rootWindow.geometry("400x150")

        panel = Frame(rootWindow, width=400, height=150)
        panel.pack()
        open_button = Button(panel, text="Open Image", command=self.open_new_image)
        open_button.pack(side="left", padx=10)
        close_button = Button(panel, text="Close All", command=self.close)
        close_button.pack(side="left", padx=10)

        super().__init__(rootWindow, None)

    def start(self):
        self.tkWindow.mainloop()

    def open_new_image(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            image_window = ImageWindow(path=file_path, image=Image.open(file_path), parent=self)
            self.add_child(image_window)
