def threshold_isodata(image, nbins=256, return_all=False):
    'Return threshold value(s) based on ISODATA method.\n\n    Histogram-based threshold, known as Ridler-Calvard method or inter-means.\n    Threshold values returned satisfy the following equality::\n\n        threshold = (image[image <= threshold].mean() +\n                     image[image > threshold].mean()) / 2.0\n\n    That is, returned thresholds are intensities that separate the image into\n    two groups of pixels, where the threshold intensity is midway between the\n    mean intensities of these groups.\n\n    For integer images, the above equality holds to within one; for floating-\n    point images, the equality holds to within the histogram bin-width.\n\n    Parameters\n    ----------\n    image : (N, M) ndarray\n        Input image.\n    nbins : int, optional\n        Number of bins used to calculate histogram. This value is ignored for\n        integer arrays.\n    return_all: bool, optional\n        If False (default), return only the lowest threshold that satisfies\n        the above equality. If True, return all valid thresholds.\n\n    Returns\n    -------\n    threshold : float or int or array\n        Threshold value(s).\n\n    References\n    ----------\n    .. [1] Ridler, TW & Calvard, S (1978), "Picture thresholding using an\n           iterative selection method"\n           IEEE Transactions on Systems, Man and Cybernetics 8: 630-632,\n           :DOI:`10.1109/TSMC.1978.4310039`\n    .. [2] Sezgin M. and Sankur B. (2004) "Survey over Image Thresholding\n           Techniques and Quantitative Performance Evaluation" Journal of\n           Electronic Imaging, 13(1): 146-165,\n           http://www.busim.ee.boun.edu.tr/~sankur/SankurFolder/Threshold_survey.pdf\n           :DOI:`10.1117/1.1631315`\n    .. [3] ImageJ AutoThresholder code,\n           http://fiji.sc/wiki/index.php/Auto_Threshold\n\n    Examples\n    --------\n    >>> from skimage.data import coins\n    >>> image = coins()\n    >>> thresh = threshold_isodata(image)\n    >>> binary = image > thresh\n    '
    (hist, bin_centers) = histogram(image.ravel(), nbins, source_range='image')
    if (len(bin_centers) == 1):
        if return_all:
            return bin_centers
        else:
            return bin_centers[0]
    hist = hist.astype(np.float32)
    csuml = np.cumsum(hist)
    csumh = (np.cumsum(hist[::(- 1)])[::(- 1)] - hist)
    intensity_sum = (hist * bin_centers)
    csumh[(- 1)] = 1
    l = (np.cumsum(intensity_sum) / csuml)
    h = ((np.cumsum(intensity_sum[::(- 1)])[::(- 1)] - intensity_sum) / csumh)
    all_mean = ((l + h) / 2.0)
    bin_width = (bin_centers[1] - bin_centers[0])
    distances = (all_mean - bin_centers)
    thresholds = bin_centers[((distances >= 0) & (distances < bin_width))]
    if return_all:
        return thresholds
    else:
        return thresholds[0]