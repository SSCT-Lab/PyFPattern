def test_agg_reduce(self, axis, float_frame):
    other_axis = (1 if (axis in {0, 'index'}) else 0)
    (name1, name2) = float_frame.axes[other_axis].unique()[:2].sort_values()
    expected = pd.concat([float_frame.mean(axis=axis), float_frame.max(axis=axis), float_frame.sum(axis=axis)], axis=1)
    expected.columns = ['mean', 'max', 'sum']
    expected = (expected.T if (axis in {0, 'index'}) else expected)
    result = float_frame.agg(['mean', 'max', 'sum'], axis=axis)
    assert_frame_equal(result, expected)
    func = OrderedDict([(name1, 'mean'), (name2, 'sum')])
    result = float_frame.agg(func, axis=axis)
    expected = Series([float_frame.loc(other_axis)[name1].mean(), float_frame.loc(other_axis)[name2].sum()], index=[name1, name2])
    assert_series_equal(result, expected)
    func = OrderedDict([(name1, ['mean']), (name2, ['sum'])])
    result = float_frame.agg(func, axis=axis)
    expected = DataFrame({
        name1: Series([float_frame.loc(other_axis)[name1].mean()], index=['mean']),
        name2: Series([float_frame.loc(other_axis)[name2].sum()], index=['sum']),
    })
    expected = (expected.T if (axis in {1, 'columns'}) else expected)
    assert_frame_equal(result, expected)
    func = OrderedDict([(name1, ['mean', 'sum']), (name2, ['sum', 'max'])])
    result = float_frame.agg(func, axis=axis)
    expected = DataFrame(OrderedDict([(name1, Series([float_frame.loc(other_axis)[name1].mean(), float_frame.loc(other_axis)[name1].sum()], index=['mean', 'sum'])), (name2, Series([float_frame.loc(other_axis)[name2].sum(), float_frame.loc(other_axis)[name2].max()], index=['sum', 'max']))]))
    expected = (expected.T if (axis in {1, 'columns'}) else expected)
    assert_frame_equal(result, expected)