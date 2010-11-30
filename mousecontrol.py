from Xlib import X, display
from numpy import matrix

class MouseControl:
    def __init__(self, current_display=None):
        self.display = current_display.Display() if current_display else display.Display()
        self.mouse = self.mouse_position()
        self.last_position = None
        self.max_y = self.display.screen().height_in_pixels
        self.max_x = self.display.screen().width_in_pixels

    def update(self):
        self.display.sync()

    def mouse_position(self):
        data = self.display.screen().root.query_pointer()._data
        return data["root_x"], data["root_y"]

    def position(self):
        if(self.last_position):
            return self.last_position
        else:
            self.last_position = self.mouse_position()
            return self.last_position

    def target_x(self, value):
        if (value > self.max_x ):
            value = self.max_x
        elif (value < 0):
            value = 0
        return value

    def target_y(self, value):
        if (value > self.max_y ):
            value = self.max_y
        elif (value < 0):
            value = 0
        return value

    def to_target(self, target):
        if (self.last_position):
            target = (self.target_x(target[0]), self.target_y(target[0]))
            self.mouse_to(target)
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
