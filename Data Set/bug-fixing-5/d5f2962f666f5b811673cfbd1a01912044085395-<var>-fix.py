def var(self, axis=None, dtype=None, out=None, ddof=0, keepdims=np._NoValue):
    '\n        Returns the variance of the array elements along given axis.\n\n        Masked entries are ignored, and result elements which are not\n        finite will be masked.\n\n        Refer to `numpy.var` for full documentation.\n\n        See Also\n        --------\n        ndarray.var : corresponding function for ndarrays\n        numpy.var : Equivalent function\n        '
    kwargs = ({
        
    } if (keepdims is np._NoValue) else {
        'keepdims': keepdims,
    })
    if (self._mask is nomask):
        ret = super(MaskedArray, self).var(axis=axis, dtype=dtype, out=out, ddof=ddof, **kwargs)[()]
        if (out is not None):
            if isinstance(out, MaskedArray):
                out.__setmask__(nomask)
            return out
        return ret
    cnt = (self.count(axis=axis, **kwargs) - ddof)
    danom = (self - self.mean(axis, dtype, keepdims=True))
    if iscomplexobj(self):
        danom = (umath.absolute(danom) ** 2)
    else:
        danom *= danom
    dvar = divide(danom.sum(axis, **kwargs), cnt).view(type(self))
    if dvar.ndim:
        dvar._mask = mask_or(self._mask.all(axis, **kwargs), (cnt <= 0))
        dvar._update_from(self)
    elif getmask(dvar):
        dvar = masked
        if (out is not None):
            if isinstance(out, MaskedArray):
                out.flat = 0
                out.__setmask__(True)
            elif (out.dtype.kind in 'biu'):
                errmsg = 'Masked data information would be lost in one or more location.'
                raise MaskError(errmsg)
            else:
                out.flat = np.nan
            return out
    if (out is not None):
        out.flat = dvar
        if isinstance(out, MaskedArray):
            out.__setmask__(dvar.mask)
        return out
    return dvar