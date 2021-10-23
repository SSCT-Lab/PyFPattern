

def threshold_li(image, *, tolerance=None):
    'Compute threshold value by Li\'s iterative Minimum Cross Entropy method.\n\n    Parameters\n    ----------\n    image : ndarray\n        Input image.\n\n    tolerance : float, optional\n        Finish the computation when the change in the threshold in an iteration\n        is less than this value. By default, this is half of the range of the\n        input image, divided by 256.\n\n    Returns\n    -------\n    threshold : float\n        Upper threshold value. All pixels with an intensity higher than\n        this value are assumed to be foreground.\n\n    References\n    ----------\n    .. [1] Li C.H. and Lee C.K. (1993) "Minimum Cross Entropy Thresholding"\n           Pattern Recognition, 26(4): 617-625\n           :DOI:`10.1016/0031-3203(93)90115-D`\n    .. [2] Li C.H. and Tam P.K.S. (1998) "An Iterative Algorithm for Minimum\n           Cross Entropy Thresholding" Pattern Recognition Letters, 18(8): 771-776\n           :DOI:`10.1016/S0167-8655(98)00057-9`\n    .. [3] Sezgin M. and Sankur B. (2004) "Survey over Image Thresholding\n           Techniques and Quantitative Performance Evaluation" Journal of\n           Electronic Imaging, 13(1): 146-165\n           :DOI:`10.1117/1.1631315`\n    .. [4] ImageJ AutoThresholder code, http://fiji.sc/wiki/index.php/Auto_Threshold\n\n    Examples\n    --------\n    >>> from skimage.data import camera\n    >>> image = camera()\n    >>> thresh = threshold_li(image)\n    >>> binary = image > thresh\n    '
    image = image[(~ np.isnan(image))]
    if (image.size == 0):
        return np.nan
    if np.all((image == image.flat[0])):
        return image.flat[0]
    image = image[np.isfinite(image)]
    if (image.size == 0):
        return 0.0
    image_min = np.min(image)
    image -= image_min
    image_range = np.max(image)
    tolerance = (tolerance or ((0.5 * image_range) / 256))
    t_curr = np.mean(image)
    t_next = (t_curr + (2 * tolerance))
    while (abs((t_next - t_curr)) > tolerance):
        t_curr = t_next
        foreground = (image > t_curr)
        mean_fore = np.mean(image[foreground])
        mean_back = np.mean(image[(~ foreground)])
        t_next = ((mean_back - mean_fore) / (np.log(mean_back) - np.log(mean_fore)))
    threshold = (t_next + image_min)
    return threshold
