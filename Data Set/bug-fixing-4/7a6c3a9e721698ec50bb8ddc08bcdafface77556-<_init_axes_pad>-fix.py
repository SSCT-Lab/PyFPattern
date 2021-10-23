def _init_axes_pad(self, axes_pad):
    axes_pad = np.broadcast_to(axes_pad, 2)
    self._horiz_pad_size = Size.Fixed(axes_pad[0])
    self._vert_pad_size = Size.Fixed(axes_pad[1])