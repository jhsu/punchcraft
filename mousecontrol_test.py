import unittest
import sys
from mousecontrol import MouseControl

class MouseControlTest(unittest.TestCase):
    def setUp(self):
        self.mc = MouseControl()

    def test_has_display(self):
        self.assertTrue(self.mc.display, 'MouseControl should be DISPLAY aware')

if __name__ == '__main__':
    unittest.main()
