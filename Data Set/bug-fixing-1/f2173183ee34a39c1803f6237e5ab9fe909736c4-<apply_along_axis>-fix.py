

def apply_along_axis(func1d, axis, arr, *args, **kwargs):
    '\n    Apply a function to 1-D slices along the given axis.\n\n    Execute `func1d(a, *args)` where `func1d` operates on 1-D arrays and `a`\n    is a 1-D slice of `arr` along `axis`.\n\n    Parameters\n    ----------\n    func1d : function\n        This function should accept 1-D arrays. It is applied to 1-D\n        slices of `arr` along the specified axis.\n    axis : integer\n        Axis along which `arr` is sliced.\n    arr : ndarray\n        Input array.\n    args : any\n        Additional arguments to `func1d`.\n    kwargs : any\n        Additional named arguments to `func1d`.\n\n        .. versionadded:: 1.9.0\n\n\n    Returns\n    -------\n    apply_along_axis : ndarray\n        The output array. The shape of `outarr` is identical to the shape of\n        `arr`, except along the `axis` dimension. This axis is removed, and\n        replaced with new dimensions equal to the shape of the return value\n        of `func1d`. So if `func1d` returns a scalar `outarr` will have one\n        fewer dimensions than `arr`.\n\n    See Also\n    --------\n    apply_over_axes : Apply a function repeatedly over multiple axes.\n\n    Examples\n    --------\n    >>> def my_func(a):\n    ...     """Average first and last element of a 1-D array"""\n    ...     return (a[0] + a[-1]) * 0.5\n    >>> b = np.array([[1,2,3], [4,5,6], [7,8,9]])\n    >>> np.apply_along_axis(my_func, 0, b)\n    array([ 4.,  5.,  6.])\n    >>> np.apply_along_axis(my_func, 1, b)\n    array([ 2.,  5.,  8.])\n\n    For a function that returns a 1D array, the number of dimensions in\n    `outarr` is the same as `arr`.\n\n    >>> b = np.array([[8,1,7], [4,3,9], [5,2,6]])\n    >>> np.apply_along_axis(sorted, 1, b)\n    array([[1, 7, 8],\n           [3, 4, 9],\n           [2, 5, 6]])\n\n    For a function that returns a higher dimensional array, those dimensions\n    are inserted in place of the `axis` dimension.\n\n    >>> b = np.array([[1,2,3], [4,5,6], [7,8,9]])\n    >>> np.apply_along_axis(np.diag, -1, b)\n    array([[[1, 0, 0],\n            [0, 2, 0],\n            [0, 0, 3]],\n           [[4, 0, 0],\n            [0, 5, 0],\n            [0, 0, 6]],\n           [[7, 0, 0],\n            [0, 8, 0],\n            [0, 0, 9]]])\n    '
    arr = asanyarray(arr)
    nd = arr.ndim
    axis = normalize_axis_index(axis, nd)
    in_dims = list(range(nd))
    inarr_view = transpose(arr, ((in_dims[:axis] + in_dims[(axis + 1):]) + [axis]))
    inds = ndindex(inarr_view.shape[:(- 1)])
    inds = ((ind + (Ellipsis,)) for ind in inds)
    try:
        ind0 = next(inds)
    except StopIteration:
        raise ValueError('Cannot apply_along_axis when any iteration dimensions are 0')
    res = asanyarray(func1d(inarr_view[ind0], *args, **kwargs))
    buff = zeros((inarr_view.shape[:(- 1)] + res.shape), res.dtype)
    buff_dims = list(range(buff.ndim))
    buff_permute = ((buff_dims[0:axis] + buff_dims[(buff.ndim - res.ndim):buff.ndim]) + buff_dims[axis:(buff.ndim - res.ndim)])
    if (not isinstance(res, matrix)):
        buff = res.__array_prepare__(buff)
    buff[ind0] = res
    for ind in inds:
        buff[ind] = asanyarray(func1d(inarr_view[ind], *args, **kwargs))
    if (not isinstance(res, matrix)):
        buff = res.__array_wrap__(buff)
        return transpose(buff, buff_permute)
    else:
        out_arr = transpose(buff, buff_permute)
        return res.__array_wrap__(out_arr)
