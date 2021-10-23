def half(self):
    'Casts all floating point parameters and buffers to `half` datatype.\n\n        Returns:\n            Module: self\n        '
    return self._apply((lambda t: (t.half() if t.is_floating_point() else t)))