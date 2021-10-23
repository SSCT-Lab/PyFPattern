

def clear_session():
    'Destroys the current TF graph and creates a new one.\n\n    Useful to avoid clutter from old models / layers.\n    '
    global _SESSION
    global _GRAPH_LEARNING_PHASES
    tf.reset_default_graph()
    reset_uids()
    _SESSION = None
    phase = tf.placeholder(dtype='bool', name='keras_learning_phase')
    _GRAPH_LEARNING_PHASES[tf.get_default_graph()] = phase
