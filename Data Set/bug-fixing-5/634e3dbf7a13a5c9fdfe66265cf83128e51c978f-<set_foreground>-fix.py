def set_foreground(self, fg, isRGBA=False):
    '\n        Set the foreground color.\n\n        Parameters\n        ----------\n        fg : color\n        isRGBA : bool\n            If *fg* is known to be an ``(r, g, b, a)`` tuple, *isRGBA* can be\n            set to True to improve performance.\n        '
    if (self._forced_alpha and isRGBA):
        self._rgb = (fg[:3] + (self._alpha,))
    elif self._forced_alpha:
        self._rgb = colors.to_rgba(fg, self._alpha)
    elif isRGBA:
        self._rgb = fg
    else:
        self._rgb = colors.to_rgba(fg)