#!/usr/bin/env python
import freenect
import cv
import numpy as np

from array_mods import *
from threshold import *
from mousecontrol import *
from helpers import *
from jeffFuncs import *
from queue import * 
#from arrayfilter import *

DEFAULT_THRESHOLD = 640
COLOR = (100, 255, 100)

depthThreshold = Threshold(DEFAULT_THRESHOLD)

cv.NamedWindow('Depth')
cv.CreateTrackbar('Threshold', 'Depth', DEFAULT_THRESHOLD, 1200, depthThreshold)

mouse_control = MouseControl(320, 240)
depth_values_queue = Queue(40)
while 1:
    depth, timestamp = freenect.sync_get_depth_np()
    depth = depth[::2,::2]
    #depth = gaussian(depth)
    threshold_depths = ((depth <= depthThreshold.level).astype(np.uint8) * depth).astype(np.uint16)
    depth_points = Points(np.argwhere(threshold_depths!=0))


    if depth_points.points.any():

        threshold_depths = array2cv(threshold_depths.astype(np.uint8))
        bound_rect = depth_points.boundingBox()
        cv.Rectangle(threshold_depths, bound_rect[0], bound_rect[1], COLOR, thickness=3)
        cv.Circle(threshold_depths, depth_points.calculateCenter(), 2, COLOR)

        mouse_control.to_target(depth_points.center)
        # cv.Circle(threshold_depths, mouse_control.location(), 3, (255,255,255))

        # Punching Code
        depth_values = depth[depth <= depthThreshold.level]
        depth_values_queue.pop(sum(depth_values)/len(depth_values), timestamp)
        # print(depth_values_queue.averages)
        punch_state = depth_values_queue.punches()

    else:
        mouse_control.reset()


    cv.ShowImage('Depth', threshold_depths)

    # Listen for ESC key
    c = cv.WaitKey(7) % 0x100
    if c == 27:
        break
