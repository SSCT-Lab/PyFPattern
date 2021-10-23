def compute_accuracy(predictions, labels):
    'Compute classification accuracy with a fixed threshold on distances.\n    '
    preds = (predictions.ravel() < 0.5)
    return (((preds & labels).sum() + (np.logical_not(preds) & np.logical_not(labels)).sum()) / float(labels.size))