def __get__(self, obj, type=None):
    return getattr(obj.hyperparam, self._attr_name)