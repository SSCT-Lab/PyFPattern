def test_project_and_cluster():
    model = SpectralBiclustering(random_state=0)
    data = np.array([[1, 1, 1], [1, 1, 1], [3, 6, 3], [3, 6, 3]])
    vectors = np.array([[1, 0], [0, 1], [0, 0]])
    for mat in (data, csr_matrix(data)):
        labels = model._project_and_cluster(data, vectors, n_clusters=2)
        assert_array_equal(labels, [0, 0, 1, 1])