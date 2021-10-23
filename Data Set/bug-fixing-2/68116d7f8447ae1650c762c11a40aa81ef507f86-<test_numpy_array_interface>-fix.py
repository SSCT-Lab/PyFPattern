

@unittest.skipIf((not TEST_NUMPY), 'Numpy not found')
def test_numpy_array_interface(self):
    types = [torch.DoubleTensor, torch.FloatTensor, torch.LongTensor, torch.IntTensor, torch.ShortTensor, torch.ByteTensor]
    dtypes = [np.float64, np.float32, np.int64, np.int32, np.int16, np.uint8]
    for (tp, dtype) in zip(types, dtypes):
        if (np.dtype(dtype).kind == 'u'):
            x = torch.Tensor([1, 2, 3, 4]).type(tp)
            array = np.array([1, 2, 3, 4], dtype=dtype)
        else:
            x = torch.Tensor([1, (- 2), 3, (- 4)]).type(tp)
            array = np.array([1, (- 2), 3, (- 4)], dtype=dtype)
        asarray = np.asarray(x)
        self.assertIsInstance(asarray, np.ndarray)
        self.assertEqual(asarray.dtype, dtype)
        for i in range(len(x)):
            self.assertEqual(asarray[i], x[i])
        abs_x = np.abs(x)
        abs_array = np.abs(array)
        self.assertIsInstance(abs_x, tp)
        for i in range(len(x)):
            self.assertEqual(abs_x[i], abs_array[i])
    for dtype in dtypes:
        x = torch.IntTensor([1, (- 2), 3, (- 4)])
        asarray = np.asarray(x, dtype=dtype)
        self.assertEqual(asarray.dtype, dtype)
        if (np.dtype(dtype).kind == 'u'):
            wrapped_x = np.array([1, (- 2), 3, (- 4)], dtype=dtype)
            for i in range(len(x)):
                self.assertEqual(asarray[i], wrapped_x[i])
        else:
            for i in range(len(x)):
                self.assertEqual(asarray[i], x[i])
    float_types = [torch.DoubleTensor, torch.FloatTensor]
    float_dtypes = [np.float64, np.float32]
    for (tp, dtype) in zip(float_types, float_dtypes):
        x = torch.Tensor([1, 2, 3, 4]).type(tp)
        array = np.array([1, 2, 3, 4], dtype=dtype)
        for func in ['sin', 'sqrt', 'ceil']:
            ufunc = getattr(np, func)
            res_x = ufunc(x)
            res_array = ufunc(array)
            self.assertIsInstance(res_x, tp)
            for i in range(len(x)):
                self.assertEqual(res_x[i], res_array[i])
    for (tp, dtype) in zip(types, dtypes):
        x = torch.Tensor([1, 2, 3, 4]).type(tp)
        array = np.array([1, 2, 3, 4], dtype=dtype)
        geq2_x = np.greater_equal(x, 2)
        geq2_array = np.greater_equal(array, 2).astype('uint8')
        self.assertIsInstance(geq2_x, torch.ByteTensor)
        for i in range(len(x)):
            self.assertEqual(geq2_x[i], geq2_array[i])
