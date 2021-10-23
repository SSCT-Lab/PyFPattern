def test_append_many(self):
    pieces = [self.ts[:5], self.ts[5:10], self.ts[10:]]
    result = pieces[0].append(pieces[1:])
    assert_series_equal(result, self.ts)