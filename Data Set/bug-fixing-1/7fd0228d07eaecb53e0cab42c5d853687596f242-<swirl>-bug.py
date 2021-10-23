

def swirl(image, center=None, strength=1, radius=100, rotation=0, output_shape=None, order=1, mode=None, cval=0, clip=True, preserve_range=False):
    "Perform a swirl transformation.\n\n    Parameters\n    ----------\n    image : ndarray\n        Input image.\n    center : (row, column) tuple or (2,) ndarray, optional\n        Center coordinate of transformation.\n    strength : float, optional\n        The amount of swirling applied.\n    radius : float, optional\n        The extent of the swirl in pixels.  The effect dies out\n        rapidly beyond `radius`.\n    rotation : float, optional\n        Additional rotation applied to the image.\n\n    Returns\n    -------\n    swirled : ndarray\n        Swirled version of the input.\n\n    Other parameters\n    ----------------\n    output_shape : tuple (rows, cols), optional\n        Shape of the output image generated. By default the shape of the input\n        image is preserved.\n    order : int, optional\n        The order of the spline interpolation, default is 1. The order has to\n        be in the range 0-5. See `skimage.transform.warp` for detail.\n    mode : {'constant', 'edge', 'symmetric', 'reflect', 'wrap'}, optional\n        Points outside the boundaries of the input are filled according\n        to the given mode, with 'constant' used as the default. Modes match\n        the behaviour of `numpy.pad`.\n    cval : float, optional\n        Used in conjunction with mode 'constant', the value outside\n        the image boundaries.\n    clip : bool, optional\n        Whether to clip the output to the range of values of the input image.\n        This is enabled by default, since higher order interpolation may\n        produce values outside the given input range.\n    preserve_range : bool, optional\n        Whether to keep the original range of values. Otherwise, the input\n        image is converted according to the conventions of `img_as_float`.\n\n    "
    if (mode is None):
        warn('The default of `mode` in `skimage.transform.swirl` will change to `reflect` in version 0.15.')
        mode = 'constant'
    if (center is None):
        center = (np.array(image.shape)[:2] / 2)
    warp_args = {
        'center': center,
        'rotation': rotation,
        'strength': strength,
        'radius': radius,
    }
    return warp(image, _swirl_mapping, map_args=warp_args, output_shape=output_shape, order=order, mode=mode, cval=cval, clip=clip, preserve_range=preserve_range)
