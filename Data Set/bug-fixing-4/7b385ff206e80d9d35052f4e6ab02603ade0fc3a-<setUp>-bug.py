def setUp(self):
    self.op_type = 'modified_huber_loss'
    samples_num = 32
    self.inputs = {
        'X': np.random.uniform((- 1), 1.0, (samples_num, 1)).astype('float32'),
        'Y': np.random.choice([0, 1], samples_num).reshape((samples_num, 1)),
    }
    product_res = (self.inputs['X'] * ((2 * self.inputs['Y']) - 1))
    loss = np.vectorize(modified_huber_loss_forward)(product_res)
    self.outputs = {
        'IntermediateVal': product_res,
        'Out': loss.reshape((samples_num, 1)),
    }