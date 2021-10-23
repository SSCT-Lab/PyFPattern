

def format_coord(self, xd, yd):
    '\n        Given the 2D view coordinates attempt to guess a 3D coordinate.\n        Looks for the nearest edge to the point and then assumes that\n        the point is at the same z location as the nearest point on the edge.\n        '
    if (self.M is None):
        return ''
    if (self.button_pressed in self._rotate_btn):
        return 'azimuth={:.0f} deg, elevation={:.0f} deg '.format(self.azim, self.elev)
    (p0, p1) = min(self.tunit_edges(), key=(lambda edge: proj3d.line2d_seg_dist(edge[0], edge[1], (xd, yd))))
    (x0, y0, z0) = p0
    (x1, y1, z1) = p1
    d0 = np.hypot((x0 - xd), (y0 - yd))
    d1 = np.hypot((x1 - xd), (y1 - yd))
    dt = (d0 + d1)
    z = (((d1 / dt) * z0) + ((d0 / dt) * z1))
    (x, y, z) = proj3d.inv_transform(xd, yd, z, self.M)
    xs = self.format_xdata(x)
    ys = self.format_ydata(y)
    zs = self.format_zdata(z)
    return ('x=%s, y=%s, z=%s' % (xs, ys, zs))
