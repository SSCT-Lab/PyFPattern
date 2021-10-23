def check_array_length_consistency(inputs, targets, weights=None):
    'Checks if batch axes are the same for numpy arrays.\n\n    # Arguments\n        inputs: list of Numpy arrays of inputs.\n        targets: list of Numpy arrays of targets.\n        weights: list of Numpy arrays of sample weights.\n\n    # Raises\n        ValueError: in case of incorrectly formatted data.\n    '

    def set_of_lengths(x):
        if (x is None):
            return {0}
        else:
            return set([(0 if (y is None) else int(y.shape[0])) for y in x])
    set_x = set_of_lengths(inputs)
    set_y = set_of_lengths(targets)
    set_w = set_of_lengths(weights)
    if (len(set_x) > 1):
        raise ValueError(('All input arrays (x) should have the same number of samples. Got array shapes: ' + str([x.shape for x in inputs])))
    if (len(set_y) > 1):
        raise ValueError(('All target arrays (y) should have the same number of samples. Got array shapes: ' + str([y.shape for y in targets])))
    if (set_x and set_y and (list(set_x)[0] != list(set_y)[0])):
        raise ValueError((((('Input arrays should have the same number of samples as target arrays. Found ' + str(list(set_x)[0])) + ' input samples and ') + str(list(set_y)[0])) + ' target samples.'))
    if (len(set_w) > 1):
        raise ValueError(('All sample_weight arrays should have the same number of samples. Got array shapes: ' + str([w.shape for w in weights])))
    if (set_y and set_w and (list(set_y)[0] != list(set_w)[0])):
        raise ValueError((((('Sample_weight arrays should have the same number of samples as target arrays. Got ' + str(list(set_y)[0])) + ' input samples and ') + str(list(set_w)[0])) + ' target samples.'))