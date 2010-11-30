"""
Class containing queues

"""

import numpy as np
class Queue(list):
    def __init__(self, size):
        self.averages = []
        self.timestamps = []
        self.size = size
    
    def __repr__(self):
        print("\t".join(self.averages))

    def pop(self,new_average, timestamp):
        if len(self.averages) >= self.size:
            self.averages.pop(0)
            self.averages.append(new_average)
            self.timestamps.pop(0)
            self.timestamps.append(timestamp)
        else: 
            self.averages.append(new_average)
            self.timestamps.append(timestamp)
    def punches(self):
        """ Returns true if the newest value is significantly different than the slope over
        the WHOLE time-period
        than the previous values.  Currently uses OLS to calculate the slope
        and to see if it differs. 

        :TODO Come up with a better method for detecting 
        differences in detecting averages in depth
        """
        #:TODO Need to parameterize n
        n = 5
        assert (len(self.averages)==len(self.timestamps))
        size = len(self.averages)
        slopes = []
        for t in [0,size-n]:
            averages = np.asarray(self.averages[t:size])
            timestamps = np.asarray(self.timestamps[t:size])
            """
            slope = np.absolute((np.corrcoef(averages, 
                                 timestamps))*np.std(averages)/np.std(timestamps))
            """
            slope = np.absolute(np.polyfit(timestamps, averages, 1)[0])
            print(slope)
            slopes.append(slope)
        if slopes[0] < slopes[1]:return True
        else: return False
        
    def plot():
        pass
