

def clim(vmin=None, vmax=None):
    '\n    Set the color limits of the current image.\n\n    To apply clim to all axes images do::\n\n      clim(0, 0.5)\n\n    If either *vmin* or *vmax* is None, the image min/max respectively\n    will be used for color scaling.\n\n    If you want to set the clim of multiple images,\n    use, for example::\n\n      for im in gca().get_images():\n          im.set_clim(0, 0.05)\n\n    '
    im = gci()
    if (im is None):
        raise RuntimeError('You must first define an image, e.g., with imshow')
    im.set_clim(vmin, vmax)
