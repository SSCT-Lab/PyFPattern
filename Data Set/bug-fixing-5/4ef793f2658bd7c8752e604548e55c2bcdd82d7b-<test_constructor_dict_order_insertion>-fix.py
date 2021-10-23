@pytest.mark.skipif((not PY36), reason='Insertion order for Python>=3.6')
def test_constructor_dict_order_insertion(self):
    datetime_series = tm.makeTimeSeries(nper=30)
    datetime_series_short = tm.makeTimeSeries(nper=25)
    d = {
        'b': datetime_series_short,
        'a': datetime_series,
    }
    frame = DataFrame(data=d)
    expected = DataFrame(data=d, columns=list('ba'))
    tm.assert_frame_equal(frame, expected)