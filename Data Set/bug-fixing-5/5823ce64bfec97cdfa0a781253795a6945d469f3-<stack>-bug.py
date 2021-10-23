@set_module('mxnet.symbol.numpy')
def stack(arrays, axis=0, out=None):
    'Join a sequence of arrays along a new axis.\n        The axis parameter specifies the index of the new axis in the dimensions of the result.\n        For example, if `axis=0` it will be the first dimension and if `axis=-1` it will be the last dimension.\n    Parameters\n    ----------\n    arrays : sequence of array_like\n        Each array must have the same shape.\n    axis : int, optional\n        The axis in the result array along which the input arrays are stacked.\n    out : ndarray, optional\n        If provided, the destination to place the result. The shape must be correct,\n        matching that of what stack would have returned if no out argument were specified.\n    Returns\n    -------\n    stacked : ndarray\n        The stacked array has one more dimension than the input arrays.'

    def get_list(arrays):
        if ((not hasattr(arrays, '__getitem__')) and hasattr(arrays, '__iter__')):
            raise ValueError('expected iterable for arrays but got {}'.format(type(arrays)))
        return [arr for arr in arrays]
    arrays = get_list(arrays)
    return _npi.stack(*arrays, axis=axis, out=out)