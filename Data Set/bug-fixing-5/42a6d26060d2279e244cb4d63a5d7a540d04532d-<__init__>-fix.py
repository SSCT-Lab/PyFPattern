def __init__(self, indexes, mode=None):
    self._indexes = list(indexes)
    self._curfile = None
    self._curidx = None
    self.mode = mode
    self.open()