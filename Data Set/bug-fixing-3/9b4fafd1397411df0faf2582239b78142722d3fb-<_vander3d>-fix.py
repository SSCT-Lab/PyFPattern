def _vander3d(vander_f, x, y, z, deg):
    '\n    Helper function used to implement the ``<type>vander3d`` functions.\n\n    Parameters\n    ----------\n    vander_f : function(array_like, int) -> ndarray\n        The 1d vander function, such as ``polyvander``\n    x, y, z, deg :\n        See the ``<type>vander3d`` functions for more detail\n    '
    (degx, degy, degz) = deg
    (x, y, z) = (np.array((x, y, z), copy=False) + 0.0)
    vx = vander_f(x, degx)
    vy = vander_f(y, degy)
    vz = vander_f(z, degz)
    v = ((vx[(..., None, None)] * vy[..., None, :, None]) * vz[..., None, None, :])
    return v.reshape((v.shape[:(- 3)] + ((- 1),)))