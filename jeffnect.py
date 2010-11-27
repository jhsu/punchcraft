#!/usr/bin/env python
import freenect
# import cv
import numpy as np
import cv
import sys


def array2cv(a):
    dtype2depth = {
        'uint8':   cv.CV_8UC1,
        'int8':    cv.CV_8UC1,
        'uint16':  cv.CV_16UC1,
        'int16':   cv.IPL_DEPTH_16S,
        'int32':   cv.IPL_DEPTH_32S,
        'float32': cv.IPL_DEPTH_32F,
        'float64': cv.IPL_DEPTH_64F,
    }
    cv_im = cv.CreateMatHeader(a.shape[0],a.shape[1],
                                 dtype2depth[str(a.dtype)])
    cv.SetData(cv_im, a.tostring())
    return cv_im


class Threshold(object):
    """
        Class for setting thresholds
    """
    
    def __init__(self, initial_value):
        self.p = initial_value


    def __call__(self, sliderbar):
        self.p = sliderbar


def close(event, x, y, flags, param):
    if event == cv.CV_EVENT_LBUTTONDOWN:
        freenect.sync_stop()
        sys.exit()
color = (100,255, 100)
cv.NamedWindow('Depth')
cv.SetMouseCallback('Depth', close, param=None)
depthThreshold = Threshold(0)
cv.CreateTrackbar('Depth Threshold', 'Depth', 0, 1200, depthThreshold)
depth_history = []
while 1:
    depth, dts = freenect.sync_get_depth_np()
    #rgb, rts = freenect.sync_get_rgb_np()
    depth = ((depth <= depthThreshold.p).astype(np.uint8)*depth).astype(np.uint16)
    points = np.argwhere(depth!=0)
    avg_dep=0
        #depth = depth.astype(np.uint8)
    if points.any():
        depth_values =depth[depth != 0]
        avg_dep=sum(depth_values)/len(depth_values)
        if len(depth_history) == 5:

        y_max = np.max(points[:,0].ravel())
        x_max = np.max(points[:,1].ravel())
        y_min = np.min(points[:,0].ravel())
        x_min = np.min(points[:,1].ravel())
        depth = array2cv(depth.astype(np.uint8))
        cv.Rectangle(depth, (x_max, y_max), (x_min, y_min), color, thickness=3)
        #cv.PutText(detph, str(avg_dep), (50,50), ,  
        y_avg =reduce(lambda x,y: x+y, points[:,0],0)/float(len(points))
        x_avg =reduce(lambda x,y: x+y, points[:,1],0)/float(len(points))
        cv.Circle(depth, (int(x_avg), int(y_avg)), 48, color)
    #depth = depth.astype(np.uint8)
    cv.ShowImage('Depth', depth)
    cv.WaitKey(10)
