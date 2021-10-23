def _asfarray(x):
    '\n    Convert to array with floating or complex dtype.\n\n    float16 values are also promoted to float32.\n    '
    if (not hasattr(x, 'dtype')):
        x = np.asarray(x)
    if (x.dtype == np.float16):
        return np.asarray(x, np.float32)
    elif (x.dtype.kind not in 'fc'):
        return np.asarray(x, np.float64)
    return np.array(x, copy=(not x.flags['ALIGNED']))