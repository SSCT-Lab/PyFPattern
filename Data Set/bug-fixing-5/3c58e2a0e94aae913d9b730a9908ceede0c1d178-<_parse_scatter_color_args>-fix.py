@staticmethod
def _parse_scatter_color_args(c, edgecolors, kwargs, xsize, get_next_color_func):
    "\n        Helper function to process color related arguments of `.Axes.scatter`.\n\n        Argument precedence for facecolors:\n\n        - c (if not None)\n        - kwargs['facecolors']\n        - kwargs['facecolor']\n        - kwargs['color'] (==kwcolor)\n        - 'b' if in classic mode else the result of ``get_next_color_func()``\n\n        Argument precedence for edgecolors:\n\n        - edgecolors (is an explicit kw argument in scatter())\n        - kwargs['edgecolor']\n        - kwargs['color'] (==kwcolor)\n        - 'face' if not in classic mode else None\n\n        Parameters\n        ----------\n        c : color or sequence or sequence of color or None\n            See argument description of `.Axes.scatter`.\n        edgecolors : color or sequence of color or {'face', 'none'} or None\n            See argument description of `.Axes.scatter`.\n        kwargs : dict\n            Additional kwargs. If these keys exist, we pop and process them:\n            'facecolors', 'facecolor', 'edgecolor', 'color'\n            Note: The dict is modified by this function.\n        xsize : int\n            The size of the x and y arrays passed to `.Axes.scatter`.\n        get_next_color_func : callable\n            A callable that returns a color. This color is used as facecolor\n            if no other color is provided.\n\n            Note, that this is a function rather than a fixed color value to\n            support conditional evaluation of the next color.  As of the\n            current implementation obtaining the next color from the\n            property cycle advances the cycle. This must only happen if we\n            actually use the color, which will only be decided within this\n            method.\n\n        Returns\n        -------\n        c\n            The input *c* if it was not *None*, else a color derived from the\n            other inputs or defaults.\n        colors : array(N, 4) or None\n            The facecolors as RGBA values, or *None* if a colormap is used.\n        edgecolors\n            The edgecolor.\n\n        "
    facecolors = kwargs.pop('facecolors', None)
    facecolors = kwargs.pop('facecolor', facecolors)
    edgecolors = kwargs.pop('edgecolor', edgecolors)
    kwcolor = kwargs.pop('color', None)
    if ((kwcolor is not None) and (c is not None)):
        raise ValueError("Supply a 'c' argument or a 'color' kwarg but not both; they differ but their functionalities overlap.")
    if (kwcolor is not None):
        try:
            mcolors.to_rgba_array(kwcolor)
        except ValueError:
            raise ValueError("'color' kwarg must be an color or sequence of color specs.  For a sequence of values to be color-mapped, use the 'c' argument instead.")
        if (edgecolors is None):
            edgecolors = kwcolor
        if (facecolors is None):
            facecolors = kwcolor
    if ((edgecolors is None) and (not rcParams['_internal.classic_mode'])):
        edgecolors = rcParams['scatter.edgecolors']
    c_was_none = (c is None)
    if (c is None):
        c = (facecolors if (facecolors is not None) else ('b' if rcParams['_internal.classic_mode'] else get_next_color_func()))
    c_is_string_or_strings = (isinstance(c, str) or (np.iterable(c) and (len(c) > 0) and isinstance(cbook.safe_first_element(c), str)))

    def invalid_shape_exception(csize, xsize):
        return ValueError(f"'c' argument has {csize} elements, which is inconsistent with 'x' and 'y' with size {xsize}.")
    c_is_mapped = False
    valid_shape = True
    if ((not c_was_none) and (kwcolor is None) and (not c_is_string_or_strings)):
        try:
            c = np.asanyarray(c, dtype=float)
        except ValueError:
            pass
        else:
            if (c.size == xsize):
                c = c.ravel()
                c_is_mapped = True
            else:
                if (c.shape in ((3,), (4,))):
                    _log.warning("'c' argument looks like a single numeric RGB or RGBA sequence, which should be avoided as value-mapping will have precedence in case its length matches with 'x' & 'y'.  Please use a 2-D array with a single row if you really want to specify the same RGB or RGBA value for all points.")
                valid_shape = False
    if (not c_is_mapped):
        try:
            colors = mcolors.to_rgba_array(c)
        except (TypeError, ValueError):
            if (not valid_shape):
                raise invalid_shape_exception(c.size, xsize)
            raise ValueError(f"'c' argument must be a color, a sequence of colors, or a sequence of numbers, not {c}")
        else:
            if (len(colors) not in (0, 1, xsize)):
                raise invalid_shape_exception(len(colors), xsize)
    else:
        colors = None
    return (c, colors, edgecolors)