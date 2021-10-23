

def _spectral_helper(x, y=None, NFFT=None, Fs=None, detrend_func=None, window=None, noverlap=None, pad_to=None, sides=None, scale_by_freq=None, mode=None):
    '\n    This is a helper function that implements the commonality between the\n    psd, csd, spectrogram and complex, magnitude, angle, and phase spectrums.\n    It is *NOT* meant to be used outside of mlab and may change at any time.\n    '
    if (y is None):
        same_data = True
    else:
        same_data = (y is x)
    if (Fs is None):
        Fs = 2
    if (noverlap is None):
        noverlap = 0
    if (detrend_func is None):
        detrend_func = detrend_none
    if (window is None):
        window = window_hanning
    if (NFFT is None):
        NFFT = 256
    if ((mode is None) or (mode == 'default')):
        mode = 'psd'
    elif (mode not in ['psd', 'complex', 'magnitude', 'angle', 'phase']):
        raise ValueError(("Unknown value for mode %s, must be one of: 'default', 'psd', 'complex', 'magnitude', 'angle', 'phase'" % mode))
    if ((not same_data) and (mode != 'psd')):
        raise ValueError("x and y must be equal if mode is not 'psd'")
    x = np.asarray(x)
    if (not same_data):
        y = np.asarray(y)
    if ((sides is None) or (sides == 'default')):
        if np.iscomplexobj(x):
            sides = 'twosided'
        else:
            sides = 'onesided'
    elif (sides not in ['onesided', 'twosided']):
        raise ValueError(("Unknown value for sides %s, must be one of: 'default', 'onesided', or 'twosided'" % sides))
    if (len(x) < NFFT):
        n = len(x)
        x = np.resize(x, (NFFT,))
        x[n:] = 0
    if ((not same_data) and (len(y) < NFFT)):
        n = len(y)
        y = np.resize(y, (NFFT,))
        y[n:] = 0
    if (pad_to is None):
        pad_to = NFFT
    if (mode != 'psd'):
        scale_by_freq = False
    elif (scale_by_freq is None):
        scale_by_freq = True
    if (sides == 'twosided'):
        numFreqs = pad_to
        if (pad_to % 2):
            freqcenter = (((pad_to - 1) // 2) + 1)
        else:
            freqcenter = (pad_to // 2)
        scaling_factor = 1.0
    elif (sides == 'onesided'):
        if (pad_to % 2):
            numFreqs = ((pad_to + 1) // 2)
        else:
            numFreqs = ((pad_to // 2) + 1)
        scaling_factor = 2.0
    result = stride_windows(x, NFFT, noverlap, axis=0)
    result = detrend(result, detrend_func, axis=0)
    (result, windowVals) = apply_window(result, window, axis=0, return_window=True)
    result = np.fft.fft(result, n=pad_to, axis=0)[:numFreqs, :]
    freqs = np.fft.fftfreq(pad_to, (1 / Fs))[:numFreqs]
    if (not same_data):
        resultY = stride_windows(y, NFFT, noverlap)
        resultY = apply_window(resultY, window, axis=0)
        resultY = detrend(resultY, detrend_func, axis=0)
        resultY = np.fft.fft(resultY, n=pad_to, axis=0)[:numFreqs, :]
        result = (np.conj(result) * resultY)
    elif (mode == 'psd'):
        result = (np.conj(result) * result)
    elif (mode == 'magnitude'):
        result = (np.abs(result) / np.abs(windowVals).sum())
    elif ((mode == 'angle') or (mode == 'phase')):
        result = np.angle(result)
    elif (mode == 'complex'):
        result /= np.abs(windowVals).sum()
    if (mode == 'psd'):
        if (not (NFFT % 2)):
            slc = slice(1, (- 1), None)
        else:
            slc = slice(1, None, None)
        result[slc] *= scaling_factor
        if scale_by_freq:
            result /= Fs
            result /= (np.abs(windowVals) ** 2).sum()
        else:
            result /= (np.abs(windowVals).sum() ** 2)
    t = (np.arange((NFFT / 2), ((len(x) - (NFFT / 2)) + 1), (NFFT - noverlap)) / Fs)
    if (sides == 'twosided'):
        freqs = np.concatenate((freqs[freqcenter:], freqs[:freqcenter]))
        result = np.concatenate((result[freqcenter:, :], result[:freqcenter, :]), 0)
    elif (not (pad_to % 2)):
        freqs[(- 1)] *= (- 1)
    if (mode == 'phase'):
        result = np.unwrap(result, axis=0)
    return (result, freqs, t)
