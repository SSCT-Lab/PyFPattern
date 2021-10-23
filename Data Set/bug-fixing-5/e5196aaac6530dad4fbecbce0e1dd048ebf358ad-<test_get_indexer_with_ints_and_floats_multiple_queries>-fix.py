@pytest.mark.parametrize('query, expected', [([1, 2], [0, 1]), ([1, 2, 3], [0, 1, (- 1)]), ([1, 2, 3, 4], [0, 1, (- 1), 2]), ([1, 2, 3, 4, 2], [0, 1, (- 1), 2, 1])])
def test_get_indexer_with_ints_and_floats_multiple_queries(self, query, expected):
    index = IntervalIndex.from_tuples([(0, 1), (1, 2), (3, 4)], closed='right')
    result = index.get_indexer(query)
    expected = np.array(expected, dtype='intp')
    tm.assert_numpy_array_equal(result, expected)
    index = IntervalIndex.from_tuples([(0, 2), (1, 3), (2, 4)])