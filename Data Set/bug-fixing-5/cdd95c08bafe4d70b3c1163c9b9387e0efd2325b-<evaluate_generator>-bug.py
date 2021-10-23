@interfaces.legacy_generator_methods_support
def evaluate_generator(self, generator, steps=None, max_queue_size=10, workers=1, use_multiprocessing=False):
    "Evaluates the model on a data generator.\n\n        The generator should return the same kind of data\n        as accepted by `test_on_batch`.\n\n        # Arguments\n            generator: Generator yielding tuples (inputs, targets)\n                or (inputs, targets, sample_weights)\n                or an instance of Sequence (keras.utils.Sequence)\n                    object in order to avoid duplicate data\n                    when using multiprocessing.\n            steps: Total number of steps (batches of samples)\n                to yield from `generator` before stopping.\n                Optional for `Sequence`: if unspecified, will use\n                the `len(generator)` as a number of steps.\n            max_queue_size: maximum size for the generator queue\n            workers: Integer. Maximum number of processes to spin up\n                when using process based threading.\n                If unspecified, `workers` will default to 1. If 0, will\n                execute the generator on the main thread.\n            use_multiprocessing: if True, use process based threading.\n                Note that because\n                this implementation relies on multiprocessing,\n                you should not pass\n                non picklable arguments to the generator\n                as they can't be passed\n                easily to children processes.\n\n        # Returns\n            Scalar test loss (if the model has a single output and no metrics)\n            or list of scalars (if the model has multiple outputs\n            and/or metrics). The attribute `model.metrics_names` will give you\n            the display labels for the scalar outputs.\n\n        # Raises\n            ValueError: In case the generator yields\n                data in an invalid format.\n        "
    self._make_test_function()
    steps_done = 0
    wait_time = 0.01
    all_outs = []
    batch_sizes = []
    is_sequence = isinstance(generator, Sequence)
    if ((not is_sequence) and use_multiprocessing and (workers > 1)):
        warnings.warn(UserWarning('Using a generator with `use_multiprocessing=True` and multiple workers may duplicate your data. Please consider using the`keras.utils.Sequence class.'))
    if (steps is None):
        if is_sequence:
            steps = len(generator)
        else:
            raise ValueError('`steps=None` is only valid for a generator based on the `keras.utils.Sequence` class. Please specify `steps` or use the `keras.utils.Sequence` class.')
    enqueuer = None
    try:
        if (workers > 0):
            if is_sequence:
                enqueuer = OrderedEnqueuer(generator, use_multiprocessing=use_multiprocessing)
            else:
                enqueuer = GeneratorEnqueuer(generator, use_multiprocessing=use_multiprocessing, wait_time=wait_time)
            enqueuer.start(workers=workers, max_queue_size=max_queue_size)
            output_generator = enqueuer.get()
        else:
            output_generator = generator
        while (steps_done < steps):
            generator_output = next(output_generator)
            if (not hasattr(generator_output, '__len__')):
                raise ValueError(('Output of generator should be a tuple (x, y, sample_weight) or (x, y). Found: ' + str(generator_output)))
            if (len(generator_output) == 2):
                (x, y) = generator_output
                sample_weight = None
            elif (len(generator_output) == 3):
                (x, y, sample_weight) = generator_output
            else:
                raise ValueError(('Output of generator should be a tuple (x, y, sample_weight) or (x, y). Found: ' + str(generator_output)))
            outs = self.test_on_batch(x, y, sample_weight=sample_weight)
            if isinstance(x, list):
                batch_size = len(x[0])
            elif isinstance(x, dict):
                batch_size = len(list(x.values())[0])
            else:
                batch_size = len(x)
            if (batch_size == 0):
                raise ValueError('Received an empty batch. Batches should at least contain one item.')
            all_outs.append(outs)
            steps_done += 1
            batch_sizes.append(batch_size)
    finally:
        if (enqueuer is not None):
            enqueuer.stop()
    if (not isinstance(outs, list)):
        return np.average(np.asarray(all_outs), weights=batch_sizes)
    else:
        averages = []
        for i in range(len(outs)):
            averages.append(np.average([out[i] for out in all_outs], weights=batch_sizes))
        return averages