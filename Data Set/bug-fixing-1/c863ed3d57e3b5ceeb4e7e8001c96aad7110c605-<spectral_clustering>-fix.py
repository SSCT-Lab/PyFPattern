

def spectral_clustering(affinity, n_clusters=8, n_components=None, eigen_solver=None, random_state=None, n_init=10, eigen_tol=0.0, assign_labels='kmeans'):
    "Apply clustering to a projection of the normalized Laplacian.\n\n    In practice Spectral Clustering is very useful when the structure of\n    the individual clusters is highly non-convex or more generally when\n    a measure of the center and spread of the cluster is not a suitable\n    description of the complete cluster. For instance, when clusters are\n    nested circles on the 2D plane.\n\n    If affinity is the adjacency matrix of a graph, this method can be\n    used to find normalized graph cuts.\n\n    Read more in the :ref:`User Guide <spectral_clustering>`.\n\n    Parameters\n    -----------\n    affinity : array-like or sparse matrix, shape: (n_samples, n_samples)\n        The affinity matrix describing the relationship of the samples to\n        embed. **Must be symmetric**.\n\n        Possible examples:\n          - adjacency matrix of a graph,\n          - heat kernel of the pairwise distance matrix of the samples,\n          - symmetric k-nearest neighbours connectivity matrix of the samples.\n\n    n_clusters : integer, optional\n        Number of clusters to extract.\n\n    n_components : integer, optional, default is n_clusters\n        Number of eigen vectors to use for the spectral embedding\n\n    eigen_solver : {None, 'arpack', 'lobpcg', or 'amg'}\n        The eigenvalue decomposition strategy to use. AMG requires pyamg\n        to be installed. It can be faster on very large, sparse problems,\n        but may also lead to instabilities\n\n    random_state : int, RandomState instance or None (default)\n        A pseudo random number generator used for the initialization of the\n        lobpcg eigen vectors decomposition when eigen_solver == 'amg' and by\n        the K-Means initialization. Use an int to make the randomness\n        deterministic.\n        See :term:`Glossary <random_state>`.\n\n    n_init : int, optional, default: 10\n        Number of time the k-means algorithm will be run with different\n        centroid seeds. The final results will be the best output of\n        n_init consecutive runs in terms of inertia.\n\n    eigen_tol : float, optional, default: 0.0\n        Stopping criterion for eigendecomposition of the Laplacian matrix\n        when using arpack eigen_solver.\n\n    assign_labels : {'kmeans', 'discretize'}, default: 'kmeans'\n        The strategy to use to assign labels in the embedding\n        space.  There are two ways to assign labels after the laplacian\n        embedding.  k-means can be applied and is a popular choice. But it can\n        also be sensitive to initialization. Discretization is another\n        approach which is less sensitive to random initialization. See\n        the 'Multiclass spectral clustering' paper referenced below for\n        more details on the discretization approach.\n\n    Returns\n    -------\n    labels : array of integers, shape: n_samples\n        The labels of the clusters.\n\n    References\n    ----------\n\n    - Normalized cuts and image segmentation, 2000\n      Jianbo Shi, Jitendra Malik\n      http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.160.2324\n\n    - A Tutorial on Spectral Clustering, 2007\n      Ulrike von Luxburg\n      http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.165.9323\n\n    - Multiclass spectral clustering, 2003\n      Stella X. Yu, Jianbo Shi\n      https://www1.icsi.berkeley.edu/~stellayu/publication/doc/2003kwayICCV.pdf\n\n    Notes\n    ------\n    The graph should contain only one connect component, elsewhere\n    the results make little sense.\n\n    This algorithm solves the normalized cut for k=2: it is a\n    normalized spectral clustering.\n    "
    if (assign_labels not in ('kmeans', 'discretize')):
        raise ValueError(("The 'assign_labels' parameter should be 'kmeans' or 'discretize', but '%s' was given" % assign_labels))
    random_state = check_random_state(random_state)
    n_components = (n_clusters if (n_components is None) else n_components)
    maps = spectral_embedding(affinity, n_components=n_components, eigen_solver=eigen_solver, random_state=random_state, eigen_tol=eigen_tol, drop_first=False)
    if (assign_labels == 'kmeans'):
        (_, labels, _) = k_means(maps, n_clusters, random_state=random_state, n_init=n_init)
    else:
        labels = discretize(maps, random_state=random_state)
    return labels
