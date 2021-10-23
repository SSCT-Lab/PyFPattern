def test_applymap(self, float_frame):
    applied = float_frame.applymap((lambda x: (x * 2)))
    tm.assert_frame_equal(applied, (float_frame * 2))
    float_frame.applymap(type)
    result = float_frame.applymap((lambda x: (x, x)))
    assert isinstance(result['A'][0], tuple)
    df = DataFrame(data=[1, 'a'])
    result = df.applymap((lambda x: x))
    assert (result.dtypes[0] == object)
    df = DataFrame(data=[1.0, 'a'])
    result = df.applymap((lambda x: x))
    assert (result.dtypes[0] == object)
    df = DataFrame(np.random.random((3, 4)))
    df2 = df.copy()
    cols = ['a', 'a', 'a', 'a']
    df.columns = cols
    expected = df2.applymap(str)
    expected.columns = cols
    result = df.applymap(str)
    tm.assert_frame_equal(result, expected)
    df['datetime'] = Timestamp('20130101')
    df['timedelta'] = pd.Timedelta('1 min')
    result = df.applymap(str)
    for f in ['datetime', 'timedelta']:
        assert (result.loc[(0, f)] == str(df.loc[(0, f)]))
    empty_frames = [pd.DataFrame(), pd.DataFrame(columns=list('ABC')), pd.DataFrame(index=list('ABC')), pd.DataFrame({
        'A': [],
        'B': [],
        'C': [],
    })]
    for frame in empty_frames:
        for func in [round, (lambda x: x)]:
            result = frame.applymap(func)
            tm.assert_frame_equal(result, frame)