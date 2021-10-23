def test_fit_csr_matrix():
    random_state = check_random_state(0)
    X = random_state.randn(50, 2)
    X[(np.random.randint(0, 50, 25), np.random.randint(0, 2, 25))] = 0.0
    X_csr = sp.csr_matrix(X)
    tsne = TSNE(n_components=2, perplexity=10, learning_rate=100.0, random_state=0, method='exact', n_iter=500)
    X_embedded = tsne.fit_transform(X_csr)
    assert_almost_equal(trustworthiness(X_csr, X_embedded, n_neighbors=1), 1.0, decimal=1)