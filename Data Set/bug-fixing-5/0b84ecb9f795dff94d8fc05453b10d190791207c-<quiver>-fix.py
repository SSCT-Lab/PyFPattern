def quiver(self, *args, length=1, arrow_length_ratio=0.3, pivot='tail', normalize=False, **kwargs):
    "\n        ax.quiver(X, Y, Z, U, V, W, /, length=1, arrow_length_ratio=.3, pivot='tail', normalize=False, **kwargs)\n\n        Plot a 3D field of arrows.\n\n        The arguments could be array-like or scalars, so long as they\n        they can be broadcast together. The arguments can also be\n        masked arrays. If an element in any of argument is masked, then\n        that corresponding quiver element will not be plotted.\n\n        Parameters\n        ----------\n        X, Y, Z : array-like\n            The x, y and z coordinates of the arrow locations (default is\n            tail of arrow; see *pivot* kwarg)\n\n        U, V, W : array-like\n            The x, y and z components of the arrow vectors\n\n        length : float\n            The length of each quiver, default to 1.0, the unit is\n            the same with the axes\n\n        arrow_length_ratio : float\n            The ratio of the arrow head with respect to the quiver,\n            default to 0.3\n\n        pivot : {'tail', 'middle', 'tip'}\n            The part of the arrow that is at the grid point; the arrow\n            rotates about this point, hence the name *pivot*.\n            Default is 'tail'\n\n        normalize : bool\n            When True, all of the arrows will be the same length. This\n            defaults to False, where the arrows will be different lengths\n            depending on the values of u,v,w.\n\n        **kwargs\n            Any additional keyword arguments are delegated to\n            :class:`~matplotlib.collections.LineCollection`\n        "

    def calc_arrow(uvw, angle=15):
        '\n            To calculate the arrow head. uvw should be a unit vector.\n            We normalize it here:\n            '
        norm = np.linalg.norm(uvw[:2])
        if (norm > 0):
            x = (uvw[1] / norm)
            y = ((- uvw[0]) / norm)
        else:
            (x, y) = (0, 1)
        ra = math.radians(angle)
        c = math.cos(ra)
        s = math.sin(ra)
        Rpos = np.array([[(c + ((x ** 2) * (1 - c))), ((x * y) * (1 - c)), (y * s)], [((y * x) * (1 - c)), (c + ((y ** 2) * (1 - c))), ((- x) * s)], [((- y) * s), (x * s), c]])
        Rneg = Rpos.copy()
        Rneg[([0, 1, 2, 2], [2, 2, 0, 1])] = (- Rneg[([0, 1, 2, 2], [2, 2, 0, 1])])
        return (Rpos.dot(uvw), Rneg.dot(uvw))
    had_data = self.has_data()
    argi = 6
    if (len(args) < argi):
        raise ValueError(('Wrong number of arguments. Expected %d got %d' % (argi, len(args))))
    input_args = args[:argi]
    input_args = [([k] if isinstance(k, (int, float)) else k) for k in input_args]
    masks = [k.mask for k in input_args if isinstance(k, np.ma.MaskedArray)]
    bcast = np.broadcast_arrays(*(input_args + masks))
    input_args = bcast[:argi]
    masks = bcast[argi:]
    if masks:
        mask = reduce(np.logical_or, masks)
        input_args = [np.ma.array(k, mask=mask).compressed() for k in input_args]
    else:
        input_args = [k.flatten() for k in input_args]
    if any(((len(v) == 0) for v in input_args)):
        linec = art3d.Line3DCollection([], *args[argi:], **kwargs)
        self.add_collection(linec)
        return linec
    assert all((isinstance(k, np.ndarray) for k in input_args))
    assert (len({k.shape for k in input_args}) == 1)
    shaft_dt = np.linspace(0, length, num=2)
    arrow_dt = (shaft_dt * arrow_length_ratio)
    if (pivot == 'tail'):
        shaft_dt -= length
    elif (pivot == 'middle'):
        shaft_dt -= (length / 2.0)
    elif (pivot != 'tip'):
        raise ValueError(('Invalid pivot argument: ' + str(pivot)))
    XYZ = np.column_stack(input_args[:3])
    UVW = np.column_stack(input_args[3:argi]).astype(float)
    norm = np.linalg.norm(UVW, axis=1)
    mask = (norm > 0)
    XYZ = XYZ[mask]
    if normalize:
        UVW = (UVW[mask] / norm[mask].reshape(((- 1), 1)))
    else:
        UVW = UVW[mask]
    if (len(XYZ) > 0):
        shafts = (XYZ - np.multiply.outer(shaft_dt, UVW)).swapaxes(0, 1)
        head_dirs = np.array([calc_arrow(d) for d in UVW])
        heads = (shafts[:, :1] - np.multiply.outer(arrow_dt, head_dirs))
        heads.shape = (len(arrow_dt), (- 1), 3)
        heads = heads.swapaxes(0, 1)
        lines = [*shafts, *heads]
    else:
        lines = []
    linec = art3d.Line3DCollection(lines, *args[argi:], **kwargs)
    self.add_collection(linec)
    self.auto_scale_xyz(XYZ[:, 0], XYZ[:, 1], XYZ[:, 2], had_data)
    return linec