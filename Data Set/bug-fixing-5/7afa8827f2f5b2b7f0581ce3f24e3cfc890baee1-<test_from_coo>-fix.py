def test_from_coo(self):
    sparse = pytest.importorskip('scipy.sparse')
    row = [0, 3, 1, 0]
    col = [0, 3, 1, 2]
    data = [4, 5, 7, 9]
    sp_array = sparse.coo_matrix((data, (row, col)))
    result = pd.Series.sparse.from_coo(sp_array)
    index = pd.MultiIndex.from_arrays([[0, 0, 1, 3], [0, 2, 1, 3]])
    expected = pd.Series([4, 9, 7, 5], index=index, dtype='Sparse[int]')
    tm.assert_series_equal(result, expected)