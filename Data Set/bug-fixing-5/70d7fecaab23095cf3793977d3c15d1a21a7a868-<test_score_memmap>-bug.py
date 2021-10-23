def test_score_memmap():
    iris = load_iris()
    (X, y) = (iris.data, iris.target)
    clf = MockClassifier()
    tf = tempfile.NamedTemporaryFile(mode='wb', delete=False)
    tf.write(b'Hello world!!!!!')
    tf.close()
    scores = np.memmap(tf.name, dtype=float)
    score = np.memmap(tf.name, shape=(), mode='w+', dtype=float)
    try:
        cross_val_score(clf, X, y, scoring=(lambda est, X, y: score))
        assert_raises(ValueError, cross_val_score, clf, X, y, scoring=(lambda est, X, y: scores))
    finally:
        os.unlink(tf.name)