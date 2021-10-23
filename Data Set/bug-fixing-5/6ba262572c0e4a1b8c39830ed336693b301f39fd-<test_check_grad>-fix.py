def test_check_grad(self):
    if (self.dtype == np.float16):
        return
    if self.testcudnn():
        place = core.CUDAPlace(0)
        self.check_grad_with_place(place, set(['Input', 'Filter']), 'Output', max_relative_error=0.02)
    else:
        self.check_grad(set(['Input', 'Filter']), 'Output', max_relative_error=0.02)