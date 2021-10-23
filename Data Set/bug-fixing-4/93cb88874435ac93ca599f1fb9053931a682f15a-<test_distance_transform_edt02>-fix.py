def test_distance_transform_edt02(self):
    for type_ in self.types:
        data = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], type_)
        (tdt, tft) = ndimage.distance_transform_edt(data, return_indices=True)
        dts = []
        fts = []
        dt = numpy.zeros(data.shape, dtype=numpy.float64)
        ndimage.distance_transform_edt(data, distances=dt)
        dts.append(dt)
        ft = ndimage.distance_transform_edt(data, return_distances=0, return_indices=True)
        fts.append(ft)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        ndimage.distance_transform_edt(data, return_distances=False, return_indices=True, indices=ft)
        fts.append(ft)
        (dt, ft) = ndimage.distance_transform_edt(data, return_indices=True)
        dts.append(dt)
        fts.append(ft)
        dt = numpy.zeros(data.shape, dtype=numpy.float64)
        ft = ndimage.distance_transform_edt(data, distances=dt, return_indices=True)
        dts.append(dt)
        fts.append(ft)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        dt = ndimage.distance_transform_edt(data, return_indices=True, indices=ft)
        dts.append(dt)
        fts.append(ft)
        dt = numpy.zeros(data.shape, dtype=numpy.float64)
        ft = numpy.indices(data.shape, dtype=numpy.int32)
        ndimage.distance_transform_edt(data, distances=dt, return_indices=True, indices=ft)
        dts.append(dt)
        fts.append(ft)
        for dt in dts:
            assert_array_almost_equal(tdt, dt)
        for ft in fts:
            assert_array_almost_equal(tft, ft)