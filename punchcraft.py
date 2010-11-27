#!/usr/bin/env python
import freenect
import cv
import numpy as np
from Xlib import X, display

def array2cv(a):
  dtype2depth = {
        'uint8':   cv.IPL_DEPTH_8U,
        'int8':    cv.IPL_DEPTH_8S,
        'uint16':  cv.IPL_DEPTH_16U,
        'int16':   cv.IPL_DEPTH_16S,
        'int32':   cv.IPL_DEPTH_32S,
        'float32': cv.IPL_DEPTH_32F,
        'float64': cv.IPL_DEPTH_64F,
    }
  try:
    nChannels = a.shape[2]
  except:
    nChannels = 1
  cv_im = cv.CreateImageHeader((a.shape[1],a.shape[0]),
          dtype2depth[str(a.dtype)],
          nChannels)
  cv.SetData(cv_im, a.tostring(),
             a.dtype.itemsize*nChannels*a.shape[1])
  return cv_im

class Threshold(object):
    def __init__(self, initial_level):
        self.level = initial_level

    def __call__(self, level):
        self.level = level

d = display.Display()
s = d.screen()
root = s.root

def mousepos():
    """mousepos() --> (x, y) get the mouse coordinates on the screen (linux, Xlib)."""
    data = root.query_pointer()._data
    return data["root_x"], data["root_y"]

def toresolution(coord):
    # 1024 x 600
    # 320 x 240
    return (coord[0] / 320.0 * 1024, coord[1] / 240.0 * 600)

depthThreshold = Threshold(640)
max_x, max_y = 1020, 600

cv.NamedWindow('Depth')
cv.CreateTrackbar('Threshold', 'Depth', 640, 1200, depthThreshold)

movable_pos = (100,80)
while 1:
    depth, timestamp = freenect.sync_get_depth_np()
    depth = depth[::2,::2]
    threshold_depths = (depth <= depthThreshold.level).astype(np.uint8)

    depth = array2cv(threshold_depths * depth.astype(np.uint8))

    depth_image = cv.CreateImage(cv.GetSize(depth), cv.IPL_DEPTH_8U, 1)

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
        #   mouse_x_dist = center_point[0] - mouse_x
        #   mouse_y_dist = center_point[1] - mouse_y
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
        root.warp_pointer(mouse_x, 600 - mouse_y)
        d.sync()
    else:
        last_center = None


    cv.Circle(depth, (movable_pos[0], 240 - movable_pos[1]), 3, cv.CV_RGB(255, 255, 255), 3)
    cv.ShowImage('Depth', depth)

    # Listen for ESC key
    c = cv.WaitKey(7) % 0x100
    if c == 27:
        break
