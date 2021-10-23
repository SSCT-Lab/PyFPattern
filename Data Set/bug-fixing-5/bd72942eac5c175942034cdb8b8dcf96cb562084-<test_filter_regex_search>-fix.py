def test_filter_regex_search(self, float_frame):
    fcopy = float_frame.copy()
    fcopy['AA'] = 1
    filtered = fcopy.filter(regex='[A]+')
    assert (len(filtered.columns) == 2)
    assert ('AA' in filtered)
    df = DataFrame({
        'aBBa': [1, 2],
        'BBaBB': [1, 2],
        'aCCa': [1, 2],
        'aCCaBB': [1, 2],
    })
    result = df.filter(regex='BB')
    exp = df[[x for x in df.columns if ('BB' in x)]]
    assert_frame_equal(result, exp)