

@dec.slow
def test_more_barycentric_transforms(self):
    eps = np.finfo(float).eps
    npoints = {
        2: 70,
        3: 11,
        4: 5,
        5: 3,
    }
    _is_32bit_platform = (np.intp(0).itemsize < 8)
    for ndim in xrange(2, 6):
        x = np.linspace(0, 1, npoints[ndim])
        grid = np.c_[list(map(np.ravel, np.broadcast_arrays(*np.ix_(*([x] * ndim)))))].T
        err_msg = ('ndim=%d' % ndim)
        tri = qhull.Delaunay(grid)
        self._check_barycentric_transforms(tri, err_msg=err_msg, unit_cube=True)
        np.random.seed(1234)
        m = (np.random.rand(grid.shape[0]) < 0.2)
        grid[m, :] += ((2 * eps) * (np.random.rand(*grid[m, :].shape) - 0.5))
        tri = qhull.Delaunay(grid)
        self._check_barycentric_transforms(tri, err_msg=err_msg, unit_cube=True, unit_cube_tol=(2 * eps))
        tri = qhull.Delaunay(np.r_[(grid, grid)])
        self._check_barycentric_transforms(tri, err_msg=err_msg, unit_cube=True, unit_cube_tol=(2 * eps))
        if (not _is_32bit_platform):
            np.random.seed(4321)
            m = (np.random.rand(grid.shape[0]) < 0.2)
            grid[m, :] += ((1000 * eps) * (np.random.rand(*grid[m, :].shape) - 0.5))
            tri = qhull.Delaunay(grid)
            self._check_barycentric_transforms(tri, err_msg=err_msg, unit_cube=True, unit_cube_tol=(1500 * eps))
            np.random.seed(4321)
            m = (np.random.rand(grid.shape[0]) < 0.2)
            grid[m, :] += ((1000000.0 * eps) * (np.random.rand(*grid[m, :].shape) - 0.5))
            tri = qhull.Delaunay(grid)
            self._check_barycentric_transforms(tri, err_msg=err_msg, unit_cube=True, unit_cube_tol=(10000000.0 * eps))
