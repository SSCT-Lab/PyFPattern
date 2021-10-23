def svd(tensor, full_matrices=False, compute_uv=True, name=None):
    'Computes the singular value decompositions of one or more matrices.\n\n  Computes the SVD of each inner matrix in `tensor` such that\n  `tensor[..., :, :] = u[..., :, :] * diag(s[..., :, :]) * transpose(v[..., :,\n  :])`\n\n  ```prettyprint\n  # a is a tensor.\n  # s is a tensor of singular values.\n  # u is a tensor of left singular vectors.\n  # v is a tensor of right singular vectors.\n  s, u, v = svd(a)\n  s = svd(a, compute_uv=False)\n  ```\n\n  Args:\n    tensor: `Tensor` of shape `[..., M, N]`. Let `P` be the minimum of `M` and\n      `N`.\n    full_matrices: If true, compute full-sized `u` and `v`. If false\n      (the default), compute only the leading `P` singular vectors.\n      Ignored if `compute_uv` is `False`.\n    compute_uv: If `True` then left and right singular vectors will be\n      computed and returned in `u` and `v`, respectively. Otherwise, only the\n      singular values will be computed, which can be significantly faster.\n    name: string, optional name of the operation.\n\n  Returns:\n    s: Singular values. Shape is `[..., P]`.\n    u: Left singular vectors. If `full_matrices` is `False` (default) then\n      shape is `[..., M, P]`; if `full_matrices` is `True` then shape is\n      `[..., M, M]`. Not returned if `compute_uv` is `False`.\n    v: Right singular vectors. If `full_matrices` is `False` (default) then\n      shape is `[..., N, P]`. If `full_matrices` is `True` then shape is\n      `[..., N, N]`. Not returned if `compute_uv` is `False`.\n\n  @compatibility(numpy)\n  Mostly equivalent to numpy.linalg.svd, except that the order of output\n  arguments here is `s`, `u`, `v` when `compute_uv` is `True`, as opposed to\n  `u`, `s`, `v` for numpy.linalg.svd.\n  @end_compatibility\n  '
    (s, u, v) = gen_linalg_ops._svd(tensor, compute_uv=compute_uv, full_matrices=full_matrices)
    if compute_uv:
        return (math_ops.real(s), u, v)
    else:
        return math_ops.real(s)