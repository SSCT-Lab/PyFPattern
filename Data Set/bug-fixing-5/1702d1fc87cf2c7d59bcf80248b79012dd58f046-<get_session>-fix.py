def get_session():
    'Returns the TF session to be used by the backend.\n\n    If a default TensorFlow session is available, we will return it.\n\n    Else, we will return the global Keras session.\n\n    If no global Keras session exists at this point:\n    we will create a new global session.\n\n    Note that you can manually set the global session\n    via `K.set_session(sess)`.\n\n    # Returns\n        A TensorFlow session.\n    '
    global _SESSION
    if (tf.get_default_session() is not None):
        session = tf.get_default_session()
    else:
        if (_SESSION is None):
            if (not os.environ.get('OMP_NUM_THREADS')):
                config = tf.ConfigProto(allow_soft_placement=True)
            else:
                num_thread = int(os.environ.get('OMP_NUM_THREADS'))
                config = tf.ConfigProto(intra_op_parallelism_threads=num_thread, allow_soft_placement=True)
            _SESSION = tf.Session(config=config)
        session = _SESSION
    if (not _MANUAL_VAR_INIT):
        with session.graph.as_default():
            variables = tf.global_variables()
            candidate_vars = []
            for v in variables:
                if (not getattr(v, '_keras_initialized', False)):
                    candidate_vars.append(v)
            if candidate_vars:
                is_initialized = session.run([tf.is_variable_initialized(v) for v in candidate_vars])
                uninitialized_vars = []
                for (flag, v) in zip(is_initialized, candidate_vars):
                    if (not flag):
                        uninitialized_vars.append(v)
                    v._keras_initialized = True
                if uninitialized_vars:
                    session.run(tf.variables_initializer(uninitialized_vars))
    if (not hasattr(session, 'list_devices')):
        session.list_devices = (lambda : device_lib.list_local_devices())
    return session