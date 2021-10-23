def test_predict_equal_labels():
    km = KMeans(random_state=13, n_jobs=1, n_init=1, max_iter=1, algorithm='full')
    km.fit(X)
    assert_array_equal(km.predict(X), km.labels_)
    km = KMeans(random_state=13, n_jobs=1, n_init=1, max_iter=1, algorithm='elkan')
    km.fit(X)
    assert_array_equal(km.predict(X), km.labels_)