

def clip_grad_norm_(parameters, max_norm, norm_type=2):
    "Clips gradient norm of an iterable of parameters.\n\n    The norm is computed over all gradients together, as if they were\n    concatenated into a single vector. Gradients are modified in-place.\n\n    Arguments:\n        parameters (Iterable[Tensor]): an iterable of Tensors that will have\n            gradients normalized\n        max_norm (float or int): max norm of the gradients\n        norm_type (float or int): type of the used p-norm. Can be ``'inf'`` for\n            infinity norm.\n\n    Returns:\n        Total norm of the parameters (viewed as a single vector).\n    "
    parameters = list(filter((lambda p: (p.grad is not None)), parameters))
    max_norm = float(max_norm)
    norm_type = float(norm_type)
    if (norm_type == float('inf')):
        total_norm = max((p.grad.data.abs().max() for p in parameters))
    else:
        total_norm = 0
        for p in parameters:
            param_norm = p.grad.data.norm(norm_type)
            total_norm += (param_norm ** norm_type)
        total_norm = (total_norm ** (1.0 / norm_type))
    clip_coef = (max_norm / (total_norm + 1e-06))
    if (clip_coef < 1):
        for p in parameters:
            p.grad.data.mul_(clip_coef)
    return total_norm
