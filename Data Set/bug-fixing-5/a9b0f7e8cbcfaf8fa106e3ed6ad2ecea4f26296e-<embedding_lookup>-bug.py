@tf_export(v1=['nn.embedding_lookup'])
def embedding_lookup(params, ids, partition_strategy='mod', name=None, validate_indices=True, max_norm=None):
    'Looks up `ids` in a list of embedding tensors.\n\n  This function is used to perform parallel lookups on the list of\n  tensors in `params`.  It is a generalization of\n  `tf.gather`, where `params` is\n  interpreted as a partitioning of a large embedding tensor.  `params` may be\n  a `PartitionedVariable` as returned by using `tf.compat.v1.get_variable()`\n  with a\n  partitioner.\n\n  If `len(params) > 1`, each element `id` of `ids` is partitioned between\n  the elements of `params` according to the `partition_strategy`.\n  In all strategies, if the id space does not evenly divide the number of\n  partitions, each of the first `(max_id + 1) % len(params)` partitions will\n  be assigned one more id.\n\n  If `partition_strategy` is `"mod"`, we assign each id to partition\n  `p = id % len(params)`. For instance,\n  13 ids are split across 5 partitions as:\n  `[[0, 5, 10], [1, 6, 11], [2, 7, 12], [3, 8], [4, 9]]`\n\n  If `partition_strategy` is `"div"`, we assign ids to partitions in a\n  contiguous manner. In this case, 13 ids are split across 5 partitions as:\n  `[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10], [11, 12]]`\n\n  If the input ids are ragged tensors, partition variables are not supported and\n  the partition strategy and the max_norm are ignored.\n  The results of the lookup are concatenated into a dense\n  tensor. The returned tensor has shape `shape(ids) + shape(params)[1:]`.\n\n  Args:\n    params: A single tensor representing the complete embedding tensor, or a\n      list of P tensors all of same shape except for the first dimension,\n      representing sharded embedding tensors.  Alternatively, a\n      `PartitionedVariable`, created by partitioning along dimension 0. Each\n      element must be appropriately sized for the given `partition_strategy`.\n    ids: A `Tensor` or a \'RaggedTensor\' with type `int32` or `int64` containing\n      the ids to be looked up in `params`.\n    partition_strategy: A string specifying the partitioning strategy, relevant\n      if `len(params) > 1`. Currently `"div"` and `"mod"` are supported. Default\n      is `"mod"`.\n    name: A name for the operation (optional).\n    validate_indices: DEPRECATED. If this operation is assigned to CPU, values\n      in `indices` are always validated to be within range.  If assigned to GPU,\n      out-of-bound indices result in safe but unspecified behavior, which may\n      include raising an error.\n    max_norm: If not `None`, each embedding is clipped if its l2-norm is larger\n      than this value.\n\n  Returns:\n    A `Tensor` or a \'RaggedTensor\', depending on the input, with the same type\n    as the tensors in `params`.\n\n  Raises:\n    ValueError: If `params` is empty.\n  '
    if isinstance(ids, ragged_tensor.RaggedTensor):
        return embedding_lookup_ragged(params, ids)
    return _embedding_lookup_and_transform(params=params, ids=ids, partition_strategy=partition_strategy, name=name, max_norm=max_norm, transform_fn=None)