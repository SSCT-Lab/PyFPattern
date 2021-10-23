def test_float_precision():
    km = KMeans(n_init=1, random_state=30)
    mb_km = MiniBatchKMeans(n_init=1, random_state=30)
    inertia = {
        
    }
    X_new = {
        
    }
    centers = {
        
    }
    for estimator in [km, mb_km]:
        for is_sparse in [False, True]:
            for dtype in [np.float64, np.float32]:
                if is_sparse:
                    X_test = sp.csr_matrix(X_csr, dtype=dtype)
                else:
                    X_test = dtype(X)
                estimator.fit(X_test)
                assert_equal(estimator.cluster_centers_.dtype, dtype)
                inertia[dtype] = estimator.inertia_
                X_new[dtype] = estimator.transform(X_test)
                centers[dtype] = estimator.cluster_centers_
                assert_equal(estimator.predict(X_test[0]), estimator.labels_[0])
                if hasattr(estimator, 'partial_fit'):
                    estimator.partial_fit(X_test[0:3])
                    assert_equal(estimator.cluster_centers_.dtype, dtype)
            assert_array_almost_equal(inertia[np.float32], inertia[np.float64], decimal=4)
            assert_array_almost_equal(X_new[np.float32], X_new[np.float64], decimal=4)
            assert_array_almost_equal(centers[np.float32], centers[np.float64], decimal=4)