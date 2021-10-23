def in_train_phase(x, alt, training=None):
    'Selects `x` in train phase, and `alt` otherwise.\n\n    Note that `alt` should have the *same shape* as `x`.\n\n    # Arguments\n        x: What to return in train phase\n            (tensor or callable that returns a tensor).\n        alt: What to return otherwise\n            (tensor or callable that returns a tensor).\n        training: Optional scalar tensor\n            (or Python boolean, or Python integer)\n            specifying the learning phase.\n\n    # Returns\n        Either `x` or `alt` based on the `training` flag.\n        the `training` flag defaults to `K.learning_phase()`.\n    '
    if (training is None):
        training = learning_phase()
        uses_learning_phase = True
    else:
        uses_learning_phase = False
    if ((training is 1) or (training is True)):
        if callable(x):
            return x()
        else:
            return x
    elif ((training is 0) or (training is False)):
        if callable(alt):
            return alt()
        else:
            return alt
    x = switch(training, x, alt)
    if uses_learning_phase:
        x._uses_learning_phase = True
    return x