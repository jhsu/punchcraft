from Xlib import X, display
from numpy import matrix

class MouseControl:
    def __init__(self,virtual_width=None, virtual_height=None, current_display=None):
        self.display = current_display.Display() if current_display else display.Display()
        self.mouse = self.mouse_position()
        self.position = None
        self.max_y = self.display.screen().height_in_pixels
        self.max_x = self.display.screen().width_in_pixels
        self.virtual_width = virtual_width
        self.virtual_height = virtual_height

    def update(self):
        self.display.sync()

    def mouse_position(self):
        data = self.display.screen().root.query_pointer()._data
        return data["root_x"], data["root_y"]

    def virtual_mouse_position(self):
        pos = self.mouse_position()
        x_pos = pos[0] / float(self.max_x) * self.virtual_width
        y_pos = pos[1] / float(self.max_y) * self.virtual_height
        return (x_pos, y_pos)

    def target_x(self, value):
        value = (self.virtual_x(value) / float(self.virtual_width)) * self.max_x
        return value

    def target_y(self, value):
        value = (self.virtual_y(value) / float(self.virtual_height)) * self.max_y
        return value

    def target_position(self, pos):
        return ( self.target_x(pos[0]), self.target_y(pos[1]) )

    def virtual_x(self, value):
        if (value > self.virtual_width):
            value = self.virtual_width
        elif (value < 0):
            value = 0
        return (self.virtual_width - value) # mirror

    def virtual_y(self, value):
        if (value > self.virtual_height):
            value = self.virtual_height
        elif (value < 0):
            value = 0
        return value

    def virtual_position(self, pos):
        return ( self.virtual_x(pos[0]), self.virtual_y(pos[1]) )

    def location(self):
        if (self.position):
            location = self.position
        else:
            location = self.virtual_position(self.mouse_position())
        return location

    def to_target(self, target):
        if (self.position != None):
            self.mouse_to(self.target_position(target))
        self.position = self.virtual_position(target)
        self.sync()
        return self

    def mouse_to(self, position):
        self.display.screen().root.warp_pointer(position[0], position[1])
        self.sync()

    def reset(self):
        self.position = None

    def sync(self):
        self.display.sync()
