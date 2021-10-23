def create_test_mkldnn_use_ceil_class(parent):

    class TestMKLDNNPool2DUseCeilCase(parent):

        def init_kernel_type(self):
            self.use_mkldnn = True

        def init_ceil_mode(self):
            self.ceil_mode = True

        def init_data_type(self):
            self.dtype = np.float32
    cls_name = '{0}_{1}'.format(parent.__name__, 'MKLDNNCeilModeCast')
    TestMKLDNNPool2DUseCeilCase.__name__ = cls_name
    globals()[cls_name] = TestMKLDNNPool2DUseCeilCase