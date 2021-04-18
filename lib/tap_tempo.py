#########################
# Tap Tempo Helper Class
#########################

from time import time

class TapTempo:
    def __init__(self):        
        self.enabled = False
        self.times = []


    def addtime(self):        
        t = time()
        if len(self.times) == 0:
            tdiff = 0  # initial seed
        else:
            tdiff = t - self.times[-1][0]
        return (t, tdiff)


    def averagetimes(self):
        averagetime = sum([row[1] for row in self.times])/float(len(self.times))
        self.tempo = (1.0/(averagetime/60.0))        

    def enable(self, current_tempo):
        self.tempo = current_tempo
        self.enabled = True
        self.times = []


    def disable(self):
        self.enabled = False


    def tap(self):        
        self.times.append(self.addtime())
        
        if len(self.times) > 1:
            if self.times[0][1] == 0 or len(self.times) > 8:
                del self.times[0]
            self.averagetimes()
