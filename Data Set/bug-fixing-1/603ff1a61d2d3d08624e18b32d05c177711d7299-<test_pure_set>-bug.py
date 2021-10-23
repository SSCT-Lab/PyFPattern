

def test_pure_set():
    X = [[(- 2), (- 1)], [(- 1), (- 1)], [(- 1), (- 2)], [1, 1], [1, 2], [2, 1]]
    y = [1, 1, 1, 1, 1, 1]
    for (name, TreeClassifier) in CLF_TREES.items():
        clf = TreeClassifier(random_state=0)
        clf.fit(X, y)
        assert_array_equal(clf.predict(X), y, err_msg='Failed with {0}'.format(name))
    for (name, TreeRegressor) in REG_TREES.items():
        reg = TreeRegressor(random_state=0)
        reg.fit(X, y)
        assert_almost_equal(clf.predict(X), y, err_msg='Failed with {0}'.format(name))
