@pytest.mark.skipif((K.backend() == 'cntk'), reason='Sparse tensors are not supported in cntk.')
def test_sparse_dot(self):
    x_d = np.array([0, 7, 2, 3], dtype=np.float32)
    x_r = np.array([0, 2, 2, 3], dtype=np.int64)
    x_c = np.array([4, 3, 2, 3], dtype=np.int64)
    x_sparse = sparse.csr_matrix((x_d, (x_r, x_c)), shape=(4, 5))
    x_dense = x_sparse.toarray()
    W = np.random.random((5, 4))
    backends = [KTF]
    if KTH.th_sparse_module:
        backends.append(KTH)
    for k in backends:
        t_W = k.variable(W)
        k_s = k.eval(k.dot(k.variable(x_sparse), t_W))
        k_d = k.eval(k.dot(k.variable(x_dense), t_W))
        assert (k_s.shape == k_d.shape)
        assert_allclose(k_s, k_d, atol=1e-05)