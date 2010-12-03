from numpy import matrix
from pymouse import PyMouse

class MouseControl:
    def __init__(self,virtual_width=None, virtual_height=None):
        self.mouse = PyMouse()
        self.position = None
        self.max_x, self.max_y = self.mouse.screen_size()
        self.virtual_width = virtual_width
        self.virtual_height = virtual_height

    def mouse_position(self):
        return self.mouse.position()

    def virtual_mouse_position(self):
        pos = self.mouse_position()
        x_pos = pos[0] / float(self.max_x) * self.virtual_width
        y_pos = pos[1] / float(self.max_y) * self.virtual_height
        return (x_pos, y_pos)

    def target_x(self, value):
        fraction = value / float(self.virtual_width)
        value = fraction * self.max_x
        return value

    def target_y(self, value):
        fraction = value / float(self.virtual_height)
        value = fraction * self.max_y
        return value

    def target_position(self, pos):
        return ( self.target_x(pos[0]), self.target_y(pos[1]) )

    def virtual_x(self, value):
        if (value > self.virtual_width):
            value = self.virtual_width
        elif (value < 0):
            value = 0
        return value

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
            location = self.virtual_mouse_position()
        return location

    def to_target(self, target):
        if target:
            target = self.virtual_position(target)
            target = (self.virtual_width - target[0], target[1])
        if (self.position != None):
            x_dist = target[0] - self.position[0]
            y_dist = target[1] - self.position[1]
            real_dist = (self.target_x(x_dist), self.target_y(y_dist))
            mouse_pos = self.mouse_position()
            mouse_pos = (mouse_pos[0] + real_dist[0], mouse_pos[1] + real_dist[1])
            self.mouse_to(mouse_pos)
        self.position = target
        return self

    def mouse_to(self, pos):
        self.mouse.move(pos[0], pos[1])

    def reset(self):
        self.position = None
