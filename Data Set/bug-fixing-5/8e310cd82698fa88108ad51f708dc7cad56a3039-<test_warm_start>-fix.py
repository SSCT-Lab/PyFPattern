@ignore_warnings(category=RuntimeWarning)
def test_warm_start():
    X = X_iris
    y = y_iris
    y_2classes = np.array((([0] * 75) + ([1] * 75)))
    y_3classes = np.array(((([0] * 40) + ([1] * 40)) + ([2] * 70)))
    y_3classes_alt = np.array(((([0] * 50) + ([1] * 50)) + ([3] * 50)))
    y_4classes = np.array((((([0] * 37) + ([1] * 37)) + ([2] * 38)) + ([3] * 38)))
    y_5classes = np.array(((((([0] * 30) + ([1] * 30)) + ([2] * 30)) + ([3] * 30)) + ([4] * 30)))
    clf = MLPClassifier(hidden_layer_sizes=2, solver='lbfgs', warm_start=True).fit(X, y)
    clf.fit(X, y)
    clf.fit(X, y_3classes)
    for y_i in (y_2classes, y_3classes_alt, y_4classes, y_5classes):
        clf = MLPClassifier(hidden_layer_sizes=2, solver='lbfgs', warm_start=True).fit(X, y)
        message = ('warm_start can only be used where `y` has the same classes as in the previous call to fit. Previously got [0 1 2], `y` has %s' % np.unique(y_i))
        with pytest.raises(ValueError, match=re.escape(message)):
            clf.fit(X, y_i)