@ops.RegisterGradient('SparseSoftmax')
def _SparseSoftmaxGrad(op, grad):
    'Gradients for SparseSoftmax.\n\n  The calculation is the same as SoftmaxGrad:\n\n    grad_x = grad_softmax * softmax - sum(grad_softmax * softmax) * softmax\n\n  where we now only operate on the non-zero values present in the SparseTensors.\n\n  Args:\n    op: the SparseSoftmax op.\n    grad: the upstream gradient w.r.t. the non-zero SparseSoftmax output values.\n\n  Returns:\n    Gradients w.r.t. the input (sp_indices, sp_values, sp_shape).\n  '
    (indices, shape) = (op.inputs[0], op.inputs[2])
    out_vals = op.outputs[0]
    sp_output = sparse_tensor.SparseTensor(indices, out_vals, shape)
    sp_grad = sparse_tensor.SparseTensor(indices, grad, shape)
    sp_product = sparse_tensor.SparseTensor(indices, (sp_output.values * sp_grad.values), shape)
    sum_reduced = (- sparse_ops.sparse_reduce_sum(sp_product, [(- 1)], keepdims=True))
    sp_sum = sparse_ops.sparse_dense_cwise_add(sp_grad, sum_reduced)
    grad_x = (sp_sum.values * sp_output.values)
    return [None, grad_x, None]