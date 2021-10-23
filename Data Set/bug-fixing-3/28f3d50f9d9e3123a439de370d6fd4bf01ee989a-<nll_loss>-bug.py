def nll_loss(input, target, weight=None, size_average=True, ignore_index=(- 100), reduce=True):
    'The negative log likelihood loss.\n\n    See :class:`~torch.nn.NLLLoss` for details.\n\n    Args:\n        input: :math:`(N, C)` where `C = number of classes` or `(N, C, H, W)`\n            in case of 2D - Loss\n        target: :math:`(N)` where each value is `0 <= targets[i] <= C-1`\n        weight (Tensor, optional): a manual rescaling weight given to each\n            class. If given, has to be a Tensor of size "nclasses"\n        size_average (bool, optional): By default, the losses are averaged\n            over observations for each minibatch. If size_average\n            is False, the losses are summed for each minibatch. Default: True\n        ignore_index (int, optional): Specifies a target value that is ignored\n            and does not contribute to the input gradient. When size_average is\n            True, the loss is averaged over non-ignored targets. Default: -100\n\n    Example::\n\n        >>> # input is of size nBatch x nClasses = 3 x 5\n        >>> input = autograd.Variable(torch.randn(3, 5))\n        >>> # each element in target has to have 0 <= value < nclasses\n        >>> target = autograd.Variable(torch.LongTensor([1, 0, 4]))\n        >>> output = F.nll_loss(F.log_softmax(input), target)\n        >>> output.backward()\n    '
    dim = input.dim()
    if torch.is_tensor(weight):
        weight = Variable(weight)
    if (dim == 2):
        return torch._C._nn.nll_loss(input, target, weight, size_average, ignore_index, reduce)
    elif (dim == 4):
        return torch._C._nn.nll_loss2d(input, target, weight, size_average, ignore_index, reduce)
    else:
        raise ValueError('Expected 2 or 4 dimensions (got {})'.format(dim))