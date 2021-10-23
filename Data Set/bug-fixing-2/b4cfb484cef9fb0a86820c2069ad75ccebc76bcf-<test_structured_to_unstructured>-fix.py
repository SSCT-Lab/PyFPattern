

def test_structured_to_unstructured(self):
    a = np.zeros(4, dtype=[('a', 'i4'), ('b', 'f4,u2'), ('c', 'f4', 2)])
    out = structured_to_unstructured(a)
    assert_equal(out, np.zeros((4, 5), dtype='f8'))
    b = np.array([(1, 2, 5), (4, 5, 7), (7, 8, 11), (10, 11, 12)], dtype=[('x', 'i4'), ('y', 'f4'), ('z', 'f8')])
    out = np.mean(structured_to_unstructured(b[['x', 'z']]), axis=(- 1))
    assert_equal(out, np.array([3.0, 5.5, 9.0, 11.0]))
    c = np.arange(20).reshape((4, 5))
    out = unstructured_to_structured(c, a.dtype)
    want = np.array([(0, (1.0, 2), [3.0, 4.0]), (5, (6.0, 7), [8.0, 9.0]), (10, (11.0, 12), [13.0, 14.0]), (15, (16.0, 17), [18.0, 19.0])], dtype=[('a', 'i4'), ('b', [('f0', 'f4'), ('f1', 'u2')]), ('c', 'f4', (2,))])
    assert_equal(out, want)
    d = np.array([(1, 2, 5), (4, 5, 7), (7, 8, 11), (10, 11, 12)], dtype=[('x', 'i4'), ('y', 'f4'), ('z', 'f8')])
    assert_equal(apply_along_fields(np.mean, d), np.array([(8.0 / 3), (16.0 / 3), (26.0 / 3), 11.0]))
    assert_equal(apply_along_fields(np.mean, d[['x', 'z']]), np.array([3.0, 5.5, 9.0, 11.0]))
    d = np.array([(1, 2, 5), (4, 5, 7), (7, 8, 11), (10, 11, 12)], dtype=[('x', 'i4'), ('y', 'i4'), ('z', 'i4')])
    dd = structured_to_unstructured(d)
    ddd = unstructured_to_structured(dd, d.dtype)
    assert_((dd.base is d))
    assert_((ddd.base is d))
    point = np.dtype([('x', int), ('y', int)])
    triangle = np.dtype([('a', point), ('b', point), ('c', point)])
    arr = np.zeros(10, triangle)
    res = structured_to_unstructured(arr, dtype=int)
    assert_equal(res, np.zeros((10, 6), dtype=int))
