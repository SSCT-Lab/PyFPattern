@pytest.mark.parametrize('query', [(- 0.5), 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
@pytest.mark.parametrize('expected_result', [(- 1), (- 1), 0, 0, 1, 1, (- 1), (- 1), 2, 2, (- 1)])
def test_get_indexer_with_ints_and_floats_single_queries(self, query, expected_result):
    index = IntervalIndex.from_tuples([(0, 1), (1, 2), (3, 4)], closed='right')
    result = index.get_indexer([query])
    expect = np.array([expected_result], dtype='intp')
    tm.assert_numpy_array_equal(result, expect)