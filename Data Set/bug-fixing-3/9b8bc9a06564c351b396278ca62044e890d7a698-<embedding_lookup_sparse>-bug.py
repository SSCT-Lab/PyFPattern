def embedding_lookup_sparse(params, sp_ids, sp_weights, partition_strategy='mod', name=None, combiner=None, max_norm=None):
    'Computes embeddings for the given ids and weights.\n\n  This op assumes that there is at least one id for each row in the dense tensor\n  represented by sp_ids (i.e. there are no rows with empty features), and that\n  all the indices of sp_ids are in canonical row-major order.\n\n  It also assumes that all id values lie in the range [0, p0), where p0\n  is the sum of the size of params along dimension 0.\n\n  Args:\n    params: A single tensor representing the complete embedding tensor,\n      or a list of P tensors all of same shape except for the first dimension,\n      representing sharded embedding tensors.  Alternatively, a\n      `PartitionedVariable`, created by partitioning along dimension 0.\n    sp_ids: N x M SparseTensor of int64 ids (typically from FeatureValueToId),\n      where N is typically batch size and M is arbitrary.\n    sp_weights: either a SparseTensor of float / double weights, or None to\n      indicate all weights should be taken to be 1. If specified, sp_weights\n      must have exactly the same shape and indices as sp_ids.\n    partition_strategy: A string specifying the partitioning strategy, relevant\n      if `len(params) > 1`. Currently `"div"` and `"mod"` are supported. Default\n      is `"mod"`. See `tf.nn.embedding_lookup` for more details.\n    name: Optional name for the op.\n    combiner: A string specifying the reduction op. Currently "mean", "sqrtn"\n      and "sum" are supported.\n      "sum" computes the weighted sum of the embedding results for each row.\n      "mean" is the weighted sum divided by the total weight.\n      "sqrtn" is the weighted sum divided by the square root of the sum of the\n      squares of the weights.\n    max_norm: If not None, each embedding is normalized to have l2 norm equal\n      to max_norm before combining.\n\n  Returns:\n    A dense tensor representing the combined embeddings for the\n    sparse ids. For each row in the dense tensor represented by sp_ids, the op\n    looks up the embeddings for all ids in that row, multiplies them by the\n    corresponding weight, and combines these embeddings as specified.\n\n    In other words, if\n\n      shape(combined params) = [p0, p1, ..., pm]\n\n    and\n\n      shape(sp_ids) = shape(sp_weights) = [d0, d1, ..., dn]\n\n    then\n\n      shape(output) = [d0, d1, ..., dn-1, p1, ..., pm].\n\n    For instance, if params is a 10x20 matrix, and sp_ids / sp_weights are\n\n      [0, 0]: id 1, weight 2.0\n      [0, 1]: id 3, weight 0.5\n      [1, 0]: id 0, weight 1.0\n      [2, 3]: id 1, weight 3.0\n\n    with `combiner`="mean", then the output will be a 3x20 matrix where\n\n      output[0, :] = (params[1, :] * 2.0 + params[3, :] * 0.5) / (2.0 + 0.5)\n      output[1, :] = params[0, :] * 1.0\n      output[2, :] = params[1, :] * 3.0\n\n  Raises:\n    TypeError: If sp_ids is not a SparseTensor, or if sp_weights is neither\n      None nor SparseTensor.\n    ValueError: If combiner is not one of {"mean", "sqrtn", "sum"}.\n  '
    if (combiner is None):
        logging.warn('The default value of combiner will change from "mean" to "sqrtn" after 2016/11/01.')
        combiner = 'mean'
    if (combiner not in ('mean', 'sqrtn', 'sum')):
        raise ValueError("combiner must be one of 'mean', 'sqrtn' or 'sum'")
    if isinstance(params, variables.PartitionedVariable):
        params = list(params)
    if (not isinstance(params, list)):
        params = [params]
    if (not isinstance(sp_ids, sparse_tensor.SparseTensor)):
        raise TypeError('sp_ids must be SparseTensor')
    ignore_weights = (sp_weights is None)
    if (not ignore_weights):
        if (not isinstance(sp_weights, sparse_tensor.SparseTensor)):
            raise TypeError('sp_weights must be either None or SparseTensor')
        sp_ids.values.get_shape().assert_is_compatible_with(sp_weights.values.get_shape())
        sp_ids.indices.get_shape().assert_is_compatible_with(sp_weights.indices.get_shape())
        sp_ids.shape.get_shape().assert_is_compatible_with(sp_weights.shape.get_shape())
    with ops.name_scope(name, 'embedding_lookup_sparse', (params + [sp_ids])) as name:
        segment_ids = sp_ids.indices[:, 0]
        if (segment_ids.dtype != dtypes.int32):
            segment_ids = math_ops.cast(segment_ids, dtypes.int32)
        ids = sp_ids.values
        if ignore_weights:
            (ids, idx) = array_ops.unique(ids)
        else:
            idx = None
        embeddings = embedding_lookup(params, ids, partition_strategy=partition_strategy, max_norm=max_norm)
        if (not ignore_weights):
            weights = sp_weights.values
            if (weights.dtype != embeddings.dtype):
                weights = math_ops.cast(weights, embeddings.dtype)
            ones = array_ops.fill(array_ops.expand_dims((array_ops.rank(embeddings) - 1), 0), 1)
            bcast_weights_shape = array_ops.concat(0, [array_ops.shape(weights), ones])
            orig_weights_shape = weights.get_shape()
            weights = array_ops.reshape(weights, bcast_weights_shape)
            if (embeddings.get_shape().ndims is not None):
                weights.set_shape(orig_weights_shape.concatenate([1 for _ in range((embeddings.get_shape().ndims - 1))]))
            embeddings *= weights
            if (combiner == 'sum'):
                embeddings = math_ops.segment_sum(embeddings, segment_ids, name=name)
            elif (combiner == 'mean'):
                embeddings = math_ops.segment_sum(embeddings, segment_ids)
                weight_sum = math_ops.segment_sum(weights, segment_ids)
                embeddings = math_ops.div(embeddings, weight_sum, name=name)
            elif (combiner == 'sqrtn'):
                embeddings = math_ops.segment_sum(embeddings, segment_ids)
                weights_squared = math_ops.pow(weights, 2)
                weight_sum = math_ops.segment_sum(weights_squared, segment_ids)
                weight_sum_sqrt = math_ops.sqrt(weight_sum)
                embeddings = math_ops.div(embeddings, weight_sum_sqrt, name=name)
            else:
                assert False, 'Unrecognized combiner'
        else:
            assert (idx is not None)
            if (combiner == 'sum'):
                embeddings = math_ops.sparse_segment_sum(embeddings, idx, segment_ids, name=name)
            elif (combiner == 'mean'):
                embeddings = math_ops.sparse_segment_mean(embeddings, idx, segment_ids, name=name)
            elif (combiner == 'sqrtn'):
                embeddings = math_ops.sparse_segment_sqrt_n(embeddings, idx, segment_ids, name=name)
            else:
                assert False, 'Unrecognized combiner'
        return embeddings