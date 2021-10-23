def test_full_vs_elkan():
    km1 = KMeans(algorithm='full', random_state=13)
    km2 = KMeans(algorithm='elkan', random_state=13)
    km1.fit(X)
    km2.fit(X)
    (homogeneity_score(km1.predict(X), km2.predict(X)) == 1.0)