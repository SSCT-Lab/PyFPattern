def test_constructor_rec(self, float_frame):
    rec = float_frame.to_records(index=False)
    rec.dtype.names = list(rec.dtype.names)[::(- 1)]
    index = float_frame.index
    df = DataFrame(rec)
    tm.assert_index_equal(df.columns, pd.Index(rec.dtype.names))
    df2 = DataFrame(rec, index=index)
    tm.assert_index_equal(df2.columns, pd.Index(rec.dtype.names))
    tm.assert_index_equal(df2.index, index)
    rng = np.arange(len(rec))[::(- 1)]
    df3 = DataFrame(rec, index=rng, columns=['C', 'B'])
    expected = DataFrame(rec, index=rng).reindex(columns=['C', 'B'])
    tm.assert_frame_equal(df3, expected)