def test_band_data(self):
    rs = GDALRaster(self.rs_path)
    band = rs.bands[0]
    self.assertEqual(band.width, 163)
    self.assertEqual(band.height, 174)
    self.assertEqual(band.description, '')
    self.assertEqual(band.datatype(), 1)
    self.assertEqual(band.datatype(as_string=True), 'GDT_Byte')
    self.assertEqual(band.color_interp(), 1)
    self.assertEqual(band.color_interp(as_string=True), 'GCI_GrayIndex')
    self.assertEqual(band.nodata_value, 15)
    if numpy:
        data = band.data()
        assert_array = numpy.loadtxt(os.path.join(os.path.dirname(__file__), '../data/rasters/raster.numpy.txt'))
        numpy.testing.assert_equal(data, assert_array)
        self.assertEqual(data.shape, (band.height, band.width))