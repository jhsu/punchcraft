"""
Class containing queues

"""

import numpy as np
import matplotlib.pyplot as plt 

class Queue(list):
    SIG_DELTA_AVERAGE =1.9

    def __init__(self, size):
        self.averages = []
        self.timestamps = []
        self.size = size
        self.timing = 2
        self.counter = 0
        self.smoothing_queue = [0]*5


    def __repr__(self):
        # print("\t".join(self.averages))
        return ""


    def pop(self,new_average, timestamp):
        """
            Removing and setting the items
        """
        if len(self.averages) >= self.size:
            self.averages.pop(0)
            self.averages.append(new_average)
            self.timestamps.pop(0)
            self.timestamps.append(timestamp)
        else:
            self.averages.append(new_average)
            self.timestamps.append(timestamp)


    def punches(self):
        """ Returns true if the newest value is different than zero over the course of four shots.
        :TODO Come up with a better method for detecting
        differences in detecting averages in depth
        """
        #:TODO Need to parameterize n
        # Initialize smoothing function
        # Also because I can't take the second derivitive

        n = 3
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
            slope = np.absolute(np.polyfit(timestamps, averages, 1)[0])*1000000
            #plt.scatter(timestamps, averages)
            slopes.append(slope)
        # If you were punching you are likely still punching need to set a weighting factor to this somehow
        # print(slopes[1])
        self.smoothing_queue.pop(0)
        if self.SIG_DELTA_AVERAGE < slopes[1]:
            self.smoothing_queue.append(1)
        else:
            self.smoothing_queue.append(0)
        if self.smoothing_queue.count(1) > len(self.smoothing_queue)/2:
            punching = True
        else: punching = False
        # print(self.smoothing_queue)

        return punching
        #self.counter +=1
        """
        if self.counter==self.timing:
            self.counter == 0
        else:
        """
