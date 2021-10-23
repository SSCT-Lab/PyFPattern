

def test_numpy():
    from sympy.utilities.pytest import skip
    np = import_module('numpy')

    def equal(x, y):
        return ((x == y) and (type(x) == type(y)))
    if (not np):
        skip('numpy not installed.Abort numpy tests.')
    assert (sympify(np.bool_(1)) is S(True))
    assert equal(sympify(np.int_(1234567891234567891)), S(1234567891234567891))
    assert equal(sympify(np.intc(1234567891)), S(1234567891))
    assert equal(sympify(np.intp(1234567891234567891)), S(1234567891234567891))
    assert equal(sympify(np.int8((- 123))), S((- 123)))
    assert equal(sympify(np.int16((- 12345))), S((- 12345)))
    assert equal(sympify(np.int32((- 1234567891))), S((- 1234567891)))
    assert equal(sympify(np.int64((- 1234567891234567891))), S((- 1234567891234567891)))
    assert equal(sympify(np.uint8(123)), S(123))
    assert equal(sympify(np.uint16(12345)), S(12345))
    assert equal(sympify(np.uint32(1234567891)), S(1234567891))
    assert equal(sympify(np.uint64(1234567891234567891)), S(1234567891234567891))
    assert equal(sympify(np.float32(1.123456)), Float(1.123456, precision=24))
    assert equal(sympify(np.float64(1.1234567891234)), Float(1.1234567891234, precision=53))
    assert equal(sympify(np.longdouble(1.123456789)), Float(1.123456789, precision=80))
    assert equal(sympify(np.complex64((1 + 2j))), S((1.0 + (2.0 * I))))
    assert equal(sympify(np.complex128((1 + 2j))), S((1.0 + (2.0 * I))))
    assert equal(sympify(np.longcomplex((1 + 2j))), S((1.0 + (2.0 * I))))
    try:
        assert equal(sympify(np.float96(1.123456789)), Float(1.123456789, precision=80))
    except AttributeError:
        pass
    try:
        assert equal(sympify(np.float128(1.123456789123)), Float(1.123456789123, precision=80))
    except AttributeError:
        pass
