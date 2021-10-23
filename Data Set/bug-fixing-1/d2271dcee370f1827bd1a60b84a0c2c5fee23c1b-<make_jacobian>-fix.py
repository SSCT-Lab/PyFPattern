

def make_jacobian(input, num_out):
    if isinstance(input, torch.Tensor):
        if (not input.is_floating_point()):
            return None
        if (not input.requires_grad):
            return None
        return torch.zeros(input.nelement(), num_out, dtype=input.dtype)
    elif isinstance(input, Iterable):
        jacobians = list(filter((lambda x: (x is not None)), (make_jacobian(elem, num_out) for elem in input)))
        if (not jacobians):
            return None
        return type(input)(jacobians)
    else:
        return None
