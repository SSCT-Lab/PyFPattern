

def test_quantile_interpolation_int(self, int_frame):
    df = int_frame
    q = df.quantile(0.1)
    assert (q['A'] == np.percentile(df['A'], 10))
    q1 = df.quantile(0.1)
    assert (q1['A'] == np.percentile(df['A'], 10))
    tm.assert_series_equal(q, q1)
