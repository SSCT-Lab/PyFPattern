def _analytical_jacobian(self, module, input, jacobian_input=True, jacobian_parameters=True):
    output = self._forward(module, input)
    output_size = output.nelement()
    output_t = (output.data if isinstance(output, Variable) else output)
    if jacobian_input:
        jacobian_inp = self._jacobian(input, output_size)
        flat_jacobian_input = list(iter_tensors(jacobian_inp))
    if jacobian_parameters:
        num_param = sum((p.numel() for p in self._get_parameters(module)[0]))
        jacobian_param = torch.zeros(num_param, output_size)
    for i in range(output_size):
        (_, d_param) = self._get_parameters(module)
        d_out = torch.zeros_like(output_t)
        flat_d_out = d_out.view((- 1))
        flat_d_out[i] = 1
        if jacobian_parameters:
            self._zero_grad_parameters(module)
        if jacobian_input:
            self._zero_grad_input(input)
        d_input = self._backward(module, input, output, d_out)
        if jacobian_input:
            for (jacobian_x, d_x) in zip(flat_jacobian_input, iter_tensors(d_input)):
                jacobian_x[:, i] = d_x
        if jacobian_parameters:
            jacobian_param[:, i] = torch.cat(self._flatten_tensors(d_param), 0)
    res = tuple()
    if jacobian_input:
        res += (jacobian_inp,)
    if jacobian_parameters:
        res += (jacobian_param,)
    return res