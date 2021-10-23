def softsign(x):
    'Softsign activation function.\n\n    # Arguments\n        x: Input tensor.\n\n    # Returns\n        The softsign activation: `x / (abs(x) + 1)`.\n    '
    return K.softsign(x)