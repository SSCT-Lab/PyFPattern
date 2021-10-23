@pytest.mark.parametrize('op_str,opname', [('/', 'truediv'), ('//', 'floordiv'), ('**', 'pow')])
def test_bool_ops_raise_on_arithmetic(self, op_str, opname):
    df = DataFrame({
        'a': (np.random.rand(10) > 0.5),
        'b': (np.random.rand(10) > 0.5),
    })
    msg = f'operator {repr(op_str)} not implemented for bool dtypes'
    f = getattr(operator, opname)
    err_msg = re.escape(msg)
    with pytest.raises(NotImplementedError, match=err_msg):
        f(df, df)
    with pytest.raises(NotImplementedError, match=err_msg):
        f(df.a, df.b)
    with pytest.raises(NotImplementedError, match=err_msg):
        f(df.a, True)
    with pytest.raises(NotImplementedError, match=err_msg):
        f(False, df.a)
    with pytest.raises(NotImplementedError, match=err_msg):
        f(False, df)
    with pytest.raises(NotImplementedError, match=err_msg):
        f(df, True)