def _numerical_jacobian(self, module, input, jacobian_input=True, jacobian_parameters=True):

    def fw(input):
        out = self._forward(module, input)
        if isinstance(out, Variable):
            return out.data
        return out
    res = tuple()
    input = contiguous(input)
    if jacobian_input:
        res += (get_numerical_jacobian(fw, input, input, eps=1e-06),)
    if jacobian_parameters:
        (param, _) = self._get_parameters(module)
        res += (torch.cat(list((get_numerical_jacobian(fw, input, p, eps=1e-06) for p in param)), 0),)
    return res