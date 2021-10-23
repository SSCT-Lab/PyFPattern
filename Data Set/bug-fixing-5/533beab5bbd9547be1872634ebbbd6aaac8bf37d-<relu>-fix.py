def relu(input, inplace=False):
    'relu(input, inplace=False) -> Tensor\n\n    Applies the rectified linear unit function element-wise. See\n    :class:`~torch.nn.ReLU` for more details.\n    '
    if inplace:
        return torch.relu_(input)
    return torch.relu(input)