

def compute_output_shape(self, input_shape):
    'Computes the output shape of the layer.\n\n        Assumes that the layer will be built\n        to match that input shape provided.\n\n        # Arguments\n            input_shape: Shape tuple (tuple of integers)\n                or list of shape tuples (one per output tensor of the layer).\n                Shape tuples can include None for free dimensions,\n                instead of an integer.\n\n        # Returns\n            An input shape tuple.\n        '
    return input_shape
