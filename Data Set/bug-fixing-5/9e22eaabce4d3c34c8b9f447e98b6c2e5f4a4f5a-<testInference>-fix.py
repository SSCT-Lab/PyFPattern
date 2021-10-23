def testInference(self):
    channel = 3
    x_shape = [2, 2, 6, channel]
    scale_shape = [channel]
    x_val = np.random.random_sample(x_shape).astype(np.float32)
    scale_val = np.random.random_sample(scale_shape).astype(np.float32)
    offset_val = np.random.random_sample(scale_shape).astype(np.float32)
    data_format = 'NHWC'
    with self.test_session() as sess, self.test_scope():
        t_val = array_ops.placeholder(np.float32, shape=x_shape, name='x')
        scale = array_ops.placeholder(np.float32, shape=scale_shape, name='scale')
        offset = array_ops.placeholder(np.float32, shape=scale_shape, name='offset')
        epsilon = 0.001
        (y_ref, mean_ref, var_ref) = self._reference_training(x_val, scale_val, offset_val, epsilon, data_format)
        (y, mean, variance) = nn.fused_batch_norm(t_val, scale, offset, mean=mean_ref, variance=var_ref, epsilon=epsilon, data_format=data_format, is_training=False)
        (y_val, _, _) = sess.run([y, mean, variance], {
            t_val: x_val,
            scale: scale_val,
            offset: offset_val,
        })
        self.assertAllClose(y_val, y_ref, atol=0.001)