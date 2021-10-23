def test_filter(self, float_frame, float_string_frame):
    filtered = float_frame.filter(['A', 'B', 'E'])
    assert (len(filtered.columns) == 2)
    assert ('E' not in filtered)
    filtered = float_frame.filter(['A', 'B', 'E'], axis='columns')
    assert (len(filtered.columns) == 2)
    assert ('E' not in filtered)
    idx = float_frame.index[0:4]
    filtered = float_frame.filter(idx, axis='index')
    expected = float_frame.reindex(index=idx)
    tm.assert_frame_equal(filtered, expected)
    fcopy = float_frame.copy()
    fcopy['AA'] = 1
    filtered = fcopy.filter(like='A')
    assert (len(filtered.columns) == 2)
    assert ('AA' in filtered)
    df = DataFrame(0.0, index=[0, 1, 2], columns=[0, 1, '_A', '_B'])
    filtered = df.filter(like='_')
    assert (len(filtered.columns) == 2)
    df = DataFrame(0.0, index=[0, 1, 2], columns=['A1', 1, 'B', 2, 'C'])
    expected = DataFrame(0.0, index=[0, 1, 2], columns=pd.Index([1, 2], dtype=object))
    filtered = df.filter(regex='^[0-9]+$')
    tm.assert_frame_equal(filtered, expected)
    expected = DataFrame(0.0, index=[0, 1, 2], columns=[0, '0', 1, '1'])
    filtered = expected.filter(regex='^[0-9]+$')
    tm.assert_frame_equal(filtered, expected)
    with pytest.raises(TypeError, match='Must pass'):
        float_frame.filter()
    with pytest.raises(TypeError, match='Must pass'):
        float_frame.filter(items=None)
    with pytest.raises(TypeError, match='Must pass'):
        float_frame.filter(axis=1)
    with pytest.raises(TypeError, match='mutually exclusive'):
        float_frame.filter(items=['one', 'three'], regex='e$', like='bbi')
    with pytest.raises(TypeError, match='mutually exclusive'):
        float_frame.filter(items=['one', 'three'], regex='e$', axis=1)
    with pytest.raises(TypeError, match='mutually exclusive'):
        float_frame.filter(items=['one', 'three'], regex='e$')
    with pytest.raises(TypeError, match='mutually exclusive'):
        float_frame.filter(items=['one', 'three'], like='bbi', axis=0)
    with pytest.raises(TypeError, match='mutually exclusive'):
        float_frame.filter(items=['one', 'three'], like='bbi')
    filtered = float_string_frame.filter(like='foo')
    assert ('foo' in filtered)
    df = float_frame.rename(columns={
        'B': '∂',
    })
    filtered = df.filter(like='C')
    assert ('C' in filtered)