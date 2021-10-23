def bar3d(self, x, y, z, dx, dy, dz, color=None, zsort='average', *args, **kwargs):
    '\n        Generate a 3D bar, or multiple bars.\n\n        When generating multiple bars, x, y, z have to be arrays.\n        dx, dy, dz can be arrays or scalars.\n\n        *color* can be:\n\n         - A single color value, to color all bars the same color.\n\n         - An array of colors of length N bars, to color each bar\n           independently.\n\n         - An array of colors of length 6, to color the faces of the\n           bars similarly.\n\n         - An array of colors of length 6 * N bars, to color each face\n           independently.\n\n         When coloring the faces of the boxes specifically, this is\n         the order of the coloring:\n\n          1. -Z (bottom of box)\n          2. +Z (top of box)\n          3. -Y\n          4. +Y\n          5. -X\n          6. +X\n\n        Keyword arguments are passed onto\n        :func:`~mpl_toolkits.mplot3d.art3d.Poly3DCollection`\n        '
    had_data = self.has_data()
    if (not cbook.iterable(x)):
        x = [x]
    if (not cbook.iterable(y)):
        y = [y]
    if (not cbook.iterable(z)):
        z = [z]
    if (not cbook.iterable(dx)):
        dx = [dx]
    if (not cbook.iterable(dy)):
        dy = [dy]
    if (not cbook.iterable(dz)):
        dz = [dz]
    if (len(dx) == 1):
        dx = (dx * len(x))
    if (len(dy) == 1):
        dy = (dy * len(y))
    if (len(dz) == 1):
        dz = (dz * len(z))
    if ((len(x) != len(y)) or (len(x) != len(z))):
        warnings.warn('x, y, and z must be the same length.')
    (minx, miny, minz) = (1e+20, 1e+20, 1e+20)
    (maxx, maxy, maxz) = ((- 1e+20), (- 1e+20), (- 1e+20))
    polys = []
    for (xi, yi, zi, dxi, dyi, dzi) in zip(x, y, z, dx, dy, dz):
        minx = min(xi, minx)
        maxx = max((xi + dxi), maxx)
        miny = min(yi, miny)
        maxy = max((yi + dyi), maxy)
        minz = min(zi, minz)
        maxz = max((zi + dzi), maxz)
        polys.extend([((xi, yi, zi), ((xi + dxi), yi, zi), ((xi + dxi), (yi + dyi), zi), (xi, (yi + dyi), zi)), ((xi, yi, (zi + dzi)), ((xi + dxi), yi, (zi + dzi)), ((xi + dxi), (yi + dyi), (zi + dzi)), (xi, (yi + dyi), (zi + dzi))), ((xi, yi, zi), ((xi + dxi), yi, zi), ((xi + dxi), yi, (zi + dzi)), (xi, yi, (zi + dzi))), ((xi, (yi + dyi), zi), ((xi + dxi), (yi + dyi), zi), ((xi + dxi), (yi + dyi), (zi + dzi)), (xi, (yi + dyi), (zi + dzi))), ((xi, yi, zi), (xi, (yi + dyi), zi), (xi, (yi + dyi), (zi + dzi)), (xi, yi, (zi + dzi))), (((xi + dxi), yi, zi), ((xi + dxi), (yi + dyi), zi), ((xi + dxi), (yi + dyi), (zi + dzi)), ((xi + dxi), yi, (zi + dzi)))])
    facecolors = []
    if (color is None):
        color = [self._get_lines.get_next_color()]
    if (len(color) == len(x)):
        for c in color:
            facecolors.extend(([c] * 6))
    else:
        facecolors = list(mcolors.to_rgba_array(color))
        if (len(facecolors) < len(x)):
            facecolors *= (6 * len(x))
    normals = self._generate_normals(polys)
    sfacecolors = self._shade_colors(facecolors, normals)
    col = art3d.Poly3DCollection(polys, *args, zsort=zsort, facecolor=sfacecolors, **kwargs)
    self.add_collection(col)
    self.auto_scale_xyz((minx, maxx), (miny, maxy), (minz, maxz), had_data)
    return col