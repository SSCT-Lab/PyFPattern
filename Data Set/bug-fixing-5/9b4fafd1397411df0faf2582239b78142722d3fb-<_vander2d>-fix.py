def _vander2d(vander_f, x, y, deg):
    '\n    Helper function used to implement the ``<type>vander2d`` functions.\n\n    Parameters\n    ----------\n    vander_f : function(array_like, int) -> ndarray\n        The 1d vander function, such as ``polyvander``\n    x, y, deg :\n        See the ``<type>vander2d`` functions for more detail\n    '
    (degx, degy) = deg
    (x, y) = (np.array((x, y), copy=False) + 0.0)
    vx = vander_f(x, degx)
    vy = vander_f(y, degy)
    v = (vx[(..., None)] * vy[..., None, :])
    return v.reshape((v.shape[:(- 2)] + ((- 1),)))