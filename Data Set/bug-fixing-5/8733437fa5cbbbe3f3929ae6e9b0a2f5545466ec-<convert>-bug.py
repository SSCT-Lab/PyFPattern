def convert(image, dtype, force_copy=False, uniform=False):
    '\n    Convert an image to the requested data-type.\n\n    Warnings are issued in case of precision loss, or when negative values\n    are clipped during conversion to unsigned integer types (sign loss).\n\n    Floating point values are expected to be normalized and will be clipped\n    to the range [0.0, 1.0] or [-1.0, 1.0] when converting to unsigned or\n    signed integers respectively.\n\n    Numbers are not shifted to the negative side when converting from\n    unsigned to signed integer types. Negative values will be clipped when\n    converting to unsigned integers.\n\n    Parameters\n    ----------\n    image : ndarray\n        Input image.\n    dtype : dtype\n        Target data-type.\n    force_copy : bool, optional\n        Force a copy of the data, irrespective of its current dtype.\n    uniform : bool, optional\n        Uniformly quantize the floating point range to the integer range.\n        By default (uniform=False) floating point values are scaled and\n        rounded to the nearest integers, which minimizes back and forth\n        conversion errors.\n\n    References\n    ----------\n    (1) DirectX data conversion rules.\n        http://msdn.microsoft.com/en-us/library/windows/desktop/dd607323%28v=vs.85%29.aspx\n    (2) Data Conversions.\n        In "OpenGL ES 2.0 Specification v2.0.25", pp 7-8. Khronos Group, 2010.\n    (3) Proper treatment of pixels as integers. A.W. Paeth.\n        In "Graphics Gems I", pp 249-256. Morgan Kaufmann, 1990.\n    (4) Dirty Pixels. J. Blinn.\n        In "Jim Blinn\'s corner: Dirty Pixels", pp 47-57. Morgan Kaufmann, 1998.\n\n    '
    image = np.asarray(image)
    dtypeobj = np.dtype(dtype)
    dtypeobj_in = image.dtype
    dtype = dtypeobj.type
    dtype_in = dtypeobj_in.type
    if (dtype_in == dtype):
        if force_copy:
            image = image.copy()
        return image
    if (not ((dtype_in in _supported_types) and (dtype in _supported_types))):
        raise ValueError(('can not convert %s to %s.' % (dtypeobj_in, dtypeobj)))

    def sign_loss():
        warn(('Possible sign loss when converting negative image of type %s to positive image of type %s.' % (dtypeobj_in, dtypeobj)))

    def prec_loss():
        warn(('Possible precision loss when converting from %s to %s' % (dtypeobj_in, dtypeobj)))

    def _dtype(itemsize, *dtypes):
        return next((dt for dt in dtypes if (itemsize < np.dtype(dt).itemsize)))

    def _dtype2(kind, bits, itemsize=1):
        c = (lambda x, y: ((x <= y) if (kind == 'u') else (x < y)))
        s = next((i for i in ((itemsize,) + (2, 4, 8)) if c(bits, (i * 8))))
        return np.dtype((kind + str(s)))

    def _scale(a, n, m, copy=True):
        kind = a.dtype.kind
        if ((n > m) and (a.max() < (2 ** m))):
            mnew = int((np.ceil((m / 2)) * 2))
            if (mnew > m):
                dtype = ('int%s' % mnew)
            else:
                dtype = ('uint%s' % mnew)
            n = int((np.ceil((n / 2)) * 2))
            msg = ('Downcasting %s to %s without scaling because max value %s fits in %s' % (a.dtype, dtype, a.max(), dtype))
            warn(msg)
            return a.astype(_dtype2(kind, m))
        elif (n == m):
            return (a.copy() if copy else a)
        elif (n > m):
            prec_loss()
            if copy:
                b = np.empty(a.shape, _dtype2(kind, m))
                np.floor_divide(a, (2 ** (n - m)), out=b, dtype=a.dtype, casting='unsafe')
                return b
            else:
                a //= (2 ** (n - m))
                return a
        elif ((m % n) == 0):
            if copy:
                b = np.empty(a.shape, _dtype2(kind, m))
                np.multiply(a, (((2 ** m) - 1) // ((2 ** n) - 1)), out=b, dtype=b.dtype)
                return b
            else:
                a = np.array(a, _dtype2(kind, m, a.dtype.itemsize), copy=False)
                a *= (((2 ** m) - 1) // ((2 ** n) - 1))
                return a
        else:
            prec_loss()
            o = (((m // n) + 1) * n)
            if copy:
                b = np.empty(a.shape, _dtype2(kind, o))
                np.multiply(a, (((2 ** o) - 1) // ((2 ** n) - 1)), out=b, dtype=b.dtype)
                b //= (2 ** (o - m))
                return b
            else:
                a = np.array(a, _dtype2(kind, o, a.dtype.itemsize), copy=False)
                a *= (((2 ** o) - 1) // ((2 ** n) - 1))
                a //= (2 ** (o - m))
                return a
    kind = dtypeobj.kind
    kind_in = dtypeobj_in.kind
    itemsize = dtypeobj.itemsize
    itemsize_in = dtypeobj_in.itemsize
    if (kind == 'b'):
        if (kind_in in 'fi'):
            sign_loss()
        prec_loss()
        return (image > dtype_in((dtype_range[dtype_in][1] / 2)))
    if (kind_in == 'b'):
        result = image.astype(dtype)
        if (kind != 'f'):
            result *= dtype(dtype_range[dtype][1])
        return result
    if (kind in 'ui'):
        imin = np.iinfo(dtype).min
        imax = np.iinfo(dtype).max
    if (kind_in in 'ui'):
        imin_in = np.iinfo(dtype_in).min
        imax_in = np.iinfo(dtype_in).max
    if (kind_in == 'f'):
        if ((np.min(image) < (- 1.0)) or (np.max(image) > 1.0)):
            raise ValueError('Images of type float must be between -1 and 1.')
        if (kind == 'f'):
            if (itemsize_in > itemsize):
                prec_loss()
            return image.astype(dtype)
        prec_loss()
        image = np.array(image, _dtype(itemsize, dtype_in, np.float32, np.float64))
        if (not uniform):
            if (kind == 'u'):
                image *= imax
            else:
                image *= (imax - imin)
                image -= 1.0
                image /= 2.0
            np.rint(image, out=image)
            np.clip(image, imin, imax, out=image)
        elif (kind == 'u'):
            image *= (imax + 1)
            np.clip(image, 0, imax, out=image)
        else:
            image *= (((imax - imin) + 1.0) / 2.0)
            np.floor(image, out=image)
            np.clip(image, imin, imax, out=image)
        return image.astype(dtype)
    if (kind == 'f'):
        if (itemsize_in >= itemsize):
            prec_loss()
        image = np.array(image, _dtype(itemsize_in, dtype, np.float32, np.float64))
        if (kind_in == 'u'):
            image /= imax_in
        else:
            image *= 2.0
            image += 1.0
            image /= (imax_in - imin_in)
        return image.astype(dtype)
    if (kind_in == 'u'):
        if (kind == 'i'):
            image = _scale(image, (8 * itemsize_in), ((8 * itemsize) - 1))
            return image.view(dtype)
        else:
            return _scale(image, (8 * itemsize_in), (8 * itemsize))
    if (kind == 'u'):
        sign_loss()
        image = _scale(image, ((8 * itemsize_in) - 1), (8 * itemsize))
        result = np.empty(image.shape, dtype)
        np.maximum(image, 0, out=result, dtype=image.dtype, casting='unsafe')
        return result
    if (itemsize_in > itemsize):
        return _scale(image, ((8 * itemsize_in) - 1), ((8 * itemsize) - 1))
    image = image.astype(_dtype2('i', (itemsize * 8)))
    image -= imin_in
    image = _scale(image, (8 * itemsize_in), (8 * itemsize), copy=False)
    image += imin
    return image.astype(dtype)