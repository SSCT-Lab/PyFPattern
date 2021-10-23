

def deconv_length(dim_size, stride_size, kernel_size, padding):
    if (dim_size is None):
        return None
    if (padding == 'valid'):
        dim_size = ((dim_size * stride_size) + max((kernel_size - stride_size), 0))
    elif (padding == 'full'):
        dim_size = ((dim_size * stride_size) - ((stride_size + kernel_size) - 2))
    elif (padding == 'same'):
        dim_size = (dim_size * stride_size)
    return dim_size
