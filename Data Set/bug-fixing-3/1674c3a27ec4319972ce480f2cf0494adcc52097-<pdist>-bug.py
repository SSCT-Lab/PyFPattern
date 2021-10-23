def pdist(X, metric='euclidean', p=2, w=None, V=None, VI=None):
    "\n    Pairwise distances between observations in n-dimensional space.\n\n    The following are common calling conventions.\n\n    1. ``Y = pdist(X, 'euclidean')``\n\n       Computes the distance between m points using Euclidean distance\n       (2-norm) as the distance metric between the points. The points\n       are arranged as m n-dimensional row vectors in the matrix X.\n\n    2. ``Y = pdist(X, 'minkowski', p)``\n\n       Computes the distances using the Minkowski distance\n       :math:`||u-v||_p` (p-norm) where :math:`p \\geq 1`.\n\n    3. ``Y = pdist(X, 'cityblock')``\n\n       Computes the city block or Manhattan distance between the\n       points.\n\n    4. ``Y = pdist(X, 'seuclidean', V=None)``\n\n       Computes the standardized Euclidean distance. The standardized\n       Euclidean distance between two n-vectors ``u`` and ``v`` is\n\n       .. math::\n\n          \\sqrt{\\sum {(u_i-v_i)^2 / V[x_i]}}\n\n\n       V is the variance vector; V[i] is the variance computed over all\n       the i'th components of the points.  If not passed, it is\n       automatically computed.\n\n    5. ``Y = pdist(X, 'sqeuclidean')``\n\n       Computes the squared Euclidean distance :math:`||u-v||_2^2` between\n       the vectors.\n\n    6. ``Y = pdist(X, 'cosine')``\n\n       Computes the cosine distance between vectors u and v,\n\n       .. math::\n\n          1 - \\frac{u \\cdot v}\n                   {{||u||}_2 {||v||}_2}\n\n       where :math:`||*||_2` is the 2-norm of its argument ``*``, and\n       :math:`u \\cdot v` is the dot product of ``u`` and ``v``.\n\n    7. ``Y = pdist(X, 'correlation')``\n\n       Computes the correlation distance between vectors u and v. This is\n\n       .. math::\n\n          1 - \\frac{(u - \\bar{u}) \\cdot (v - \\bar{v})}\n                   {{||(u - \\bar{u})||}_2 {||(v - \\bar{v})||}_2}\n\n       where :math:`\\bar{v}` is the mean of the elements of vector v,\n       and :math:`x \\cdot y` is the dot product of :math:`x` and :math:`y`.\n\n    8. ``Y = pdist(X, 'hamming')``\n\n       Computes the normalized Hamming distance, or the proportion of\n       those vector elements between two n-vectors ``u`` and ``v``\n       which disagree. To save memory, the matrix ``X`` can be of type\n       boolean.\n\n    9. ``Y = pdist(X, 'jaccard')``\n\n       Computes the Jaccard distance between the points. Given two\n       vectors, ``u`` and ``v``, the Jaccard distance is the\n       proportion of those elements ``u[i]`` and ``v[i]`` that\n       disagree.\n\n    10. ``Y = pdist(X, 'chebyshev')``\n\n       Computes the Chebyshev distance between the points. The\n       Chebyshev distance between two n-vectors ``u`` and ``v`` is the\n       maximum norm-1 distance between their respective elements. More\n       precisely, the distance is given by\n\n       .. math::\n\n          d(u,v) = \\max_i {|u_i-v_i|}\n\n    11. ``Y = pdist(X, 'canberra')``\n\n       Computes the Canberra distance between the points. The\n       Canberra distance between two points ``u`` and ``v`` is\n\n       .. math::\n\n         d(u,v) = \\sum_i \\frac{|u_i-v_i|}\n                              {|u_i|+|v_i|}\n\n\n    12. ``Y = pdist(X, 'braycurtis')``\n\n       Computes the Bray-Curtis distance between the points. The\n       Bray-Curtis distance between two points ``u`` and ``v`` is\n\n\n       .. math::\n\n            d(u,v) = \\frac{\\sum_i {u_i-v_i}}\n                          {\\sum_i {u_i+v_i}}\n\n    13. ``Y = pdist(X, 'mahalanobis', VI=None)``\n\n       Computes the Mahalanobis distance between the points. The\n       Mahalanobis distance between two points ``u`` and ``v`` is\n       :math:`(u-v)(1/V)(u-v)^T` where :math:`(1/V)` (the ``VI``\n       variable) is the inverse covariance. If ``VI`` is not None,\n       ``VI`` will be used as the inverse covariance matrix.\n\n    14. ``Y = pdist(X, 'yule')``\n\n       Computes the Yule distance between each pair of boolean\n       vectors. (see yule function documentation)\n\n    15. ``Y = pdist(X, 'matching')``\n\n       Synonym for 'hamming'.\n\n    16. ``Y = pdist(X, 'dice')``\n\n       Computes the Dice distance between each pair of boolean\n       vectors. (see dice function documentation)\n\n    17. ``Y = pdist(X, 'kulsinski')``\n\n       Computes the Kulsinski distance between each pair of\n       boolean vectors. (see kulsinski function documentation)\n\n    18. ``Y = pdist(X, 'rogerstanimoto')``\n\n       Computes the Rogers-Tanimoto distance between each pair of\n       boolean vectors. (see rogerstanimoto function documentation)\n\n    19. ``Y = pdist(X, 'russellrao')``\n\n       Computes the Russell-Rao distance between each pair of\n       boolean vectors. (see russellrao function documentation)\n\n    20. ``Y = pdist(X, 'sokalmichener')``\n\n       Computes the Sokal-Michener distance between each pair of\n       boolean vectors. (see sokalmichener function documentation)\n\n    21. ``Y = pdist(X, 'sokalsneath')``\n\n       Computes the Sokal-Sneath distance between each pair of\n       boolean vectors. (see sokalsneath function documentation)\n\n    22. ``Y = pdist(X, 'wminkowski')``\n\n       Computes the weighted Minkowski distance between each pair of\n       vectors. (see wminkowski function documentation)\n\n    23. ``Y = pdist(X, f)``\n\n       Computes the distance between all pairs of vectors in X\n       using the user supplied 2-arity function f. For example,\n       Euclidean distance between the vectors could be computed\n       as follows::\n\n         dm = pdist(X, lambda u, v: np.sqrt(((u-v)**2).sum()))\n\n       Note that you should avoid passing a reference to one of\n       the distance functions defined in this library. For example,::\n\n         dm = pdist(X, sokalsneath)\n\n       would calculate the pair-wise distances between the vectors in\n       X using the Python function sokalsneath. This would result in\n       sokalsneath being called :math:`{n \\choose 2}` times, which\n       is inefficient. Instead, the optimized C version is more\n       efficient, and we call it using the following syntax.::\n\n         dm = pdist(X, 'sokalsneath')\n\n    Parameters\n    ----------\n    X : ndarray\n        An m by n array of m original observations in an\n        n-dimensional space.\n    metric : str or function, optional\n        The distance metric to use. The distance function can\n        be 'braycurtis', 'canberra', 'chebyshev', 'cityblock',\n        'correlation', 'cosine', 'dice', 'euclidean', 'hamming',\n        'jaccard', 'kulsinski', 'mahalanobis', 'matching',\n        'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',\n        'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'.\n    w : ndarray, optional\n        The weight vector (for weighted Minkowski).\n    p : double, optional\n        The p-norm to apply (for Minkowski, weighted and unweighted)\n    V : ndarray, optional\n        The variance vector (for standardized Euclidean).\n    VI : ndarray, optional\n        The inverse of the covariance matrix (for Mahalanobis).\n\n    Returns\n    -------\n    Y : ndarray\n        Returns a condensed distance matrix Y.  For\n        each :math:`i` and :math:`j` (where :math:`i<j<n`), the\n        metric ``dist(u=X[i], v=X[j])`` is computed and stored in entry ``ij``.\n\n    See Also\n    --------\n    squareform : converts between condensed distance matrices and\n                 square distance matrices.\n\n    Notes\n    -----\n    See ``squareform`` for information on how to calculate the index of\n    this entry or to convert the condensed distance matrix to a\n    redundant square matrix.\n\n    "
    X = np.asarray(X, order='c')
    X = _copy_array_if_base_present(X)
    s = X.shape
    if (len(s) != 2):
        raise ValueError('A 2-dimensional array must be passed.')
    (m, n) = s
    dm = np.zeros(((m * (m - 1)) // 2), dtype=np.double)
    wmink_names = ['wminkowski', 'wmi', 'wm', 'wpnorm']
    if ((w is None) and ((metric == wminkowski) or (metric in wmink_names))):
        raise ValueError('weighted minkowski requires a weight vector `w` to be given.')
    if callable(metric):
        if (metric == minkowski):

            def dfun(u, v):
                return minkowski(u, v, p)
        elif (metric == wminkowski):

            def dfun(u, v):
                return wminkowski(u, v, p, w)
        elif (metric == seuclidean):

            def dfun(u, v):
                return seuclidean(u, v, V)
        elif (metric == mahalanobis):

            def dfun(u, v):
                return mahalanobis(u, v, V)
        else:
            dfun = metric
        X = _convert_to_double(X)
        k = 0
        for i in xrange(0, (m - 1)):
            for j in xrange((i + 1), m):
                dm[k] = dfun(X[i], X[j])
                k = (k + 1)
    elif isinstance(metric, string_types):
        mstr = metric.lower()
        try:
            (validate, pdist_fn) = _SIMPLE_PDIST[mstr]
            X = validate(X)
            pdist_fn(X, dm)
            return dm
        except KeyError:
            pass
        if (mstr in ['hamming', 'hamm', 'ha', 'h']):
            if (X.dtype == bool):
                X = _convert_to_bool(X)
                _distance_wrap.pdist_hamming_bool_wrap(X, dm)
            else:
                X = _convert_to_double(X)
                _distance_wrap.pdist_hamming_wrap(X, dm)
        elif (mstr in ['jaccard', 'jacc', 'ja', 'j']):
            if (X.dtype == bool):
                X = _convert_to_bool(X)
                _distance_wrap.pdist_jaccard_bool_wrap(X, dm)
            else:
                X = _convert_to_double(X)
                _distance_wrap.pdist_jaccard_wrap(X, dm)
        elif (mstr in ['minkowski', 'mi', 'm']):
            X = _convert_to_double(X)
            _distance_wrap.pdist_minkowski_wrap(X, dm, p)
        elif (mstr in wmink_names):
            X = _convert_to_double(X)
            w = _convert_to_double(np.asarray(w))
            _distance_wrap.pdist_weighted_minkowski_wrap(X, dm, p, w)
        elif (mstr in ['seuclidean', 'se', 's']):
            X = _convert_to_double(X)
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
                VV = np.var(X, axis=0, ddof=1)
            _distance_wrap.pdist_seuclidean_wrap(X, VV, dm)
        elif (mstr in ['cosine', 'cos']):
            X = _convert_to_double(X)
            norms = _row_norms(X)
            _distance_wrap.pdist_cosine_wrap(X, dm, norms)
        elif (mstr in ['old_cosine', 'old_cos']):
            X = _convert_to_double(X)
            norms = _row_norms(X)
            nV = norms.reshape(m, 1)
            nm = np.dot(X, X.T)
            de = np.dot(nV, nV.T)
            dm = (1.0 - (nm / de))
            dm[(xrange(0, m), xrange(0, m))] = 0.0
            dm = squareform(dm)
        elif (mstr in ['correlation', 'co']):
            X = _convert_to_double(X)
            X2 = (X - X.mean(1)[:, np.newaxis])
            norms = _row_norms(X2)
            _distance_wrap.pdist_cosine_wrap(X2, dm, norms)
        elif (mstr in ['mahalanobis', 'mahal', 'mah']):
            X = _convert_to_double(X)
            if (VI is not None):
                VI = _convert_to_double(np.asarray(VI, order='c'))
                VI = _copy_array_if_base_present(VI)
            else:
                if (m <= n):
                    raise ValueError(('The number of observations (%d) is too small; the covariance matrix is singular. For observations with %d dimensions, at least %d observations are required.' % (m, n, (n + 1))))
                V = np.atleast_2d(np.cov(X.T))
                VI = _convert_to_double(np.linalg.inv(V).T.copy())
            _distance_wrap.pdist_mahalanobis_wrap(X, VI, dm)
        elif (metric == 'test_euclidean'):
            dm = pdist(X, euclidean)
        elif (metric == 'test_sqeuclidean'):
            if (V is None):
                V = np.var(X, axis=0, ddof=1)
            else:
                V = np.asarray(V, order='c')
            dm = pdist(X, (lambda u, v: seuclidean(u, v, V)))
        elif (metric == 'test_braycurtis'):
            dm = pdist(X, braycurtis)
        elif (metric == 'test_mahalanobis'):
            if (VI is None):
                V = np.cov(X.T)
                VI = np.linalg.inv(V)
            else:
                VI = np.asarray(VI, order='c')
            VI = _copy_array_if_base_present(VI)
            dm = pdist(X, (lambda u, v: mahalanobis(u, v, VI)))
        elif (metric == 'test_canberra'):
            dm = pdist(X, canberra)
        elif (metric == 'test_cityblock'):
            dm = pdist(X, cityblock)
        elif (metric == 'test_minkowski'):
            dm = pdist(X, minkowski, p=p)
        elif (metric == 'test_wminkowski'):
            dm = pdist(X, wminkowski, p=p, w=w)
        elif (metric == 'test_cosine'):
            dm = pdist(X, cosine)
        elif (metric == 'test_correlation'):
            dm = pdist(X, correlation)
        elif (metric == 'test_hamming'):
            dm = pdist(X, hamming)
        elif (metric == 'test_jaccard'):
            dm = pdist(X, jaccard)
        elif ((metric == 'test_chebyshev') or (metric == 'test_chebychev')):
            dm = pdist(X, chebyshev)
        elif (metric == 'test_yule'):
            dm = pdist(X, yule)
        elif (metric == 'test_matching'):
            dm = pdist(X, matching)
        elif (metric == 'test_dice'):
            dm = pdist(X, dice)
        elif (metric == 'test_kulsinski'):
            dm = pdist(X, kulsinski)
        elif (metric == 'test_rogerstanimoto'):
            dm = pdist(X, rogerstanimoto)
        elif (metric == 'test_russellrao'):
            dm = pdist(X, russellrao)
        elif (metric == 'test_sokalsneath'):
            dm = pdist(X, sokalsneath)
        elif (metric == 'test_sokalmichener'):
            dm = pdist(X, sokalmichener)
        else:
            raise ValueError(('Unknown Distance Metric: %s' % mstr))
    else:
        raise TypeError('2nd argument metric must be a string identifier or a function.')
    return dm