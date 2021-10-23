def test_append_many(self, sort, float_frame):
    chunks = [float_frame[:5], float_frame[5:10], float_frame[10:15], float_frame[15:]]
    result = chunks[0].append(chunks[1:])
    tm.assert_frame_equal(result, float_frame)
    chunks[(- 1)] = chunks[(- 1)].copy()
    chunks[(- 1)]['foo'] = 'bar'
    result = chunks[0].append(chunks[1:], sort=sort)
    tm.assert_frame_equal(result.loc[:, float_frame.columns], float_frame)
    assert (result['foo'][15:] == 'bar').all()
    assert result['foo'][:15].isna().all()