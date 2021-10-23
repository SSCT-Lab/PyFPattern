def embedding_lookup(params, ids, partition_strategy='mod', name=None, validate_indices=True, max_norm=None):
    'Looks up `ids` in a list of embedding tensors.\n\n  This function is used to perform parallel lookups on the list of\n  tensors in `params`.  It is a generalization of\n  [`tf.gather()`](../../api_docs/python/array_ops.md#gather), where `params` is\n  interpreted as a partitioning of a large embedding tensor.  `params` may be\n  a `PartitionedVariable` as returned by using `tf.get_variable()` with a\n  partitioner.\n\n  If `len(params) > 1`, each element `id` of `ids` is partitioned between\n  the elements of `params` according to the `partition_strategy`.\n  In all strategies, if the id space does not evenly divide the number of\n  partitions, each of the first `(max_id + 1) % len(params)` partitions will\n  be assigned one more id.\n\n  If `partition_strategy` is `"mod"`, we assign each id to partition\n  `p = id % len(params)`. For instance,\n  13 ids are split across 5 partitions as:\n  `[[0, 5, 10], [1, 6, 11], [2, 7, 12], [3, 8], [4, 9]]`\n\n  If `partition_strategy` is `"div"`, we assign ids to partitions in a\n  contiguous manner. In this case, 13 ids are split across 5 partitions as:\n  `[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10], [11, 12]]`\n\n  The results of the lookup are concatenated into a dense\n  tensor. The returned tensor has shape `shape(ids) + shape(params)[1:]`.\n\n  Args:\n    params: A single tensor representing the complete embedding tensor,\n      or a list of P tensors all of same shape except for the first dimension,\n      representing sharded embedding tensors.  Alternatively, a\n      `PartitionedVariable`, created by partitioning along dimension 0. Each\n      element must be appropriately sized for the given `partition_strategy`.\n    ids: A `Tensor` with type `int32` or `int64` containing the ids to be looked\n      up in `params`.\n    partition_strategy: A string specifying the partitioning strategy, relevant\n      if `len(params) > 1`. Currently `"div"` and `"mod"` are supported. Default\n      is `"mod"`.\n    name: A name for the operation (optional).\n    validate_indices: Whether or not to validate gather indices.\n    max_norm: If not None, embedding values are l2-normalized to the value of\n     max_norm.\n\n  Returns:\n    A `Tensor` with the same type as the tensors in `params`.\n\n  Raises:\n    ValueError: If `params` is empty.\n  '
    if ((params is None) or (params == [])):
        raise ValueError('Need at least one param')
    if isinstance(params, variables.PartitionedVariable):
        params = list(params)
    if (not isinstance(params, list)):
        params = [params]

    def maybe_normalize(x):
        if (max_norm is not None):
            if (x.get_shape().ndims is not None):
                ndims = x.get_shape().ndims
            else:
                ndims = array_ops.size(array_ops.shape(x))
            return clip_ops.clip_by_norm(x, max_norm, axes=list(range(1, ndims)))
        return x
    with ops.name_scope(name, 'embedding_lookup', (params + [ids])) as name:
        np = len(params)
        params = ops.convert_n_to_tensor_or_indexed_slices(params, name='params')
        if (np == 1):
            with ops.colocate_with(params[0]):
                if isinstance(params[0], resource_variable_ops.ResourceVariable):
                    ret = params[0].sparse_read(ids, name=name)
                else:
                    ret = array_ops.gather(params[0], ids, name=name, validate_indices=validate_indices)
            return maybe_normalize(ret)
        else:
            ids = ops.convert_to_tensor(ids, name='ids')
            flat_ids = array_ops.reshape(ids, [(- 1)])
            original_indices = math_ops.range(array_ops.size(flat_ids))
            if (partition_strategy == 'mod'):
                p_assignments = (flat_ids % np)
                new_ids = (flat_ids // np)
            elif (partition_strategy == 'div'):
                dim_0_size = params[0].get_shape()[0]
                for p in xrange(1, np):
                    dim_0_size += params[p].get_shape()[0]
                if dim_0_size.value:
                    num_total_ids = constant_op.constant(dim_0_size.value, flat_ids.dtype)
                else:
                    dim_0_sizes = []
                    for p in xrange(np):
                        if (params[p].get_shape()[0].value is not None):
                            dim_0_sizes.append(params[p].get_shape()[0].value)
                        else:
                            with ops.colocate_with(params[p]):
                                dim_0_sizes.append(array_ops.shape(params[p])[0])
                    num_total_ids = math_ops.reduce_sum(math_ops.cast(array_ops.pack(dim_0_sizes), flat_ids.dtype))
                ids_per_partition = (num_total_ids // np)
                extras = (num_total_ids % np)
                p_assignments = math_ops.maximum((flat_ids // (ids_per_partition + 1)), ((flat_ids - extras) // ids_per_partition))
                is_in_first_extras_partitions = math_ops.cast((p_assignments < extras), flat_ids.dtype)
                new_ids = ((is_in_first_extras_partitions * (flat_ids % (ids_per_partition + 1))) + ((1 - is_in_first_extras_partitions) * ((flat_ids - extras) % ids_per_partition)))
            else:
                raise ValueError(('Unrecognized partition strategy: ' + partition_strategy))
            p_assignments = math_ops.cast(p_assignments, dtypes.int32)
            gather_ids = data_flow_ops.dynamic_partition(new_ids, p_assignments, np)
            pindices = data_flow_ops.dynamic_partition(original_indices, p_assignments, np)
            partitioned_result = []
            for p in xrange(np):
                with ops.colocate_with(params[p]):
                    partitioned_result.append(array_ops.gather(params[p], gather_ids[p], validate_indices=validate_indices))
            ret = data_flow_ops.dynamic_stitch(pindices, partitioned_result, name=name)
            element_shape = params[0].get_shape()[1:]
            for p in params[1:]:
                element_shape = element_shape.merge_with(p.get_shape()[1:])
            if element_shape.is_fully_defined():
                ret = array_ops.reshape(ret, array_ops.concat(0, [array_ops.shape(ids), element_shape]))
            else:
                with ops.colocate_with(params[0]):
                    params_shape = array_ops.shape(params[0])
                ret = array_ops.reshape(ret, array_ops.concat(0, [array_ops.shape(ids), array_ops.slice(params_shape, [1], [(- 1)])]))
            ret.set_shape(ids.get_shape().concatenate(element_shape))
            return maybe_normalize(ret)