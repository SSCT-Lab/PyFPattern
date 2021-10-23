def test_round(self):
    self.ts.index.name = 'index_name'
    result = self.ts.round(2)
    expected = Series(np.round(self.ts.values, 2), index=self.ts.index, name='ts')
    assert_series_equal(result, expected)
    assert (result.name == self.ts.name)