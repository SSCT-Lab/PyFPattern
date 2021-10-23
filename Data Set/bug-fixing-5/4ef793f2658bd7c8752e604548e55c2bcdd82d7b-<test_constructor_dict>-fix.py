def test_constructor_dict(self):
    datetime_series = tm.makeTimeSeries(nper=30)
    datetime_series_short = tm.makeTimeSeries(nper=30)[5:]
    frame = DataFrame({
        'col1': datetime_series,
        'col2': datetime_series_short,
    })
    assert (len(datetime_series) == 30)
    assert (len(datetime_series_short) == 25)
    tm.assert_series_equal(frame['col1'], datetime_series.rename('col1'))
    exp = pd.Series(np.concatenate([([np.nan] * 5), datetime_series_short.values]), index=datetime_series.index, name='col2')
    tm.assert_series_equal(exp, frame['col2'])
    frame = DataFrame({
        'col1': datetime_series,
        'col2': datetime_series_short,
    }, columns=['col2', 'col3', 'col4'])
    assert (len(frame) == len(datetime_series_short))
    assert ('col1' not in frame)
    assert isna(frame['col3']).all()
    assert (len(DataFrame()) == 0)
    with pytest.raises(ValueError):
        DataFrame({
            'A': {
                'a': 'a',
                'b': 'b',
            },
            'B': ['a', 'b', 'c'],
        })
    frame = DataFrame({
        'A': {
            '1': 1,
            '2': 2,
        },
    })
    tm.assert_index_equal(frame.index, pd.Index(['1', '2']))
    idx = Index([0, 1, 2])
    frame = DataFrame({
        
    }, index=idx)
    assert (frame.index is idx)
    idx = Index([0, 1, 2])
    frame = DataFrame({
        
    }, index=idx, columns=idx)
    assert (frame.index is idx)
    assert (frame.columns is idx)
    assert (len(frame._series) == 3)
    frame = DataFrame({
        'A': [],
        'B': [],
    }, columns=['A', 'B'])
    tm.assert_index_equal(frame.index, Index([], dtype=np.int64))
    frame_none = DataFrame(dict(a=None), index=[0])
    frame_none_list = DataFrame(dict(a=[None]), index=[0])
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        assert (frame_none.get_value(0, 'a') is None)
    with tm.assert_produces_warning(FutureWarning, check_stacklevel=False):
        assert (frame_none_list.get_value(0, 'a') is None)
    tm.assert_frame_equal(frame_none, frame_none_list)
    msg = 'If using all scalar values, you must pass an index'
    with pytest.raises(ValueError, match=msg):
        DataFrame({
            'a': 0.7,
        })
    with pytest.raises(ValueError, match=msg):
        DataFrame({
            'a': 0.7,
        }, columns=['a'])