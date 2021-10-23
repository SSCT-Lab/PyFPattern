def _test_scatter(self, input, chunk_sizes=None, dim=0):
    if (not TEST_MULTIGPU):
        raise unittest.SkipTest('only one GPU detected')
    result = comm.scatter(input, (0, 1), chunk_sizes, dim)
    self.assertEqual(len(result), 2)
    if (chunk_sizes is None):
        chunk_sizes = tuple(repeat((input.size(dim) // 2), 2))
    chunk_start = 0
    for (i, r) in enumerate(result):
        chunk_end = (chunk_start + chunk_sizes[i])
        index = [slice(None, None), slice(None, None)]
        index[dim] = slice(chunk_start, chunk_end)
        self.assertEqual(r, input[tuple(index)], 0)
        chunk_start = chunk_end