def test_score_memmap():
    iris = load_iris()
    (X, y) = (iris.data, iris.target)
    clf = MockClassifier()
    tf = tempfile.NamedTemporaryFile(mode='wb', delete=False)
    tf.write(b'Hello world!!!!!')
    tf.close()
    scores = np.memmap(tf.name, dtype=np.float64)
    score = np.memmap(tf.name, shape=(), mode='r', dtype=np.float64)
    try:
        cross_val_score(clf, X, y, scoring=(lambda est, X, y: score))
        assert_raises(ValueError, cross_val_score, clf, X, y, scoring=(lambda est, X, y: scores))
    finally:
        (scores, score) = (None, None)
        for _ in range(3):
            try:
                os.unlink(tf.name)
                break
            except WindowsError:
                sleep(1.0)