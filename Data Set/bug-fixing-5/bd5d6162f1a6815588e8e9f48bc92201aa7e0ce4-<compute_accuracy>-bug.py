def compute_accuracy(predictions, labels):
    'Compute classification accuracy with a fixed threshold on distances.\n    '
    return labels[(predictions.ravel() < 0.5)].mean()