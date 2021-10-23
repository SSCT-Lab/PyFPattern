

def cdist(XA, XB, metric='euclidean', p=2, V=None, VI=None, w=None):
    "\n    Computes distance between each pair of the two collections of inputs.\n\n    The following are common calling conventions:\n\n    1. ``Y = cdist(XA, XB, 'euclidean')``\n\n       Computes the distance between :math:`m` points using\n       Euclidean distance (2-norm) as the distance metric between the\n       points. The points are arranged as :math:`m`\n       :math:`n`-dimensional row vectors in the matrix X.\n\n    2. ``Y = cdist(XA, XB, 'minkowski', p)``\n\n       Computes the distances using the Minkowski distance\n       :math:`||u-v||_p` (:math:`p`-norm) where :math:`p \\geq 1`.\n\n    3. ``Y = cdist(XA, XB, 'cityblock')``\n\n       Computes the city block or Manhattan distance between the\n       points.\n\n    4. ``Y = cdist(XA, XB, 'seuclidean', V=None)``\n\n       Computes the standardized Euclidean distance. The standardized\n       Euclidean distance between two n-vectors ``u`` and ``v`` is\n\n       .. math::\n\n          \\sqrt{\\sum {(u_i-v_i)^2 / V[x_i]}}.\n\n       V is the variance vector; V[i] is the variance computed over all\n       the i'th components of the points. If not passed, it is\n       automatically computed.\n\n    5. ``Y = cdist(XA, XB, 'sqeuclidean')``\n\n       Computes the squared Euclidean distance :math:`||u-v||_2^2` between\n       the vectors.\n\n    6. ``Y = cdist(XA, XB, 'cosine')``\n\n       Computes the cosine distance between vectors u and v,\n\n       .. math::\n\n          1 - \\frac{u \\cdot v}\n                   {{||u||}_2 {||v||}_2}\n\n       where :math:`||*||_2` is the 2-norm of its argument ``*``, and\n       :math:`u \\cdot v` is the dot product of :math:`u` and :math:`v`.\n\n    7. ``Y = cdist(XA, XB, 'correlation')``\n\n       Computes the correlation distance between vectors u and v. This is\n\n       .. math::\n\n          1 - \\frac{(u - \\bar{u}) \\cdot (v - \\bar{v})}\n                   {{||(u - \\bar{u})||}_2 {||(v - \\bar{v})||}_2}\n\n       where :math:`\\bar{v}` is the mean of the elements of vector v,\n       and :math:`x \\cdot y` is the dot product of :math:`x` and :math:`y`.\n\n\n    8. ``Y = cdist(XA, XB, 'hamming')``\n\n       Computes the normalized Hamming distance, or the proportion of\n       those vector elements between two n-vectors ``u`` and ``v``\n       which disagree. To save memory, the matrix ``X`` can be of type\n       boolean.\n\n    9. ``Y = cdist(XA, XB, 'jaccard')``\n\n       Computes the Jaccard distance between the points. Given two\n       vectors, ``u`` and ``v``, the Jaccard distance is the\n       proportion of those elements ``u[i]`` and ``v[i]`` that\n       disagree where at least one of them is non-zero.\n\n    10. ``Y = cdist(XA, XB, 'chebyshev')``\n\n       Computes the Chebyshev distance between the points. The\n       Chebyshev distance between two n-vectors ``u`` and ``v`` is the\n       maximum norm-1 distance between their respective elements. More\n       precisely, the distance is given by\n\n       .. math::\n\n          d(u,v) = \\max_i {|u_i-v_i|}.\n\n    11. ``Y = cdist(XA, XB, 'canberra')``\n\n       Computes the Canberra distance between the points. The\n       Canberra distance between two points ``u`` and ``v`` is\n\n       .. math::\n\n         d(u,v) = \\sum_i \\frac{|u_i-v_i|}\n                              {|u_i|+|v_i|}.\n\n    12. ``Y = cdist(XA, XB, 'braycurtis')``\n\n       Computes the Bray-Curtis distance between the points. The\n       Bray-Curtis distance between two points ``u`` and ``v`` is\n\n\n       .. math::\n\n            d(u,v) = \\frac{\\sum_i (u_i-v_i)}\n                          {\\sum_i (u_i+v_i)}\n\n    13. ``Y = cdist(XA, XB, 'mahalanobis', VI=None)``\n\n       Computes the Mahalanobis distance between the points. The\n       Mahalanobis distance between two points ``u`` and ``v`` is\n       :math:`(u-v)(1/V)(u-v)^T` where :math:`(1/V)` (the ``VI``\n       variable) is the inverse covariance. If ``VI`` is not None,\n       ``VI`` will be used as the inverse covariance matrix.\n\n    14. ``Y = cdist(XA, XB, 'yule')``\n\n       Computes the Yule distance between the boolean\n       vectors. (see `yule` function documentation)\n\n    15. ``Y = cdist(XA, XB, 'matching')``\n\n       Synonym for 'hamming'.\n\n    16. ``Y = cdist(XA, XB, 'dice')``\n\n       Computes the Dice distance between the boolean vectors. (see\n       `dice` function documentation)\n\n    17. ``Y = cdist(XA, XB, 'kulsinski')``\n\n       Computes the Kulsinski distance between the boolean\n       vectors. (see `kulsinski` function documentation)\n\n    18. ``Y = cdist(XA, XB, 'rogerstanimoto')``\n\n       Computes the Rogers-Tanimoto distance between the boolean\n       vectors. (see `rogerstanimoto` function documentation)\n\n    19. ``Y = cdist(XA, XB, 'russellrao')``\n\n       Computes the Russell-Rao distance between the boolean\n       vectors. (see `russellrao` function documentation)\n\n    20. ``Y = cdist(XA, XB, 'sokalmichener')``\n\n       Computes the Sokal-Michener distance between the boolean\n       vectors. (see `sokalmichener` function documentation)\n\n    21. ``Y = cdist(XA, XB, 'sokalsneath')``\n\n       Computes the Sokal-Sneath distance between the vectors. (see\n       `sokalsneath` function documentation)\n\n\n    22. ``Y = cdist(XA, XB, 'wminkowski')``\n\n       Computes the weighted Minkowski distance between the\n       vectors. (see `wminkowski` function documentation)\n\n    23. ``Y = cdist(XA, XB, f)``\n\n       Computes the distance between all pairs of vectors in X\n       using the user supplied 2-arity function f. For example,\n       Euclidean distance between the vectors could be computed\n       as follows::\n\n         dm = cdist(XA, XB, lambda u, v: np.sqrt(((u-v)**2).sum()))\n\n       Note that you should avoid passing a reference to one of\n       the distance functions defined in this library. For example,::\n\n         dm = cdist(XA, XB, sokalsneath)\n\n       would calculate the pair-wise distances between the vectors in\n       X using the Python function `sokalsneath`. This would result in\n       sokalsneath being called :math:`{n \\choose 2}` times, which\n       is inefficient. Instead, the optimized C version is more\n       efficient, and we call it using the following syntax::\n\n         dm = cdist(XA, XB, 'sokalsneath')\n\n    Parameters\n    ----------\n    XA : ndarray\n        An :math:`m_A` by :math:`n` array of :math:`m_A`\n        original observations in an :math:`n`-dimensional space.\n        Inputs are converted to float type.\n    XB : ndarray\n        An :math:`m_B` by :math:`n` array of :math:`m_B`\n        original observations in an :math:`n`-dimensional space.\n        Inputs are converted to float type.\n    metric : str or callable, optional\n        The distance metric to use.  If a string, the distance function can be\n        'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation',\n        'cosine', 'dice', 'euclidean', 'hamming', 'jaccard', 'kulsinski',\n        'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao',\n        'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean',\n        'wminkowski', 'yule'.\n    w : ndarray, optional\n        The weight vector (for weighted Minkowski).\n    p : scalar, optional\n        The p-norm to apply (for Minkowski, weighted and unweighted)\n    V : ndarray, optional\n        The variance vector (for standardized Euclidean).\n    VI : ndarray, optional\n        The inverse of the covariance matrix (for Mahalanobis).\n\n    Returns\n    -------\n    Y : ndarray\n        A :math:`m_A` by :math:`m_B` distance matrix is returned.\n        For each :math:`i` and :math:`j`, the metric\n        ``dist(u=XA[i], v=XB[j])`` is computed and stored in the\n        :math:`ij` th entry.\n\n    Raises\n    ------\n    ValueError\n        An exception is thrown if `XA` and `XB` do not have\n        the same number of columns.\n\n    Examples\n    --------\n    Find the Euclidean distances between four 2-D coordinates:\n\n    >>> from scipy.spatial import distance\n    >>> coords = [(35.0456, -85.2672),\n    ...           (35.1174, -89.9711),\n    ...           (35.9728, -83.9422),\n    ...           (36.1667, -86.7833)]\n    >>> distance.cdist(coords, coords, 'euclidean')\n    array([[ 0.    ,  4.7044,  1.6172,  1.8856],\n           [ 4.7044,  0.    ,  6.0893,  3.3561],\n           [ 1.6172,  6.0893,  0.    ,  2.8477],\n           [ 1.8856,  3.3561,  2.8477,  0.    ]])\n\n\n    Find the Manhattan distance from a 3-D point to the corners of the unit\n    cube:\n\n    >>> a = np.array([[0, 0, 0],\n    ...               [0, 0, 1],\n    ...               [0, 1, 0],\n    ...               [0, 1, 1],\n    ...               [1, 0, 0],\n    ...               [1, 0, 1],\n    ...               [1, 1, 0],\n    ...               [1, 1, 1]])\n    >>> b = np.array([[ 0.1,  0.2,  0.4]])\n    >>> distance.cdist(a, b, 'cityblock')\n    array([[ 0.7],\n           [ 0.9],\n           [ 1.3],\n           [ 1.5],\n           [ 1.5],\n           [ 1.7],\n           [ 2.1],\n           [ 2.3]])\n\n    "
    XA = np.asarray(XA, order='c')
    XB = np.asarray(XB, order='c')
    XA = _copy_array_if_base_present(_convert_to_double(XA))
    XB = _copy_array_if_base_present(_convert_to_double(XB))
    s = XA.shape
    sB = XB.shape
    if (len(s) != 2):
        raise ValueError('XA must be a 2-dimensional array.')
    if (len(sB) != 2):
        raise ValueError('XB must be a 2-dimensional array.')
    if (s[1] != sB[1]):
        raise ValueError('XA and XB must have the same number of columns (i.e. feature dimension.)')
    mA = s[0]
    mB = sB[0]
    n = s[1]
    dm = np.zeros((mA, mB), dtype=np.double)
    if callable(metric):
        if (metric == minkowski):
            for i in xrange(0, mA):
                for j in xrange(0, mB):
                    dm[(i, j)] = minkowski(XA[i, :], XB[j, :], p)
        elif (metric == wminkowski):
            for i in xrange(0, mA):
                for j in xrange(0, mB):
                    dm[(i, j)] = wminkowski(XA[i, :], XB[j, :], p, w)
        elif (metric == seuclidean):
            for i in xrange(0, mA):
                for j in xrange(0, mB):
                    dm[(i, j)] = seuclidean(XA[i, :], XB[j, :], V)
        elif (metric == mahalanobis):
            for i in xrange(0, mA):
                for j in xrange(0, mB):
                    dm[(i, j)] = mahalanobis(XA[i, :], XB[j, :], V)
        else:
            for i in xrange(0, mA):
                for j in xrange(0, mB):
                    dm[(i, j)] = metric(XA[i, :], XB[j, :])
    elif isinstance(metric, string_types):
        mstr = metric.lower()
        try:
            (validate, cdist_fn) = _SIMPLE_CDIST[mstr]
            XA = validate(XA)
            XB = validate(XB)
            cdist_fn(XA, XB, dm)
            return dm
        except KeyError:
            pass
        if (mstr in ['hamming', 'hamm', 'ha', 'h']):
            if (XA.dtype == bool):
                XA = _convert_to_bool(XA)
                XB = _convert_to_bool(XB)
                _distance_wrap.cdist_hamming_bool_wrap(XA, XB, dm)
            else:
                XA = _convert_to_double(XA)
                XB = _convert_to_double(XB)
                _distance_wrap.cdist_hamming_wrap(XA, XB, dm)
        elif (mstr in ['jaccard', 'jacc', 'ja', 'j']):
            if (XA.dtype == bool):
                XA = _convert_to_bool(XA)
                XB = _convert_to_bool(XB)
                _distance_wrap.cdist_jaccard_bool_wrap(XA, XB, dm)
            else:
                XA = _convert_to_double(XA)
                XB = _convert_to_double(XB)
                _distance_wrap.cdist_jaccard_wrap(XA, XB, dm)
        elif (mstr in ['minkowski', 'mi', 'm', 'pnorm']):
            XA = _convert_to_double(XA)
            XB = _convert_to_double(XB)
            _distance_wrap.cdist_minkowski_wrap(XA, XB, dm, p)
        elif (mstr in ['wminkowski', 'wmi', 'wm', 'wpnorm']):
            XA = _convert_to_double(XA)
            XB = _convert_to_double(XB)
            w = _convert_to_double(w)
            _distance_wrap.cdist_weighted_minkowski_wrap(XA, XB, dm, p, w)
        elif (mstr in ['seuclidean', 'se', 's']):
            XA = _convert_to_double(XA)
            XB = _convert_to_double(XB)
            if (V is not None):
                V = np.asarray(V, order='c')
                if (V.dtype != np.double):
                    raise TypeError('Variance vector V must contain doubles.')
                if (len(V.shape) != 1):
                    raise ValueError('Variance vector V must be one-dimensional.')
                if (V.shape[0] != n):
                    raise ValueError('Variance vector V must be of the same dimension as the vectors on which the distances are computed.')
                VV = _copy_array_if_base_present(_convert_to_double(V))
            else:
                VV = np.var(np.vstack([XA, XB]), axis=0, ddof=1)
            _distance_wrap.cdist_seuclidean_wrap(XA, XB, VV, dm)
        elif (mstr in ['cosine', 'cos']):
            XA = _convert_to_double(XA)
            XB = _convert_to_double(XB)
            _cosine_cdist(XA, XB, dm)
        elif (mstr in ['correlation', 'co']):
            XA = _convert_to_double(XA)
            XB = _convert_to_double(XB)
            XA -= XA.mean(axis=1)[:, np.newaxis]
            XB -= XB.mean(axis=1)[:, np.newaxis]
            _cosine_cdist(XA, XB, dm)
        elif (mstr in ['mahalanobis', 'mahal', 'mah']):
            XA = _convert_to_double(XA)
            XB = _convert_to_double(XB)
            if (VI is not None):
                VI = _convert_to_double(np.asarray(VI, order='c'))
                VI = _copy_array_if_base_present(VI)
            else:
                m = (mA + mB)
                if (m <= n):
                    raise ValueError(('The number of observations (%d) is too small; the covariance matrix is singular. For observations with %d dimensions, at least %d observations are required.' % (m, n, (n + 1))))
                X = np.vstack([XA, XB])
                V = np.atleast_2d(np.cov(X.T))
                del X
                VI = np.linalg.inv(V).T.copy()
            _distance_wrap.cdist_mahalanobis_wrap(XA, XB, VI, dm)
        elif (metric == 'test_euclidean'):
            dm = cdist(XA, XB, euclidean)
        elif (metric == 'test_seuclidean'):
            if (V is None):
                V = np.var(np.vstack([XA, XB]), axis=0, ddof=1)
            else:
                V = np.asarray(V, order='c')
            dm = cdist(XA, XB, (lambda u, v: seuclidean(u, v, V)))
        elif (metric == 'test_sqeuclidean'):
            dm = cdist(XA, XB, (lambda u, v: sqeuclidean(u, v)))
        elif (metric == 'test_braycurtis'):
            dm = cdist(XA, XB, braycurtis)
        elif (metric == 'test_mahalanobis'):
            if (VI is None):
                X = np.vstack([XA, XB])
                V = np.cov(X.T)
                VI = np.linalg.inv(V)
                X = None
                del X
            else:
                VI = np.asarray(VI, order='c')
            VI = _copy_array_if_base_present(VI)
            dm = cdist(XA, XB, (lambda u, v: mahalanobis(u, v, VI)))
        elif (metric == 'test_canberra'):
            dm = cdist(XA, XB, canberra)
        elif (metric == 'test_cityblock'):
            dm = cdist(XA, XB, cityblock)
        elif (metric == 'test_minkowski'):
            dm = cdist(XA, XB, minkowski, p=p)
        elif (metric == 'test_wminkowski'):
            dm = cdist(XA, XB, wminkowski, p=p, w=w)
        elif (metric == 'test_correlation'):
            dm = cdist(XA, XB, correlation)
        elif (metric == 'test_hamming'):
            dm = cdist(XA, XB, hamming)
        elif (metric == 'test_jaccard'):
            dm = cdist(XA, XB, jaccard)
        elif ((metric == 'test_chebyshev') or (metric == 'test_chebychev')):
            dm = cdist(XA, XB, chebyshev)
        elif (metric == 'test_yule'):
            dm = cdist(XA, XB, yule)
        elif (metric == 'test_matching'):
            dm = cdist(XA, XB, matching)
        elif (metric == 'test_dice'):
            dm = cdist(XA, XB, dice)
        elif (metric == 'test_kulsinski'):
            dm = cdist(XA, XB, kulsinski)
        elif (metric == 'test_rogerstanimoto'):
            dm = cdist(XA, XB, rogerstanimoto)
        elif (metric == 'test_russellrao'):
            dm = cdist(XA, XB, russellrao)
        elif (metric == 'test_sokalsneath'):
            dm = cdist(XA, XB, sokalsneath)
        elif (metric == 'test_sokalmichener'):
            dm = cdist(XA, XB, sokalmichener)
        else:
            raise ValueError(('Unknown Distance Metric: %s' % mstr))
    else:
        raise TypeError('2nd argument metric must be a string identifier or a function.')
    return dm
