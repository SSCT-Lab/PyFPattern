def _raw_fft(a, n=None, axis=(- 1), init_function=fftpack.cffti, work_function=fftpack.cfftf, fft_cache=_fft_cache):
    a = asarray(a)
    if (n is None):
        n = a.shape[axis]
    if (n < 1):
        raise ValueError(('Invalid number of FFT data points (%d) specified.' % n))
    wsave = fft_cache.pop_twiddle_factors(n)
    if (wsave is None):
        wsave = init_function(n)
    if (a.shape[axis] != n):
        s = list(a.shape)
        if (s[axis] > n):
            index = ([slice(None)] * len(s))
            index[axis] = slice(0, n)
            a = a[tuple(index)]
        else:
            index = ([slice(None)] * len(s))
            index[axis] = slice(0, s[axis])
            s[axis] = n
            z = zeros(s, a.dtype.char)
            z[tuple(index)] = a
            a = z
    if (axis != (- 1)):
        a = swapaxes(a, axis, (- 1))
    r = work_function(a, wsave)
    if (axis != (- 1)):
        r = swapaxes(r, axis, (- 1))
    fft_cache.put_twiddle_factors(n, wsave)
    return r