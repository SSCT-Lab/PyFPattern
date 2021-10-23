

def standardize_input_data(data, names, shapes=None, check_batch_dim=True, exception_prefix=''):
    "Users may pass data as a list of arrays, dictionary of arrays,\n    or as a single array. We normalize this to an ordered list of\n    arrays (same order as `names`), while checking that the provided\n    arrays have shapes that match the network's expectations.\n    "
    if (type(data) is dict):
        arrays = []
        for name in names:
            if (name not in data):
                raise Exception(((('No data provided for input "' + name) + '". Input data keys: ') + str(data.keys())))
            arrays.append(data[name])
    elif (type(data) is list):
        if (len(data) != len(names)):
            if ((len(data) > 0) and hasattr(data[0], 'shape')):
                raise Exception((((((((('Error when checking ' + exception_prefix) + ': the list of Numpy arrays that you are passing to your model is not the size the model expected. Expected to see ') + str(len(names))) + ' arrays but instead got the following list of ') + str(len(data))) + ' arrays: ') + str(data)[:200]) + '...'))
            elif (len(names) == 1):
                data = [np.asarray(data)]
            else:
                raise Exception(((((('Error when checking ' + exception_prefix) + ': you are passing a list as input to your model, but the model expects a a list of ') + str(len(names))) + ' Numpy arrays instead. The list you passed was: ') + str(data)[:200]))
        arrays = data
    else:
        if (not hasattr(data, 'shape')):
            raise Exception((((('Error when checking ' + exception_prefix) + ': data should be a Numpy array, or list/dict of Numpy arrays. Found: ') + str(data)[:200]) + '...'))
        arrays = [data]
    for i in range(len(names)):
        array = arrays[i]
        if (len(array.shape) == 1):
            array = np.expand_dims(array, 1)
            arrays[i] = array
    if shapes:
        for i in range(len(names)):
            if ((not i) and (not check_batch_dim)):
                continue
            array = arrays[i]
            if (len(array.shape) != len(shapes[i])):
                raise Exception(((((((('Error when checking ' + exception_prefix) + ': expected ') + names[i]) + ' to have ') + str(len(shapes[i]))) + ' dimensions, but got array with shape ') + str(array.shape)))
            for (dim, ref_dim) in zip(array.shape, shapes[i]):
                if ref_dim:
                    if (ref_dim != dim):
                        raise Exception(((((((('Error when checking ' + exception_prefix) + ': expected ') + names[i]) + ' to have shape ') + str(shapes[i])) + ' but got array with shape ') + str(array.shape)))
    return arrays
