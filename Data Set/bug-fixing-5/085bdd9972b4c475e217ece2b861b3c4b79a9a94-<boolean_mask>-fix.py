@tf_export(v1=['boolean_mask'])
def boolean_mask(tensor, mask, name='boolean_mask', axis=None):
    "Apply boolean mask to tensor.\n\n  Numpy equivalent is `tensor[mask]`.\n\n  ```python\n  # 1-D example\n  tensor = [0, 1, 2, 3]\n  mask = np.array([True, False, True, False])\n  boolean_mask(tensor, mask)  # [0, 2]\n  ```\n\n  In general, `0 < dim(mask) = K <= dim(tensor)`, and `mask`'s shape must match\n  the first K dimensions of `tensor`'s shape.  We then have:\n    `boolean_mask(tensor, mask)[i, j1,...,jd] = tensor[i1,...,iK,j1,...,jd]`\n  where `(i1,...,iK)` is the ith `True` entry of `mask` (row-major order).\n  The `axis` could be used with `mask` to indicate the axis to mask from.\n  In that case, `axis + dim(mask) <= dim(tensor)` and `mask`'s shape must match\n  the first `axis + dim(mask)` dimensions of `tensor`'s shape.\n\n  See also: `tf.ragged.boolean_mask`, which can be applied to both dense and\n  ragged tensors, and can be used if you need to preserve the masked dimensions\n  of `tensor` (rather than flattening them, as `tf.boolean_mask` does).\n\n  Args:\n    tensor:  N-D tensor.\n    mask:  K-D boolean tensor, K <= N and K must be known statically.\n    name:  A name for this operation (optional).\n    axis:  A 0-D int Tensor representing the axis in `tensor` to mask from. By\n      default, axis is 0 which will mask from the first dimension. Otherwise K +\n      axis <= N.\n\n  Returns:\n    (N-K+1)-dimensional tensor populated by entries in `tensor` corresponding\n    to `True` values in `mask`.\n\n  Raises:\n    ValueError:  If shapes do not conform.\n\n  Examples:\n\n  ```python\n  # 2-D example\n  tensor = [[1, 2], [3, 4], [5, 6]]\n  mask = np.array([True, False, True])\n  boolean_mask(tensor, mask)  # [[1, 2], [5, 6]]\n  ```\n  "

    def _apply_mask_1d(reshaped_tensor, mask, axis=None):
        'Mask tensor along dimension 0 with a 1-D mask.'
        indices = squeeze(where_v2(mask), axis=[1])
        return gather(reshaped_tensor, indices, axis=axis)
    with ops.name_scope(name, values=[tensor, mask]):
        tensor = ops.convert_to_tensor(tensor, name='tensor')
        mask = ops.convert_to_tensor(mask, name='mask')
        shape_mask = mask.get_shape()
        ndims_mask = shape_mask.ndims
        shape_tensor = tensor.get_shape()
        if (ndims_mask == 0):
            raise ValueError('mask cannot be scalar.')
        if (ndims_mask is None):
            raise ValueError('Number of mask dimensions must be specified, even if some dimensions are None.  E.g. shape=[None] is ok, but shape=None is not.')
        axis = (0 if (axis is None) else axis)
        shape_tensor[axis:(axis + ndims_mask)].assert_is_compatible_with(shape_mask)
        leading_size = gen_math_ops.prod(shape(tensor)[axis:(axis + ndims_mask)], [0])
        tensor = reshape(tensor, concat([shape(tensor)[:axis], [leading_size], shape(tensor)[(axis + ndims_mask):]], 0))
        first_dim = shape_tensor[axis:(axis + ndims_mask)].num_elements()
        tensor.set_shape(tensor_shape.as_shape(shape_tensor[:axis]).concatenate([first_dim]).concatenate(shape_tensor[(axis + ndims_mask):]))
        mask = reshape(mask, [(- 1)])
        return _apply_mask_1d(tensor, mask, axis)