def __init__(self, indexes):
    self._indexes = list(indexes)
    self._curfile = None
    self._curidx = None
    self.open()