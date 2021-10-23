def _standardize_input_data(data, names, shapes=None, check_batch_axis=True, exception_prefix=''):
    "Normalizes inputs and targets provided by users.\n\n    Users may pass data as a list of arrays, dictionary of arrays,\n    or as a single array. We normalize this to an ordered list of\n    arrays (same order as `names`), while checking that the provided\n    arrays have shapes that match the network's expectations.\n\n    # Arguments\n        data: User-provided input data (polymorphic).\n        names: List of expected array names.\n        shapes: Optional list of expected array shapes.\n        check_batch_axis: Boolean; whether to check that\n            the batch axis of the arrays matches the expected\n            value found in `shapes`.\n        exception_prefix: String prefix used for exception formatting.\n\n    # Returns\n        List of standardized input arrays (one array per model input).\n\n    # Raises\n        ValueError: in case of improperly formatted user-provided data.\n    "
    if (not names):
        return []
    if (data is None):
        return [None for _ in range(len(names))]
    if isinstance(data, dict):
        arrays = []
        for name in names:
            if (name not in data):
                raise ValueError(((('No data provided for "' + name) + '". Need data for each key in: ') + str(names)))
            arrays.append(data[name])
    elif isinstance(data, list):
        if (len(data) != len(names)):
            if (data and hasattr(data[0], 'shape')):
                raise ValueError((((((((('Error when checking model ' + exception_prefix) + ': the list of Numpy arrays that you are passing to your model is not the size the model expected. Expected to see ') + str(len(names))) + ' array(s), but instead got the following list of ') + str(len(data))) + ' arrays: ') + str(data)[:200]) + '...'))
            elif (len(names) == 1):
                data = [np.asarray(data)]
            else:
                raise ValueError(((((('Error when checking model ' + exception_prefix) + ': you are passing a list as input to your model, but the model expects a list of ') + str(len(names))) + ' Numpy arrays instead. The list you passed was: ') + str(data)[:200]))
        arrays = data
    else:
        if (not hasattr(data, 'shape')):
            raise TypeError((((('Error when checking model ' + exception_prefix) + ': data should be a Numpy array, or list/dict of Numpy arrays. Found: ') + str(data)[:200]) + '...'))
        if (len(names) > 1):
            raise ValueError(((((('The model expects ' + str(len(names))) + ' ') + exception_prefix) + ' arrays, but only received one array. Found: array with shape ') + str(data.shape)))
        arrays = [data]
    for i in range(len(names)):
        array = arrays[i]
        if (len(array.shape) == 1):
            array = np.expand_dims(array, 1)
            arrays[i] = array
    if shapes:
        for i in range(len(names)):
            if (shapes[i] is None):
                continue
            array = arrays[i]
            if (len(array.shape) != len(shapes[i])):
                raise ValueError(((((((('Error when checking ' + exception_prefix) + ': expected ') + names[i]) + ' to have ') + str(len(shapes[i]))) + ' dimensions, but got array with shape ') + str(array.shape)))
            for (j, (dim, ref_dim)) in enumerate(zip(array.shape, shapes[i])):
                if ((not j) and (not check_batch_axis)):
                    continue
                if ref_dim:
                    if (ref_dim != dim):
                        raise ValueError(((((((('Error when checking ' + exception_prefix) + ': expected ') + names[i]) + ' to have shape ') + str(shapes[i])) + ' but got array with shape ') + str(array.shape)))
    return arrays