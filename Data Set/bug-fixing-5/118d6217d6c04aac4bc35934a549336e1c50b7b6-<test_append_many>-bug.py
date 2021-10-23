def test_append_many(self, sort):
    chunks = [self.frame[:5], self.frame[5:10], self.frame[10:15], self.frame[15:]]
    result = chunks[0].append(chunks[1:])
    tm.assert_frame_equal(result, self.frame)
    chunks[(- 1)] = chunks[(- 1)].copy()
    chunks[(- 1)]['foo'] = 'bar'
    result = chunks[0].append(chunks[1:], sort=sort)
    tm.assert_frame_equal(result.loc[:, self.frame.columns], self.frame)
    assert (result['foo'][15:] == 'bar').all()
    assert result['foo'][:15].isna().all()