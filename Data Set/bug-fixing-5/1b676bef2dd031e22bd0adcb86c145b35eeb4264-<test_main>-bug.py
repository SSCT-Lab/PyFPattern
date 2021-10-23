def test_main(self):
    self.check_network_convergence(transformer, use_cuda=True)
    self.check_network_convergence(transformer, use_cuda=False, iter=5)