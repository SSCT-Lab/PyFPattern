def test_new(self):
    (x, indices, values) = self._gen_sparse(3, 10, 100)
    if (not x.is_cuda):
        self.assertEqual(x.new(indices, values), x)
    self.assertEqual(x.new(indices, values, x.size()), x)
    self.assertIs(torch.sparse.uint8, Variable(x).new(dtype=torch.sparse.uint8).dtype)
    self.assertIs(torch.sparse.uint8, Variable(x).new(1, 2, dtype=torch.sparse.uint8).dtype)