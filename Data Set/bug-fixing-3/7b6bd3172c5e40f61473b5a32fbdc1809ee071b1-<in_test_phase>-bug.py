def in_test_phase(x, alt, training=None):
    'Selects `x` in test phase, and `alt` otherwise.\n\n    Note that `alt` should have the *same shape* as `x`.\n\n    # Arguments\n        x: What to return in test phase\n            (tensor or callable that returns a tensor).\n        alt: What to return otherwise\n            (tensor or callable that returns a tensor).\n        training: Optional scalar tensor\n            (or Python boolean, or Python integer)\n            specifing the learning phase.\n\n    # Returns\n        Either `x` or `alt` based on `K.learning_phase`.\n    '
    return in_train_phase(alt, x, training=training)