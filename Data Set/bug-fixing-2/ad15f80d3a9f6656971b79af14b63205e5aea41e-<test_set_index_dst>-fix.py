

def test_set_index_dst(self):
    di = pd.date_range('2006-10-29 00:00:00', periods=3, freq='H', tz='US/Pacific')
    df = pd.DataFrame(data={
        'a': [0, 1, 2],
        'b': [3, 4, 5],
    }, index=di).reset_index()
    res = df.set_index('index')
    exp = pd.DataFrame(data={
        'a': [0, 1, 2],
        'b': [3, 4, 5],
    }, index=pd.Index(di, name='index'))
    tm.assert_frame_equal(res, exp)
    res = df.set_index(['index', 'a'])
    exp_index = pd.MultiIndex.from_arrays([di, [0, 1, 2]], names=['index', 'a'])
    exp = pd.DataFrame({
        'b': [3, 4, 5],
    }, index=exp_index)
    tm.assert_frame_equal(res, exp)
