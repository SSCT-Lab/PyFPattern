@pytest.mark.parametrize('query, expected', [((- 0.5), (- 1)), (0, (- 1)), (0.5, 0), (1, 0), (1.5, 1), (2, 1), (2.5, (- 1)), (3, (- 1)), (3.5, 2), (4, 2), (4.5, (- 1))])
def test_get_indexer_with_ints_and_floats_single_queries(self, query, expected):
    index = IntervalIndex.from_tuples([(0, 1), (1, 2), (3, 4)], closed='right')
    result = index.get_indexer([query])
    expected = np.array([expected], dtype='intp')
    tm.assert_numpy_array_equal(result, expected)