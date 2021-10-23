def testGradient(self):
    x_shape = [2, 2, 6, 2]
    scale_shape = [2]
    grad_val = np.random.random_sample(x_shape).astype(np.float32)
    x_val = np.random.random_sample(x_shape).astype(np.float32)
    scale_val = np.random.random_sample(scale_shape).astype(np.float32)
    mean_val = np.random.random_sample(scale_shape).astype(np.float32)
    var_val = np.random.random_sample(scale_shape).astype(np.float32)
    epsilon = 0.001
    with self.test_session() as sess, self.test_scope():
        grad = array_ops.placeholder(np.float32, shape=x_shape, name='grad')
        x = array_ops.placeholder(np.float32, shape=x_shape, name='x')
        mean = array_ops.placeholder(np.float32, shape=scale_shape, name='mean')
        var = array_ops.placeholder(np.float32, shape=scale_shape, name='var')
        scale = array_ops.placeholder(np.float32, shape=scale_shape, name='scale')
        (grad_x, grad_scale, grad_offset, _, _) = gen_nn_ops.fused_batch_norm_grad(grad, x, scale, mean, var, data_format='NHWC')
        (grad_x_val, grad_scale_val, grad_offset_val) = sess.run([grad_x, grad_scale, grad_offset], {
            grad: grad_val,
            x: x_val,
            mean: mean_val,
            var: var_val,
            scale: scale_val,
        })
        (grad_x_ref, grad_scale_ref, grad_offset_ref) = self._reference_grad(x_val, grad_val, scale_val, mean_val, var_val, epsilon, 'NHWC')
        self.assertAllClose(grad_x_val, grad_x_ref, atol=0.01)
        self.assertAllClose(grad_scale_val, grad_scale_ref, atol=0.01)
        self.assertAllClose(grad_offset_val, grad_offset_ref, atol=0.001)