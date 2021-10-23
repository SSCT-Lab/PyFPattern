def test_distance_transform_edt01(self):
    for type_ in self.types:
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], type_)
        (out, ft) = ndimage.distance_transform_edt(data, return_indices=True)
        bf = ndimage.distance_transform_bf(data, 'euclidean')
        assert_array_almost_equal(bf, out)
        dt = (ft - numpy.indices(ft.shape[1:], dtype=ft.dtype))
        dt = dt.astype(numpy.float64)
        numpy.multiply(dt, dt, dt)
        dt = numpy.add.reduce(dt, axis=0)
        numpy.sqrt(dt, dt)
        assert_array_almost_equal(bf, dt)