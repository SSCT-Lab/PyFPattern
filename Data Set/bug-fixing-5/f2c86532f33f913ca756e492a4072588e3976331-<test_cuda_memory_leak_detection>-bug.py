def test_cuda_memory_leak_detection(self):
    l = []

    @self.wrap_with_cuda_memory_check
    def no_leak():
        pass

    @self.wrap_with_cuda_memory_check
    def leak_gpu0():
        l.append(torch.tensor(10, device=torch.device('cuda:0')))
    no_leak()
    with self.assertRaisesRegex(AssertionError, 'leaked \\d+ bytes CUDA memory on device 0'):
        leak_gpu0()
    if TEST_MULTIGPU:

        @self.wrap_with_cuda_memory_check
        def leak_gpu1():
            l.append(torch.tensor(10, device=torch.device('cuda:1')))
        with self.assertRaisesRegex(AssertionError, 'leaked \\d+ bytes CUDA memory on device 1'):
            leak_gpu1()