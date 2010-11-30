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

    """
    depth = array2cv(threshold_depths * depth.astype(np.uint8))

    depth_image = cv.CreateImage(cv.GetSize(threshold_depths), cv.IPL_DEPTH_8U, 1)

    cv.Smooth(depth, depth_image, cv.CV_GAUSSIAN, 3, 0)
    cv.Dilate(depth_image, depth_image, None, 18)
    cv.Erode(depth_image, depth_image, None, 10)

    cv.Threshold(depth_image, depth_image, 70, 255, cv.CV_THRESH_BINARY)

    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(depth_image, storage, 
                              cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    points = []

    while contour:
        bound_rect = cv.BoundingRect(list(contour))
        contour = contour.h_next()

        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        points.append(pt1)
        points.append(pt2)
        cv.Rectangle(depth, pt1, pt2, cv.CV_RGB(255,255,255), 1)
    if len(points):
        center_point = reduce(lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), points)
        cv.Circle(depth, center_point, 40, cv.CV_RGB(255, 255, 255), 1)
        cv.Circle(depth, center_point, 30, cv.CV_RGB(255, 100, 0), 1)
        cv.Circle(depth, center_point, 20, cv.CV_RGB(255, 255, 255), 1)
        cv.Circle(depth, center_point, 10, cv.CV_RGB(255, 100, 0), 1)

        mouse_x, mouse_y = mousepos()
        try:
            if last_center == None:
                last_center = center_point
        except:
            last_center = center_point

        move_to_pos_x, move_to_pos_y = (movable_pos[0] + last_center[0] - center_point[0],
        movable_pos[1] + last_center[1] - center_point[1])

        if move_to_pos_x > 320 or move_to_pos_x < 0:
            move_to_pos_x = movable_pos[0]
        if move_to_pos_y > 240 or move_to_pos_y < 0:
            move_to_pos_y = movable_pos[1]

        movable_pos = (move_to_pos_x, move_to_pos_y)
        last_center = center_point
        mouse_x, mouse_y = toresolution(movable_pos)
        mouse_move_to((mouse_x, 600 - mouse_y))
    else:
        last_center = None

    cv.Circle(depth, (movable_pos[0], 240 - movable_pos[1]), 3, cv.CV_RGB(255, 255, 255), 3)
    """
    cv.ShowImage('Depth', threshold_depths)

    # Listen for ESC key
    c = cv.WaitKey(7) % 0x100
    if c == 27:
        break
