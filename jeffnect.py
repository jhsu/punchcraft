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
        
class Points(object):
    """
    N x 2 numpy array containing 2-Dimensional points.  
    """
    
    def __init__(self, points):
        self.points = points
    
    def calculateCenter(self):
        """
        Calculate center from a 2-d array of [x,y] points.  Returns tuple of 
        center value.  
        """
        y_avg = int(sum(self.points[:,0])/float(len(self.points)))
        x_avg = int(sum(self.points[:,1])/float(len(self.points)))
        self.center = (x_avg, y_avg)
        return(x_avg,y_avg)
    
    
    def boundingBox(self):
        """
        Calculates a bounding box from a set of points.  Returns a tuple of the top right
        and the bottom left corners.
        """
        y_max = np.max(self.points[:,0])
        x_max = np.max(self.points[:,1])
        y_min = np.min(self.points[:,0])
        x_min = np.min(self.points[:,1])
        
        return ((x_max, y_max), (x_min, y_min)) 
    
    
    def noiseReduction(self):
        """
        Gaussian Smoothing to reduce the noise.
        """
        pass


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
    dP = Points(np.argwhere(depth!=0))
    avg_dep=0
        #depth = depth.astype(np.uint8)
    if dP.points.any():
        # Average of the depth values that meet threshold
        depth_values =depth[depth != 0]
        avg_dep=sum(depth_values)/len(depth_values)
        #if len(depth_history) == 5:
        depth = array2cv(depth.astype(np.uint8))
        bound_Rect = dP.boundingBox()
        cv.Rectangle(depth, bound_Rect[0], bound_Rect[1], color, thickness=3)
        #cv.PutText(detph, str(avg_dep), (50,50), ,  
        cv.Circle(depth, dP.calculateCenter(), 48, color)
    cv.ShowImage('Depth', depth)
    cv.WaitKey(10)
