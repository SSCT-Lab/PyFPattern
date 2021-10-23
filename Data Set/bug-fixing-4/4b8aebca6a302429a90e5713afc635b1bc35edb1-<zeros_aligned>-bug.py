def zeros_aligned(shape, dtype, order='C', align=128):
    'Like `np.zeros()`, but the array will be aligned at `align` byte boundary.'
    nbytes = (np.prod(shape, dtype=np.int64) * np.dtype(dtype).itemsize)
    buffer = np.zeros((nbytes + align), dtype=np.uint8)
    start_index = ((- buffer.ctypes.data) % align)
    return buffer[start_index:(start_index + nbytes)].view(dtype).reshape(shape, order=order)