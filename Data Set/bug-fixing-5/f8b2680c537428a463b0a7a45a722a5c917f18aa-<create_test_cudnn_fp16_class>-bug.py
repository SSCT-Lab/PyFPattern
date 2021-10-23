def create_test_cudnn_fp16_class(parent, cls_name, grad_check=True):

    @unittest.skipIf((not core.is_compiled_with_cuda()), 'core is not compiled with CUDA')
    class TestConv2DCUDNNFp16(parent):

        def init_kernel_type(self):
            self.use_cudnn = True
            self.dtype = np.float16

        def test_check_output(self):
            if core.is_compiled_with_cuda():
                place = core.CUDAPlace(0)
                if core.is_float16_supported(place):
                    self.check_output_with_place(place, atol=0.02)

        def test_check_grad_no_filter(self):
            place = core.CUDAPlace(0)
            if (core.is_float16_supported(place) and grad_check):
                self.check_grad_with_place(place, ['Input'], 'Output', max_relative_error=0.02, no_grad_set=set(['Filter']))

        def test_check_grad_no_input(self):
            place = core.CUDAPlace(0)
            if (core.is_float16_supported(place) and grad_check):
                self.check_grad_with_place(place, ['Filter'], 'Output', max_relative_error=0.02, no_grad_set=set(['Input']))
    cls_name = '{0}'.format(cls_name)
    TestConv2DCUDNNFp16.__name__ = cls_name
    globals()[cls_name] = TestConv2DCUDNNFp16