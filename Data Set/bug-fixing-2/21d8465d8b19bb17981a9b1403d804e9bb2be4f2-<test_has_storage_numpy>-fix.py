

@unittest.skipIf((not TEST_NUMPY), 'Numpy not found')
def test_has_storage_numpy(self):
    for dtype in [np.float32, np.float64, np.int64, np.int32, np.int16, np.uint8]:
        arr = np.array([1], dtype=dtype)
        self.assertIsNotNone(torch.FloatTensor(arr).storage())
        self.assertIsNotNone(torch.DoubleTensor(arr).storage())
        self.assertIsNotNone(torch.IntTensor(arr).storage())
        self.assertIsNotNone(torch.LongTensor(arr).storage())
        self.assertIsNotNone(torch.ByteTensor(arr).storage())
        if torch.cuda.is_available():
            self.assertIsNotNone(torch.cuda.FloatTensor(arr).storage())
            self.assertIsNotNone(torch.cuda.DoubleTensor(arr).storage())
            self.assertIsNotNone(torch.cuda.IntTensor(arr).storage())
            self.assertIsNotNone(torch.cuda.LongTensor(arr).storage())
            self.assertIsNotNone(torch.cuda.ByteTensor(arr).storage())
