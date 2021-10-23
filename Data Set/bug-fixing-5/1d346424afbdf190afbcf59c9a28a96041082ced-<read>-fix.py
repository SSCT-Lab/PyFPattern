def read(self, queue, name=None):
    'Returns the next record (key, value) pair produced by a reader.\n\n    Will dequeue a work unit from queue if necessary (e.g. when the\n    Reader needs to start reading from a new file since it has\n    finished with the previous file).\n\n    Args:\n      queue: A Queue or a mutable string Tensor representing a handle\n        to a Queue, with string work items.\n      name: A name for the operation (optional).\n\n    Returns:\n      A tuple of Tensors (key, value).\n      key: A string scalar Tensor.\n      value: A string scalar Tensor.\n    '
    if isinstance(queue, ops.Tensor):
        queue_ref = queue
    else:
        queue_ref = queue.queue_ref
    if (self._reader_ref.dtype == dtypes.resource):
        return gen_io_ops._reader_read_v2(self._reader_ref, queue_ref, name=name)
    else:
        old_queue_op = gen_data_flow_ops._fake_queue(queue_ref)
        return gen_io_ops._reader_read(self._reader_ref, old_queue_op, name=name)