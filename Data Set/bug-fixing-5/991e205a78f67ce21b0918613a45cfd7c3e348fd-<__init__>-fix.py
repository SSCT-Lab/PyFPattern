def __init__(self, input_rows, input_cols, n_components, unobserved_weight=0.1, regularization=None, row_init='random', col_init='random', num_row_shards=1, num_col_shards=1, row_weights=1, col_weights=1, use_factors_weights_cache=True, use_gramian_cache=True):
    'Creates model for WALS matrix factorization.\n\n    Args:\n      input_rows: total number of rows for input matrix.\n      input_cols: total number of cols for input matrix.\n      n_components: number of dimensions to use for the factors.\n      unobserved_weight: weight given to unobserved entries of matrix.\n      regularization: weight of L2 regularization term. If None, no\n        regularization is done.\n      row_init: initializer for row factor. Can be a tensor or numpy constant.\n        If set to "random", the value is initialized randomly.\n      col_init: initializer for column factor. See row_init for details.\n      num_row_shards: number of shards to use for row factors.\n      num_col_shards: number of shards to use for column factors.\n      row_weights: Must be in one of the following three formats: None, a list\n        of lists of non-negative real numbers (or equivalent iterables) or a\n        single non-negative real number.\n        - When set to None, w_ij = unobserved_weight, which simplifies to ALS.\n        Note that col_weights must also be set to "None" in this case.\n        - If it is a list of lists of non-negative real numbers, it needs to be\n        in the form of \\([[w_0, w_1, ...], [w_k, ... ], [...]]\\), with the\n        number of inner lists matching the number of row factor shards and the\n        elements in each inner list are the weights for the rows of the\n        corresponding row factor shard. In this case,  \\(w_ij\\) =\n        unobserved_weight + row_weights[i] * col_weights[j].\n        - If this is a single non-negative real number, this value is used for\n        all row weights and \\(w_ij\\) = unobserved_weight + row_weights *\n                                   col_weights[j].\n        Note that it is allowed to have row_weights as a list while col_weights\n        a single number or vice versa.\n      col_weights: See row_weights.\n      use_factors_weights_cache: When True, the factors and weights will be\n        cached on the workers before the updates start. Defaults to True. Note\n        that the weights cache is initialized through `worker_init`, and the\n        row/col factors cache is initialized through\n        `initialize_{col/row}_update_op`. In the case where the weights are\n        computed outside and set before the training iterations start, it is\n        important to ensure the `worker_init` op is run afterwards for the\n        weights cache to take effect.\n      use_gramian_cache: When True, the Gramians will be cached on the workers\n        before the updates start. Defaults to True.\n    '
    self._input_rows = input_rows
    self._input_cols = input_cols
    self._num_row_shards = num_row_shards
    self._num_col_shards = num_col_shards
    self._n_components = n_components
    self._unobserved_weight = unobserved_weight
    self._regularization = regularization
    self._regularization_matrix = ((regularization * linalg_ops.eye(self._n_components)) if (regularization is not None) else None)
    assert ((row_weights is None) == (col_weights is None))
    self._row_weights = WALSModel._create_weights(row_weights, self._input_rows, self._num_row_shards, 'row_weights')
    self._col_weights = WALSModel._create_weights(col_weights, self._input_cols, self._num_col_shards, 'col_weights')
    self._use_factors_weights_cache = use_factors_weights_cache
    self._use_gramian_cache = use_gramian_cache
    self._row_factors = self._create_factors(self._input_rows, self._n_components, self._num_row_shards, row_init, 'row_factors')
    self._col_factors = self._create_factors(self._input_cols, self._n_components, self._num_col_shards, col_init, 'col_factors')
    self._row_gramian = self._create_gramian(self._n_components, 'row_gramian')
    self._col_gramian = self._create_gramian(self._n_components, 'col_gramian')
    self._row_update_prep_gramian = self._prepare_gramian(self._col_factors, self._col_gramian)
    self._col_update_prep_gramian = self._prepare_gramian(self._row_factors, self._row_gramian)
    self._create_transient_vars()