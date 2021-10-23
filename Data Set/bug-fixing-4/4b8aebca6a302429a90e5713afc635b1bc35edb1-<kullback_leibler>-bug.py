def kullback_leibler(vec1, vec2, num_features=None):
    '\n    A distance metric between two probability distributions.\n    Returns a distance value in range <0, +∞> where values closer to 0 mean less distance (and a higher similarity)\n    Uses the scipy.stats.entropy method to identify kullback_leibler convergence value.\n    If the distribution draws from a certain number of docs, that value must be passed.\n    '
    (vec1, vec2) = convert_vec(vec1, vec2, num_features=num_features)
    return entropy(vec1, vec2)