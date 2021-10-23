

def deconv_length(dim_size, stride_size, kernel_size, padding):
    if (dim_size is not None):
        dim_size *= stride_size
    if ((padding == 'valid') and (dim_size is not None)):
        dim_size += max((kernel_size - stride_size), 0)
    return dim_size
