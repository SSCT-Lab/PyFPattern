def to_rgba(self, x, alpha=None, bytes=False, norm=True):
    '\n        Return a normalized rgba array corresponding to *x*.\n\n        In the normal case, *x* is a 1-D or 2-D sequence of scalars, and\n        the corresponding ndarray of rgba values will be returned,\n        based on the norm and colormap set for this ScalarMappable.\n\n        There is one special case, for handling images that are already\n        rgb or rgba, such as might have been read from an image file.\n        If *x* is an ndarray with 3 dimensions,\n        and the last dimension is either 3 or 4, then it will be\n        treated as an rgb or rgba array, and no mapping will be done.\n        The array can be uint8, or it can be floating point with\n        values in the 0-1 range; otherwise a ValueError will be raised.\n        If it is a masked array, the mask will be ignored.\n        If the last dimension is 3, the *alpha* kwarg (defaulting to 1)\n        will be used to fill in the transparency.  If the last dimension\n        is 4, the *alpha* kwarg is ignored; it does not\n        replace the pre-existing alpha.  A ValueError will be raised\n        if the third dimension is other than 3 or 4.\n\n        In either case, if *bytes* is *False* (default), the rgba\n        array will be floats in the 0-1 range; if it is *True*,\n        the returned rgba array will be uint8 in the 0 to 255 range.\n\n        If norm is False, no normalization of the input data is\n        performed, and it is assumed to be in the range (0-1).\n\n        '
    try:
        if (x.ndim == 3):
            if (x.shape[2] == 3):
                if (alpha is None):
                    alpha = 1
                if (x.dtype == np.uint8):
                    alpha = np.uint8((alpha * 255))
                (m, n) = x.shape[:2]
                xx = np.empty(shape=(m, n, 4), dtype=x.dtype)
                xx[:, :, :3] = x
                xx[:, :, 3] = alpha
            elif (x.shape[2] == 4):
                xx = x
            else:
                raise ValueError('third dimension must be 3 or 4')
            if (xx.dtype.kind == 'f'):
                if (norm and ((xx.max() > 1) or (xx.min() < 0))):
                    raise ValueError('Floating point image RGB values must be in the 0..1 range.')
                if bytes:
                    xx = (xx * 255).astype(np.uint8)
            elif (xx.dtype == np.uint8):
                if (not bytes):
                    xx = (xx.astype(np.float32) / 255)
            else:
                raise ValueError(('Image RGB array must be uint8 or floating point; found %s' % xx.dtype))
            return xx
    except AttributeError:
        pass
    x = ma.asarray(x)
    if norm:
        x = self.norm(x)
    rgba = self.cmap(x, alpha=alpha, bytes=bytes)
    return rgba