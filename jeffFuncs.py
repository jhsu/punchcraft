"""
Class and functions that work on a series of 2D points in numpy.

Jeffrey Hsu
""" 

import numpy as np

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
    
    def kmeans2():
        """
        Calculates kmeans clustering with a maximum of two groups
        """
        pass
