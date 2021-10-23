def test_unsortable(self):
    arr = np.array([1, 2, datetime.now(), 0, 3], dtype=object)
    if (compat.PY2 and (not pd._np_version_under1p10)):
        with tm.assert_produces_warning(RuntimeWarning):
            pytest.raises(TypeError, algos.safe_sort, arr)
    else:
        pytest.raises(TypeError, algos.safe_sort, arr)