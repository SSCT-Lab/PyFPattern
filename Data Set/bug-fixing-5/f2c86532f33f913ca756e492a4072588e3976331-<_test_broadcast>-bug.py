def _test_broadcast(self, input):
    if (not TEST_MULTIGPU):
        raise unittest.SkipTest('only one GPU detected')
    result = comm.broadcast(input, (0, 1))
    for (i, t) in enumerate(result):
        self.assertEqual(t.get_device(), i)
        self.assertEqual(t, input)