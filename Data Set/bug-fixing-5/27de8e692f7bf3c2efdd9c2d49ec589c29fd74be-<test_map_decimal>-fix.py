def test_map_decimal(self, string_series):
    from decimal import Decimal
    result = string_series.map((lambda x: Decimal(str(x))))
    assert (result.dtype == np.object_)
    assert isinstance(result[0], Decimal)