

def ward_tree(X, connectivity=None, n_clusters=None, return_distance=False):
    "Ward clustering based on a Feature matrix.\n\n    Recursively merges the pair of clusters that minimally increases\n    within-cluster variance.\n\n    The inertia matrix uses a Heapq-based representation.\n\n    This is the structured version, that takes into account some topological\n    structure between samples.\n\n    Read more in the :ref:`User Guide <hierarchical_clustering>`.\n\n    Parameters\n    ----------\n    X : array, shape (n_samples, n_features)\n        feature matrix  representing n_samples samples to be clustered\n\n    connectivity : sparse matrix (optional).\n        connectivity matrix. Defines for each sample the neighboring samples\n        following a given structure of the data. The matrix is assumed to\n        be symmetric and only the upper triangular half is used.\n        Default is None, i.e, the Ward algorithm is unstructured.\n\n    n_clusters : int (optional)\n        Stop early the construction of the tree at n_clusters. This is\n        useful to decrease computation time if the number of clusters is\n        not small compared to the number of samples. In this case, the\n        complete tree is not computed, thus the 'children' output is of\n        limited use, and the 'parents' output should rather be used.\n        This option is valid only when specifying a connectivity matrix.\n\n    return_distance : bool (optional)\n        If True, return the distance between the clusters.\n\n    Returns\n    -------\n    children : 2D array, shape (n_nodes-1, 2)\n        The children of each non-leaf node. Values less than `n_samples`\n        correspond to leaves of the tree which are the original samples.\n        A node `i` greater than or equal to `n_samples` is a non-leaf\n        node and has children `children_[i - n_samples]`. Alternatively\n        at the i-th iteration, children[i][0] and children[i][1]\n        are merged to form node `n_samples + i`\n\n    n_components : int\n        The number of connected components in the graph.\n\n    n_leaves : int\n        The number of leaves in the tree\n\n    parents : 1D array, shape (n_nodes, ) or None\n        The parent of each node. Only returned when a connectivity matrix\n        is specified, elsewhere 'None' is returned.\n\n    distances : 1D array, shape (n_nodes-1, )\n        Only returned if return_distance is set to True (for compatibility).\n        The distances between the centers of the nodes. `distances[i]`\n        corresponds to a weighted euclidean distance between\n        the nodes `children[i, 1]` and `children[i, 2]`. If the nodes refer to\n        leaves of the tree, then `distances[i]` is their unweighted euclidean\n        distance. Distances are updated in the following way\n        (from scipy.hierarchy.linkage):\n\n        The new entry :math:`d(u,v)` is computed as follows,\n\n        .. math::\n\n           d(u,v) = \\sqrt{\\frac{|v|+|s|}\n                               {T}d(v,s)^2\n                        + \\frac{|v|+|t|}\n                               {T}d(v,t)^2\n                        - \\frac{|v|}\n                               {T}d(s,t)^2}\n\n        where :math:`u` is the newly joined cluster consisting of\n        clusters :math:`s` and :math:`t`, :math:`v` is an unused\n        cluster in the forest, :math:`T=|v|+|s|+|t|`, and\n        :math:`|*|` is the cardinality of its argument. This is also\n        known as the incremental algorithm.\n    "
    X = np.asarray(X)
    if (X.ndim == 1):
        X = np.reshape(X, ((- 1), 1))
    (n_samples, n_features) = X.shape
    if (connectivity is None):
        from scipy.cluster import hierarchy
        if (n_clusters is not None):
            warnings.warn('Partial build of the tree is implemented only for structured clustering (i.e. with explicit connectivity). The algorithm will build the full tree and only retain the lower branches required for the specified number of clusters', stacklevel=2)
        X = np.require(X, requirements='W')
        out = hierarchy.ward(X)
        children_ = out[:, :2].astype(np.intp)
        if return_distance:
            distances = out[:, 2]
            return (children_, 1, n_samples, None, distances)
        else:
            return (children_, 1, n_samples, None)
    (connectivity, n_components) = _fix_connectivity(X, connectivity, affinity='euclidean')
    if (n_clusters is None):
        n_nodes = ((2 * n_samples) - 1)
    else:
        if (n_clusters > n_samples):
            raise ValueError(('Cannot provide more clusters than samples. %i n_clusters was asked, and there are %i samples.' % (n_clusters, n_samples)))
        n_nodes = ((2 * n_samples) - n_clusters)
    coord_row = []
    coord_col = []
    A = []
    for (ind, row) in enumerate(connectivity.rows):
        A.append(row)
        row = [i for i in row if (i < ind)]
        coord_row.extend((len(row) * [ind]))
        coord_col.extend(row)
    coord_row = np.array(coord_row, dtype=np.intp, order='C')
    coord_col = np.array(coord_col, dtype=np.intp, order='C')
    moments_1 = np.zeros(n_nodes, order='C')
    moments_1[:n_samples] = 1
    moments_2 = np.zeros((n_nodes, n_features), order='C')
    moments_2[:n_samples] = X
    inertia = np.empty(len(coord_row), dtype=np.float64, order='C')
    _hierarchical.compute_ward_dist(moments_1, moments_2, coord_row, coord_col, inertia)
    inertia = list(six.moves.zip(inertia, coord_row, coord_col))
    heapify(inertia)
    parent = np.arange(n_nodes, dtype=np.intp)
    used_node = np.ones(n_nodes, dtype=bool)
    children = []
    if return_distance:
        distances = np.empty((n_nodes - n_samples))
    not_visited = np.empty(n_nodes, dtype=np.int8, order='C')
    for k in range(n_samples, n_nodes):
        while True:
            (inert, i, j) = heappop(inertia)
            if (used_node[i] and used_node[j]):
                break
        (parent[i], parent[j]) = (k, k)
        children.append((i, j))
        used_node[i] = used_node[j] = False
        if return_distance:
            distances[(k - n_samples)] = inert
        moments_1[k] = (moments_1[i] + moments_1[j])
        moments_2[k] = (moments_2[i] + moments_2[j])
        coord_col = []
        not_visited.fill(1)
        not_visited[k] = 0
        _hierarchical._get_parents(A[i], coord_col, parent, not_visited)
        _hierarchical._get_parents(A[j], coord_col, parent, not_visited)
        [A[l].append(k) for l in coord_col]
        A.append(coord_col)
        coord_col = np.array(coord_col, dtype=np.intp, order='C')
        coord_row = np.empty(coord_col.shape, dtype=np.intp, order='C')
        coord_row.fill(k)
        n_additions = len(coord_row)
        ini = np.empty(n_additions, dtype=np.float64, order='C')
        _hierarchical.compute_ward_dist(moments_1, moments_2, coord_row, coord_col, ini)
        [heappush(inertia, (ini[idx], k, coord_col[idx])) for idx in range(n_additions)]
    n_leaves = n_samples
    children = [c[::(- 1)] for c in children]
    children = np.array(children)
    if return_distance:
        distances = np.sqrt((2.0 * distances))
        return (children, n_components, n_leaves, parent, distances)
    else:
        return (children, n_components, n_leaves, parent)
