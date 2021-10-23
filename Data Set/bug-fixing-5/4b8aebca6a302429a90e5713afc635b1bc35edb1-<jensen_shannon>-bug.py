def jensen_shannon(vec1, vec2, num_features=None):
    '\n    A method of measuring the similarity between two probability distributions.\n    It is a symmetrized and finite version of the Kullback–Leibler divergence.\n    '
    (vec1, vec2) = convert_vec(vec1, vec2, num_features=num_features)
    avg_vec = (0.5 * (vec1 + vec2))
    return (0.5 * (entropy(vec1, avg_vec) + entropy(vec2, avg_vec)))