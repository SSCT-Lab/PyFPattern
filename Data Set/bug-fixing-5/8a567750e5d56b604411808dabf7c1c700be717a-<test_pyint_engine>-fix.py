def test_pyint_engine(self):
    N = 5
    keys = [tuple(l) for l in [(([0] * 10) * N), (([1] * 10) * N), (([2] * 10) * N), (([np.nan] * N) + (([2] * 9) * N)), (([0] * N) + (([2] * 9) * N)), ((([np.nan] * N) + (([2] * 8) * N)) + ([0] * N))]]
    for idx in range(len(keys)):
        index = MultiIndex.from_tuples(keys)
        assert (index.get_loc(keys[idx]) == idx)
        expected = np.arange((idx + 1), dtype=np.intp)
        result = index.get_indexer([keys[i] for i in expected])
        tm.assert_numpy_array_equal(result, expected)
    idces = range(len(keys))
    expected = np.array(([(- 1)] + list(idces)), dtype=np.intp)
    missing = tuple((([0, 1] * 5) * N))
    result = index.get_indexer(([missing] + [keys[i] for i in idces]))
    tm.assert_numpy_array_equal(result, expected)