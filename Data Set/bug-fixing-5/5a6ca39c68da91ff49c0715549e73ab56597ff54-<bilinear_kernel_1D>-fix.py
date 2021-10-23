def bilinear_kernel_1D(ratio, normalize=True):
    'Compute 1D kernel for bilinear upsampling\n\n    This function builds the 1D kernel that can be used to upsample\n    a tensor by the given ratio using bilinear interpolation.\n\n    Parameters\n    ----------\n    ratio: int or Constant/Scalar Theano tensor of int* dtype\n        the ratio by which an image will be upsampled by the returned filter\n        in the 2D space.\n\n    normalize: bool\n        param normalize: indicates whether to normalize the kernel or not.\n        Default is True.\n\n    Returns\n    -------\n    symbolic 1D tensor\n        the 1D kernels that can be applied to any given image to upsample it\n        by the indicated ratio using bilinear interpolation in one dimension.\n\n    '
    T = theano.tensor
    half_kern = T.arange(1, (ratio + 1), dtype=theano.config.floatX)
    kern = T.concatenate([half_kern, half_kern[(- 2)::(- 1)]])
    if normalize:
        kern /= T.cast(ratio, theano.config.floatX)
    return kern