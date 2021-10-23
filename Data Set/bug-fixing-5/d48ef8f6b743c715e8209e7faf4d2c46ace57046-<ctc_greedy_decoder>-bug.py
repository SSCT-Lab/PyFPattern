def ctc_greedy_decoder(inputs, sequence_length, merge_repeated=True):
    "Performs greedy decoding on the logits given in input (best path).\n\n  Note: Regardless of the value of merge_repeated, if the maximum index of a\n  given time and batch corresponds to the blank index `(num_classes - 1)`, no\n  new element is emitted.\n\n  If `merge_repeated` is `True`, merge repeated classes in output.\n  This means that if consecutive logits' maximum indices are the same,\n  only the first of these is emitted.  The sequence `A B B * B * B` (where '*'\n  is the blank label) becomes\n\n    * `A B B B` if `merge_repeated=True`.\n    * `A B B B B` if `merge_repeated=False`.\n\n  Args:\n    inputs: 3-D `float` `Tensor` sized\n      `[max_time x batch_size x num_classes]`.  The logits.\n    sequence_length: 1-D `int32` vector containing sequence lengths,\n      having size `[batch_size]`.\n    merge_repeated: Boolean.  Default: True.\n\n  Returns:\n    A tuple `(decoded, log_probabilities)` where\n    decoded: A single-element list. `decoded[0]`\n      is an `SparseTensor` containing the decoded outputs s.t.:\n      `decoded.indices`: Indices matrix `(total_decoded_outputs x 2)`.\n        The rows store: `[batch, time]`.\n      `decoded.values`: Values vector, size `(total_decoded_outputs)`.\n        The vector stores the decoded classes.\n      `decoded.shape`: Shape vector, size `(2)`.\n        The shape values are: `[batch_size, max_decoded_length]`\n    log_probability: A `float` matrix `(batch_size x 1)` containing sequence\n        log-probabilities.\n  "
    outputs = gen_ctc_ops._ctc_greedy_decoder(inputs, sequence_length, merge_repeated=merge_repeated)
    (decoded_ix, decoded_val, decoded_shape, log_probabilities) = outputs
    return ([sparse_tensor.SparseTensor(decoded_ix, decoded_val, decoded_shape)], log_probabilities)