def test_preserve_trustworthiness_approximately():
    random_state = check_random_state(0)
    n_components = 2
    methods = ['exact', 'barnes_hut']
    X = random_state.randn(50, n_components).astype(np.float32)
    for init in ('random', 'pca'):
        for method in methods:
            tsne = TSNE(n_components=n_components, init=init, random_state=0, method=method)
            X_embedded = tsne.fit_transform(X)
            t = trustworthiness(X, X_embedded, n_neighbors=1)
            assert_greater(t, 0.9, msg='Trustworthiness={:0.3f} < 0.9 for method={} and init={}'.format(t, method, init))