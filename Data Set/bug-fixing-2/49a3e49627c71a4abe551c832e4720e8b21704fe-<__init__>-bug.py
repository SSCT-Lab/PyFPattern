

def __init__(self, loc, covariance_matrix=None, precision_matrix=None, scale_tril=None, validate_args=None):
    event_shape = torch.Size(loc.shape[(- 1):])
    if ((((covariance_matrix is not None) + (scale_tril is not None)) + (precision_matrix is not None)) != 1):
        raise ValueError('Exactly one of covariance_matrix or precision_matrix or scale_tril may be specified.')
    if (scale_tril is not None):
        if (scale_tril.dim() < 2):
            raise ValueError('scale_tril matrix must be at least two-dimensional, with optional leading batch dimensions')
        self.scale_tril = scale_tril
        batch_shape = _get_batch_shape(scale_tril, loc)
    elif (covariance_matrix is not None):
        if (covariance_matrix.dim() < 2):
            raise ValueError('covariance_matrix must be at least two-dimensional, with optional leading batch dimensions')
        self.covariance_matrix = covariance_matrix
        batch_shape = _get_batch_shape(covariance_matrix, loc)
    else:
        if (precision_matrix.dim() < 2):
            raise ValueError('precision_matrix must be at least two-dimensional, with optional leading batch dimensions')
        self.precision_matrix = precision_matrix
        self.covariance_matrix = _batch_inverse(precision_matrix)
        batch_shape = _get_batch_shape(precision_matrix, loc)
    self.loc = loc
    super(MultivariateNormal, self).__init__(batch_shape, event_shape, validate_args=validate_args)
