def cossim(vec1, vec2):
    '\n    Return cosine similarity between two sparse vectors.\n    The similarity is a number between <-1.0, 1.0>, higher is more similar.\n    '
    (vec1, vec2) = (dict(vec1), dict(vec2))
    if ((not vec1) or (not vec2)):
        return 0.0
    vec1len = (1.0 * math.sqrt(sum(((val * val) for val in itervalues(vec1)))))
    vec2len = (1.0 * math.sqrt(sum(((val * val) for val in itervalues(vec2)))))
    assert ((vec1len > 0.0) and (vec2len > 0.0)), 'sparse documents must not contain any explicit zero entries'
    if (len(vec2) < len(vec1)):
        (vec1, vec2) = (vec2, vec1)
    result = sum(((value * vec2.get(index, 0.0)) for (index, value) in iteritems(vec1)))
    result /= (vec1len * vec2len)
    return result