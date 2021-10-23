def _grid_from_X(X, percentiles=(0.05, 0.95), grid_resolution=100):
    'Generate a grid of points based on the ``percentiles of ``X``.\n\n    The grid is generated by placing ``grid_resolution`` equally\n    spaced points between the ``percentiles`` of each column\n    of ``X``.\n\n    Parameters\n    ----------\n    X : ndarray\n        The data\n    percentiles : tuple of floats\n        The percentiles which are used to construct the extreme\n        values of the grid axes.\n    grid_resolution : int\n        The number of equally spaced points that are placed\n        on the grid.\n\n    Returns\n    -------\n    grid : ndarray\n        All data points on the grid; ``grid.shape[1] == X.shape[1]``\n        and ``grid.shape[0] == grid_resolution * X.shape[1]``.\n    axes : seq of ndarray\n        The axes with which the grid has been created.\n    '
    if (len(percentiles) != 2):
        raise ValueError('percentile must be tuple of len 2')
    if (not all(((0.0 <= x <= 1.0) for x in percentiles))):
        raise ValueError('percentile values must be in [0, 1]')
    axes = []
    for col in range(X.shape[1]):
        uniques = np.unique(X[:, col])
        if (uniques.shape[0] < grid_resolution):
            axis = uniques
        else:
            emp_percentiles = mquantiles(X, prob=percentiles, axis=0)
            axis = np.linspace(emp_percentiles[(0, col)], emp_percentiles[(1, col)], num=grid_resolution, endpoint=True)
        axes.append(axis)
    return (cartesian(axes), axes)