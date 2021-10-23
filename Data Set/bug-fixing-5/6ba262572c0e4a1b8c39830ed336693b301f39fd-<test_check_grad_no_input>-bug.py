def test_check_grad_no_input(self):
    if (self.dtype == np.float16):
        return
    if self.use_cudnn:
        place = core.CUDAPlace(0)
        self.check_grad_with_place(place, ['Filter'], 'Output', max_relative_error=0.02, no_grad_set=set(['Input']))
    else:
        self.check_grad(['Filter'], 'Output', max_relative_error=0.02, no_grad_set=set(['Input']))