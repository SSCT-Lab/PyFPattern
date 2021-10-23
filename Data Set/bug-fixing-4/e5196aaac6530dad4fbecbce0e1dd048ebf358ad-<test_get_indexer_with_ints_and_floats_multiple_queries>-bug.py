@pytest.mark.parametrize('query', [[1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 2]])
@pytest.mark.parametrize('expected_result', [[0, 1], [0, 1, (- 1)], [0, 1, (- 1), 2], [0, 1, (- 1), 2, 1]])
def test_get_indexer_with_ints_and_floats_multiple_queries(self, query, expected_result):
    index = IntervalIndex.from_tuples([(0, 1), (1, 2), (3, 4)], closed='right')
    result = index.get_indexer(query)
    expect = np.array(expected_result, dtype='intp')
    tm.assert_numpy_array_equal(result, expect)
    index = IntervalIndex.from_tuples([(0, 2), (1, 3), (2, 4)])