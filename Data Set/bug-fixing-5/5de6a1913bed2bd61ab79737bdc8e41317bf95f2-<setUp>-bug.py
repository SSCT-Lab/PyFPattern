def setUp(self):
    self.op_type = 'bilinear_tensor_product'
    batch_size = 6
    size0 = 30
    size1 = 20
    size2 = 100
    a = np.random.random((batch_size, size0)).astype('float64')
    b = np.random.random((batch_size, size1)).astype('float64')
    w = np.random.random((size2, size0, size1)).astype('float64')
    bias = np.random.random((1, size2)).astype('float64')
    output = np.zeros((batch_size, size2)).astype('float64')
    for i in range(size2):
        w_i = w[i, :, :]
        output[:, i] = np.sum((np.matmul(a, w_i) * b), axis=1)
    self.inputs = {
        'X': a,
        'Y': b,
        'Weight': w,
        'Bias': bias,
    }
    self.outputs = {
        'Out': (output + bias),
    }