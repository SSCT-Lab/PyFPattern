def boolean_mask(tensor, mask, name='boolean_mask'):
    "Apply boolean mask to tensor.  Numpy equivalent is `tensor[mask]`.\n\n  ```python\n  # 1-D example\n  tensor = [0, 1, 2, 3]\n  mask = [True, False, True, False]\n  boolean_mask(tensor, mask) ==> [0, 2]\n  ```\n\n  In general, `0 < dim(mask) = K <= dim(tensor)`, and `mask`'s shape must match\n  the first K dimensions of `tensor`'s shape.  We then have:\n    `boolean_mask(tensor, mask)[i, j1,...,jd] = tensor[i1,...,iK,j1,...,jd]`\n  where `(i1,...,iK)` is the ith `True` entry of `mask` (row-major order).\n\n  Args:\n    tensor:  N-D tensor.  First K dimensions can be None, which allows e.g.\n      undefined batch size.  Trailing dimensions must be specified.\n    mask:  K-D boolean tensor, K <= N.\n    name:  A name for this operation (optional).\n\n  Returns:\n    Tensor populated by entries in `tensor` corresponding to `True` values in\n      `mask`.\n\n  Raises:\n    ValueError:  If shapes do not conform.\n\n  Examples:\n\n  ```python\n  # 2-D example\n  tensor = [[1, 2], [3, 4], [5, 6]]\n  mask = [True, False, True]\n  boolean_mask(tensor, mask) ==> [[1, 2], [5, 6]]\n  ```\n  "

    def _apply_mask_1d(reshaped_tensor, mask):
        'Mask tensor along dimension 0 with a 1-D mask.'
        indices = squeeze(where(mask), squeeze_dims=[1])
        return gather(reshaped_tensor, indices)
    with ops.op_scope([tensor, mask], name):
        tensor = ops.convert_to_tensor(tensor, name='tensor')
        mask = ops.convert_to_tensor(mask, name='mask')
        shape_mask = mask.get_shape()
        ndims_mask = shape_mask.ndims
        shape_tensor = tensor.get_shape()
        if (ndims_mask == 0):
            raise ValueError('mask cannot be scalar.')
        if (ndims_mask is None):
            raise ValueError('mask dimensions must be specified, even if some dimensions are None.  E.g. shape=[None] is ok, but shape=None is not.')
        shape_tensor[:ndims_mask].assert_is_compatible_with(shape_mask)
        tensor = reshape(tensor, ([(- 1)] + shape_tensor.as_list()[ndims_mask:]))
        mask = reshape(mask, [(- 1)])
        return _apply_mask_1d(tensor, mask)