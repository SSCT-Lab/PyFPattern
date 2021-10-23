def order_filter(a, domain, rank):
    '\n    Perform an order filter on an N-dimensional array.\n\n    Perform an order filter on the array in.  The domain argument acts as a\n    mask centered over each pixel.  The non-zero elements of domain are\n    used to select elements surrounding each input pixel which are placed\n    in a list.   The list is sorted, and the output for that pixel is the\n    element corresponding to rank in the sorted list.\n\n    Parameters\n    ----------\n    a : ndarray\n        The N-dimensional input array.\n    domain : array_like\n        A mask array with the same number of dimensions as `a`.\n        Each dimension should have an odd number of elements.\n    rank : int\n        A non-negative integer which selects the element from the\n        sorted list (0 corresponds to the smallest element, 1 is the\n        next smallest element, etc.).\n\n    Returns\n    -------\n    out : ndarray\n        The results of the order filter in an array with the same\n        shape as `a`.\n\n    Examples\n    --------\n    >>> from scipy import signal\n    >>> x = np.arange(25).reshape(5, 5)\n    >>> domain = np.identity(3)\n    >>> x\n    array([[ 0,  1,  2,  3,  4],\n           [ 5,  6,  7,  8,  9],\n           [10, 11, 12, 13, 14],\n           [15, 16, 17, 18, 19],\n           [20, 21, 22, 23, 24]])\n    >>> signal.order_filter(x, domain, 0)\n    array([[  0.,   0.,   0.,   0.,   0.],\n           [  0.,   0.,   1.,   2.,   0.],\n           [  0.,   5.,   6.,   7.,   0.],\n           [  0.,  10.,  11.,  12.,   0.],\n           [  0.,   0.,   0.,   0.,   0.]])\n    >>> signal.order_filter(x, domain, 2)\n    array([[  6.,   7.,   8.,   9.,   4.],\n           [ 11.,  12.,  13.,  14.,   9.],\n           [ 16.,  17.,  18.,  19.,  14.],\n           [ 21.,  22.,  23.,  24.,  19.],\n           [ 20.,  21.,  22.,  23.,  24.]])\n\n    '
    domain = np.asarray(domain)
    size = domain.shape
    for k in range(len(size)):
        if ((size[k] % 2) != 1):
            raise ValueError('Each dimension of domain argument  should have an odd number of elements.')
    return sigtools._order_filterND(a, domain, rank)