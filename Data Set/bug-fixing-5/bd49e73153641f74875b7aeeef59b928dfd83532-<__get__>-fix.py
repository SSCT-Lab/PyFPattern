def __get__(self, obj, type=None):
    if (obj is None):
        return self
    return getattr(obj.hyperparam, self._attr_name)