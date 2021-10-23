@pytest.mark.parametrize('query, expected', [([Interval(2, 4, closed='right'), Interval(1, 3, closed='right')], [2, 1]), ([Interval(1, 3, closed='right'), Interval(0, 2, closed='right')], [1, (- 1)]), ([Interval(1, 3, closed='right'), Interval(1, 3, closed='left')], [1, (- 1)])])
def test_get_indexer_with_interval_multiple_queries(self, query, expected):
    index = IntervalIndex.from_tuples([(0, 2.5), (1, 3), (2, 4)], closed='right')
    result = index.get_indexer(query)
    expected = np.array(expected, dtype='intp')
    tm.assert_numpy_array_equal(result, expected)