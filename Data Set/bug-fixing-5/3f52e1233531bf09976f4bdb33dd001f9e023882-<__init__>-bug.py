def __init__(self, directory, min_freq=10):
    self.directory = directory
    self.counts = PreshCounter()
    self.strings = {
        
    }
    self.min_freq = min_freq