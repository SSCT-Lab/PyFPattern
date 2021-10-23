def set_data(self, data):
    "Sets this parameter's value on all contexts."
    self.shape = data.shape
    if (self._data is None):
        assert (self._deferred_init is not None), ("Parameter '%s' has not been initialized" % self.name)
        self._deferred_init = (self._deferred_init[:3] + (data,))
        return
    for arr in self.list_data():
        arr[:] = data