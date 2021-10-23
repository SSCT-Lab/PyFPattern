def check_num_samples(ins, batch_size=None, steps=None, steps_name='steps'):
    "Checks the number of samples provided for training and evaluation.\n\n    The number of samples is not defined when running with `steps`,\n    in which case the number of samples is set to `None`.\n\n    # Arguments\n        ins: List of tensors to be fed to the Keras function.\n        batch_size: Integer batch size or `None` if not defined.\n        steps: Total number of steps (batches of samples)\n            before declaring `predict_loop` finished.\n            Ignored with the default value of `None`.\n        steps_name: The public API's parameter name for `steps`.\n\n    # Raises\n        ValueError: when `steps` is `None` and the attribute `ins.shape`\n        does not exist. Also raises ValueError when `steps` is not `None`\n        and `batch_size` is not `None` because they are mutually\n        exclusive.\n\n    # Returns\n        When steps is `None`, returns the number of samples to be\n        processed based on the size of the first dimension of the\n        first input numpy array. When steps is not `None` and\n        `batch_size` is `None`, returns `None`.\n\n    # Raises\n        ValueError: In case of invalid arguments.\n    "
    if ((steps is not None) and (batch_size is not None)):
        raise ValueError((('If ' + steps_name) + ' is set, the `batch_size` must be None.'))
    if ((not ins) or any((K.is_tensor(x) for x in ins))):
        if (steps is None):
            raise ValueError((('If your data is in the form of symbolic tensors, you should specify the `' + steps_name) + '` argument (instead of the `batch_size` argument, because symbolic tensors are expected to produce batches of input data).'))
        return None
    if hasattr(ins[0], 'shape'):
        return int(ins[0].shape[0])
    return None