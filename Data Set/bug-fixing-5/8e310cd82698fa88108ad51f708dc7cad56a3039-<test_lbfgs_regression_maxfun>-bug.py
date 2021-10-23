@pytest.mark.parametrize('X,y', regression_datasets)
def test_lbfgs_regression_maxfun(X, y):
    max_fun = 10
    for activation in ACTIVATION_TYPES:
        mlp = MLPRegressor(solver='lbfgs', hidden_layer_sizes=50, max_iter=150, max_fun=max_fun, shuffle=True, random_state=1, activation=activation)
        with pytest.warns(ConvergenceWarning):
            mlp.fit(X, y)
            assert (max_fun >= mlp.n_iter_)
    mlp.max_fun = (- 1)
    assert_raises(ValueError, mlp.fit, X, y)