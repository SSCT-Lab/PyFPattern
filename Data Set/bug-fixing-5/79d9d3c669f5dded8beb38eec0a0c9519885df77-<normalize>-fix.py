def normalize(x):
    'utility function to normalize a tensor.\n\n    # Arguments\n        x: An input tensor.\n\n    # Returns\n        The normalized input tensor.\n    '
    return (x / (K.sqrt(K.mean(K.square(x))) + K.epsilon()))