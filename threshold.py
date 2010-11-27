class Threshold(object):
    def __init__(self, initial_level):
        self.level = initial_level

    def __call__(self, level):
        self.level = level
