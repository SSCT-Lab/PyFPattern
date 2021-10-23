

@tf_export('linalg.eigvalsh', v1=['linalg.eigvalsh', 'self_adjoint_eigvals'])
@deprecation.deprecated_endpoints('self_adjoint_eigvals')
def self_adjoint_eigvals(tensor, name=None):
    'Computes the eigenvalues of one or more self-adjoint matrices.\n\n  Note: If your program backpropagates through this function, you should replace\n  it with a call to tf.linalg.eigvalsh (possibly ignoring the second output) to\n  avoid computing the eigen decomposition twice. This is because the\n  eigenvectors are used to compute the gradient w.r.t. the eigenvalues. See\n  _SelfAdjointEigV2Grad in linalg_grad.py.\n\n  Args:\n    tensor: `Tensor` of shape `[..., N, N]`.\n    name: string, optional name of the operation.\n\n  Returns:\n    e: Eigenvalues. Shape is `[..., N]`. The vector `e[..., :]` contains the `N`\n      eigenvalues of `tensor[..., :, :]`.\n  '
    (e, _) = gen_linalg_ops.self_adjoint_eig_v2(tensor, compute_v=False, name=name)
    return e
