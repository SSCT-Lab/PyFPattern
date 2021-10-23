@pytest.mark.parametrize('query, expected', [([1, 2], (Int64Index([0, 1, 0, 1, 2], dtype='int64'), np.array([]))), ([1, 2, 3], (Int64Index([0, 1, 0, 1, 2, 2], dtype='int64'), np.array([]))), ([1, 2, 3, 4], (Int64Index([0, 1, 0, 1, 2, 2, (- 1)], dtype='int64'), np.array([3]))), ([1, 2, 3, 4, 2], (Int64Index([0, 1, 0, 1, 2, 2, (- 1), 0, 1, 2], dtype='int64'), np.array([3])))])
def test_get_indexer_non_unique_with_ints_and_floats_multiple_queries(self, query, expected):
    index = IntervalIndex.from_tuples([(0, 2.5), (1, 3), (2, 4)], closed='left')
    result = index.get_indexer_non_unique(query)
    tm.assert_numpy_array_equal(result, expected)