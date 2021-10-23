@staticmethod
def from_string_handle(string_handle, output_types, output_shapes=None, output_classes=None):
    'Creates a new, uninitialized `Iterator` based on the given handle.\n\n    This method allows you to define a "feedable" iterator where you can choose\n    between concrete iterators by feeding a value in a @{tf.Session.run} call.\n    In that case, `string_handle` would be a @{tf.placeholder}, and you would feed\n    it with the value of @{tf.data.Iterator.string_handle} in each step.\n\n    For example, if you had two iterators that marked the current position in\n    a training dataset and a test dataset, you could choose which to use in\n    each step as follows:\n\n    ```python\n    train_iterator = tf.data.Dataset(...).make_one_shot_iterator()\n    train_iterator_handle = sess.run(train_iterator.string_handle())\n\n    test_iterator = tf.data.Dataset(...).make_one_shot_iterator()\n    test_iterator_handle = sess.run(test_iterator.string_handle())\n\n    handle = tf.placeholder(tf.string, shape=[])\n    iterator = tf.data.Iterator.from_string_handle(\n        handle, train_iterator.output_types)\n\n    next_element = iterator.get_next()\n    loss = f(next_element)\n\n    train_loss = sess.run(loss, feed_dict={handle: train_iterator_handle})\n    test_loss = sess.run(loss, feed_dict={handle: test_iterator_handle})\n    ```\n\n    Args:\n      string_handle: A scalar `tf.Tensor` of type `tf.string` that evaluates\n        to a handle produced by the `Iterator.string_handle()` method.\n      output_types: A nested structure of `tf.DType` objects corresponding to\n        each component of an element of this dataset.\n      output_shapes: (Optional.) A nested structure of `tf.TensorShape` objects\n        corresponding to each component of an element of this dataset. If\n        omitted, each component will have an unconstrainted shape.\n      output_classes: (Optional.) A nested structure of Python `type` objects\n        corresponding to each component of an element of this iterator. If\n        omitted, each component is assumed to be of type `tf.Tensor`.\n\n    Returns:\n      An `Iterator`.\n    '
    output_types = nest.map_structure(dtypes.as_dtype, output_types)
    if (output_shapes is None):
        output_shapes = nest.map_structure((lambda _: tensor_shape.TensorShape(None)), output_types)
    else:
        output_shapes = nest.map_structure_up_to(output_types, tensor_shape.as_shape, output_shapes)
    if (output_classes is None):
        output_classes = nest.map_structure((lambda _: ops.Tensor), output_types)
    nest.assert_same_structure(output_types, output_shapes)
    string_handle = ops.convert_to_tensor(string_handle, dtype=dtypes.string)
    if compat.forward_compatible(2018, 8, 3):
        if (not ops.get_default_graph()._graph_device_function_stack):
            with ops.device('/cpu:0'):
                iterator_resource = gen_dataset_ops.iterator_from_string_handle_v2(string_handle, output_types=nest.flatten(sparse.as_dense_types(output_types, output_classes)), output_shapes=nest.flatten(sparse.as_dense_shapes(output_shapes, output_classes)))
        else:
            iterator_resource = gen_dataset_ops.iterator_from_string_handle_v2(string_handle, output_types=nest.flatten(sparse.as_dense_types(output_types, output_classes)), output_shapes=nest.flatten(sparse.as_dense_shapes(output_shapes, output_classes)))
    else:
        iterator_resource = gen_dataset_ops.iterator_from_string_handle(string_handle, output_types=nest.flatten(sparse.as_dense_types(output_types, output_classes)), output_shapes=nest.flatten(sparse.as_dense_shapes(output_shapes, output_classes)))
    return Iterator(iterator_resource, None, output_types, output_shapes, output_classes)