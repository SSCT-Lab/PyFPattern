@pytest.mark.parametrize('mapper', [(lambda values, idx: {i: e for (e, i) in zip(values, idx)}), (lambda values, idx: pd.Series(values, idx))])
def test_map_dictlike(idx, mapper):
    if isinstance(idx, (pd.CategoricalIndex, pd.IntervalIndex)):
        pytest.skip(f'skipping tests for {type(idx)}')
    identity = mapper(idx.values, idx)
    if (isinstance(idx, pd.UInt64Index) and isinstance(identity, dict)):
        expected = idx.astype('int64')
    else:
        expected = idx
    result = idx.map(identity)
    tm.assert_index_equal(result, expected)
    expected = pd.Index(([np.nan] * len(idx)))
    result = idx.map(mapper(expected, idx))
    tm.assert_index_equal(result, expected)