

def _preprocess_deconv_output_shape(x, shape, dim_ordering):
    if (dim_ordering == 'th'):
        shape = (shape[0], shape[2], shape[3], shape[1])
    if (shape[0] is None):
        shape = ((tf.shape(x)[0],) + shape[1:])
    return shape
