def zeros_aligned(shape, dtype, order='C', align=128):
    "Get array aligned at `align` byte boundary.\n\n    Parameters\n    ----------\n    shape : int or (int, int)\n        Shape of array.\n    dtype : data-type\n        Data type of array.\n    order : {'C', 'F'}, optional\n        Whether to store multidimensional data in C- or Fortran-contiguous (row- or column-wise) order in memory.\n    align : int, optional\n        Boundary for alignment in bytes.\n\n    Returns\n    -------\n    numpy.ndarray\n        Aligned array.\n\n    "
    nbytes = (np.prod(shape, dtype=np.int64) * np.dtype(dtype).itemsize)
    buffer = np.zeros((nbytes + align), dtype=np.uint8)
    start_index = ((- buffer.ctypes.data) % align)
    return buffer[start_index:(start_index + nbytes)].view(dtype).reshape(shape, order=order)