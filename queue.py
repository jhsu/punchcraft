"""
Class containing queues

"""
import matplotlib as mp


class Queue(list):
    def __init__(self, size):
        self.averages = []
        self.timestamps = []
        self.size = size
    
    def __repr__(self):
        print("\t".join(self.averages))

    def pop(new_average):
        if len(self.averages)) >= self.size:
            self.averages.pop(0)
            self.averages.append(new_average)
        else: 
            self.averages.append(new_average)

    def difference():
        """ Returns true if the newest value is significantly different i
        than the previous values.  Currently uses OLS to calculate the slope
        and to see if  

        :TODO Come up with a better method for detecting 
        differences in detecting averages in depth
        """
        
        for t in self.average:
        mean(s

    def plot()
