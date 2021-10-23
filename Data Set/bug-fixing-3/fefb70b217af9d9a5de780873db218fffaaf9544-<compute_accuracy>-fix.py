def compute_accuracy(predictions, labels):
    'Compute classification accuracy with a fixed threshold on distances.\n    '
    return np.mean((labels == (predictions.ravel() > 0.5)))