def create_test_mkldnn_class(parent):

    class TestMKLDNNCase(parent):

        def init_kernel_type(self):
            self.use_mkldnn = True
    cls_name = '{0}_{1}'.format(parent.__name__, 'MKLDNNOp')
    TestMKLDNNCase.__name__ = cls_name
    globals()[cls_name] = TestMKLDNNCase