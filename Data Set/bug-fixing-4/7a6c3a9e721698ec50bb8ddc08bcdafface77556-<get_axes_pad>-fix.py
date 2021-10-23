def get_axes_pad(self):
    '\n        Return the axes padding.\n\n        Returns\n        -------\n        hpad, vpad\n            Padding (horizontal pad, vertical pad) in inches.\n        '
    return (self._horiz_pad_size.fixed_size, self._vert_pad_size.fixed_size)