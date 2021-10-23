def test_main(self):
    if core.is_compiled_with_cuda():
        self.check_network_convergence(transformer, use_cuda=True)
    self.check_network_convergence(transformer, use_cuda=False, iter=5)