def _pad_sym(arr, pad_amt, method, axis=(- 1)):
    "\n    Pad `axis` of `arr` by symmetry.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : tuple of ints, length 2\n        Padding to (prepend, append) along `axis`.\n    method : str\n        Controls method of symmetry; options are 'even' or 'odd'.\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt[0]` values prepended and `pad_amt[1]`\n        values appended along `axis`. Both regions are padded with symmetric\n        values from the original array.\n\n    Notes\n    -----\n    This algorithm DOES pad with repetition, i.e. the edges are repeated.\n    For padding without repeated edges, use `mode='reflect'`.\n\n    The modes 'reflect', 'symmetric', and 'wrap' must be padded with a\n    single function, lest the indexing tricks in non-integer multiples of the\n    original shape would violate repetition in the final iteration.\n\n    "
    if ((pad_amt[0] == 0) and (pad_amt[1] == 0)):
        return arr
    sym_slice = tuple(((slice(None) if (i != axis) else slice(0, pad_amt[0])) for (i, x) in enumerate(arr.shape)))
    rev_idx = tuple(((slice(None) if (i != axis) else slice(None, None, (- 1))) for (i, x) in enumerate(arr.shape)))
    sym_chunk1 = arr[sym_slice][rev_idx]
    if (('odd' in method) and (pad_amt[0] > 0)):
        edge_slice1 = tuple(((slice(None) if (i != axis) else slice(0, 1)) for (i, x) in enumerate(arr.shape)))
        edge_chunk = arr[edge_slice1]
        sym_chunk1 = ((2 * edge_chunk) - sym_chunk1)
        del edge_chunk
    start = (arr.shape[axis] - pad_amt[1])
    end = arr.shape[axis]
    sym_slice = tuple(((slice(None) if (i != axis) else slice(start, end)) for (i, x) in enumerate(arr.shape)))
    sym_chunk2 = arr[sym_slice][rev_idx]
    if ('odd' in method):
        edge_slice2 = tuple(((slice(None) if (i != axis) else slice((x - 1), x)) for (i, x) in enumerate(arr.shape)))
        edge_chunk = arr[edge_slice2]
        sym_chunk2 = ((2 * edge_chunk) - sym_chunk2)
        del edge_chunk
    return np.concatenate((sym_chunk1, arr, sym_chunk2), axis=axis)