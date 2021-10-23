

def test_extract_xi():
    rng = np.random.RandomState(0)
    n_points_per_cluster = 5
    C1 = ([(- 5), (- 2)] + (0.8 * rng.randn(n_points_per_cluster, 2)))
    C2 = ([4, (- 1)] + (0.1 * rng.randn(n_points_per_cluster, 2)))
    C3 = ([1, (- 2)] + (0.2 * rng.randn(n_points_per_cluster, 2)))
    C4 = ([(- 2), 3] + (0.3 * rng.randn(n_points_per_cluster, 2)))
    C5 = ([3, (- 2)] + (0.6 * rng.randn(n_points_per_cluster, 2)))
    C6 = ([5, 6] + (0.2 * rng.randn(n_points_per_cluster, 2)))
    X = np.vstack((C1, C2, C3, C4, C5, np.array([[100, 100]]), C6))
    expected_labels = np.r_[(([2] * 5), ([0] * 5), ([1] * 5), ([3] * 5), ([1] * 5), (- 1), ([4] * 5))]
    (X, expected_labels) = shuffle(X, expected_labels, random_state=rng)
    clust = OPTICS(min_samples=3, min_cluster_size=2, max_eps=20, cluster_method='xi', xi=0.4).fit(X)
    assert_array_equal(clust.labels_, expected_labels)
    X = np.vstack((C1, C2, C3, C4, C5, np.array(([[100, 100]] * 2)), C6))
    expected_labels = np.r_[(([1] * 5), ([3] * 5), ([2] * 5), ([0] * 5), ([2] * 5), (- 1), (- 1), ([4] * 5))]
    (X, expected_labels) = shuffle(X, expected_labels, random_state=rng)
    clust = OPTICS(min_samples=3, min_cluster_size=3, max_eps=20, cluster_method='xi', xi=0.3).fit(X)
    assert_array_equal(clust.labels_, expected_labels)
    C1 = [[0, 0], [0, 0.1], [0, (- 0.1)], [0.1, 0]]
    C2 = [[10, 10], [10, 9], [10, 11], [9, 10]]
    C3 = [[100, 100], [100, 90], [100, 110], [90, 100]]
    X = np.vstack((C1, C2, C3))
    expected_labels = np.r_[(([0] * 4), ([1] * 4), ([2] * 4))]
    (X, expected_labels) = shuffle(X, expected_labels, random_state=rng)
    clust = OPTICS(min_samples=2, min_cluster_size=2, max_eps=np.inf, cluster_method='xi', xi=0.04).fit(X)
    assert_array_equal(clust.labels_, expected_labels)
