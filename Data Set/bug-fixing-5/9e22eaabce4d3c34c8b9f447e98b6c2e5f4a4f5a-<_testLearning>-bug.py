def _testLearning(self, use_gradient_checker):
    x_shape = [2, 2, 6, 2]
    scale_shape = [2]
    x_val = np.random.random_sample(x_shape).astype(np.float32)
    scale_val = np.random.random_sample(scale_shape).astype(np.float32)
    offset_val = np.random.random_sample(scale_shape).astype(np.float32)
    mean_val = np.random.random_sample(scale_shape).astype(np.float32)
    var_val = np.random.random_sample(scale_shape).astype(np.float32)
    data_format = 'NHWC'
    with self.test_session() as sess, self.test_scope():
        t_val = array_ops.placeholder(np.float32, shape=x_shape, name='x')
        scale = array_ops.placeholder(np.float32, shape=[2], name='scale')
        offset = array_ops.placeholder(np.float32, shape=[2], name='offset')
        epsilon = 0.001
        (y, mean, var) = nn.fused_batch_norm(t_val, scale, offset, mean=None, variance=None, epsilon=epsilon, data_format=data_format, is_training=True)
        if use_gradient_checker:
            err = gradient_checker.compute_gradient_error(t_val, x_shape, y, x_shape, extra_feed_dict={
                t_val: x_val,
                scale: scale_val,
                offset: offset_val,
            })
            self.assertLess(err, 0.001)
        (y_val, mean_val, var_val) = sess.run([y, mean, var], {
            t_val: x_val,
            scale: scale_val,
            offset: offset_val,
        })
        (y_ref, mean_ref, var_ref) = self._reference_training(x_val, scale_val, offset_val, epsilon, data_format)
        self.assertAllClose(mean_val, mean_ref, atol=0.001)
        self.assertAllClose(y_val, y_ref, atol=0.001)
        self.assertAllClose(var_val, var_ref, atol=0.001)