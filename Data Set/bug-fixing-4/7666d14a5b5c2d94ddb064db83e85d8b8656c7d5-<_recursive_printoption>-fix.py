def _recursive_printoption(result, mask, printopt):
    '\n    Puts printoptions in result where mask is True.\n\n    Private function allowing for recursion\n\n    '
    names = result.dtype.names
    if names:
        for name in names:
            curdata = result[name]
            curmask = mask[name]
            _recursive_printoption(curdata, curmask, printopt)
    else:
        np.copyto(result, printopt, where=mask)
    return