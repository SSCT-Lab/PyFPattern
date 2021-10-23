@pytest.mark.parametrize('op', [np.fft.fftn, np.fft.ifftn, np.fft.rfftn, np.fft.irfftn])
def test_axes(self, op):
    x = random((30, 20, 10))
    axes = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
    for a in axes:
        op_tr = op(np.transpose(x, a))
        tr_op = np.transpose(op(x, axes=a), a)
        assert_allclose(op_tr, tr_op, atol=1e-06)