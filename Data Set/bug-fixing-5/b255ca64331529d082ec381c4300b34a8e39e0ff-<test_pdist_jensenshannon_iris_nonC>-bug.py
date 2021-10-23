def test_pdist_jensenshannon_iris_nonC(self):
    eps = 5e-13
    X = eo['iris']
    Y_right = eo['pdist-jensenshannon-iris']
    Y_test2 = pdist(X, 'test_jensenshannon')
    _assert_within_tol(Y_test2, Y_right, eps)