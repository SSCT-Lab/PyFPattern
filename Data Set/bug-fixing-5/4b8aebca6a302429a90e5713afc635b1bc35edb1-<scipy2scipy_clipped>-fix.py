def scipy2scipy_clipped(matrix, topn, eps=1e-09):
    "Get a `scipy.sparse` vector / matrix consisting of 'topn' elements of the greatest magnitude (absolute value).\n\n    Parameters\n    ----------\n    matrix : `scipy.sparse`\n        Input vector / matrix.\n    topn : int\n        Number of greatest (by module) elements, that will be in result.\n    eps : float\n        PARAMETER IGNORED.\n\n    Returns\n    -------\n    `scipy.sparse.csr.csr_matrix`\n        Clipped matrix.\n\n    "
    if (not scipy.sparse.issparse(matrix)):
        raise ValueError(("'%s' is not a scipy sparse vector." % matrix))
    if (topn <= 0):
        return scipy.sparse.csr_matrix([])
    if (matrix.shape[0] == 1):
        biggest = argsort(abs(matrix.data), topn, reverse=True)
        (indices, data) = (matrix.indices.take(biggest), matrix.data.take(biggest))
        return scipy.sparse.csr_matrix((data, indices, [0, len(indices)]))
    else:
        matrix_indices = []
        matrix_data = []
        matrix_indptr = [0]
        matrix_abs = abs(matrix)
        for i in range(matrix.shape[0]):
            v = matrix.getrow(i)
            v_abs = matrix_abs.getrow(i)
            biggest = argsort(v_abs.data, topn, reverse=True)
            (indices, data) = (v.indices.take(biggest), v.data.take(biggest))
            matrix_data.append(data)
            matrix_indices.append(indices)
            matrix_indptr.append((matrix_indptr[(- 1)] + min(len(indices), topn)))
        matrix_indices = np.concatenate(matrix_indices).ravel()
        matrix_data = np.concatenate(matrix_data).ravel()
        return scipy.sparse.csr.csr_matrix((matrix_data, matrix_indices, matrix_indptr), shape=(matrix.shape[0], (np.max(matrix_indices) + 1)))