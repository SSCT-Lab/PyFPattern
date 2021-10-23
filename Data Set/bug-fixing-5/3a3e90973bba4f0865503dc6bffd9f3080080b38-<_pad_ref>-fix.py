def _pad_ref(arr, pad_amt, method, axis=(- 1)):
    "\n    Pad `axis` of `arr` by reflection.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : tuple of ints, length 2\n        Padding to (prepend, append) along `axis`.\n    method : str\n        Controls method of reflection; options are 'even' or 'odd'.\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt[0]` values prepended and `pad_amt[1]`\n        values appended along `axis`. Both regions are padded with reflected\n        values from the original array.\n\n    Notes\n    -----\n    This algorithm does not pad with repetition, i.e. the edges are not\n    repeated in the reflection. For that behavior, use `mode='symmetric'`.\n\n    The modes 'reflect', 'symmetric', and 'wrap' must be padded with a\n    single function, lest the indexing tricks in non-integer multiples of the\n    original shape would violate repetition in the final iteration.\n\n    "
    if ((pad_amt[0] == 0) and (pad_amt[1] == 0)):
        return arr
    ref_slice = _slice_at_axis(arr.shape, slice(pad_amt[0], 0, (- 1)), axis=axis)
    ref_chunk1 = arr[ref_slice]
    if (('odd' in method) and (pad_amt[0] > 0)):
        edge_slice1 = _slice_first(arr.shape, 1, axis=axis)
        edge_chunk = arr[edge_slice1]
        ref_chunk1 = ((2 * edge_chunk) - ref_chunk1)
        del edge_chunk
    start = ((arr.shape[axis] - pad_amt[1]) - 1)
    end = (arr.shape[axis] - 1)
    ref_slice = _slice_at_axis(arr.shape, slice(start, end), axis=axis)
    rev_idx = _slice_at_axis(arr.shape, slice(None, None, (- 1)), axis=axis)
    ref_chunk2 = arr[ref_slice][rev_idx]
    if ('odd' in method):
        edge_slice2 = _slice_last(arr.shape, 1, axis=axis)
        edge_chunk = arr[edge_slice2]
        ref_chunk2 = ((2 * edge_chunk) - ref_chunk2)
        del edge_chunk
    return np.concatenate((ref_chunk1, arr, ref_chunk2), axis=axis)