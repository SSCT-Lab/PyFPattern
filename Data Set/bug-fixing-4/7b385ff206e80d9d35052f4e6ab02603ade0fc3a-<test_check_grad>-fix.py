def test_check_grad(self):
    self.check_grad(['X'], 'Out', max_relative_error=0.01)