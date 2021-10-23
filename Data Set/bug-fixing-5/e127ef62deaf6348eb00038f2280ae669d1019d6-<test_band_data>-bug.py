def test_band_data(self):
    pam_file = (self.rs_path + '.aux.xml')
    self.assertEqual(self.band.width, 163)
    self.assertEqual(self.band.height, 174)
    self.assertEqual(self.band.description, '')
    self.assertEqual(self.band.datatype(), 1)
    self.assertEqual(self.band.datatype(as_string=True), 'GDT_Byte')
    self.assertEqual(self.band.color_interp(), 1)
    self.assertEqual(self.band.color_interp(as_string=True), 'GCI_GrayIndex')
    self.assertEqual(self.band.nodata_value, 15)
    if numpy:
        data = self.band.data()
        assert_array = numpy.loadtxt(os.path.join(os.path.dirname(__file__), '../data/rasters/raster.numpy.txt'))
        numpy.testing.assert_equal(data, assert_array)
        self.assertEqual(data.shape, (self.band.height, self.band.width))
    try:
        (smin, smax, smean, sstd) = self.band.statistics(approximate=True)
        self.assertEqual(smin, 0)
        self.assertEqual(smax, 9)
        self.assertAlmostEqual(smean, 2.842331288343558)
        self.assertAlmostEqual(sstd, 2.3965567248965356)
        (smin, smax, smean, sstd) = self.band.statistics(approximate=False, refresh=True)
        self.assertEqual(smin, 0)
        self.assertEqual(smax, 9)
        self.assertAlmostEqual(smean, 2.828326634228898)
        self.assertAlmostEqual(sstd, 2.4260526986669095)
        self.assertEqual(self.band.min, 0)
        self.assertEqual(self.band.max, 9)
        self.assertAlmostEqual(self.band.mean, 2.828326634228898)
        self.assertAlmostEqual(self.band.std, 2.4260526986669095)
        self.band = None
        self.assertTrue(os.path.isfile(pam_file))
    finally:
        self.band = None
        if os.path.isfile(pam_file):
            os.remove(pam_file)