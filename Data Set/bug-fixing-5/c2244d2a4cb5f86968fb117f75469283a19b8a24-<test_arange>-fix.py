@pytest.mark.skipif((K.backend() == 'cntk'), reason='cntk has issues with negative number.')
def test_arange(self):
    for test_value in ((- 20), 0, 1, 10):
        a_list = []
        dtype_list = []
        for k in WITH_NP:
            t = k.arange(test_value)
            a = k.eval(t)
            assert np.array_equal(a, np.arange(test_value))
            dtype_list.append(k.dtype(t))
            a_list.append(a)
        for i in range((len(a_list) - 1)):
            assert np.array_equal(a_list[i], a_list[(i + 1)])
    for (start, stop, step) in ((0, 5, 1), ((- 5), 5, 2), (0, 1, 2)):
        a_list = []
        for k in WITH_NP:
            a = k.eval(k.arange(start, stop, step))
            assert np.array_equal(a, np.arange(start, stop, step))
            a_list.append(a)
        for i in range((len(a_list) - 1)):
            assert np.array_equal(a_list[i], a_list[(i + 1)])
    for dtype in ('int32', 'int64', 'float32', 'float64'):
        for k in WITH_NP:
            t = k.arange(10, dtype=dtype)
            assert (k.dtype(t) == dtype)
    start = K.constant(1, dtype='int32')
    t = K.arange(start)
    assert (len(K.eval(t)) == 1)
    start = K.constant((- 1), dtype='int32')
    t = K.arange(start)
    assert (len(K.eval(t)) == 0)