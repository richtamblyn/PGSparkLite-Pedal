class mock_oled:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.mock = True

    def begin(self):
        pass
    
    def clear(self):
        pass

    def display(self):
        pass

    def image(self, obj):
        pass