class Window:
    tkWindow = None
    parent = None

    def __init__(self, tkWindow, parent):
        self.parent = parent
        self.tkWindow = tkWindow
        self.tkWindow.focus_force()
        self.children = []

    def add_child(self, window):
        self.children.append(window)

    def close(self):
        [window.close() for window in self.children]
        self.tkWindow.destroy()



    def isRoot(self):
        if self.parent is None:
            return True
        else:
            return False
