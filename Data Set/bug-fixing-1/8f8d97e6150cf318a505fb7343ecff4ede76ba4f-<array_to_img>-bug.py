

def array_to_img(x, dim_ordering='default', scale=True):
    'Converts a 3D Numpy array to a PIL Image instance.\n\n    # Arguments\n        x: Input Numpy array.\n        dim_ordering: Image data format.\n        scale: Whether to rescale image values\n            to be within [0, 255].\n\n    # Returns\n        A PIL Image instance.\n\n    # Raises\n        ImportError: if PIL is not available.\n        ValueError: if invalid `x` or `dim_ordering` is passed.\n    '
    if (pil_image is None):
        raise ImportError('Could not import PIL.Image. The use of `array_to_img` requires PIL.')
    x = np.asarray(x)
    if (x.ndim != 3):
        raise ValueError('Expected image array to have rank 3 (single image). Got array with shape:', x.shape)
    if (dim_ordering == 'default'):
        dim_ordering = K.image_dim_ordering()
    if (dim_ordering not in {'th', 'tf'}):
        raise ValueError('Invalid dim_ordering:', dim_ordering)
    if (dim_ordering == 'th'):
        x = x.transpose(1, 2, 0)
    if scale:
        x += max((- np.min(x)), 0)
        x_max = np.max(x)
        if (x_max != 0):
            x /= x_max
        x *= 255
    if (x.shape[2] == 3):
        return pil_image.fromarray(x.astype('uint8'), 'RGB')
    elif (x.shape[2] == 1):
        return pil_image.fromarray(x[:, :, 0].astype('uint8'), 'L')
    else:
        raise ValueError('Unsupported channel number: ', x.shape[2])
