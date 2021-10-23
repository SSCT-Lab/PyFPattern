def test_k_and_radius_neighbors_X_None():
    for algorithm in ALGORITHMS:
        nn = neighbors.NearestNeighbors(n_neighbors=1, algorithm=algorithm)
        X = [[0], [1]]
        nn.fit(X)
        (dist, ind) = nn.kneighbors()
        assert_array_equal(dist, [[1], [1]])
        assert_array_equal(ind, [[1], [0]])
        (dist, ind) = nn.radius_neighbors(None, radius=1.5)
        check_object_arrays(dist, [[1], [1]])
        check_object_arrays(ind, [[1], [0]])
        rng = nn.radius_neighbors_graph(None, radius=1.5)
        kng = nn.kneighbors_graph(None)
        for graph in [rng, kng]:
            assert_array_equal(rng.A, [[0, 1], [1, 0]])
            assert_array_equal(rng.data, [1, 1])
            assert_array_equal(rng.indices, [1, 0])
        X = [[0, 1], [0, 1], [1, 1]]
        nn = neighbors.NearestNeighbors(n_neighbors=2, algorithm=algorithm)
        nn.fit(X)
        assert_array_equal(nn.kneighbors_graph().A, np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0]]))