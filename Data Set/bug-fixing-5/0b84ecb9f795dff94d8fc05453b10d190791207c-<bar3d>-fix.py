def bar3d(self, x, y, z, dx, dy, dz, color=None, zsort='average', shade=True, *args, **kwargs):
    "Generate a 3D barplot.\n\n        This method creates three dimensional barplot where the width,\n        depth, height, and color of the bars can all be uniquely set.\n\n        Parameters\n        ----------\n        x, y, z : array-like\n            The coordinates of the anchor point of the bars.\n\n        dx, dy, dz : scalar or array-like\n            The width, depth, and height of the bars, respectively.\n\n        color : sequence of valid color specifications, optional\n            The color of the bars can be specified globally or\n            individually. This parameter can be:\n\n              - A single color value, to color all bars the same color.\n              - An array of colors of length N bars, to color each bar\n                independently.\n              - An array of colors of length 6, to color the faces of the\n                bars similarly.\n              - An array of colors of length 6 * N bars, to color each face\n                independently.\n\n            When coloring the faces of the boxes specifically, this is\n            the order of the coloring:\n\n              1. -Z (bottom of box)\n              2. +Z (top of box)\n              3. -Y\n              4. +Y\n              5. -X\n              6. +X\n\n        zsort : str, optional\n            The z-axis sorting scheme passed onto\n            :func:`~mpl_toolkits.mplot3d.art3d.Poly3DCollection`\n\n        shade : bool, optional (default = True)\n            When true, this shades the dark sides of the bars (relative\n            to the plot's source of light).\n\n        **kwargs\n            Any additional keyword arguments are passed onto\n            :class:`~mpl_toolkits.mplot3d.art3d.Poly3DCollection`\n\n        Returns\n        -------\n        collection : Poly3DCollection\n            A collection of three dimensional polygons representing\n            the bars.\n        "
    had_data = self.has_data()
    (x, y, z, dx, dy, dz) = np.broadcast_arrays(np.atleast_1d(x), y, z, dx, dy, dz)
    minx = np.min(x)
    maxx = np.max((x + dx))
    miny = np.min(y)
    maxy = np.max((y + dy))
    minz = np.min(z)
    maxz = np.max((z + dz))
    polys = []
    for (xi, yi, zi, dxi, dyi, dzi) in zip(x, y, z, dx, dy, dz):
        polys.extend([((xi, yi, zi), ((xi + dxi), yi, zi), ((xi + dxi), (yi + dyi), zi), (xi, (yi + dyi), zi)), ((xi, yi, (zi + dzi)), ((xi + dxi), yi, (zi + dzi)), ((xi + dxi), (yi + dyi), (zi + dzi)), (xi, (yi + dyi), (zi + dzi))), ((xi, yi, zi), ((xi + dxi), yi, zi), ((xi + dxi), yi, (zi + dzi)), (xi, yi, (zi + dzi))), ((xi, (yi + dyi), zi), ((xi + dxi), (yi + dyi), zi), ((xi + dxi), (yi + dyi), (zi + dzi)), (xi, (yi + dyi), (zi + dzi))), ((xi, yi, zi), (xi, (yi + dyi), zi), (xi, (yi + dyi), (zi + dzi)), (xi, yi, (zi + dzi))), (((xi + dxi), yi, zi), ((xi + dxi), (yi + dyi), zi), ((xi + dxi), (yi + dyi), (zi + dzi)), ((xi + dxi), yi, (zi + dzi)))])
    facecolors = []
    if (color is None):
        color = [self._get_patches_for_fill.get_next_color()]
    if (len(color) == len(x)):
        for c in color:
            facecolors.extend(([c] * 6))
    else:
        facecolors = list(mcolors.to_rgba_array(color))
        if (len(facecolors) < len(x)):
            facecolors *= (6 * len(x))
    if shade:
        normals = self._generate_normals(polys)
        sfacecolors = self._shade_colors(facecolors, normals)
    else:
        sfacecolors = facecolors
    col = art3d.Poly3DCollection(polys, *args, zsort=zsort, facecolor=sfacecolors, **kwargs)
    self.add_collection(col)
    self.auto_scale_xyz((minx, maxx), (miny, maxy), (minz, maxz), had_data)
    return col