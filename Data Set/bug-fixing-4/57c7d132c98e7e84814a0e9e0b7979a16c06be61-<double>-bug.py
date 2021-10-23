def double(self):
    'Casts all floating point parameters and buffers to `double` datatype.\n\n        Returns:\n            Module: self\n        '
    return self._apply((lambda t: (t.double() if t.is_floating_point() else t)))