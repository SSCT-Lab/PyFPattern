def project_col_factors(self, sp_input=None, transpose_input=False, projection_weights=None):
    'Projects the column factors.\n\n    This computes the column embedding v_j for an observed column a_j by solving\n    one iteration of the update equations.\n\n    Args:\n      sp_input: A SparseTensor representing a set of columns. Please note that\n        the row indices of this SparseTensor must match the model row feature\n        indexing while the column indices are ignored. The returned results will\n        be in the same ordering as the input columns.\n      transpose_input: If true, the input will be logically transposed and the\n        columns corresponding to the transposed input are projected.\n      projection_weights: The column weights to be used for the projection. If\n        None then 1.0 is used. This can be either a scaler or a rank-1 tensor\n        with the number of elements matching the number of columns to be\n        projected. Note that the row weights will be determined by the\n        underlying WALS model.\n\n    Returns:\n      Projected column factors.\n    '
    if (projection_weights is None):
        projection_weights = 1
    return self._process_input_helper(False, sp_input=sp_input, transpose_input=transpose_input, row_weights=projection_weights)[0]