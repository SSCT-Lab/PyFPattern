def _centered(arr, newshape):
    newshape = np.asarray(newshape)
    currshape = np.array(arr.shape)
    startind = ((currshape - newshape) // 2)
    endind = (startind + newshape)
    myslice = [slice(startind[k], endind[k]) for k in range(len(endind))]
    return arr[tuple(myslice)]