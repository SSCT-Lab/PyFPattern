@pytest.mark.parametrize('query, expected', [(Interval(1, 3, closed='right'), 1), (Interval(1, 3, closed='left'), (- 1)), (Interval(1, 3, closed='both'), (- 1)), (Interval(1, 3, closed='neither'), (- 1)), (Interval(1, 4, closed='right'), (- 1)), (Interval(0, 4, closed='right'), (- 1)), (Interval(1, 2, closed='right'), (- 1))])
def test_get_indexer_with_interval_single_queries(self, query, expected):
    index = IntervalIndex.from_tuples([(0, 2.5), (1, 3), (2, 4)], closed='right')
    result = index.get_indexer([query])
    expected = np.array([expected], dtype='intp')
    tm.assert_numpy_array_equal(result, expected)