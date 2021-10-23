

def test_seresnext_with_fused_all_reduce(self):
    check_func_1 = _get_origin_result
    check_func_2 = partial(self.check_network_convergence, optimizer=optimizer, fuse_all_reduce_ops=True)
    self._compare_result_with_origin_model(check_func_1, check_func_2, use_cuda=False, rm_drop_out=True, rm_bn=True)
    self._compare_result_with_origin_model(check_func_1, check_func_2, use_cuda=True, rm_drop_out=True, rm_bn=True, delta2=0.001)
