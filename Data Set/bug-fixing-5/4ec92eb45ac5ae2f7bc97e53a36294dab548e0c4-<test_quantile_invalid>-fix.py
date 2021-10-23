def test_quantile_invalid(self, datetime_frame):
    msg = 'percentiles should all be in the interval \\[0, 1\\]'
    for invalid in [(- 1), 2, [0.5, (- 1)], [0.5, 2]]:
        with pytest.raises(ValueError, match=msg):
            datetime_frame.quantile(invalid)