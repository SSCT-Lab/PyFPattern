

def scatter(data, indices, updates, axis=0):
    if (axis < 0):
        axis = (data.ndim + axis)
    idx_xsection_shape = (indices.shape[:axis] + indices.shape[(axis + 1):])

    def make_slice(arr, axis, i):
        slc = ([slice(None)] * arr.ndim)
        slc[axis] = i
        return slc

    def unpack(packed):
        unpacked = packed[0]
        for i in range(1, len(packed)):
            unpacked = (unpacked, packed[i])
        return unpacked
    idx = [[unpack(np.indices(idx_xsection_shape).reshape((indices.ndim - 1), (- 1))), indices[tuple(make_slice(indices, axis, i))].reshape(1, (- 1))[0]] for i in range(indices.shape[axis])]
    idx = list(np.concatenate(idx, axis=1))
    idx.insert(axis, idx.pop())
    updates_idx = list(idx)
    updates_idx.pop(axis)
    updates_idx.insert(axis, np.repeat(np.arange(indices.shape[axis]), np.prod(idx_xsection_shape)))
    scattered = np.copy(data)
    scattered[idx] = updates[tuple(updates_idx)]
    return scattered
