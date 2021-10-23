def text3d(ax, xyz, s, zdir='z', size=None, angle=0, usetex=False, **kwargs):
    "\n    Plots the string 's' on the axes 'ax', with position 'xyz', size 'size',\n    and rotation angle 'angle'.  'zdir' gives the axis which is to be treated\n    as the third dimension.  usetex is a boolean indicating whether the string\n    should be interpreted as latex or not.  Any additional keyword arguments\n    are passed on to transform_path.\n\n    Note: zdir affects the interpretation of xyz.\n    "
    (x, y, z) = xyz
    if (zdir == 'y'):
        (xy1, z1) = ((x, z), y)
    elif (zdir == 'x'):
        (xy1, z1) = ((y, z), x)
    else:
        (xy1, z1) = ((x, y), z)
    text_path = TextPath((0, 0), s, size=size, usetex=usetex)
    trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])
    p1 = PathPatch(trans.transform_path(text_path), **kwargs)
    ax.add_patch(p1)
    art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)