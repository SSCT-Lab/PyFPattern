def test_constructor_series_copy(self, float_frame):
    series = float_frame._series
    df = DataFrame({
        'A': series['A'],
    })
    df['A'][:] = 5
    assert (not (series['A'] == 5).all())