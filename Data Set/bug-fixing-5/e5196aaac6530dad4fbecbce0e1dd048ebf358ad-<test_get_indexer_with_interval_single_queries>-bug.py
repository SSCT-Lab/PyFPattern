@pytest.mark.parametrize('query', [Interval(1, 3, closed='right'), Interval(1, 3, closed='left'), Interval(1, 3, closed='both'), Interval(1, 3, closed='neither'), Interval(1, 4, closed='right'), Interval(0, 4, closed='right'), Interval(1, 2, closed='right')])
@pytest.mark.parametrize('expected_result', [1, (- 1), (- 1), (- 1), (- 1), (- 1), (- 1)])
def test_get_indexer_with_interval_single_queries(self, query, expected_result):
    index = IntervalIndex.from_tuples([(0, 2.5), (1, 3), (2, 4)], closed='right')
    result = index.get_indexer([query])
    expect = np.array([expected_result], dtype='intp')
    tm.assert_numpy_array_equal(result, expect)