def read_up_to(self, queue, num_records, name=None):
    'Returns up to num_records (key, value) pairs produced by a reader.\n\n    Will dequeue a work unit from queue if necessary (e.g., when the\n    Reader needs to start reading from a new file since it has\n    finished with the previous file).\n    It may return less than num_records even before the last batch.\n\n    Args:\n      queue: A Queue or a mutable string Tensor representing a handle\n        to a Queue, with string work items.\n      num_records: Number of records to read.\n      name: A name for the operation (optional).\n\n    Returns:\n      A tuple of Tensors (keys, values).\n      keys: A 1-D string Tensor.\n      values: A 1-D string Tensor.\n    '
    if isinstance(queue, ops.Tensor):
        queue_ref = queue
    else:
        queue_ref = queue.queue_ref
    if (self._reader_ref.dtype == dtypes.resource):
        return gen_io_ops._reader_read_up_to_v2(self._reader_ref, queue_ref, num_records, name=name)
    else:
        old_queue_op = gen_data_flow_ops._fake_queue(queue_ref)
        return gen_io_ops._reader_read_up_to(self._reader_ref, old_queue_op, num_records, name=name)