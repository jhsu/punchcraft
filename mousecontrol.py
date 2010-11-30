from Xlib import X, display
from numpy import matrix

current_display = display.Display()
current_screen = current_display.screen()
current_root = current_screen.root


class MouseControl:
    def __init__(self, current_display=None):
        self.display = current_display.Display() if current_display else display.Display()
        self.mouse = self.mouse_position()
        self.last_position = None

    def update(self):
        self.display.sync()

    def mouse_position(self):
        data = self.display.screen().root.query_pointer()._data
        return data["root_x"], data["root_y"]

    def position(self):
        if(self.last_position != None):
            return self.last_position
        else:
            self.last_position = self.mouse_position()
            return self.last_position

    def to_target(self, target):
        offset = matrix(target) - matrix(self.position())
        self.display.warp_pointer(offset.flat[0], offset.flat[1])
        self.last_position = target
        self.sync()
        return self

    def mouse_to(self, position):
        self.display.screen().root.warp_pointer(position[0], position[1])
        self.sync()

    def reset(self):
        self.last_position = None

    def sync(self):
        self.display.sync()
