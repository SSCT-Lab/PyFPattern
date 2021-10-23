def predict_on_batch(self, x):
    'Returns predictions for a single batch of samples.\n        '
    x = standardize_input_data(x, self.input_names, self.internal_input_shapes)
    if self.uses_learning_phase:
        ins = (x + [0.0])
    else:
        ins = x
    outputs = self.predict_function(ins)
    if (len(outputs) == 1):
        return outputs[0]
    return outputs