

def linear_sum_assignment(cost_matrix):
    'Solve the linear sum assignment problem.\n\n    The linear sum assignment problem is also known as minimum weight matching\n    in bipartite graphs. A problem instance is described by a matrix C, where\n    each C[i,j] is the cost of matching vertex i of the first partite set\n    (a "worker") and vertex j of the second set (a "job"). The goal is to find\n    a complete assignment of workers to jobs of minimal cost.\n\n    Formally, let X be a boolean matrix where :math:`X[i,j] = 1` iff row i is\n    assigned to column j. Then the optimal assignment has cost\n\n    .. math::\n        \\min \\sum_i \\sum_j C_{i,j} X_{i,j}\n\n    s.t. each row is assignment to at most one column, and each column to at\n    most one row.\n\n    This function can also solve a generalization of the classic assignment\n    problem where the cost matrix is rectangular. If it has more rows than\n    columns, then not every row needs to be assigned to a column, and vice\n    versa.\n\n    The method used is the Hungarian algorithm, also known as the Munkres or\n    Kuhn-Munkres algorithm.\n\n    Parameters\n    ----------\n    cost_matrix : array\n        The cost matrix of the bipartite graph.\n\n    Returns\n    -------\n    row_ind, col_ind : array\n        An array of row indices and one of corresponding column indices giving\n        the optimal assignment. The cost of the assignment can be computed\n        as ``cost_matrix[row_ind, col_ind].sum()``. The row indices will be\n        sorted; in the case of a square cost matrix they will be equal to\n        ``numpy.arange(cost_matrix.shape[0])``.\n\n    Notes\n    -----\n    .. versionadded:: 0.17.0\n\n    Examples\n    --------\n    >>> cost = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])\n    >>> from scipy.optimize import linear_sum_assignment\n    >>> row_ind, col_ind = linear_sum_assignment(cost)\n    >>> col_ind\n    array([1, 0, 2])\n    >>> cost[row_ind, col_ind].sum()\n    5\n\n    References\n    ----------\n    1. http://csclab.murraystate.edu/bob.pilgrim/445/munkres.html\n\n    2. Harold W. Kuhn. The Hungarian Method for the assignment problem.\n       *Naval Research Logistics Quarterly*, 2:83-97, 1955.\n\n    3. Harold W. Kuhn. Variants of the Hungarian method for assignment\n       problems. *Naval Research Logistics Quarterly*, 3: 253-258, 1956.\n\n    4. Munkres, J. Algorithms for the Assignment and Transportation Problems.\n       *J. SIAM*, 5(1):32-38, March, 1957.\n\n    5. https://en.wikipedia.org/wiki/Hungarian_algorithm\n    '
    cost_matrix = np.asarray(cost_matrix)
    if (len(cost_matrix.shape) != 2):
        raise ValueError(('expected a matrix (2-d array), got a %r array' % (cost_matrix.shape,)))
    if (not (np.issubdtype(cost_matrix.dtype, np.number) or (cost_matrix.dtype is np.dtype(np.bool)))):
        raise ValueError(('expected a matrix containing numerical entries, got %s' % (cost_matrix.dtype,)))
    if np.any((np.isinf(cost_matrix) | np.isnan(cost_matrix))):
        raise ValueError('matrix contains invalid numeric entries')
    if (cost_matrix.dtype is np.dtype(np.bool)):
        cost_matrix = cost_matrix.astype(np.int)
    if (cost_matrix.shape[1] < cost_matrix.shape[0]):
        cost_matrix = cost_matrix.T
        transposed = True
    else:
        transposed = False
    state = _Hungary(cost_matrix)
    step = (None if (0 in cost_matrix.shape) else _step1)
    while (step is not None):
        step = step(state)
    if transposed:
        marked = state.marked.T
    else:
        marked = state.marked
    return np.where((marked == 1))
