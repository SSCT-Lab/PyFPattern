def _init_axes_pad(self, axes_pad):
    axes_pad = _extend_axes_pad(axes_pad)
    self._axes_pad = axes_pad
    self._horiz_pad_size = Size.Fixed(axes_pad[0])
    self._vert_pad_size = Size.Fixed(axes_pad[1])