def test_datetimes(self, engine, ext):
    datetimes = [datetime(2013, 1, 13, 1, 2, 3), datetime(2013, 1, 13, 2, 45, 56), datetime(2013, 1, 13, 4, 29, 49), datetime(2013, 1, 13, 6, 13, 42), datetime(2013, 1, 13, 7, 57, 35), datetime(2013, 1, 13, 9, 41, 28), datetime(2013, 1, 13, 11, 25, 21), datetime(2013, 1, 13, 13, 9, 14), datetime(2013, 1, 13, 14, 53, 7), datetime(2013, 1, 13, 16, 37, 0), datetime(2013, 1, 13, 18, 20, 52)]
    write_frame = DataFrame({
        'A': datetimes,
    })
    write_frame.to_excel(self.path, 'Sheet1')
    read_frame = pd.read_excel(self.path, 'Sheet1', header=0)
    tm.assert_series_equal(write_frame['A'], read_frame['A'])