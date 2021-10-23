def nll_loss(input, target, weight=None, size_average=True, ignore_index=(- 100), reduce=True):
    'The negative log likelihood loss.\n\n    See :class:`~torch.nn.NLLLoss` for details.\n\n    Args:\n        input: :math:`(N, C)` where `C = number of classes` or :math:`(N, C, H, W)`\n            in case of 2D Loss, or :math:`(N, C, d_1, d_2, ..., d_K)` where :math:`K > 1`\n            in the case of K-dimensional loss.\n        target: :math:`(N)` where each value is :math:`0 \\leq \\text{targets}[i] \\leq C-1`,\n            or :math:`(N, d_1, d_2, ..., d_K)` where :math:`K \\geq 1` for\n            K-dimensional loss.\n        weight (Tensor, optional): a manual rescaling weight given to each\n            class. If given, has to be a Tensor of size `C`\n        size_average (bool, optional): By default, the losses are averaged\n            over observations for each minibatch. If :attr:`size_average`\n            is ``False``, the losses are summed for each minibatch. Default: ``True``\n        ignore_index (int, optional): Specifies a target value that is ignored\n            and does not contribute to the input gradient. When :attr:`size_average` is\n            ``True``, the loss is averaged over non-ignored targets. Default: -100\n\n    Example::\n\n        >>> # input is of size N x C = 3 x 5\n        >>> input = torch.randn(3, 5)\n        >>> # each element in target has to have 0 <= value < C\n        >>> target = torch.LongTensor([1, 0, 4])\n        >>> output = F.nll_loss(F.log_softmax(input), target)\n        >>> output.backward()\n    '
    dim = input.dim()
    if torch.is_tensor(weight):
        weight = weight
    if (dim < 2):
        raise ValueError('Expected 2 or more dimensions (got {})'.format(dim))
    if (input.size(0) != target.size(0)):
        raise ValueError('Expected input batch_size ({}) to match target batch_size ({}).'.format(input.size(0), target.size(0)))
    if (dim == 2):
        return torch._C._nn.nll_loss(input, target, weight, size_average, ignore_index, reduce)
    elif (dim == 4):
        return torch._C._nn.nll_loss2d(input, target, weight, size_average, ignore_index, reduce)
    elif ((dim == 3) or (dim > 4)):
        n = input.size(0)
        c = input.size(1)
        out_size = ((n,) + input.size()[2:])
        if (target.size()[1:] != input.size()[2:]):
            raise ValueError('Expected target size {}, got {}'.format(out_size, target.size()))
        input = input.contiguous().view(n, c, 1, (- 1))
        target = target.contiguous().view(n, 1, (- 1))
        if reduce:
            return torch._C._nn.nll_loss2d(input, target, weight, size_average, ignore_index, reduce)
        out = torch._C._nn.nll_loss2d(input, target, weight, size_average, ignore_index, reduce)
        return out.view(out_size)