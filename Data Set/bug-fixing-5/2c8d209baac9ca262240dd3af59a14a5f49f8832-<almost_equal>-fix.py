def almost_equal(a, b, threshold=None):
    'Test if two numpy arrays are almost equal.'
    threshold = (threshold or default_numerical_threshold())
    rel = reldiff(a, b)
    return ((not np.isnan(rel)) and (rel <= threshold))