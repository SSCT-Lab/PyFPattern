def test_basic(self):
    (x, i, v) = self._gen_sparse(3, 10, 100)
    self.assertEqual(i, x.indices())
    self.assertEqual(v, x.values())
    (x, i, v) = self._gen_sparse(3, 10, [100, 100, 100])
    self.assertEqual(i, x.indices())
    self.assertEqual(v, x.values())
    self.assertEqual(x.ndimension(), 3)
    self.assertEqual(x.coalesce().nnz(), 10)
    for i in range(3):
        self.assertEqual(x.size(i), 100)
    x = self.SparseTensor()
    self.assertEqual(x.indices().numel(), 0)
    self.assertEqual(x.values().numel(), 0)