@pytest.mark.parametrize('algo', ['full', 'elkan'])
def test_score(algo):
    km1 = KMeans(n_clusters=n_clusters, max_iter=1, random_state=42, n_init=1, algorithm=algo)
    s1 = km1.fit(X).score(X)
    km2 = KMeans(n_clusters=n_clusters, max_iter=10, random_state=42, n_init=1, algorithm=algo)
    s2 = km2.fit(X).score(X)
    assert_greater(s2, s1)