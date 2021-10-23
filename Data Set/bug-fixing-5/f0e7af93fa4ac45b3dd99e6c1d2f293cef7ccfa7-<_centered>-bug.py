def _centered(arr, newshape):
    newshape = asarray(newshape)
    currshape = array(arr.shape)
    startind = ((currshape - newshape) // 2)
    endind = (startind + newshape)
    myslice = [slice(startind[k], endind[k]) for k in range(len(endind))]
    return arr[tuple(myslice)]