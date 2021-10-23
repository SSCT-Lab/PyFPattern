def test_tan():
    a = tan(interval(0, (np.pi / 4)))
    assert (a.start == 0)
    assert (a.end == np.tan((np.pi / 4)))
    a = tan(interval((np.pi / 4), ((3 * np.pi) / 4)))
    assert (a.is_valid is None)