def _numpy_do_teardown():
    global _old_numpy_random_state
    numpy.random.set_state(_old_numpy_random_state)
    _old_numpy_random_state = None