def variable(value, dtype=_FLOATX, name=None):
    'Instantiates a tensor.\n\n    # Arguments\n        value: numpy array, initial value of the tensor.\n        dtype: tensor type.\n        name: optional name string for the tensor.\n\n    # Returns\n        Tensor variable instance.\n    '
    if hasattr(value, 'tocoo'):
        sparse_coo = value.tocoo()
        indices = np.concatenate((np.expand_dims(sparse_coo.row, 1), np.expand_dims(sparse_coo.col, 1)), 1)
        return tf.SparseTensor(indices=indices, values=value.data, shape=value.shape)
    v = tf.Variable(value, dtype=_convert_string_dtype(dtype), name=name)
    if _MANUAL_VAR_INIT:
        return v
    if (tf.get_default_graph() is get_session().graph):
        try:
            get_session().run(v.initializer)
        except tf.errors.InvalidArgumentError:
            warnings.warn('Could not automatically initialize variable, make sure you do it manually (e.g. via `tf.initialize_all_variables()`).')
    else:
        warnings.warn('The default TensorFlow graph is not the graph associated with the TensorFlow session currently registered with Keras, and as such Keras was not able to automatically initialize a variable. You should consider registering the proper session with Keras via `K.set_session(sess)`.')
    return v