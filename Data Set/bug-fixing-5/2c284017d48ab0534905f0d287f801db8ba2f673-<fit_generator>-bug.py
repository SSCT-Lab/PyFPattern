@interfaces.legacy_generator_methods_support
def fit_generator(self, generator, steps_per_epoch, epochs=1, verbose=1, callbacks=None, validation_data=None, validation_steps=None, class_weight=None, max_q_size=10, workers=1, pickle_safe=False, initial_epoch=0):
    "Fits the model on data yielded batch-by-batch by a Python generator.\n\n        The generator is run in parallel to the model, for efficiency.\n        For instance, this allows you to do real-time data augmentation\n        on images on CPU in parallel to training your model on GPU.\n\n        # Arguments\n            generator: a generator.\n                The output of the generator must be either\n                - a tuple (inputs, targets)\n                - a tuple (inputs, targets, sample_weights).\n                All arrays should contain the same number of samples.\n                The generator is expected to loop over its data\n                indefinitely. An epoch finishes when `steps_per_epoch`\n                samples have been seen by the model.\n            steps_per_epoch: Total number of steps (batches of samples)\n                to yield from `generator` before declaring one epoch\n                finished and starting the next epoch. It should typically\n                be equal to the number of unique samples if your dataset\n                divided by the batch size.\n            epochs: integer, total number of iterations on the data.\n            verbose: verbosity mode, 0, 1, or 2.\n            callbacks: list of callbacks to be called during training.\n            validation_data: this can be either\n                - a generator for the validation data\n                - a tuple (inputs, targets)\n                - a tuple (inputs, targets, sample_weights).\n            validation_steps: Only relevant if `validation_data`\n                is a generator. Total number of steps (batches of samples)\n                to yield from `generator` before stopping.\n            class_weight: dictionary mapping class indices to a weight\n                for the class.\n            max_q_size: maximum size for the generator queue\n            workers: maximum number of processes to spin up\n                when using process based threading\n            pickle_safe: if True, use process based threading.\n                Note that because\n                this implementation relies on multiprocessing,\n                you should not pass\n                non picklable arguments to the generator\n                as they can't be passed\n                easily to children processes.\n            initial_epoch: epoch at which to start training\n                (useful for resuming a previous training run)\n\n        # Returns\n            A `History` object.\n\n        # Example\n\n        ```python\n            def generate_arrays_from_file(path):\n                while 1:\n                    f = open(path)\n                    for line in f:\n                        # create numpy arrays of input data\n                        # and labels, from each line in the file\n                        x1, x2, y = process_line(line)\n                        yield ({'input_1': x1, 'input_2': x2}, {'output': y})\n                    f.close()\n\n            model.fit_generator(generate_arrays_from_file('/my_file.txt'),\n                                steps_per_epoch=10000, epochs=10)\n        ```\n\n        # Raises\n            ValueError: In case the generator yields\n                data in an invalid format.\n        "
    wait_time = 0.01
    epoch = initial_epoch
    do_validation = bool(validation_data)
    self._make_train_function()
    if do_validation:
        self._make_test_function()
    val_gen = (hasattr(validation_data, 'next') or hasattr(validation_data, '__next__'))
    if (val_gen and (not validation_steps)):
        raise ValueError('When using a generator for validation data, you must specify a value for `validation_steps`.')
    out_labels = self.metrics_names
    callback_metrics = (out_labels + [('val_' + n) for n in out_labels])
    self.history = cbks.History()
    callbacks = (([cbks.BaseLogger()] + (callbacks or [])) + [self.history])
    if verbose:
        callbacks += [cbks.ProgbarLogger(count_mode='steps')]
    callbacks = cbks.CallbackList(callbacks)
    if (hasattr(self, 'callback_model') and self.callback_model):
        callback_model = self.callback_model
    else:
        callback_model = self
    callbacks.set_model(callback_model)
    callbacks.set_params({
        'epochs': epochs,
        'steps': steps_per_epoch,
        'verbose': verbose,
        'do_validation': do_validation,
        'metrics': callback_metrics,
    })
    callbacks.on_train_begin()
    if (do_validation and (not val_gen)):
        if (len(validation_data) == 2):
            (val_x, val_y) = validation_data
            val_sample_weight = None
        elif (len(validation_data) == 3):
            (val_x, val_y, val_sample_weight) = validation_data
        else:
            raise ValueError(('validation_data should be a tuple `(val_x, val_y, val_sample_weight)` or `(val_x, val_y)`. Found: ' + str(validation_data)))
        (val_x, val_y, val_sample_weights) = self._standardize_user_data(val_x, val_y, val_sample_weight)
        for cbk in callbacks:
            cbk.validation_data = (val_x + [val_y, val_sample_weights])
    enqueuer = None
    try:
        enqueuer = GeneratorEnqueuer(generator, pickle_safe=pickle_safe)
        enqueuer.start(max_q_size=max_q_size, workers=workers)
        callback_model.stop_training = False
        while (epoch < epochs):
            callbacks.on_epoch_begin(epoch)
            steps_done = 0
            batch_index = 0
            while (steps_done < steps_per_epoch):
                generator_output = None
                while enqueuer.is_running():
                    if (not enqueuer.queue.empty()):
                        generator_output = enqueuer.queue.get()
                        break
                    else:
                        time.sleep(wait_time)
                if (not hasattr(generator_output, '__len__')):
                    raise ValueError(('output of generator should be a tuple `(x, y, sample_weight)` or `(x, y)`. Found: ' + str(generator_output)))
                if (len(generator_output) == 2):
                    (x, y) = generator_output
                    sample_weight = None
                elif (len(generator_output) == 3):
                    (x, y, sample_weight) = generator_output
                else:
                    raise ValueError(('output of generator should be a tuple `(x, y, sample_weight)` or `(x, y)`. Found: ' + str(generator_output)))
                batch_logs = {
                    
                }
                if isinstance(x, list):
                    batch_size = x[0].shape[0]
                elif isinstance(x, dict):
                    batch_size = list(x.values())[0].shape[0]
                else:
                    batch_size = x.shape[0]
                batch_logs['batch'] = batch_index
                batch_logs['size'] = batch_size
                callbacks.on_batch_begin(batch_index, batch_logs)
                outs = self.train_on_batch(x, y, sample_weight=sample_weight, class_weight=class_weight)
                if (not isinstance(outs, list)):
                    outs = [outs]
                for (l, o) in zip(out_labels, outs):
                    batch_logs[l] = o
                callbacks.on_batch_end(batch_index, batch_logs)
                epoch_logs = {
                    
                }
                batch_index += 1
                steps_done += 1
                if ((steps_done >= steps_per_epoch) and do_validation):
                    if val_gen:
                        val_outs = self.evaluate_generator(validation_data, validation_steps, max_q_size=max_q_size, workers=workers, pickle_safe=pickle_safe)
                    else:
                        val_outs = self.evaluate(val_x, val_y, batch_size=batch_size, sample_weight=val_sample_weights, verbose=0)
                    if (not isinstance(val_outs, list)):
                        val_outs = [val_outs]
                    for (l, o) in zip(out_labels, val_outs):
                        epoch_logs[('val_' + l)] = o
            callbacks.on_epoch_end(epoch, epoch_logs)
            epoch += 1
            if callback_model.stop_training:
                break
    finally:
        if (enqueuer is not None):
            enqueuer.stop()
    callbacks.on_train_end()
    return self.history