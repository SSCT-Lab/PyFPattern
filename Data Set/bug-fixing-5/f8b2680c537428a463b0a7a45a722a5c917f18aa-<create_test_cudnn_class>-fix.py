def create_test_cudnn_class(parent):

    @unittest.skipIf((not core.is_compiled_with_cuda()), 'core is not compiled with CUDA')
    class TestCUDNNCase(parent):

        def init_kernel_type(self):
            self.use_cudnn = True
    cls_name = '{0}_{1}'.format(parent.__name__, 'CUDNN')
    TestCUDNNCase.__name__ = cls_name
    globals()[cls_name] = TestCUDNNCase