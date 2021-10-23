def sum(self, axis=None, dtype=None, out=None, keepdims=np._NoValue):
    "\n        Return the sum of the array elements over the given axis.\n\n        Masked elements are set to 0 internally.\n\n        Refer to `numpy.sum` for full documentation.\n\n        See Also\n        --------\n        ndarray.sum : corresponding function for ndarrays\n        numpy.sum : equivalent function\n\n        Examples\n        --------\n        >>> x = np.ma.array([[1,2,3],[4,5,6],[7,8,9]], mask=[0] + [1,0]*4)\n        >>> print(x)\n        [[1 -- 3]\n         [-- 5 --]\n         [7 -- 9]]\n        >>> print(x.sum())\n        25\n        >>> print(x.sum(axis=1))\n        [4 5 16]\n        >>> print(x.sum(axis=0))\n        [8 5 12]\n        >>> print(type(x.sum(axis=0, dtype=np.int64)[0]))\n        <type 'numpy.int64'>\n\n        "
    kwargs = ({
        
    } if (keepdims is np._NoValue) else {
        'keepdims': keepdims,
    })
    _mask = self._mask
    newmask = _check_mask_axis(_mask, axis, **kwargs)
    if (out is None):
        result = self.filled(0).sum(axis, dtype=dtype, **kwargs)
        rndim = getattr(result, 'ndim', 0)
        if rndim:
            result = result.view(type(self))
            result.__setmask__(newmask)
        elif newmask:
            result = masked
        return result
    result = self.filled(0).sum(axis, dtype=dtype, out=out, **kwargs)
    if isinstance(out, MaskedArray):
        outmask = getmask(out)
        if (outmask is nomask):
            outmask = out._mask = make_mask_none(out.shape)
        outmask.flat = newmask
    return out