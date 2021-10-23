def test_on_batch(self, x, y, sample_weight=None):
    'Test the model on a single batch of samples.\n\n        # Arguments\n            x: Numpy array of test data,\n                or list of Numpy arrays if the model has multiple inputs.\n                If all inputs in the model are named, you can also pass a dictionary\n                mapping input names to Numpy arrays.\n            y: Numpy array of target data,\n                or list of Numpy arrays if the model has multiple outputs.\n                If all outputs in the model are named, you can also pass a dictionary\n                mapping output names to Numpy arrays.\n            sample_weight: optional array of the same length as x, containing\n                weights to apply to the model\'s loss for each sample.\n                In the case of temporal data, you can pass a 2D array\n                with shape (samples, sequence_length),\n                to apply a different weight to every timestep of every sample.\n                In this case you should make sure to specify sample_weight_mode="temporal" in compile().\n\n        # Returns\n            Scalar test loss (if the model has a single output and no metrics)\n            or list of scalars (if the model has multiple outputs\n            and/or metrics). The attribute `model.metrics_names` will give you\n            the display labels for the scalar outputs.\n        '
    (x, y, sample_weights) = self._standardize_user_data(x, y, sample_weight=sample_weight, check_batch_dim=True)
    if self.uses_learning_phase:
        ins = (((x + y) + sample_weights) + [0.0])
    else:
        ins = ((x + y) + sample_weights)
    outputs = self.test_function(ins)
    if (len(outputs) == 1):
        return outputs[0]
    return outputs