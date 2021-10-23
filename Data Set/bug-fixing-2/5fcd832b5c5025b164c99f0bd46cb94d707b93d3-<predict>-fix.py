

def predict(self, x, batch_size=None, verbose=0, steps=None):
    "Generates output predictions for the input samples.\n\n        Computation is done in batches.\n\n        # Arguments\n            x: The input data, as a Numpy array\n                (or list of Numpy arrays if the model has multiple inputs).\n            batch_size: Integer. If unspecified, it will default to 32.\n            verbose: Verbosity mode, 0 or 1.\n            steps: Total number of steps (batches of samples)\n                before declaring the prediction round finished.\n                Ignored with the default value of `None`.\n\n        # Returns\n            Numpy array(s) of predictions.\n\n        # Raises\n            ValueError: In case of mismatch between the provided\n                input data and the model's expectations,\n                or in case a stateful model receives a number of samples\n                that is not a multiple of the batch size.\n        "
    if ((batch_size is None) and (steps is None)):
        batch_size = 32
    if ((x is None) and (steps is None)):
        raise ValueError('If predicting from data tensors, you should specify the `steps` argument.')
    (x, _, _) = self._standardize_user_data(x)
    if self.stateful:
        if ((x[0].shape[0] > batch_size) and ((x[0].shape[0] % batch_size) != 0)):
            raise ValueError((((('In a stateful network, you should only pass inputs with a number of samples that can be divided by the batch size. Found: ' + str(x[0].shape[0])) + ' samples. Batch size: ') + str(batch_size)) + '.'))
    if self._uses_dynamic_learning_phase():
        ins = (x + [0.0])
    else:
        ins = x
    self._make_predict_function()
    f = self.predict_function
    return training_arrays.predict_loop(self, f, ins, batch_size=batch_size, verbose=verbose, steps=steps)
