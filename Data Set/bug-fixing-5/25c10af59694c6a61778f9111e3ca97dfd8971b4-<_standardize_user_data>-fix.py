def _standardize_user_data(self, x, y, sample_weight=None, class_weight=None, check_batch_dim=True, batch_size=None):
    if (not hasattr(self, 'optimizer')):
        raise Exception('You must compile a model before training/testing. Use `model.compile(optimizer, loss)`.')
    output_shapes = self.internal_output_shapes
    if (self.loss == 'sparse_categorical_crossentropy'):
        output_shapes = [(s[:(- 1)] + (1,)) for s in output_shapes]
    x = standardize_input_data(x, self.input_names, self.internal_input_shapes, check_batch_dim=False, exception_prefix='model input')
    y = standardize_input_data(y, self.output_names, output_shapes, check_batch_dim=False, exception_prefix='model target')
    sample_weights = standardize_sample_weights(sample_weight, self.output_names)
    class_weights = standardize_class_weights(class_weight, self.output_names)
    sample_weights = [standardize_weights(ref, sw, cw, mode) for (ref, sw, cw, mode) in zip(y, sample_weights, class_weights, self.sample_weight_modes)]
    check_array_lengths(x, y, sample_weights)
    check_loss_and_target_compatibility(y, self.loss_functions, self.internal_output_shapes)
    if (self.stateful and batch_size):
        if ((x[0].shape[0] % batch_size) != 0):
            raise Exception((('In a stateful network, you should only pass inputs with a number of samples that can be divided by the batch size. Found: ' + str(x[0].shape[0])) + ' samples'))
    return (x, y, sample_weights)