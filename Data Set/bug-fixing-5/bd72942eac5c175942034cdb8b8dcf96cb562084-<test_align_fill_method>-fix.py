@pytest.mark.parametrize('meth', ['pad', 'bfill'])
@pytest.mark.parametrize('ax', [0, 1, None])
@pytest.mark.parametrize('fax', [0, 1])
@pytest.mark.parametrize('how', ['inner', 'outer', 'left', 'right'])
def test_align_fill_method(self, how, meth, ax, fax, float_frame):
    df = float_frame
    self._check_align_fill(df, how, meth, ax, fax)