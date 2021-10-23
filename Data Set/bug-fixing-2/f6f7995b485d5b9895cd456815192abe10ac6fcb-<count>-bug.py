

def count(self, axis=None, keepdims=np._NoValue):
    '\n        Count the non-masked elements of the array along the given axis.\n\n        Parameters\n        ----------\n        axis : None or int or tuple of ints, optional\n            Axis or axes along which the count is performed.\n            The default (`axis` = `None`) performs the count over all\n            the dimensions of the input array. `axis` may be negative, in\n            which case it counts from the last to the first axis.\n\n            .. versionadded:: 1.10.0\n\n            If this is a tuple of ints, the count is performed on multiple\n            axes, instead of a single axis or all the axes as before.\n        keepdims : bool, optional\n            If this is set to True, the axes which are reduced are left\n            in the result as dimensions with size one. With this option,\n            the result will broadcast correctly against the array.\n\n        Returns\n        -------\n        result : ndarray or scalar\n            An array with the same shape as the input array, with the specified\n            axis removed. If the array is a 0-d array, or if `axis` is None, a\n            scalar is returned.\n\n        See Also\n        --------\n        count_masked : Count masked elements in array or along a given axis.\n\n        Examples\n        --------\n        >>> import numpy.ma as ma\n        >>> a = ma.arange(6).reshape((2, 3))\n        >>> a[1, :] = ma.masked\n        >>> a\n        masked_array(\n          data=[[0, 1, 2],\n                [--, --, --]],\n          mask=[[False, False, False],\n                [ True,  True,  True]],\n          fill_value=999999)\n        >>> a.count()\n        3\n\n        When the `axis` keyword is specified an array of appropriate size is\n        returned.\n\n        >>> a.count(axis=0)\n        array([1, 1, 1])\n        >>> a.count(axis=1)\n        array([3, 0])\n\n        '
    kwargs = ({
        
    } if (keepdims is np._NoValue) else {
        'keepdims': keepdims,
    })
    m = self._mask
    if isinstance(self.data, np.matrix):
        if (m is nomask):
            m = np.zeros(self.shape, dtype=np.bool_)
        m = m.view(type(self.data))
    if (m is nomask):
        if (self.shape is ()):
            if (axis not in (None, 0)):
                raise np.AxisError(axis=axis, ndim=self.ndim)
            return 1
        elif (axis is None):
            if kwargs.get('keepdims', False):
                return np.array(self.size, dtype=np.intp, ndmin=self.ndim)
            return self.size
        axes = normalize_axis_tuple(axis, self.ndim)
        items = 1
        for ax in axes:
            items *= self.shape[ax]
        if kwargs.get('keepdims', False):
            out_dims = list(self.shape)
            for a in axes:
                out_dims[a] = 1
        else:
            out_dims = [d for (n, d) in enumerate(self.shape) if (n not in axes)]
        return np.full(out_dims, items, dtype=np.intp)
    if (self is masked):
        return 0
    return (~ m).sum(axis=axis, dtype=np.intp, **kwargs)
