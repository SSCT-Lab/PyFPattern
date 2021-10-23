

def affine_grid(theta, size):
    'Generates a 2d flow field, given a batch of affine matrices :attr:`theta`\n    Generally used in conjunction with :func:`grid_sample` to\n    implement Spatial Transformer Networks.\n\n    Args:\n        theta (Variable): input batch of affine matrices (N x 2 x 3)\n        size (torch.Size): the target output image size (N x C x H x W)\n                           Example: torch.Size((32, 3, 24, 24))\n\n    Returns:\n        output (Variable): output Tensor of size (N x H x W x 2)\n    '
    return AffineGridGenerator.apply(theta, size)
