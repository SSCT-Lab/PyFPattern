@pytest.mark.parametrize('query', [(- 0.5), 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
@pytest.mark.parametrize('expected_result', [(Int64Index([], dtype='int64'), np.array([0])), (Int64Index([0], dtype='int64'), np.array([])), (Int64Index([0], dtype='int64'), np.array([])), (Int64Index([0, 1], dtype='int64'), np.array([])), (Int64Index([0, 1], dtype='int64'), np.array([])), (Int64Index([0, 1, 2], dtype='int64'), np.array([])), (Int64Index([1, 2], dtype='int64'), np.array([])), (Int64Index([2], dtype='int64'), np.array([])), (Int64Index([2], dtype='int64'), np.array([])), (Int64Index([], dtype='int64'), np.array([0])), (Int64Index([], dtype='int64'), np.array([0]))])
def test_get_indexer_non_unique_with_ints_and_floats_single_queries(self, query, expected_result):
    index = IntervalIndex.from_tuples([(0, 2.5), (1, 3), (2, 4)], closed='left')
    result = index.get_indexer_non_unique([query])
    tm.assert_numpy_array_equal(result, expected_result)