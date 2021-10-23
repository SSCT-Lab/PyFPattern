@pytest.mark.skipif(PY2, reason='pytest.raises match regex fails')
def test_unsortable(self):
    arr = np.array([1, 2, datetime.now(), 0, 3], dtype=object)
    msg = "'(<|>)' not supported between instances of ('datetime\\.datetime' and 'int'|'int' and 'datetime\\.datetime')|unorderable types: int\\(\\) > datetime\\.datetime\\(\\)"
    if compat.PY2:
        with warnings.catch_warnings():
            with pytest.raises(TypeError, match=msg):
                safe_sort(arr)
    else:
        with pytest.raises(TypeError, match=msg):
            safe_sort(arr)