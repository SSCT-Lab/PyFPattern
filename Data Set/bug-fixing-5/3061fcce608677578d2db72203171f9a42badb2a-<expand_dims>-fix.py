def expand_dims(x, axis=(- 1)):
    'Adds a 1-sized dimension at index "axis".\n\n    # Arguments\n        x: A tensor or variable.\n        axis: Position where to add a new axis.\n\n    # Returns\n        A tensor with expanded dimensions.\n    '
    return tf.expand_dims(x, axis)