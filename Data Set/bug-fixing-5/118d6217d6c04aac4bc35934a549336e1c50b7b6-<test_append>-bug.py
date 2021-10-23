def test_append(self, sort):
    begin_index = self.frame.index[:5]
    end_index = self.frame.index[5:]
    begin_frame = self.frame.reindex(begin_index)
    end_frame = self.frame.reindex(end_index)
    appended = begin_frame.append(end_frame)
    tm.assert_almost_equal(appended['A'], self.frame['A'])
    del end_frame['A']
    partial_appended = begin_frame.append(end_frame, sort=sort)
    assert ('A' in partial_appended)
    partial_appended = end_frame.append(begin_frame, sort=sort)
    assert ('A' in partial_appended)
    appended = self.mixed_frame[:5].append(self.mixed_frame[5:])
    tm.assert_frame_equal(appended, self.mixed_frame)
    mixed_appended = self.mixed_frame[:5].append(self.frame[5:], sort=sort)
    mixed_appended2 = self.frame[:5].append(self.mixed_frame[5:], sort=sort)
    tm.assert_frame_equal(mixed_appended.reindex(columns=['A', 'B', 'C', 'D']), mixed_appended2.reindex(columns=['A', 'B', 'C', 'D']))
    empty = DataFrame()
    appended = self.frame.append(empty)
    tm.assert_frame_equal(self.frame, appended)
    assert (appended is not self.frame)
    appended = empty.append(self.frame)
    tm.assert_frame_equal(self.frame, appended)
    assert (appended is not self.frame)
    msg = 'Indexes have overlapping values'
    with pytest.raises(ValueError, match=msg):
        self.frame.append(self.frame, verify_integrity=True)
    df = DataFrame({
        'a': {
            'x': 1,
            'y': 2,
        },
        'b': {
            'x': 3,
            'y': 4,
        },
    })
    row = Series([5, 6, 7], index=['a', 'b', 'c'], name='z')
    expected = DataFrame({
        'a': {
            'x': 1,
            'y': 2,
            'z': 5,
        },
        'b': {
            'x': 3,
            'y': 4,
            'z': 6,
        },
        'c': {
            'z': 7,
        },
    })
    result = df.append(row)
    tm.assert_frame_equal(result, expected)