@tf_export(v1=['reverse_sequence'])
@deprecation.deprecated_args(None, 'seq_dim is deprecated, use seq_axis instead', 'seq_dim')
@deprecation.deprecated_args(None, 'batch_dim is deprecated, use batch_axis instead', 'batch_dim')
def reverse_sequence(input, seq_lengths, seq_axis=None, batch_axis=None, name=None, seq_dim=None, batch_dim=None):
    'Reverses variable length slices.\n\n  This op first slices `input` along the dimension `batch_axis`, and for\n  each slice `i`, reverses the first `seq_lengths[i]` elements along the\n  dimension `seq_axis`.\n\n  The elements of `seq_lengths` must obey `seq_lengths[i] <=\n  input.dims[seq_dim]`, and `seq_lengths` must be a vector of length\n  `input.dims[batch_dim]`.\n\n  The output slice `i` along dimension `batch_axis` is then given by\n  input slice `i`, with the first `seq_lengths[i]` slices along\n  dimension `seq_axis` reversed.\n\n  Example usage:\n\n  >>> seq_lengths = [7, 2, 3, 5]\n  >>> input = [[1, 2, 3, 4, 5, 0, 0, 0], [1, 2, 0, 0, 0, 0, 0, 0],\n  ...          [1, 2, 3, 4, 0, 0, 0, 0], [1, 2, 3, 4, 5, 6, 7, 8]]\n  >>> output = reverse_sequence(input, seq_lengths, seq_dim=1, batch_dim=0)\n  >>> print(output)\n  <tf.Tensor: id=5, shape=(4, 8), dtype=int32, numpy=\n  array([[0, 0, 5, 4, 3, 2, 1, 0],\n         [2, 1, 0, 0, 0, 0, 0, 0],\n         [3, 2, 1, 4, 0, 0, 0, 0],\n         [5, 4, 3, 2, 1, 6, 7, 8]], dtype=int32)>\n\n  Args:\n    `input`: A `Tensor`. The input to reverse.\n    `seq_lengths`: A `Tensor`. Must be one of the following types: `int32`,\n      `int64`. 1-D with length `input.dims(batch_dim)` and `max(seq_lengths) <=\n      input.dims(seq_dim)`\n    `seq_axis`: An `int`. The dimension which is partially reversed.\n    `batch_axis`: An optional `int`. Defaults to `0`. The dimension along which\n      reversal is performed.\n    `name`: A name for the operation (optional).\n\n  Returns:\n    A Tensor. Has the same type as input.\n  '
    seq_axis = deprecation.deprecated_argument_lookup('seq_axis', seq_axis, 'seq_dim', seq_dim)
    batch_axis = deprecation.deprecated_argument_lookup('batch_axis', batch_axis, 'batch_dim', batch_dim)
    return gen_array_ops.reverse_sequence(input=input, seq_lengths=seq_lengths, seq_dim=seq_axis, batch_dim=batch_axis, name=name)