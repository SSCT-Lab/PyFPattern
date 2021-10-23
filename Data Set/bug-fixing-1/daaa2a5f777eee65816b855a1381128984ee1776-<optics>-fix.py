

def optics(X, min_samples=5, max_eps=np.inf, metric='euclidean', p=2, metric_params=None, maxima_ratio=0.75, rejection_ratio=0.7, similarity_threshold=0.4, significant_min=0.003, min_cluster_size=0.005, min_maxima_ratio=0.001, algorithm='ball_tree', leaf_size=30, n_jobs=None):
    'Perform OPTICS clustering from vector array\n\n    OPTICS: Ordering Points To Identify the Clustering Structure\n    Closely related to DBSCAN, finds core sample of high density and expands\n    clusters from them. Unlike DBSCAN, keeps cluster hierarchy for a variable\n    neighborhood radius. Better suited for usage on large point datasets than\n    the current sklearn implementation of DBSCAN.\n\n    Read more in the :ref:`User Guide <optics>`.\n\n    Parameters\n    ----------\n    X : array, shape (n_samples, n_features)\n        The data.\n\n    min_samples : int (default=5)\n        The number of samples in a neighborhood for a point to be considered\n        as a core point.\n\n    max_eps : float, optional (default=np.inf)\n        The maximum distance between two samples for them to be considered\n        as in the same neighborhood. Default value of "np.inf" will identify\n        clusters across all scales; reducing `max_eps` will result in\n        shorter run times.\n\n    metric : string or callable, optional (default=\'euclidean\')\n        metric to use for distance computation. Any metric from scikit-learn\n        or scipy.spatial.distance can be used.\n\n        If metric is a callable function, it is called on each\n        pair of instances (rows) and the resulting value recorded. The callable\n        should take two arrays as input and return one value indicating the\n        distance between them. This works for Scipy\'s metrics, but is less\n        efficient than passing the metric name as a string.\n\n        Distance matrices are not supported.\n\n        Valid values for metric are:\n\n        - from scikit-learn: [\'cityblock\', \'cosine\', \'euclidean\', \'l1\', \'l2\',\n          \'manhattan\']\n\n        - from scipy.spatial.distance: [\'braycurtis\', \'canberra\', \'chebyshev\',\n          \'correlation\', \'dice\', \'hamming\', \'jaccard\', \'kulsinski\',\n          \'mahalanobis\', \'minkowski\', \'rogerstanimoto\', \'russellrao\',\n          \'seuclidean\', \'sokalmichener\', \'sokalsneath\', \'sqeuclidean\',\n          \'yule\']\n\n        See the documentation for scipy.spatial.distance for details on these\n        metrics.\n\n    p : integer, optional (default=2)\n        Parameter for the Minkowski metric from\n        :class:`sklearn.metrics.pairwise_distances`. When p = 1, this is\n        equivalent to using manhattan_distance (l1), and euclidean_distance\n        (l2) for p = 2. For arbitrary p, minkowski_distance (l_p) is used.\n\n    metric_params : dict, optional (default=None)\n        Additional keyword arguments for the metric function.\n\n    maxima_ratio : float, optional (default=.75)\n        The maximum ratio we allow of average height of clusters on the\n        right and left to the local maxima in question. The higher the\n        ratio, the more generous the algorithm is to preserving local\n        minima, and the more cuts the resulting tree will have.\n\n    rejection_ratio : float, optional (default=.7)\n        Adjusts the fitness of the clustering. When the maxima_ratio is\n        exceeded, determine which of the clusters to the left and right to\n        reject based on rejection_ratio. Higher values will result in points\n        being more readily classified as noise; conversely, lower values will\n        result in more points being clustered.\n\n    similarity_threshold : float, optional (default=.4)\n        Used to check if nodes can be moved up one level, that is, if the\n        new cluster created is too "similar" to its parent, given the\n        similarity threshold. Similarity can be determined by 1) the size\n        of the new cluster relative to the size of the parent node or\n        2) the average of the reachability values of the new cluster\n        relative to the average of the reachability values of the parent\n        node. A lower value for the similarity threshold means less levels\n        in the tree.\n\n    significant_min : float, optional (default=.003)\n        Sets a lower threshold on how small a significant maxima can be.\n\n    min_cluster_size : int > 1 or float between 0 and 1 (default=0.005)\n        Minimum number of samples in an OPTICS cluster, expressed as an\n        absolute number or a fraction of the number of samples (rounded\n        to be at least 2).\n\n    min_maxima_ratio : float, optional (default=.001)\n        Used to determine neighborhood size for minimum cluster membership.\n        Each local maxima should be a largest value in a neighborhood\n        of the `size min_maxima_ratio * len(X)` from left and right.\n\n    algorithm : {\'auto\', \'ball_tree\', \'kd_tree\', \'brute\'}, optional\n        Algorithm used to compute the nearest neighbors:\n\n        - \'ball_tree\' will use :class:`BallTree` (default)\n        - \'kd_tree\' will use :class:`KDTree`\n        - \'brute\' will use a brute-force search.\n        - \'auto\' will attempt to decide the most appropriate algorithm\n          based on the values passed to :meth:`fit` method.\n\n        Note: fitting on sparse input will override the setting of\n        this parameter, using brute force.\n\n    leaf_size : int, optional (default=30)\n        Leaf size passed to :class:`BallTree` or :class:`KDTree`. This can\n        affect the speed of the construction and query, as well as the memory\n        required to store the tree. The optimal value depends on the\n        nature of the problem.\n\n    n_jobs : int or None, optional (default=None)\n        The number of parallel jobs to run for neighbors search.\n        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.\n        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`\n        for more details.\n\n    Returns\n    -------\n    core_sample_indices_ : array, shape (n_core_samples,)\n        The indices of the core samples.\n\n    labels_ : array, shape (n_samples,)\n        The estimated labels.\n\n    See also\n    --------\n    OPTICS\n        An estimator interface for this clustering algorithm.\n    dbscan\n        A similar clustering for a specified neighborhood radius (eps).\n        Our implementation is optimized for runtime.\n\n    References\n    ----------\n    Ankerst, Mihael, Markus M. Breunig, Hans-Peter Kriegel, and Jörg Sander.\n    "OPTICS: ordering points to identify the clustering structure." ACM SIGMOD\n    Record 28, no. 2 (1999): 49-60.\n    '
    clust = OPTICS(min_samples, max_eps, metric, p, metric_params, maxima_ratio, rejection_ratio, similarity_threshold, significant_min, min_cluster_size, min_maxima_ratio, algorithm, leaf_size, n_jobs)
    clust.fit(X)
    return (clust.core_sample_indices_, clust.labels_)
