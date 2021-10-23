def _analytical_jacobian(self, module, input, jacobian_input=True, jacobian_parameters=True):
    output = self._forward(module, input)
    output_t = (output.data if isinstance(output, Variable) else output)
    d_out = output_t.new().resize_(output_t.size())
    flat_d_out = d_out.view((- 1))
    if jacobian_input:
        jacobian_inp = self._jacobian(input, d_out.nelement())
        flat_jacobian_input = list(iter_tensors(jacobian_inp))
    if jacobian_parameters:
        (param, d_param) = self._get_parameters(module)
        num_param = sum((p.numel() for p in param))
        jacobian_param = torch.zeros(num_param, d_out.nelement())
    for i in range(flat_d_out.nelement()):
        d_out.zero_()
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