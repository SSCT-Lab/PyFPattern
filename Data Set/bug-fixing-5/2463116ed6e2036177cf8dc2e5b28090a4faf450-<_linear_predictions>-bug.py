def _linear_predictions(self, examples):
    'Returns predictions of the form w*x.'
    with name_scope('sdca/prediction'):
        sparse_variables = self._convert_n_to_tensor(self._variables['sparse_features_weights'])
        result = 0.0
        for (sfc, sv) in zip(examples['sparse_features'], sparse_variables):
            result += math_ops.segment_sum(math_ops.multiply(array_ops.gather(sv, sfc.feature_indices), sfc.feature_values), sfc.example_indices)
        dense_features = self._convert_n_to_tensor(examples['dense_features'])
        dense_variables = self._convert_n_to_tensor(self._variables['dense_features_weights'])
        for i in range(len(dense_variables)):
            result += math_ops.matmul(dense_features[i], array_ops.expand_dims(dense_variables[i], (- 1)))
    return array_ops.reshape(result, [(- 1)])