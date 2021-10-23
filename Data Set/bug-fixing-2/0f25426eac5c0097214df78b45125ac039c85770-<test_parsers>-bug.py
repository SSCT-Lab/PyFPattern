

def test_parsers(self):
    import dateutil
    yearfirst = (dateutil.__version__ >= LooseVersion('2.5.0'))
    cases = {
        '2011-01-01': datetime(2011, 1, 1),
        '2Q2005': datetime(2005, 4, 1),
        '2Q05': datetime(2005, 4, 1),
        '2005Q1': datetime(2005, 1, 1),
        '05Q1': datetime(2005, 1, 1),
        '2011Q3': datetime(2011, 7, 1),
        '11Q3': datetime(2011, 7, 1),
        '3Q2011': datetime(2011, 7, 1),
        '3Q11': datetime(2011, 7, 1),
        '2000Q4': datetime(2000, 10, 1),
        '00Q4': datetime(2000, 10, 1),
        '4Q2000': datetime(2000, 10, 1),
        '4Q00': datetime(2000, 10, 1),
        '2000q4': datetime(2000, 10, 1),
        '2000-Q4': datetime(2000, 10, 1),
        '00-Q4': datetime(2000, 10, 1),
        '4Q-2000': datetime(2000, 10, 1),
        '4Q-00': datetime(2000, 10, 1),
        '00q4': datetime(2000, 10, 1),
        '2005': datetime(2005, 1, 1),
        '2005-11': datetime(2005, 11, 1),
        '2005 11': datetime(2005, 11, 1),
        '11-2005': datetime(2005, 11, 1),
        '11 2005': datetime(2005, 11, 1),
        '200511': datetime(2020, 5, 11),
        '20051109': datetime(2005, 11, 9),
        '20051109 10:15': datetime(2005, 11, 9, 10, 15),
        '20051109 08H': datetime(2005, 11, 9, 8, 0),
        '2005-11-09 10:15': datetime(2005, 11, 9, 10, 15),
        '2005-11-09 08H': datetime(2005, 11, 9, 8, 0),
        '2005/11/09 10:15': datetime(2005, 11, 9, 10, 15),
        '2005/11/09 08H': datetime(2005, 11, 9, 8, 0),
        'Thu Sep 25 10:36:28 2003': datetime(2003, 9, 25, 10, 36, 28),
        'Thu Sep 25 2003': datetime(2003, 9, 25),
        'Sep 25 2003': datetime(2003, 9, 25),
        'January 1 2014': datetime(2014, 1, 1),
        '2014-06': datetime(2014, 6, 1),
        '06-2014': datetime(2014, 6, 1),
        '2014-6': datetime(2014, 6, 1),
        '6-2014': datetime(2014, 6, 1),
        '20010101 12': datetime(2001, 1, 1, 12),
        '20010101 1234': datetime(2001, 1, 1, 12, 34),
        '20010101 123456': datetime(2001, 1, 1, 12, 34, 56),
    }
    for (date_str, expected) in compat.iteritems(cases):
        (result1, _, _) = tools.parse_time_string(date_str, yearfirst=yearfirst)
        result2 = to_datetime(date_str, yearfirst=yearfirst)
        result3 = to_datetime([date_str], yearfirst=yearfirst)
        result4 = to_datetime(np.array([date_str], dtype=object), yearfirst=yearfirst)
        result6 = DatetimeIndex([date_str], yearfirst=yearfirst)
        result8 = DatetimeIndex(Index([date_str]), yearfirst=yearfirst)
        result9 = DatetimeIndex(Series([date_str]), yearfirst=yearfirst)
        for res in [result1, result2]:
            assert (res == expected)
        for res in [result3, result4, result6, result8, result9]:
            exp = DatetimeIndex([pd.Timestamp(expected)])
            tm.assert_index_equal(res, exp)
        if (not yearfirst):
            result5 = Timestamp(date_str)
            assert (result5 == expected)
            result7 = date_range(date_str, freq='S', periods=1, yearfirst=yearfirst)
            assert (result7 == expected)
    (result1, _, _) = tools.parse_time_string('NaT')
    result2 = to_datetime('NaT')
    result3 = Timestamp('NaT')
    result4 = DatetimeIndex(['NaT'])[0]
    assert (result1 is tslib.NaT)
    assert (result1 is tslib.NaT)
    assert (result1 is tslib.NaT)
    assert (result1 is tslib.NaT)
