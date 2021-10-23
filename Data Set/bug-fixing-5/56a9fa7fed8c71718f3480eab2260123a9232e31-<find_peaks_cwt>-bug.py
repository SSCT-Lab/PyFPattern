def find_peaks_cwt(vector, widths, wavelet=None, max_distances=None, gap_thresh=None, min_length=None, min_snr=1, noise_perc=10):
    '\n    Attempt to find the peaks in a 1-D array.\n\n    The general approach is to smooth `vector` by convolving it with\n    `wavelet(width)` for each width in `widths`. Relative maxima which\n    appear at enough length scales, and with sufficiently high SNR, are\n    accepted.\n\n    Parameters\n    ----------\n    vector : ndarray\n        1-D array in which to find the peaks.\n    widths : sequence\n        1-D array of widths to use for calculating the CWT matrix. In general,\n        this range should cover the expected width of peaks of interest.\n    wavelet : callable, optional\n        Should take two parameters and return a 1-D array to convolve\n        with `vector`. The first parameter determines the number of points \n        of the returned wavelet array, the second parameter is the scale \n        (`width`) of the wavelet. Should be normalized and symmetric.\n        Default is the ricker wavelet.\n    max_distances : ndarray, optional\n        At each row, a ridge line is only connected if the relative max at\n        row[n] is within ``max_distances[n]`` from the relative max at\n        ``row[n+1]``.  Default value is ``widths/4``.\n    gap_thresh : float, optional\n        If a relative maximum is not found within `max_distances`,\n        there will be a gap. A ridge line is discontinued if there are more\n        than `gap_thresh` points without connecting a new relative maximum.\n        Default is 2.\n    min_length : int, optional\n        Minimum length a ridge line needs to be acceptable.\n        Default is ``cwt.shape[0] / 4``, ie 1/4-th the number of widths.\n    min_snr : float, optional\n        Minimum SNR ratio. Default 1. The signal is the value of\n        the cwt matrix at the shortest length scale (``cwt[0, loc]``), the\n        noise is the `noise_perc`th percentile of datapoints contained within a\n        window of `window_size` around ``cwt[0, loc]``.\n    noise_perc : float, optional\n        When calculating the noise floor, percentile of data points\n        examined below which to consider noise. Calculated using\n        `stats.scoreatpercentile`.  Default is 10.\n\n    Returns\n    -------\n    peaks_indices : ndarray\n        Indices of the locations in the `vector` where peaks were found.\n        The list is sorted.\n\n    See Also\n    --------\n    cwt\n\n    Notes\n    -----\n    This approach was designed for finding sharp peaks among noisy data,\n    however with proper parameter selection it should function well for\n    different peak shapes.\n\n    The algorithm is as follows:\n     1. Perform a continuous wavelet transform on `vector`, for the supplied\n        `widths`. This is a convolution of `vector` with `wavelet(width)` for\n        each width in `widths`. See `cwt`\n     2. Identify "ridge lines" in the cwt matrix. These are relative maxima\n        at each row, connected across adjacent rows. See identify_ridge_lines\n     3. Filter the ridge_lines using filter_ridge_lines.\n\n    .. versionadded:: 0.11.0\n\n    References\n    ----------\n    .. [1] Bioinformatics (2006) 22 (17): 2059-2065.\n        :doi:`10.1093/bioinformatics/btl355`\n        http://bioinformatics.oxfordjournals.org/content/22/17/2059.long\n\n    Examples\n    --------\n    >>> from scipy import signal\n    >>> xs = np.arange(0, np.pi, 0.05)\n    >>> data = np.sin(xs)\n    >>> peakind = signal.find_peaks_cwt(data, np.arange(1,10))\n    >>> peakind, xs[peakind], data[peakind]\n    ([32], array([ 1.6]), array([ 0.9995736]))\n\n    '
    widths = np.asarray(widths)
    if (gap_thresh is None):
        gap_thresh = np.ceil(widths[0])
    if (max_distances is None):
        max_distances = (widths / 4.0)
    if (wavelet is None):
        wavelet = ricker
    cwt_dat = cwt(vector, wavelet, widths)
    ridge_lines = _identify_ridge_lines(cwt_dat, max_distances, gap_thresh)
    filtered = _filter_ridge_lines(cwt_dat, ridge_lines, min_length=min_length, min_snr=min_snr, noise_perc=noise_perc)
    max_locs = np.asarray([x[1][0] for x in filtered])
    max_locs.sort()
    return max_locs