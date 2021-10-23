def create_test_cudnn_class(parent, cls_name):

    @unittest.skipIf((not core.is_compiled_with_cuda()), 'core is not compiled with CUDA')
    class TestCUDNNCase(parent):

        def init_kernel_type(self):
            self.use_cudnn = True
    cls_name = '{0}'.format(cls_name)
    TestCUDNNCase.__name__ = cls_name
    globals()[cls_name] = TestCUDNNCase