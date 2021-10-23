def test_sparse_concat(self):
    x_d = np.array([0, 7, 2, 3], dtype=np.float32)
    x_r = np.array([0, 2, 2, 3], dtype=np.int64)
    x_c = np.array([4, 3, 2, 3], dtype=np.int64)
    x_sparse_1 = sparse.csr_matrix((x_d, (x_r, x_c)), shape=(4, 5))
    x_d = np.array([0, 7, 2, 3], dtype=np.float32)
    x_r = np.array([0, 2, 2, 3], dtype=np.int64)
    x_c = np.array([4, 3, 2, 3], dtype=np.int64)
    x_sparse_2 = sparse.csr_matrix((x_d, (x_r, x_c)), shape=(4, 5))
    x_dense_1 = x_sparse_1.toarray()
    x_dense_2 = x_sparse_2.toarray()
    backends = [KTF]
    if KTH.th_sparse_module:
        backends.append(KTH)
    for k in backends:
        k_s = k.concatenate([k.variable(x_sparse_1), k.variable(x_sparse_2)])
        assert k.is_sparse(k_s)
        k_s_d = k.eval(k_s)
        k_d = k.eval(k.concatenate([k.variable(x_dense_1), k.variable(x_dense_2)]))
        assert (k_s_d.shape == k_d.shape)
        assert_allclose(k_s_d, k_d, atol=1e-05)