def check_forward_backward(self, shape, begin_norm_axis):

    def test_with_place(place, shape, begin_norm_axis=1):
        assert ((begin_norm_axis > 0) and (begin_norm_axis < len(shape))), 'begin_norm_axis must be between 0 and len(shape)-1.'
        epsilon = 1e-05
        x_shape = shape
        D = reduce(mul, x_shape[begin_norm_axis:len(x_shape)], 1)
        scale_shape = [D]
        np.random.random(123)
        x_val = np.random.random_sample(x_shape).astype(np.float32)
        scale_val = np.random.random_sample(scale_shape).astype(np.float32)
        bias_val = np.random.random_sample(scale_shape).astype(np.float32)
        y_grad = np.random.random_sample(x_shape).astype(np.float32)
        (y_out, saved_mean, var_ref) = _reference_layer_norm_naive(x_val, scale_val, bias_val, epsilon, begin_norm_axis)
        naive_fw = {
            'Y': y_out,
            'Mean': saved_mean,
            'Variance': var_ref,
        }
        (x_grad_ref, scale_grad_ref, bias_grad_ref) = _reference_layer_norm_grad(x_val, y_grad, scale_val, saved_mean, var_ref, begin_norm_axis)
        naive_grad = {
            'X': x_grad_ref,
            'Scale': scale_grad_ref,
            'Bias': bias_grad_ref,
        }
        scope = core.Scope()
        input_map = {
            'X': x_val,
            'Scale': scale_val,
            'Bias': bias_val,
        }
        for i_name in input_map:
            create_or_get_tensor(scope, i_name, input_map[i_name], place)
        output_map = {
            'Y': None,
            'Mean': None,
            'Variance': None,
        }
        output_tensor = {
            
        }
        for o_name in output_map:
            output_tensor[o_name] = create_or_get_tensor(scope, o_name, output_map[o_name], place)
        layer_norm_op = Operator('layer_norm', X='X', Scale='Scale', Bias='Bias', Y='Y', Mean='Mean', Variance='Variance', epsilon=epsilon, begin_norm_axis=begin_norm_axis)
        layer_norm_op.run(scope, place)
        atol = (0.05 if isinstance(place, core.CUDAPlace) else 0.0001)
        for o_tensor in output_tensor:
            self.__assert_close(output_tensor[o_tensor], naive_fw[o_tensor], o_tensor, atol)
        layer_norm_op_grad = get_backward_op(scope, layer_norm_op, set())
        set_output_grad(scope, ['Y', 'Mean', 'Variance'], place, feed_dict={
            'Y': y_grad,
        })
        layer_norm_op_grad.run(scope, place)
        grad_tensor = {
            
        }
        for o_name in naive_grad:
            grad_tensor[o_name] = x_ = create_or_get_tensor(scope, grad_var_name(o_name), None, place)
        for o_grad in naive_grad:
            self.__assert_grad_close(grad_tensor[o_grad], naive_grad[o_grad], (o_grad + '@GRAD'), place)
    places = [core.CPUPlace()]
    if (core.is_compiled_with_cuda() and core.op_support_gpu('layer_norm')):
        places.append(core.CUDAPlace(0))
    for place in places:
        test_with_place(place, shape, begin_norm_axis)