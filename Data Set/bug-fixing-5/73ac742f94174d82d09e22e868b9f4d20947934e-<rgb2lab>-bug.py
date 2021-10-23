def rgb2lab(rgb, illuminant='D65', observer='2'):
    'RGB to lab color space conversion.\n\n    Parameters\n    ----------\n    rgb : array_like\n        The image in RGB format, in a 3- or 4-D array of shape\n        ``(.., ..,[ ..,] 3)``.\n    illuminant : {"A", "D50", "D55", "D65", "D75", "E"}, optional\n        The name of the illuminant (the function is NOT case sensitive).\n    observer : {"2", "10"}, optional\n        The aperture angle of the observer.\n\n    Returns\n    -------\n    out : ndarray\n        The image in Lab format, in a 3- or 4-D array of shape\n        ``(.., ..,[ ..,] 3)``.\n\n    Raises\n    ------\n    ValueError\n        If `rgb` is not a 3- or 4-D array of shape ``(.., ..,[ ..,] 3)``.\n\n    Notes\n    -----\n    This function uses rgb2xyz and xyz2lab.\n    By default Observer= 2A, Illuminant= D65. CIE XYZ tristimulus values\n    x_ref=95.047, y_ref=100., z_ref=108.883. See function `get_xyz_coords` for\n    a list of supported illuminants.\n    '
    return xyz2lab(rgb2xyz(rgb), illuminant, observer)