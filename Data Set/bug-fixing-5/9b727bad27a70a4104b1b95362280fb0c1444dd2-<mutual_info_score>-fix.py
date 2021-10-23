def mutual_info_score(labels_true, labels_pred, contingency=None):
    "Mutual Information between two clusterings.\n\n    The Mutual Information is a measure of the similarity between two labels of\n    the same data. Where :math:`|U_i|` is the number of the samples\n    in cluster :math:`U_i` and :math:`|V_j|` is the number of the\n    samples in cluster :math:`V_j`, the Mutual Information\n    between clusterings :math:`U` and :math:`V` is given as:\n\n    .. math::\n\n        MI(U,V)=\\sum_{i=1}^{|U|} \\sum_{j=1}^{|V|} \\frac{|U_i\\cap V_j|}{N}\n        \\log\\frac{N|U_i \\cap V_j|}{|U_i||V_j|}\n\n    This metric is independent of the absolute values of the labels:\n    a permutation of the class or cluster label values won't change the\n    score value in any way.\n\n    This metric is furthermore symmetric: switching ``label_true`` with\n    ``label_pred`` will return the same score value. This can be useful to\n    measure the agreement of two independent label assignments strategies\n    on the same dataset when the real ground truth is not known.\n\n    Read more in the :ref:`User Guide <mutual_info_score>`.\n\n    Parameters\n    ----------\n    labels_true : int array, shape = [n_samples]\n        A clustering of the data into disjoint subsets.\n\n    labels_pred : array, shape = [n_samples]\n        A clustering of the data into disjoint subsets.\n\n    contingency : {None, array, sparse matrix},\n                  shape = [n_classes_true, n_classes_pred]\n        A contingency matrix given by the :func:`contingency_matrix` function.\n        If value is ``None``, it will be computed, otherwise the given value is\n        used, with ``labels_true`` and ``labels_pred`` ignored.\n\n    Returns\n    -------\n    mi : float\n       Mutual information, a non-negative value\n\n    See also\n    --------\n    adjusted_mutual_info_score: Adjusted against chance Mutual Information\n    normalized_mutual_info_score: Normalized Mutual Information\n    "
    if (contingency is None):
        (labels_true, labels_pred) = check_clusterings(labels_true, labels_pred)
        contingency = contingency_matrix(labels_true, labels_pred, sparse=True)
    else:
        contingency = check_array(contingency, accept_sparse=['csr', 'csc', 'coo'], dtype=[int, np.int32, np.int64])
    if isinstance(contingency, np.ndarray):
        (nzx, nzy) = np.nonzero(contingency)
        nz_val = contingency[(nzx, nzy)]
    elif sp.issparse(contingency):
        (nzx, nzy, nz_val) = sp.find(contingency)
    else:
        raise ValueError(("Unsupported type for 'contingency': %s" % type(contingency)))
    contingency_sum = contingency.sum()
    pi = np.ravel(contingency.sum(axis=1))
    pj = np.ravel(contingency.sum(axis=0))
    log_contingency_nm = np.log(nz_val)
    contingency_nm = (nz_val / contingency_sum)
    outer = (pi.take(nzx) * pj.take(nzy))
    log_outer = (((- np.log(outer)) + log(pi.sum())) + log(pj.sum()))
    mi = ((contingency_nm * (log_contingency_nm - log(contingency_sum))) + (contingency_nm * log_outer))
    return mi.sum()