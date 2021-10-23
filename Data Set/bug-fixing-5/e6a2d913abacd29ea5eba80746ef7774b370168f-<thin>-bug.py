def thin(image, max_iter=None):
    '\n    Perform morphological thinning of a binary image.\n\n    Parameters\n    ----------\n    image : binary (M, N) ndarray\n        The image to be thinned.\n\n    max_iter : int, number of iterations, optional\n        Regardless of the value of this parameter, the thinned image\n        is returned immediately if an iteration produces no change.\n        If this parameter is specified it thus sets an upper bound on\n        the number of iterations performed.\n\n    Returns\n    -------\n    out : ndarray of bool\n        Thinned image.\n\n    See also\n    --------\n    skeletonize, skeletonize_3d, medial_axis\n\n    Notes\n    -----\n    This algorithm [1]_ works by making multiple passes over the image,\n    removing pixels matching a set of criteria designed to thin\n    connected regions while preserving eight-connected components and\n    2 x 2 squares [2]_. In each of the two sub-iterations the algorithm\n    correlates the intermediate skeleton image with a neighborhood mask,\n    then looks up each neighborhood in a lookup table indicating whether\n    the central pixel should be deleted in that sub-iteration.\n\n    References\n    ----------\n    .. [1] Z. Guo and R. W. Hall, "Parallel thinning with\n           two-subiteration algorithms," Comm. ACM, vol. 32, no. 3,\n           pp. 359-373, 1989. DOI:10.1145/62065.62074\n    .. [2] Lam, L., Seong-Whan Lee, and Ching Y. Suen, "Thinning\n           Methodologies-A Comprehensive Survey," IEEE Transactions on\n           Pattern Analysis and Machine Intelligence, Vol 14, No. 9,\n           p. 879, 1992. DOI:10.1109/34.161346\n\n    Examples\n    --------\n    >>> square = np.zeros((7, 7), dtype=np.uint8)\n    >>> square[1:-1, 2:-2] = 1\n    >>> square[0, 1] =  1\n    >>> square\n    array([[0, 1, 0, 0, 0, 0, 0],\n           [0, 0, 1, 1, 1, 0, 0],\n           [0, 0, 1, 1, 1, 0, 0],\n           [0, 0, 1, 1, 1, 0, 0],\n           [0, 0, 1, 1, 1, 0, 0],\n           [0, 0, 1, 1, 1, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0]], dtype=uint8)\n    >>> skel = thin(square)\n    >>> skel.astype(np.uint8)\n    array([[0, 1, 0, 0, 0, 0, 0],\n           [0, 0, 1, 0, 0, 0, 0],\n           [0, 0, 0, 1, 0, 0, 0],\n           [0, 0, 0, 1, 0, 0, 0],\n           [0, 0, 0, 1, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0]], dtype=uint8)\n    '
    max_iter = (max_iter or sys.maxsize)
    assert_nD(image, 2)
    skel = np.asanyarray(image, dtype=bool).astype(np.uint8)
    mask = np.array([[8, 4, 2], [16, 0, 1], [32, 64, 128]], dtype=np.uint8)
    for i in range(max_iter):
        before = np.sum(skel)
        for lut in [G123_LUT, G123P_LUT]:
            N = ndi.correlate(skel, mask, mode='constant')
            D = np.take(lut, N)
            skel[D] = 0
        after = np.sum(skel)
        if (before == after):
            break
    return skel.astype(np.bool)