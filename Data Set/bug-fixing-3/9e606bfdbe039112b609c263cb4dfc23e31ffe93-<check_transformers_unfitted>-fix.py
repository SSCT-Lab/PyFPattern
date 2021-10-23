@ignore_warnings(category=(DeprecationWarning, FutureWarning))
def check_transformers_unfitted(name, transformer):
    (X, y) = _boston_subset()
    transformer = clone(transformer)
    with assert_raises((AttributeError, ValueError), msg='The unfitted transformer {} does not raise an error when transform is called. Perhaps use check_is_fitted in transform.'.format(name)):
        transformer.transform(X)