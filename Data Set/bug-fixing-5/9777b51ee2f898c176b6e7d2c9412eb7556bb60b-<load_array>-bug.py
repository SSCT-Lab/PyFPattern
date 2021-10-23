def load_array(name):
    if (tables is None):
        raise ImportError('The use of `save_array` requires the tables module.')
    f = tables.open_file(name)
    array = f.root.data
    a = np.empty(shape=array.shape, dtype=array.dtype)
    a[:] = array[:]
    f.close()
    return a