#!/usr/bin/env python
import freenect
import cv
import numpy as np

from array_mods import *
from threshold import *
from mousecontrol import *
from helpers import *
from jeffFuncs import *

DEFAULT_THRESHOLD = 640
COLOR = (100, 255, 100)

depthThreshold = Threshold(DEFAULT_THRESHOLD)

cv.NamedWindow('Depth')
cv.CreateTrackbar('Threshold', 'Depth', DEFAULT_THRESHOLD, 1200, depthThreshold)

mouse_control = MouseControl()

while 1:
    depth, timestamp = freenect.sync_get_depth_np()
    depth = depth[::2,::2]

    threshold_depths = ((depth <= depthThreshold.level).astype(np.uint8) * depth).astype(np.uint16)
    depth_points = Points(np.argwhere(threshold_depths!=0))
    avg_dep=0

    if depth_points.points.any():
        depth_values = threshold_depths[threshold_depths != 0]
        threshold_depths = array2cv(threshold_depths.astype(np.uint8))
        bound_rect = depth_points.boundingBox()
        cv.Rectangle(threshold_depths, bound_rect[0], bound_rect[1], COLOR, thickness=3)
        cv.Circle(threshold_depths, depth_points.calculateCenter(), 48, COLOR)

        mouse_control.to_target(depth_points.center)
    else:
        mouse_control.reset()


    cv.ShowImage('Depth', threshold_depths)

    # Listen for ESC key
    c = cv.WaitKey(7) % 0x100
    if c == 27:
        break
