def _test_gather(self, dim):
    if (not TEST_MULTIGPU):
        raise unittest.SkipTest('only one GPU detected')
    x = torch.randn(2, 5).cuda(0)
    y = torch.randn(2, 5).cuda(1)
    result = comm.gather((x, y), dim)
    expected_size = list(x.size())
    expected_size[dim] += y.size(dim)
    expected_size = torch.Size(expected_size)
    self.assertEqual(result.get_device(), 0)
    self.assertEqual(result.size(), expected_size)
    index = [slice(None, None), slice(None, None)]
    index[dim] = slice(0, x.size(dim))
    self.assertEqual(result[tuple(index)], x)
    index[dim] = slice(x.size(dim), (x.size(dim) + y.size(dim)))
    self.assertEqual(result[tuple(index)], y)