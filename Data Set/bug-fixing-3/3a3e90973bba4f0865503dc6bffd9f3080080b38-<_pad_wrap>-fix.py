def _pad_wrap(arr, pad_amt, axis=(- 1)):
    "\n    Pad `axis` of `arr` via wrapping.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : tuple of ints, length 2\n        Padding to (prepend, append) along `axis`.\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt[0]` values prepended and `pad_amt[1]`\n        values appended along `axis`. Both regions are padded wrapped values\n        from the opposite end of `axis`.\n\n    Notes\n    -----\n    This method of padding is also known as 'tile' or 'tiling'.\n\n    The modes 'reflect', 'symmetric', and 'wrap' must be padded with a\n    single function, lest the indexing tricks in non-integer multiples of the\n    original shape would violate repetition in the final iteration.\n\n    "
    if ((pad_amt[0] == 0) and (pad_amt[1] == 0)):
        return arr
    wrap_slice = _slice_last(arr.shape, pad_amt[0], axis=axis)
    wrap_chunk1 = arr[wrap_slice]
    wrap_slice = _slice_first(arr.shape, pad_amt[1], axis=axis)
    wrap_chunk2 = arr[wrap_slice]
    return np.concatenate((wrap_chunk1, arr, wrap_chunk2), axis=axis)