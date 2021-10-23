def test_fillna_invalid_method(self, datetime_series):
    try:
        datetime_series.fillna(method='ffil')
    except ValueError as inst:
        assert ('ffil' in str(inst))