def binary_propagation(input, structure=None, mask=None, output=None, border_value=0, origin=0):
    '\n    Multi-dimensional binary propagation with the given structuring element.\n\n    Parameters\n    ----------\n    input : array_like\n        Binary image to be propagated inside `mask`.\n    structure : array_like, optional\n        Structuring element used in the successive dilations. The output\n        may depend on the structuring element, especially if `mask` has\n        several connex components. If no structuring element is\n        provided, an element is generated with a squared connectivity equal\n        to one.\n    mask : array_like, optional\n        Binary mask defining the region into which `input` is allowed to\n        propagate.\n    output : ndarray, optional\n        Array of the same shape as input, into which the output is placed.\n        By default, a new array is created.\n    border_value : int (cast to 0 or 1), optional\n        Value at the border in the output array.\n    origin : int or tuple of ints, optional\n        Placement of the filter, by default 0.\n\n    Returns\n    -------\n    binary_propagation : ndarray\n        Binary propagation of `input` inside `mask`.\n\n    Notes\n    -----\n    This function is functionally equivalent to calling binary_dilation\n    with the number of iterations less than one: iterative dilation until\n    the result does not change anymore.\n\n    The succession of an erosion and propagation inside the original image\n    can be used instead of an *opening* for deleting small objects while\n    keeping the contours of larger objects untouched.\n\n    References\n    ----------\n    .. [1] http://cmm.ensmp.fr/~serra/cours/pdf/en/ch6en.pdf, slide 15.\n    .. [2] http://www.qi.tnw.tudelft.nl/Courses/FIP/noframes/fip-Morpholo.html#Heading102\n\n    Examples\n    --------\n    >>> from scipy import ndimage\n    >>> input = np.zeros((8, 8), dtype=int)\n    >>> input[2, 2] = 1\n    >>> mask = np.zeros((8, 8), dtype=int)\n    >>> mask[1:4, 1:4] = mask[4, 4]  = mask[6:8, 6:8] = 1\n    >>> input\n    array([[0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 1, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0]])\n    >>> mask\n    array([[0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 1, 1, 1, 0, 0, 0, 0],\n           [0, 1, 1, 1, 0, 0, 0, 0],\n           [0, 1, 1, 1, 0, 0, 0, 0],\n           [0, 0, 0, 0, 1, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 1, 1],\n           [0, 0, 0, 0, 0, 0, 1, 1]])\n    >>> ndimage.binary_propagation(input, mask=mask).astype(int)\n    array([[0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 1, 1, 1, 0, 0, 0, 0],\n           [0, 1, 1, 1, 0, 0, 0, 0],\n           [0, 1, 1, 1, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0]])\n    >>> ndimage.binary_propagation(input, mask=mask,\\\n    ... structure=np.ones((3,3))).astype(int)\n    array([[0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 1, 1, 1, 0, 0, 0, 0],\n           [0, 1, 1, 1, 0, 0, 0, 0],\n           [0, 1, 1, 1, 0, 0, 0, 0],\n           [0, 0, 0, 0, 1, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0, 0, 0]])\n\n    >>> # Comparison between opening and erosion+propagation\n    >>> a = np.zeros((6,6), dtype=int)\n    >>> a[2:5, 2:5] = 1; a[0, 0] = 1; a[5, 5] = 1\n    >>> a\n    array([[1, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0],\n           [0, 0, 1, 1, 1, 0],\n           [0, 0, 1, 1, 1, 0],\n           [0, 0, 1, 1, 1, 0],\n           [0, 0, 0, 0, 0, 1]])\n    >>> ndimage.binary_opening(a).astype(int)\n    array([[0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 1, 0, 0],\n           [0, 0, 1, 1, 1, 0],\n           [0, 0, 0, 1, 0, 0],\n           [0, 0, 0, 0, 0, 0]])\n    >>> b = ndimage.binary_erosion(a)\n    >>> b.astype(int)\n    array([[0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 1, 0, 0],\n           [0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0]])\n    >>> ndimage.binary_propagation(b, mask=a).astype(int)\n    array([[0, 0, 0, 0, 0, 0],\n           [0, 0, 0, 0, 0, 0],\n           [0, 0, 1, 1, 1, 0],\n           [0, 0, 1, 1, 1, 0],\n           [0, 0, 1, 1, 1, 0],\n           [0, 0, 0, 0, 0, 0]])\n\n    '
    return binary_dilation(input, structure, (- 1), mask, output, border_value, origin)