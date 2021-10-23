def test_tan():
    a = tan(interval(0, (np.pi / 4)))
    assert (a.start == 0)
    assert (a.end == (np.sin((np.pi / 4)) / np.cos((np.pi / 4))))
    a = tan(interval((np.pi / 4), ((3 * np.pi) / 4)))
    assert (a.is_valid is None)