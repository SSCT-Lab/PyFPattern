def _shuffle_batch(tensors, batch_size, capacity, min_after_dequeue, keep_input, num_threads=1, seed=None, enqueue_many=False, shapes=None, allow_smaller_final_batch=False, shared_name=None, name=None):
    'Helper function for `shuffle_batch` and `maybe_shuffle_batch`.'
    tensor_list = _as_tensor_list(tensors)
    with ops.name_scope(name, 'shuffle_batch', (list(tensor_list) + [keep_input])) as name:
        tensor_list = _validate(tensor_list)
        keep_input = _validate_keep_input(keep_input, enqueue_many)
        (tensor_list, sparse_info) = _store_sparse_tensors(tensor_list, enqueue_many, keep_input)
        types = _dtypes([tensor_list])
        shapes = _shapes([tensor_list], shapes, enqueue_many)
        queue = data_flow_ops.RandomShuffleQueue(capacity=capacity, min_after_dequeue=min_after_dequeue, seed=seed, dtypes=types, shapes=shapes, shared_name=shared_name)
        _enqueue(queue, tensor_list, num_threads, enqueue_many, keep_input)
        full = (math_ops.cast(math_ops.maximum(0, (queue.size() - min_after_dequeue)), dtypes.float32) * (1.0 / (capacity - min_after_dequeue)))
        summary_name = ('fraction_over_%d_of_%d_full' % (min_after_dequeue, (capacity - min_after_dequeue)))
        summary.scalar(summary_name, full)
        if allow_smaller_final_batch:
            dequeued = queue.dequeue_up_to(batch_size, name=name)
        else:
            dequeued = queue.dequeue_many(batch_size, name=name)
        dequeued = _restore_sparse_tensors(dequeued, sparse_info)
        return _as_original_type(tensors, dequeued)