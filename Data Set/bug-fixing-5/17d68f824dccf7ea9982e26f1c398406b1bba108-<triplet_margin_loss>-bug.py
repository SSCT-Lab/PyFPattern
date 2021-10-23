def triplet_margin_loss(anchor, positive, negative, margin=1.0, p=2, eps=1e-06, swap=False):
    'Creates a criterion that measures the triplet loss given an input\n    tensors x1, x2, x3 and a margin with a value greater than 0.\n    This is used for measuring a relative similarity between samples. A triplet\n    is composed by `a`, `p` and `n`: anchor, positive examples and negative\n    example respectively. The shape of all input variables should be\n    :math:`(N, D)`.\n\n    The distance swap is described in detail in the paper `Learning shallow\n    convolutional feature descriptors with triplet losses`_ by\n    V. Balntas, E. Riba et al.\n\n    .. math::\n        L(a, p, n) = \\frac{1}{N} \\left( \\sum_{i=1}^N \\max \\{d(a_i, p_i) - d(a_i, n_i) + {\\rm margin}, 0\\} \\right)\n\n    where :math:`d(x_i, y_i) = \\| {\\bf x}_i - {\\bf y}_i \\|_2^2`.\n\n    Args:\n        anchor: anchor input tensor\n        positive: positive input tensor\n        negative: negative input tensor\n        margin: the margin value. Default: 1\n        p: the norm degree. Default: 2\n        eps: small epsilon value to avoid numerical issues. Default: 1e-6\n        swap: compute distance swap. Default: False\n\n    Shape:\n        - Input: :math:`(N, D)` where `D = vector dimension`\n        - Output: :math:`(N, 1)`\n\n    Example::\n\n        >>> input1 = autograd.Variable(torch.randn(100, 128))\n        >>> input2 = autograd.Variable(torch.randn(100, 128))\n        >>> input3 = autograd.Variable(torch.randn(100, 128))\n        >>> output = F.triplet_margin_loss(input1, input2, input3, p=2)\n        >>> output.backward()\n\n    .. _Learning shallow convolutional feature descriptors with triplet losses:\n        http://www.iis.ee.ic.ac.uk/%7Evbalnt/shallow_descr/TFeat_paper.pdf\n    '
    assert (anchor.size() == positive.size()), 'Input sizes between positive and negative must be equal.'
    assert (anchor.size() == negative.size()), 'Input sizes between anchor and negative must be equal.'
    assert (positive.size() == negative.size()), 'Input sizes between positive and negative must be equal.'
    assert (anchor.dim() == 2), 'Inputd must be a 2D matrix.'
    assert (margin > 0.0), 'Margin should be positive value.'
    d_p = pairwise_distance(anchor, positive, p, eps)
    d_n = pairwise_distance(anchor, negative, p, eps)
    if swap:
        d_s = pairwise_distance(positive, negative, p, eps)
        d_n = torch.min(d_n, d_s)
    dist_hinge = torch.clamp(((margin + d_p) - d_n), min=0.0)
    loss = torch.mean(dist_hinge)
    return loss