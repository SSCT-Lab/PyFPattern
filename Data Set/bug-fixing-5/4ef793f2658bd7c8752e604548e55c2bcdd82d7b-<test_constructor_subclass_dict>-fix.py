def test_constructor_subclass_dict(self, float_frame):
    data = {
        'col1': tm.TestSubDict(((x, (10.0 * x)) for x in range(10))),
        'col2': tm.TestSubDict(((x, (20.0 * x)) for x in range(10))),
    }
    df = DataFrame(data)
    refdf = DataFrame({col: dict(val.items()) for (col, val) in data.items()})
    tm.assert_frame_equal(refdf, df)
    data = tm.TestSubDict(data.items())
    df = DataFrame(data)
    tm.assert_frame_equal(refdf, df)
    from collections import defaultdict
    data = {
        
    }
    float_frame['B'][:10] = np.nan
    for (k, v) in float_frame.items():
        dct = defaultdict(dict)
        dct.update(v.to_dict())
        data[k] = dct
    frame = DataFrame(data)
    tm.assert_frame_equal(float_frame.sort_index(), frame)