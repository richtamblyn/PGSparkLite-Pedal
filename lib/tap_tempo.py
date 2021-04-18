#########################
# Tap Tempo Helper Class
#########################

from datetime import datetime

class TapTempo:
    def __init__(self):
        self.start_tap_time = datetime.now()
        self.enabled = False
        self.tap_count = 0
        self.tempo = 0


    def enable(self, current_tempo):
        self.tempo = current_tempo
        self.enabled = True
        self.tap_count = 0


    def disable(self):
        self.enabled = False


    def tap(self):        
        self.tap_count += 1

        if self.tap_count == 1:
            self.start_tap_time = datetime.now()
            return

        if self.tap_count > 4:
            now_tap_time = datetime.now()
            difference = (now_tap_time - self.start_tap_time)            
            self.tempo = 60 * self.tap_count / difference.seconds
            self.tap_count = 0            
