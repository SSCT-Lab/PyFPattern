def input_producer(input_tensor, element_shape=None, num_epochs=None, shuffle=True, seed=None, capacity=32, shared_name=None, summary_name=None, name=None):
    'Output the rows of `input_tensor` to a queue for an input pipeline.\n\n  Args:\n    input_tensor: A tensor with the rows to produce. Must be at\n      one-dimensional. Must either have a fully-defined shape, or\n      `element_shape` must be defined.\n    element_shape: (Optional.) A `TensorShape` representing the shape of a\n      row of `input_tensor`, if it cannot be inferred.\n    num_epochs: (Optional.) An integer. If specified `input_producer` produces\n      each row of `input_tensor` `num_epochs` times before generating an\n      `OutOfRange` error. If not specified, `input_producer` can cycle through\n      the rows of `input_tensor` an unlimited number of times.\n    shuffle: (Optional.) A boolean. If true, the rows are randomly shuffled\n      within each eopch.\n    seed: (Optional.) An integer. The seed to use if `shuffle` is true.\n    capacity: (Optional.) The capacity of the queue to be used for buffering\n      the input.\n    shared_name: (Optional.) If set, this queue will be shared under the given\n      name across multiple sessions.\n    summary_name: (Optional.) If set, a scalar summary for the current queue\n      size will be generated, using this name as part of the tag.\n    name: (Optional.) A name for queue.\n\n  Returns:\n    A queue with the output rows.  A `QueueRunner` for the queue is\n    added to the current `QUEUE_RUNNER` collection of the current\n    graph.\n\n  Raises:\n    ValueError: If the shape of the input cannot be inferred from the arguments.\n  '
    with ops.op_scope([input_tensor], name, 'input_producer'):
        input_tensor = ops.convert_to_tensor(input_tensor, name='input_tensor')
        element_shape = input_tensor.get_shape()[1:].merge_with(element_shape)
        if (not element_shape.is_fully_defined()):
            raise ValueError('Either `input_tensor` must have a fully defined shape or `element_shape` must be specified')
        if shuffle:
            input_tensor = random_ops.random_shuffle(input_tensor, seed=seed)
        input_tensor = limit_epochs(input_tensor, num_epochs)
        q = data_flow_ops.FIFOQueue(capacity=capacity, dtypes=[input_tensor.dtype.base_dtype], shapes=[element_shape], shared_name=shared_name, name=name)
        enq = q.enqueue_many([input_tensor])
        queue_runner.add_queue_runner(queue_runner.QueueRunner(q, [enq]))
        if (summary_name is not None):
            logging_ops.scalar_summary(('queue/%s/%s' % (q.name, summary_name)), (math_ops.cast(q.size(), dtypes.float32) * (1.0 / capacity)))
        return q