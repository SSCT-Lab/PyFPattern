def merge(inputs, collections=None, name=None):
    'Merges summaries.\n\n  This op creates a\n  [`Summary`](https://www.tensorflow.org/code/tensorflow/core/framework/summary.proto)\n  protocol buffer that contains the union of all the values in the input\n  summaries.\n\n  When the Op is run, it reports an `InvalidArgument` error if multiple values\n  in the summaries to merge use the same tag.\n\n  Args:\n    inputs: A list of `string` `Tensor` objects containing serialized `Summary`\n      protocol buffers.\n    collections: Optional list of graph collections keys. The new summary op is\n      added to these collections. Defaults to `[]`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A scalar `Tensor` of type `string`. The serialized `Summary` protocol\n    buffer resulting from the merging.\n  '
    name = _clean_tag(name)
    with _ops.name_scope(name, 'Merge', inputs):
        val = _gen_logging_ops._merge_summary(inputs=inputs, name=name)
        _collect(val, collections, [])
    return val