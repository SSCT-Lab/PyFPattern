def test_map_decimal(self):
    from decimal import Decimal
    result = self.series.map((lambda x: Decimal(str(x))))
    assert (result.dtype == np.object_)
    assert isinstance(result[0], Decimal)