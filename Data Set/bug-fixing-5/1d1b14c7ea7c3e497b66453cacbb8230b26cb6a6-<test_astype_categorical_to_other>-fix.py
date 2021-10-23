def test_astype_categorical_to_other(self):
    df = DataFrame({
        'value': np.random.randint(0, 10000, 100),
    })
    labels = ['{0} - {1}'.format(i, (i + 499)) for i in range(0, 10000, 500)]
    cat_labels = Categorical(labels, labels)
    df = df.sort_values(by=['value'], ascending=True)
    df['value_group'] = pd.cut(df.value, range(0, 10500, 500), right=False, labels=cat_labels)
    s = df['value_group']
    expected = s
    tm.assert_series_equal(s.astype('category'), expected)
    tm.assert_series_equal(s.astype(CategoricalDtype()), expected)
    msg = 'could not convert string to float|invalid literal for float\\(\\)'
    with pytest.raises(ValueError, match=msg):
        s.astype('float64')
    cat = Series(Categorical(['a', 'b', 'b', 'a', 'a', 'c', 'c', 'c']))
    exp = Series(['a', 'b', 'b', 'a', 'a', 'c', 'c', 'c'])
    tm.assert_series_equal(cat.astype('str'), exp)
    s2 = Series(Categorical(['1', '2', '3', '4']))
    exp2 = Series([1, 2, 3, 4]).astype(int)
    tm.assert_series_equal(s2.astype('int'), exp2)

    def cmp(a, b):
        tm.assert_almost_equal(np.sort(np.unique(a)), np.sort(np.unique(b)))
    expected = Series(np.array(s.values), name='value_group')
    cmp(s.astype('object'), expected)
    cmp(s.astype(np.object_), expected)
    tm.assert_almost_equal(np.array(s), np.array(s.values))
    for valid in [(lambda x: x.astype('category')), (lambda x: x.astype(CategoricalDtype())), (lambda x: x.astype('object').astype('category')), (lambda x: x.astype('object').astype(CategoricalDtype()))]:
        result = valid(s)
        tm.assert_series_equal(result, s, check_categorical=False)
    msg = "invalid type <class 'pandas\\.core\\.arrays\\.categorical\\.Categorical'> for astype"
    for invalid in [(lambda x: x.astype(Categorical)), (lambda x: x.astype('object').astype(Categorical))]:
        with pytest.raises(TypeError, match=msg):
            invalid(s)