def threshold_minimum(image, nbins=256, max_iter=10000):
    'Return threshold value based on minimum method.\n\n    The histogram of the input `image` is computed and smoothed until there are\n    only two maxima. Then the minimum in between is the threshold value.\n\n    Parameters\n    ----------\n    image : (M, N) ndarray\n        Input image.\n    nbins : int, optional\n        Number of bins used to calculate histogram. This value is ignored for\n        integer arrays.\n    max_iter: int, optional\n        Maximum number of iterations to smooth the histogram.\n\n    Returns\n    -------\n    threshold : float\n        Upper threshold value. All pixels with an intensity higher than\n        this value are assumed to be foreground.\n\n    Raises\n    ------\n    RuntimeError\n        If unable to find two local maxima in the histogram or if the\n        smoothing takes more than 1e4 iterations.\n\n    References\n    ----------\n    .. [1] C. A. Glasbey, "An analysis of histogram-based thresholding\n           algorithms," CVGIP: Graphical Models and Image Processing,\n           vol. 55, pp. 532-537, 1993.\n    .. [2] Prewitt, JMS & Mendelsohn, ML (1966), "The analysis of cell\n           images", Annals of the New York Academy of Sciences 128: 1035-1053\n           :DOI:`10.1111/j.1749-6632.1965.tb11715.x`\n\n    Examples\n    --------\n    >>> from skimage.data import camera\n    >>> image = camera()\n    >>> thresh = threshold_minimum(image)\n    >>> binary = image > thresh\n    '

    def find_local_maxima_idx(hist):
        maximum_idxs = list()
        direction = 1
        for i in range((hist.shape[0] - 1)):
            if (direction > 0):
                if (hist[(i + 1)] < hist[i]):
                    direction = (- 1)
                    maximum_idxs.append(i)
            elif (hist[(i + 1)] > hist[i]):
                direction = 1
        return maximum_idxs
    (hist, bin_centers) = histogram(image.ravel(), nbins, source_range='image')
    smooth_hist = np.copy(hist).astype(np.float64)
    for counter in range(max_iter):
        smooth_hist = ndi.uniform_filter1d(smooth_hist, 3)
        maximum_idxs = find_local_maxima_idx(smooth_hist)
        if (len(maximum_idxs) < 3):
            break
    if (len(maximum_idxs) != 2):
        raise RuntimeError('Unable to find two maxima in histogram')
    elif (counter == (max_iter - 1)):
        raise RuntimeError('Maximum iteration reached for histogramsmoothing')
    threshold_idx = np.argmin(smooth_hist[maximum_idxs[0]:(maximum_idxs[1] + 1)])
    return bin_centers[(maximum_idxs[0] + threshold_idx)]