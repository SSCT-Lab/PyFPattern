def test_join_index(float_frame):
    f = float_frame.loc[(float_frame.index[:10], ['A', 'B'])]
    f2 = float_frame.loc[(float_frame.index[5:], ['C', 'D'])].iloc[::(- 1)]
    joined = f.join(f2)
    tm.assert_index_equal(f.index, joined.index)
    expected_columns = Index(['A', 'B', 'C', 'D'])
    tm.assert_index_equal(joined.columns, expected_columns)
    joined = f.join(f2, how='left')
    tm.assert_index_equal(joined.index, f.index)
    tm.assert_index_equal(joined.columns, expected_columns)
    joined = f.join(f2, how='right')
    tm.assert_index_equal(joined.index, f2.index)
    tm.assert_index_equal(joined.columns, expected_columns)
    joined = f.join(f2, how='inner')
    tm.assert_index_equal(joined.index, f.index[5:10])
    tm.assert_index_equal(joined.columns, expected_columns)
    joined = f.join(f2, how='outer')
    tm.assert_index_equal(joined.index, float_frame.index.sort_values())
    tm.assert_index_equal(joined.columns, expected_columns)
    with pytest.raises(ValueError, match='join method'):
        f.join(f2, how='foo')
    msg = 'columns overlap but no suffix'
    for how in ('outer', 'left', 'inner'):
        with pytest.raises(ValueError, match=msg):
            float_frame.join(float_frame, how=how)