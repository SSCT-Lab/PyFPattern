

@unittest.skipIf((not TEST_NUMPY), 'Numpy not found')
def test_has_storage_numpy(self):
    arr = np.array([], dtype=np.float32)
    self.assertIsNotNone(torch.Tensor(arr).storage())
