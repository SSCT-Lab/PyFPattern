@register_make_test_function()
def make_slice_tests(options):
    'Make a set of tests to do slice.'
    test_parameters = [{
        'dtype': [tf.float32, tf.int32, tf.int64],
        'index_type': [tf.int32, tf.int64],
        'input_shape': [[12, 2, 2, 5]],
        'begin': [[0, 0, 0, 0], [1, 0, 1, 0]],
        'size': [[8, 2, 2, 3], [11, 2, 1, 5]],
    }, {
        'dtype': [tf.float32, tf.int32, tf.int64],
        'index_type': [tf.int32, tf.int64],
        'input_shape': [[2, 3]],
        'begin': [[0, 0], [1, 0]],
        'size': [[2, 3], [2, 2]],
    }, {
        'dtype': [tf.float32],
        'index_type': [tf.int32],
        'input_shape': [[4, 4, 4, 4]],
        'begin': [[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        'size': [[(- 1), 1, 1, 1], [1, (- 1), 1, 1], [1, 1, (- 1), 1], [1, 1, 1, (- 1)]],
    }]

    def build_graph(parameters):
        'Build graph for slice test.'
        input_tensor = tf.placeholder(dtype=parameters['dtype'], name='input', shape=parameters['input_shape'])
        begin = tf.placeholder(dtype=parameters['index_type'], name='begin', shape=[len(parameters['input_shape'])])
        size = tf.placeholder(dtype=parameters['index_type'], name='size', shape=[len(parameters['input_shape'])])
        tensors = [input_tensor, begin, size]
        out = tf.slice(input_tensor, begin, size)
        return (tensors, [out])

    def build_inputs(parameters, sess, inputs, outputs):
        'Build inputs for slice test.'
        input_values = create_tensor_data(parameters['dtype'], parameters['input_shape'])
        index_type = _TF_TYPE_INFO[parameters['index_type']][0]
        begin_values = np.array(parameters['begin']).astype(index_type)
        size_values = np.array(parameters['size']).astype(index_type)
        values = [input_values, begin_values, size_values]
        return (values, sess.run(outputs, feed_dict=dict(zip(inputs, values))))
    make_zip_of_tests(options, test_parameters, build_graph, build_inputs, expected_tf_failures=18)