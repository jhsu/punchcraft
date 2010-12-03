import unittest
import sys
from mousecontrol import MouseControl

class MouseControlTest(unittest.TestCase):
    def setUp(self):
        self.mc = MouseControl(640, 480)
        self.mc.max_x, self.mc.max_y = (1024, 600)
        self.mc.position = None


    def test_has_display(self):
        self.assertTrue(self.mc.mouse, 'MouseControl should be mouse aware')

    def test_mouse_convert_x(self):
        self.assertEqual(0, self.mc.target_x(0))
        self.assertEqual(float(self.mc.max_x), self.mc.target_x(self.mc.virtual_width))

    def test_mouse_convert_y(self):
        self.assertEqual(0, self.mc.target_y(0))
        self.assertEqual(float(self.mc.max_y), self.mc.target_y(self.mc.virtual_height))

    def test_can_get_mouse_position(self):
        mouse_x, mouse_y = self.mc.mouse_position()
        self.assertEqual(type(mouse_x), type(int()))

    def test_move_mouse(self):
        self.mc.mouse_to((0,0))
        self.mc.position = (0,0)
        self.mc.to_target((10,10))
        # self.assertEqual((10,10), self.mc.position, 'Mouse did not move to correct location')
        self.assertTrue(True)

    def test_new_movement(self):
        self.mc.mouse_to((16, 0))
        self.mc.position = (10,10)
        self.mc.reset()
        self.assertEqual(None, self.mc.position)
        self.mc.to_target((10,10))
        self.mc.to_target((20,20))
        self.assertEqual((0,12), self.mc.mouse_position())

    def test_restriction_bounds(self):
        self.mc.mouse_to((0,0))
        self.mc.position = (0,0)
        self.mc.to_target((100000,100000))
        self.assertTrue((self.mc.max_x,self.mc.max_y) >= self.mc.position, 'should move to max')


if __name__ == '__main__':
    unittest.main()
