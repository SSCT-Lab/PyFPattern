def test_main(self):
    if core.is_compiled_with_cuda():
        self.check_network_convergence(transformer, use_cuda=True, memory_opt=True, use_ir_memory_optimize=False)
        self.check_network_convergence(transformer, use_cuda=True, memory_opt=False, use_ir_memory_optimize=True)