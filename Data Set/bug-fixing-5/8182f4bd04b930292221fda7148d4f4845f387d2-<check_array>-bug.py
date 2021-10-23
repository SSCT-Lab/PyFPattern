def check_array(array, accept_sparse=None, dtype='numeric', order=None, copy=False, force_all_finite=True, ensure_2d=True, allow_nd=False, ensure_min_samples=1, ensure_min_features=1, warn_on_dtype=False, estimator=None):
    'Input validation on an array, list, sparse matrix or similar.\n\n    By default, the input is converted to an at least 2nd numpy array.\n    If the dtype of the array is object, attempt converting to float,\n    raising on failure.\n\n    Parameters\n    ----------\n    array : object\n        Input object to check / convert.\n\n    accept_sparse : string, list of string or None (default=None)\n        String[s] representing allowed sparse matrix formats, such as \'csc\',\n        \'csr\', etc.  None means that sparse matrix input will raise an error.\n        If the input is sparse but not in the allowed format, it will be\n        converted to the first listed format.\n\n    dtype : string, type, list of types or None (default="numeric")\n        Data type of result. If None, the dtype of the input is preserved.\n        If "numeric", dtype is preserved unless array.dtype is object.\n        If dtype is a list of types, conversion on the first type is only\n        performed if the dtype of the input is not in the list.\n\n    order : \'F\', \'C\' or None (default=None)\n        Whether an array will be forced to be fortran or c-style.\n\n    copy : boolean (default=False)\n        Whether a forced copy will be triggered. If copy=False, a copy might\n        be triggered by a conversion.\n\n    force_all_finite : boolean (default=True)\n        Whether to raise an error on np.inf and np.nan in X.\n\n    ensure_2d : boolean (default=True)\n        Whether to make X at least 2d.\n\n    allow_nd : boolean (default=False)\n        Whether to allow X.ndim > 2.\n\n    ensure_min_samples : int (default=1)\n        Make sure that the array has a minimum number of samples in its first\n        axis (rows for a 2D array). Setting to 0 disables this check.\n\n    ensure_min_features : int (default=1)\n        Make sure that the 2D array has some minimum number of features\n        (columns). The default value of 1 rejects empty datasets.\n        This check is only enforced when the input data has effectively 2\n        dimensions or is originally 1D and ``ensure_2d`` is True. Setting to 0\n        disables this check.\n\n    warn_on_dtype : boolean (default=False)\n        Raise DataConversionWarning if the dtype of the input data structure\n        does not match the requested dtype, causing a memory copy.\n\n    estimator : str or estimator instance (default=None)\n        If passed, include the name of the estimator in warning messages.\n\n    Returns\n    -------\n    X_converted : object\n        The converted and validated X.\n    '
    if isinstance(accept_sparse, str):
        accept_sparse = [accept_sparse]
    dtype_numeric = (dtype == 'numeric')
    dtype_orig = getattr(array, 'dtype', None)
    if (not hasattr(dtype_orig, 'kind')):
        dtype_orig = None
    if dtype_numeric:
        if ((dtype_orig is not None) and (dtype_orig.kind == 'O')):
            dtype = np.float64
        else:
            dtype = None
    if isinstance(dtype, (list, tuple)):
        if ((dtype_orig is not None) and (dtype_orig in dtype)):
            dtype = None
        else:
            dtype = dtype[0]
    if (estimator is not None):
        if isinstance(estimator, six.string_types):
            estimator_name = estimator
        else:
            estimator_name = estimator.__class__.__name__
    else:
        estimator_name = 'Estimator'
    context = ((' by %s' % estimator_name) if (estimator is not None) else '')
    if sp.issparse(array):
        array = _ensure_sparse_format(array, accept_sparse, dtype, copy, force_all_finite)
    else:
        array = np.array(array, dtype=dtype, order=order, copy=copy)
        if ensure_2d:
            if (array.ndim == 1):
                if (ensure_min_samples >= 2):
                    raise ValueError(('%s expects at least 2 samples provided in a 2 dimensional array-like input' % estimator_name))
                warnings.warn('Passing 1d arrays as data is deprecated in 0.17 and will raise ValueError in 0.19. Reshape your data either using X.reshape(-1, 1) if your data has a single feature or X.reshape(1, -1) if it contains a single sample.', DeprecationWarning)
            array = np.atleast_2d(array)
            array = np.array(array, dtype=dtype, order=order, copy=copy)
        if (dtype_numeric and (array.dtype.kind == 'O')):
            array = array.astype(np.float64)
        if ((not allow_nd) and (array.ndim >= 3)):
            raise ValueError(('Found array with dim %d. %s expected <= 2.' % (array.ndim, estimator_name)))
        if force_all_finite:
            _assert_all_finite(array)
    shape_repr = _shape_repr(array.shape)
    if (ensure_min_samples > 0):
        n_samples = _num_samples(array)
        if (n_samples < ensure_min_samples):
            raise ValueError(('Found array with %d sample(s) (shape=%s) while a minimum of %d is required%s.' % (n_samples, shape_repr, ensure_min_samples, context)))
    if ((ensure_min_features > 0) and (array.ndim == 2)):
        n_features = array.shape[1]
        if (n_features < ensure_min_features):
            raise ValueError(('Found array with %d feature(s) (shape=%s) while a minimum of %d is required%s.' % (n_features, shape_repr, ensure_min_features, context)))
    if (warn_on_dtype and (dtype_orig is not None) and (array.dtype != dtype_orig)):
        msg = ('Data with input dtype %s was converted to %s%s.' % (dtype_orig, array.dtype, context))
        warnings.warn(msg, _DataConversionWarning)
    return array