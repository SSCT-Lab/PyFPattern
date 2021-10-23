def __getitem__(self, key):
    (start, stop) = (key.start, key.stop)
    if isinstance(key, slice):
        if (start is None):
            start = 0
        if (stop is None):
            stop = self.data.shape[0]
        if ((stop + self.start) <= self.end):
            idx = slice((start + self.start), (stop + self.start))
        else:
            raise IndexError
    elif isinstance(key, int):
        if ((key + self.start) < self.end):
            idx = (key + self.start)
        else:
            raise IndexError
    elif isinstance(key, np.ndarray):
        if ((np.max(key) + self.start) < self.end):
            idx = (self.start + key).tolist()
        else:
            raise IndexError
    elif isinstance(key, list):
        if ((max(key) + self.start) < self.end):
            idx = [(x + self.start) for x in key]
        else:
            raise IndexError
    else:
        raise IndexError
    if (self.normalizer is not None):
        return self.normalizer(self.data[idx])
    else:
        return self.data[idx]