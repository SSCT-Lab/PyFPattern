def set_foreground(self, fg, isRGBA=False):
    '\n        Set the foreground color.  fg can be a MATLAB format string, a\n        html hex color string, an rgb or rgba unit tuple, or a float between 0\n        and 1.  In the latter case, grayscale is used.\n\n        If you know fg is rgba, set ``isRGBA=True`` for efficiency.\n        '
    if (self._forced_alpha and isRGBA):
        self._rgb = (fg[:3] + (self._alpha,))
    elif self._forced_alpha:
        self._rgb = colors.to_rgba(fg, self._alpha)
    elif isRGBA:
        self._rgb = fg
    else:
        self._rgb = colors.to_rgba(fg)