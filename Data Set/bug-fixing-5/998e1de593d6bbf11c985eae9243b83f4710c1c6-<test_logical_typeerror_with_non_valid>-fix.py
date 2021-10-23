@pytest.mark.parametrize('op,res', [('__eq__', False), ('__ne__', True)])
@pytest.mark.filterwarnings('ignore:elementwise:FutureWarning')
def test_logical_typeerror_with_non_valid(self, op, res, float_frame):
    result = getattr(float_frame, op)('foo')
    assert (bool(result.all().all()) is res)