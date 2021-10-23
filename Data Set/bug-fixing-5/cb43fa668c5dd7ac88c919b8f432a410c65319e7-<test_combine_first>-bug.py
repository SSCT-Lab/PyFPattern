def test_combine_first(self):
    (head, tail) = (self.frame[:5], self.frame[5:])
    combined = head.combine_first(tail)
    reordered_frame = self.frame.reindex(combined.index)
    assert_frame_equal(combined, reordered_frame)
    assert tm.equalContents(combined.columns, self.frame.columns)
    assert_series_equal(combined['A'], reordered_frame['A'])
    fcopy = self.frame.copy()
    fcopy['A'] = 1
    del fcopy['C']
    fcopy2 = self.frame.copy()
    fcopy2['B'] = 0
    del fcopy2['D']
    combined = fcopy.combine_first(fcopy2)
    assert (combined['A'] == 1).all()
    assert_series_equal(combined['B'], fcopy['B'])
    assert_series_equal(combined['C'], fcopy2['C'])
    assert_series_equal(combined['D'], fcopy['D'])
    (head, tail) = (reordered_frame[:10].copy(), reordered_frame)
    head['A'] = 1
    combined = head.combine_first(tail)
    assert (combined['A'][:10] == 1).all()
    tail['A'][:10] = 0
    combined = tail.combine_first(head)
    assert (combined['A'][:10] == 0).all()
    f = self.frame[:10]
    g = self.frame[10:]
    combined = f.combine_first(g)
    assert_series_equal(combined['A'].reindex(f.index), f['A'])
    assert_series_equal(combined['A'].reindex(g.index), g['A'])
    comb = self.frame.combine_first(self.empty)
    assert_frame_equal(comb, self.frame)
    comb = self.empty.combine_first(self.frame)
    assert_frame_equal(comb, self.frame)
    comb = self.frame.combine_first(DataFrame(index=['faz', 'boo']))
    assert ('faz' in comb.index)
    df = DataFrame({
        'a': [1],
    }, index=[datetime(2012, 1, 1)])
    df2 = DataFrame({
        
    }, columns=['b'])
    result = df.combine_first(df2)
    assert ('b' in result)