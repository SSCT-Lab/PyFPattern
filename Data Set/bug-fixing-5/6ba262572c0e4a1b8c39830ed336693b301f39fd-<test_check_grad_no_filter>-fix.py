def test_check_grad_no_filter(self):
    if (self.dtype == np.float16):
        return
    if self.testcudnn():
        place = core.CUDAPlace(0)
        self.check_grad_with_place(place, ['Input'], 'Output', max_relative_error=0.02, no_grad_set=set(['Filter']))
    else:
        self.check_grad(['Input'], 'Output', max_relative_error=0.02, no_grad_set=set(['Filter']))