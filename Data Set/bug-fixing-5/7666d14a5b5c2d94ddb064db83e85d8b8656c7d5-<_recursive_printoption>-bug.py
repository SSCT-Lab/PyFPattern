def _recursive_printoption(result, mask, printopt):
    '\n    Puts printoptions in result where mask is True.\n\n    Private function allowing for recursion\n\n    '
    names = result.dtype.names
    for name in names:
        (curdata, curmask) = (result[name], mask[name])
        if curdata.dtype.names:
            _recursive_printoption(curdata, curmask, printopt)
        else:
            np.copyto(curdata, printopt, where=curmask)
    return