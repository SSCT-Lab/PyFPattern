def evaluate(self, x, y, batch_size=None, verbose=1, sample_weight=None, steps=None):
    'Returns the loss value & metrics values for the model in test mode.\n\n        Computation is done in batches.\n\n        # Arguments\n            x: Numpy array of test data,\n                or list of Numpy arrays if the model has multiple inputs.\n                If all inputs in the model are named,\n                you can also pass a dictionary\n                mapping input names to Numpy arrays.\n            y: Numpy array of target data,\n                or list of Numpy arrays if the model has multiple outputs.\n                If all outputs in the model are named,\n                you can also pass a dictionary\n                mapping output names to Numpy arrays.\n            batch_size: Integer. If unspecified, it will default to 32.\n            verbose: Verbosity mode, 0 or 1.\n            sample_weight: Array of weights to weight the contribution\n                of different samples to the loss and metrics.\n            steps: Total number of steps (batches of samples)\n                before declaring the evaluation round finished.\n                Ignored with the default value of `None`.\n\n        # Returns\n            Scalar test loss (if the model has a single output and no metrics)\n            or list of scalars (if the model has multiple outputs\n            and/or metrics). The attribute `model.metrics_names` will give you\n            the display labels for the scalar outputs.\n        '
    if ((batch_size is None) and (steps is None)):
        batch_size = 32
    if ((x is None) and (y is None) and (steps is None)):
        raise ValueError('If evaluating from data tensors, you should specify the `steps` argument.')
    (x, y, sample_weights) = self._standardize_user_data(x, y, sample_weight=sample_weight, check_batch_axis=False, batch_size=batch_size)
    if (self.uses_learning_phase and (not isinstance(K.learning_phase(), int))):
        ins = (((x + y) + sample_weights) + [0.0])
    else:
        ins = ((x + y) + sample_weights)
    self._make_test_function()
    f = self.test_function
    return self._test_loop(f, ins, batch_size=batch_size, verbose=verbose, steps=steps)