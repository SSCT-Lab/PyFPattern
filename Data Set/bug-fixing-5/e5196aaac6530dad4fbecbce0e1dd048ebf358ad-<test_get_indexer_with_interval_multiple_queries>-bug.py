@pytest.mark.parametrize('query', [[Interval(2, 4, closed='right'), Interval(1, 3, closed='right')], [Interval(1, 3, closed='right'), Interval(0, 2, closed='right')], [Interval(1, 3, closed='right'), Interval(1, 3, closed='left')]])
@pytest.mark.parametrize('expected_result', [[2, 1], [1, (- 1)], [1, (- 1)]])
def test_get_indexer_with_interval_multiple_queries(self, query, expected_result):
    index = IntervalIndex.from_tuples([(0, 2.5), (1, 3), (2, 4)], closed='right')
    result = index.get_indexer(query)
    expect = np.array(expected_result, dtype='intp')
    tm.assert_numpy_array_equal(result, expect)