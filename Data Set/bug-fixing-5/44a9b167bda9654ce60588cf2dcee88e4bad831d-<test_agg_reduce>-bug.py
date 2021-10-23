def test_agg_reduce(self, axis):
    other_axis = (1 if (axis in {0, 'index'}) else 0)
    (name1, name2) = self.frame.axes[other_axis].unique()[:2].sort_values()
    expected = pd.concat([self.frame.mean(axis=axis), self.frame.max(axis=axis), self.frame.sum(axis=axis)], axis=1)
    expected.columns = ['mean', 'max', 'sum']
    expected = (expected.T if (axis in {0, 'index'}) else expected)
    result = self.frame.agg(['mean', 'max', 'sum'], axis=axis)
    assert_frame_equal(result, expected)
    func = OrderedDict([(name1, 'mean'), (name2, 'sum')])
    result = self.frame.agg(func, axis=axis)
    expected = Series([self.frame.loc(other_axis)[name1].mean(), self.frame.loc(other_axis)[name2].sum()], index=[name1, name2])
    assert_series_equal(result, expected)
    func = OrderedDict([(name1, ['mean']), (name2, ['sum'])])
    result = self.frame.agg(func, axis=axis)
    expected = DataFrame({
        name1: Series([self.frame.loc(other_axis)[name1].mean()], index=['mean']),
        name2: Series([self.frame.loc(other_axis)[name2].sum()], index=['sum']),
    })
    expected = (expected.T if (axis in {1, 'columns'}) else expected)
    assert_frame_equal(result, expected)
    func = OrderedDict([(name1, ['mean', 'sum']), (name2, ['sum', 'max'])])
    result = self.frame.agg(func, axis=axis)
    expected = DataFrame(OrderedDict([(name1, Series([self.frame.loc(other_axis)[name1].mean(), self.frame.loc(other_axis)[name1].sum()], index=['mean', 'sum'])), (name2, Series([self.frame.loc(other_axis)[name2].sum(), self.frame.loc(other_axis)[name2].max()], index=['sum', 'max']))]))
    expected = (expected.T if (axis in {1, 'columns'}) else expected)
    assert_frame_equal(result, expected)