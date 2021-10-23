def interpolate(input, size=None, scale_factor=None, mode='nearest', align_corners=None):
    "Down/up samples the input to either the given :attr:`size` or the given\n    :attr:`scale_factor`\n\n    The algorithm used for interpolation is determined by :attr:`mode`.\n\n    Currently temporal, spatial and volumetric sampling are supported, i.e.\n    expected inputs are 3-D, 4-D or 5-D in shape.\n\n    The input dimensions are interpreted in the form:\n    `mini-batch x channels x [optional depth] x [optional height] x width`.\n\n    The modes available for resizing are: `nearest`, `linear` (3D-only),\n    `bilinear`, `bicubic` (4D-only), `trilinear` (5D-only), `area`\n\n    Args:\n        input (Tensor): the input tensor\n        size (int or Tuple[int] or Tuple[int, int] or Tuple[int, int, int]):\n            output spatial size.\n        scale_factor (float or Tuple[float]): multiplier for spatial size. Has to match input size if it is a tuple.\n        mode (str): algorithm used for upsampling:\n            ``'nearest'`` | ``'linear'`` | ``'bilinear'`` | ``'bicubic'`` |\n            ``'trilinear'`` | ``'area'``. Default: ``'nearest'``\n        align_corners (bool, optional): Geometrically, we consider the pixels of the\n            input and output as squares rather than points.\n            If set to ``True``, the input and output tensors are aligned by the\n            center points of their corner pixels, preserving the values at the corner pixels.\n            If set to ``False``, the input and output tensors are aligned by the corner\n            points of their corner pixels, and the interpolation uses edge value padding\n            for out-of-boundary values, making this operation *independent* of input size\n            when :attr:`scale_factor` is kept the same. This only has an effect when :attr:`mode`\n            is ``'linear'``, ``'bilinear'``, ``'bicubic'`` or ``'trilinear'``.\n            Default: ``False``\n\n    .. note::\n        With ``mode='bicubic'``, it's possible to cause overshoot, in other words it can produce\n        negative values or values greater than 255 for images.\n        Explicitly call ``result.clamp(min=0, max=255)`` if you want to reduce the overshoot\n        when displaying the image.\n\n    .. warning::\n        With ``align_corners = True``, the linearly interpolating modes\n        (`linear`, `bilinear`, and `trilinear`) don't proportionally align the\n        output and input pixels, and thus the output values can depend on the\n        input size. This was the default behavior for these modes up to version\n        0.3.1. Since then, the default behavior is ``align_corners = False``.\n        See :class:`~torch.nn.Upsample` for concrete examples on how this\n        affects the outputs.\n\n    .. include:: cuda_deterministic_backward.rst\n    "
    from .modules.utils import _ntuple

    def _check_size_scale_factor(dim):
        if ((size is None) and (scale_factor is None)):
            raise ValueError('either size or scale_factor should be defined')
        if ((size is not None) and (scale_factor is not None)):
            raise ValueError('only one of size or scale_factor should be defined')
        if ((scale_factor is not None) and isinstance(scale_factor, tuple) and (len(scale_factor) != dim)):
            raise ValueError('scale_factor shape must match input shape. Input is {}D, scale_factor size is {}'.format(dim, len(scale_factor)))

    def _output_size(dim):
        _check_size_scale_factor(dim)
        if (size is not None):
            return size
        scale_factors = _ntuple(dim)(scale_factor)
        if torch._C._get_tracing_state():
            return [torch.floor((input.size((i + 2)) * torch.tensor(float(scale_factors[i]))).float()) for i in range(dim)]
        else:
            return [int(math.floor((float(input.size((i + 2))) * scale_factors[i]))) for i in range(dim)]
    if (mode in ('nearest', 'area')):
        if (align_corners is not None):
            raise ValueError('align_corners option can only be set with the interpolating modes: linear | bilinear | bicubic | trilinear')
    elif (align_corners is None):
        warnings.warn('Default upsampling behavior when mode={} is changed to align_corners=False since 0.4.0. Please specify align_corners=True if the old behavior is desired. See the documentation of nn.Upsample for details.'.format(mode))
        align_corners = False
    if ((input.dim() == 3) and (mode == 'nearest')):
        return torch._C._nn.upsample_nearest1d(input, _output_size(1))
    elif ((input.dim() == 4) and (mode == 'nearest')):
        return torch._C._nn.upsample_nearest2d(input, _output_size(2))
    elif ((input.dim() == 5) and (mode == 'nearest')):
        return torch._C._nn.upsample_nearest3d(input, _output_size(3))
    elif ((input.dim() == 3) and (mode == 'area')):
        return adaptive_avg_pool1d(input, _output_size(1))
    elif ((input.dim() == 4) and (mode == 'area')):
        return adaptive_avg_pool2d(input, _output_size(2))
    elif ((input.dim() == 5) and (mode == 'area')):
        return adaptive_avg_pool3d(input, _output_size(3))
    elif ((input.dim() == 3) and (mode == 'linear')):
        return torch._C._nn.upsample_linear1d(input, _output_size(1), align_corners)
    elif ((input.dim() == 3) and (mode == 'bilinear')):
        raise NotImplementedError('Got 3D input, but bilinear mode needs 4D input')
    elif ((input.dim() == 3) and (mode == 'trilinear')):
        raise NotImplementedError('Got 3D input, but trilinear mode needs 5D input')
    elif ((input.dim() == 4) and (mode == 'linear')):
        raise NotImplementedError('Got 4D input, but linear mode needs 3D input')
    elif ((input.dim() == 4) and (mode == 'bilinear')):
        return torch._C._nn.upsample_bilinear2d(input, _output_size(2), align_corners)
    elif ((input.dim() == 4) and (mode == 'trilinear')):
        raise NotImplementedError('Got 4D input, but trilinear mode needs 5D input')
    elif ((input.dim() == 5) and (mode == 'linear')):
        raise NotImplementedError('Got 5D input, but linear mode needs 3D input')
    elif ((input.dim() == 5) and (mode == 'bilinear')):
        raise NotImplementedError('Got 5D input, but bilinear mode needs 4D input')
    elif ((input.dim() == 5) and (mode == 'trilinear')):
        return torch._C._nn.upsample_trilinear3d(input, _output_size(3), align_corners)
    elif ((input.dim() == 4) and (mode == 'bicubic')):
        return torch._C._nn.upsample_bicubic2d(input, _output_size(2), align_corners)
    else:
        raise NotImplementedError('Input Error: Only 3D, 4D and 5D input Tensors supported (got {}D) for the modes: nearest | linear | bilinear | bicubic | trilinear (got {})'.format(input.dim(), mode))