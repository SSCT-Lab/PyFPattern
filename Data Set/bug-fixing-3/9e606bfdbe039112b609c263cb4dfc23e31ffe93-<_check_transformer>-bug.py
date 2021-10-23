def _check_transformer(name, transformer_orig, X, y):
    if ((name in ('CCA', 'LocallyLinearEmbedding', 'KernelPCA')) and _is_32bit()):
        msg = (name + ' is non deterministic on 32bit Python')
        raise SkipTest(msg)
    (n_samples, n_features) = np.asarray(X).shape
    transformer = clone(transformer_orig)
    set_random_state(transformer)
    if (name in CROSS_DECOMPOSITION):
        y_ = np.c_[(y, y)]
        y_[::2, 1] *= 2
    else:
        y_ = y
    transformer.fit(X, y_)
    transformer_clone = clone(transformer)
    X_pred = transformer_clone.fit_transform(X, y=y_)
    if isinstance(X_pred, tuple):
        for x_pred in X_pred:
            assert_equal(x_pred.shape[0], n_samples)
    else:
        assert_equal(X_pred.shape[0], n_samples)
    if hasattr(transformer, 'transform'):
        if (name in CROSS_DECOMPOSITION):
            X_pred2 = transformer.transform(X, y_)
            X_pred3 = transformer.fit_transform(X, y=y_)
        else:
            X_pred2 = transformer.transform(X)
            X_pred3 = transformer.fit_transform(X, y=y_)
        if (isinstance(X_pred, tuple) and isinstance(X_pred2, tuple)):
            for (x_pred, x_pred2, x_pred3) in zip(X_pred, X_pred2, X_pred3):
                assert_allclose_dense_sparse(x_pred, x_pred2, atol=0.01, err_msg=('fit_transform and transform outcomes not consistent in %s' % transformer))
                assert_allclose_dense_sparse(x_pred, x_pred3, atol=0.01, err_msg=('consecutive fit_transform outcomes not consistent in %s' % transformer))
        else:
            assert_allclose_dense_sparse(X_pred, X_pred2, err_msg=('fit_transform and transform outcomes not consistent in %s' % transformer), atol=0.01)
            assert_allclose_dense_sparse(X_pred, X_pred3, atol=0.01, err_msg=('consecutive fit_transform outcomes not consistent in %s' % transformer))
            assert_equal(_num_samples(X_pred2), n_samples)
            assert_equal(_num_samples(X_pred3), n_samples)
        if hasattr(X, 'T'):
            assert_raises(ValueError, transformer.transform, X.T)