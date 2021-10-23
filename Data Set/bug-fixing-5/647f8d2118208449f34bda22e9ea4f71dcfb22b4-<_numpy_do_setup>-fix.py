def _numpy_do_setup(deterministic=True):
    global _old_python_random_state
    global _old_numpy_random_state
    _old_python_random_state = random.getstate()
    _old_numpy_random_state = numpy.random.get_state()
    if (not deterministic):
        numpy.random.seed()
    else:
        numpy.random.seed(100)