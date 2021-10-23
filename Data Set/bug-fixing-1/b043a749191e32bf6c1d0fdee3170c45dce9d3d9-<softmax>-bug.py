

def softmax(input, dim=None, _stacklevel=3):
    "Applies a softmax function.\n\n    Softmax is defined as:\n\n    :math:`softmax(x) = \\frac{exp(-x_i)}{\\sum_j exp(-x_j)}`\n\n    It is applied to all slices along dim, and will rescale them so that the elements\n    lie in the range `(0, 1)` and sum to 1.\n\n    See :class:`~torch.nn.Softmax` for more details.\n\n    Arguments:\n        input (Variable): input\n        dim (int): A dimension along which softmax will be computed.\n\n    .. note::\n        This function doesn't work directly with NLLLoss,\n        which expects the Log to be computed between the Softmax and itself.\n        Use log_softmax instead (it's faster and has better numerical properties).\n\n    "
    if (dim is None):
        dim = _get_softmax_dim('softmax', input.dim(), _stacklevel)
    return torch._C._nn.softmax(input, dim)
