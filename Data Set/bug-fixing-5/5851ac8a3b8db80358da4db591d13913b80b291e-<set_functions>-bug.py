def set_functions(self, functions):
    '\n        Set how the secondary axis converts limits from the parent axes.\n\n        Parameters\n        ----------\n        functions : 2-tuple of func, or `Transform` with an inverse.\n            Transform between the parent axis values and the secondary axis\n            values.\n\n            If supplied as a 2-tuple of functions, the first function is\n            the forward transform function and the second is the inverse\n            transform.\n\n            If a transform is supplied, then the transform must have an\n            inverse.\n\n        '
    if (self._orientation == 'x'):
        set_scale = self.set_xscale
        parent_scale = self._parent.get_xscale()
    else:
        set_scale = self.set_yscale
        parent_scale = self._parent.get_yscale()
    if (parent_scale == 'log'):
        defscale = 'functionlog'
    else:
        defscale = 'function'
    if (isinstance(functions, tuple) and (len(functions) == 2) and callable(functions[0]) and callable(functions[1])):
        self._functions = functions
    elif (functions is None):
        self._functions = ((lambda x: x), (lambda x: x))
    else:
        raise ValueError('functions argument of secondary axes must be a two-tuple of callable functions with the first function being the transform and the second being the inverse')
    set_scale(defscale, functions=self._functions)