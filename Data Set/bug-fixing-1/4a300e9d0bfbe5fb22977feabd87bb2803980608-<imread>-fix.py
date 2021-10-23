

def imread(fname, as_grey=False, plugin=None, flatten=None, **plugin_args):
    'Load an image from file.\n\n    Parameters\n    ----------\n    fname : string\n        Image file name, e.g. ``test.jpg`` or URL.\n    as_grey : bool\n        If True, convert color images to grey-scale (64-bit floats).\n        Images that are already in grey-scale format are not converted.\n    plugin : str\n        Name of plugin to use.  By default, the different plugins are\n        tried (starting with the Python Imaging Library) until a suitable\n        candidate is found.  If not given and fname is a tiff file, the\n        tifffile plugin will be used.\n\n    Other Parameters\n    ----------------\n    flatten : bool\n        Backward compatible keyword, superseded by `as_grey`.\n\n    plugin_args : keywords\n        Passed to the given plugin.\n\n    Returns\n    -------\n    img_array : ndarray\n        The different color bands/channels are stored in the\n        third dimension, such that a grey-image is MxN, an\n        RGB-image MxNx3 and an RGBA-image MxNx4.\n\n    '
    if (flatten is not None):
        as_grey = flatten
    if ((plugin is None) and hasattr(fname, 'lower')):
        if fname.lower().endswith(('.tiff', '.tif')):
            plugin = 'tifffile'
    with file_or_url_context(fname) as fname:
        img = call_plugin('imread', fname, plugin=plugin, **plugin_args)
    if (not hasattr(img, 'ndim')):
        return img
    if (img.ndim > 2):
        if ((img.shape[(- 1)] not in (3, 4)) and (img.shape[(- 3)] in (3, 4))):
            img = np.swapaxes(img, (- 1), (- 3))
            img = np.swapaxes(img, (- 2), (- 3))
        if as_grey:
            img = rgb2grey(img)
    return img
