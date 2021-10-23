def mean(self, axis=None, dtype=None, out=None, keepdims=np._NoValue):
    '\n        Returns the average of the array elements along given axis.\n\n        Masked entries are ignored, and result elements which are not\n        finite will be masked.\n\n        Refer to `numpy.mean` for full documentation.\n\n        See Also\n        --------\n        ndarray.mean : corresponding function for ndarrays\n        numpy.mean : Equivalent function\n        numpy.ma.average: Weighted average.\n\n        Examples\n        --------\n        >>> a = np.ma.array([1,2,3], mask=[False, False, True])\n        >>> a\n        masked_array(data = [1 2 --],\n                     mask = [False False  True],\n               fill_value = 999999)\n        >>> a.mean()\n        1.5\n\n        '
    kwargs = ({
        
    } if (keepdims is np._NoValue) else {
        'keepdims': keepdims,
    })
    if (self._mask is nomask):
        result = super(MaskedArray, self).mean(axis=axis, dtype=dtype, **kwargs)[()]
    else:
        dsum = self.sum(axis=axis, dtype=dtype, **kwargs)
        cnt = self.count(axis=axis, **kwargs)
        if ((cnt.shape == ()) and (cnt == 0)):
            result = masked
        else:
            result = ((dsum * 1.0) / cnt)
    if (out is not None):
        out.flat = result
        if isinstance(out, MaskedArray):
            outmask = getattr(out, '_mask', nomask)
            if (outmask is nomask):
                outmask = out._mask = make_mask_none(out.shape)
            outmask.flat = getattr(result, '_mask', nomask)
        return out
    return result