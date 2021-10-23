@ignore_warnings(category=(DeprecationWarning, FutureWarning))
def check_transformers_unfitted(name, transformer):
    (X, y) = _boston_subset()
    transformer = clone(transformer)
    assert_raises((AttributeError, ValueError), transformer.transform, X)