def prod(self, axis=None, dtype=None, out=None, keepdims=np._NoValue):
    '\n        Return the product of the array elements over the given axis.\n\n        Masked elements are set to 1 internally for computation.\n\n        Refer to `numpy.prod` for full documentation.\n\n        Notes\n        -----\n        Arithmetic is modular when using integer types, and no error is raised\n        on overflow.\n\n        See Also\n        --------\n        ndarray.prod : corresponding function for ndarrays\n        numpy.prod : equivalent function\n        '
    kwargs = ({
        
    } if (keepdims is np._NoValue) else {
        'keepdims': keepdims,
    })
    _mask = self._mask
    newmask = _check_mask_axis(_mask, axis, **kwargs)
    if (out is None):
        result = self.filled(1).prod(axis, dtype=dtype, **kwargs)
        rndim = getattr(result, 'ndim', 0)
        if rndim:
            result = result.view(type(self))
            result.__setmask__(newmask)
        elif newmask:
            result = masked
        return result
    result = self.filled(1).prod(axis, dtype=dtype, out=out, **kwargs)
    if isinstance(out, MaskedArray):
        outmask = getattr(out, '_mask', nomask)
        if (outmask is nomask):
            outmask = out._mask = make_mask_none(out.shape)
        outmask.flat = newmask
    return out