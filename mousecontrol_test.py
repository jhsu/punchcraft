import unittest
import sys
from mousecontrol import MouseControl

class MouseControlTest(unittest.TestCase):
    def setUp(self):
        self.mc = MouseControl(640, 480)
        self.mc.position = None


    def test_has_display(self):
        self.assertTrue(self.mc.display, 'MouseControl should be DISPLAY aware')

    def test_can_get_mouse_position(self):
        mouse_x, mouse_y = self.mc.mouse_position()
        self.assertEqual(type(mouse_x), type(int()))

    def test_move_mouse(self):
        self.mc.mouse_to((0,0))
        self.mc.position = (0,0)
        self.mc.to_target((10,10))
        self.assertEqual((10,10), self.mc.position, 'Mouse did not move to correct location')

    def test_new_movement(self):
        self.mc.mouse_to((0,0))
        self.mc.reset()
        self.mc.to_target((20,20))
        self.assertEqual((20,20), self.mc.position)

    def test_restriction_bounds(self):
        self.mc.mouse_to((0,0))
        self.mc.position = (0,0)
        self.mc.to_target((100000,100000))
        self.assertTrue((self.mc.max_x,self.mc.max_y) >= self.mc.position, 'should move to max')


if __name__ == '__main__':
    unittest.main()
