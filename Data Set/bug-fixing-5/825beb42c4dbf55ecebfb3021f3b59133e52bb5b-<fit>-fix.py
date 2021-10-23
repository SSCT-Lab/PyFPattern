def fit(self, x, y, batch_size=32, nb_epoch=10, verbose=1, callbacks=[], validation_split=0.0, validation_data=None, shuffle=True, class_weight=None, sample_weight=None):
    'Trains the model for a fixed number of epochs (iterations on a dataset).\n\n        # Arguments\n            x: Numpy array of training data,\n                or list of Numpy arrays if the model has multiple inputs.\n                If all inputs in the model are named, you can also pass a dictionary\n                mapping input names to Numpy arrays.\n            y: Numpy array of target data,\n                or list of Numpy arrays if the model has multiple outputs.\n                If all outputs in the model are named, you can also pass a dictionary\n                mapping output names to Numpy arrays.\n            batch_size: integer. Number of samples per gradient update.\n            nb_epoch: integer, the number of times to iterate over the training data arrays.\n            verbose: 0, 1, or 2. Verbosity mode. 0 = silent, 1 = verbose, 2 = one log line per epoch.\n            callbacks: list of callbacks to be called during training.\n                See [callbacks](/callbacks).\n            validation_split: float between 0 and 1:\n                fraction of the training data to be used as validation data.\n                The model will set apart this fraction of the training data,\n                will not train on it, and will evaluate the loss and any model metrics\n                on this data at the end of each epoch.\n            validation_data: data on which to evaluate the loss and any model metrics\n                at the end of each epoch. The model will not be trained on this data.\n                This could be a tuple (x_val, y_val) or a tuple (val_x, val_y, val_sample_weights).\n            shuffle: boolean, whether to shuffle the training data before each epoch.\n            class_weight: optional dictionary mapping class indices (integers) to\n                a weight (float) to apply to the model\'s loss for the samples\n                from this class during training.\n                This can be useful to tell the model to "pay more attention" to\n                samples from an under-represented class.\n            sample_weight: optional array of the same length as x, containing\n                weights to apply to the model\'s loss for each sample.\n                In the case of temporal data, you can pass a 2D array\n                with shape (samples, sequence_length),\n                to apply a different weight to every timestep of every sample.\n                In this case you should make sure to specify sample_weight_mode="temporal" in compile().\n\n\n        # Returns\n            A `History` instance. Its `history` attribute contains\n            all information collected during training.\n        '
    (x, y, sample_weights) = self._standardize_user_data(x, y, sample_weight=sample_weight, class_weight=class_weight, check_batch_dim=False, batch_size=batch_size)
    if validation_data:
        do_validation = True
        if (len(validation_data) == 2):
            (val_x, val_y) = validation_data
            val_sample_weight = None
        elif (len(validation_data) == 3):
            (val_x, val_y, val_sample_weight) = validation_data
        else:
            raise
        (val_x, val_y, val_sample_weights) = self._standardize_user_data(val_x, val_y, sample_weight=val_sample_weight, check_batch_dim=False, batch_size=batch_size)
        self._make_test_function()
        val_f = self.test_function
        if self.uses_learning_phase:
            val_ins = (((val_x + val_y) + val_sample_weights) + [0.0])
        else:
            val_ins = ((val_x + val_y) + val_sample_weights)
    elif (validation_split and (0.0 < validation_split < 1.0)):
        do_validation = True
        split_at = int((len(x[0]) * (1.0 - validation_split)))
        (x, val_x) = (slice_X(x, 0, split_at), slice_X(x, split_at))
        (y, val_y) = (slice_X(y, 0, split_at), slice_X(y, split_at))
        (sample_weights, val_sample_weights) = (slice_X(sample_weights, 0, split_at), slice_X(sample_weights, split_at))
        self._make_test_function()
        val_f = self.test_function
        if self.uses_learning_phase:
            val_ins = (((val_x + val_y) + val_sample_weights) + [0.0])
        else:
            val_ins = ((val_x + val_y) + val_sample_weights)
    else:
        do_validation = False
        val_f = None
        val_ins = None
    if self.uses_learning_phase:
        ins = (((x + y) + sample_weights) + [1.0])
    else:
        ins = ((x + y) + sample_weights)
    self._make_train_function()
    f = self.train_function
    out_labels = self.metrics_names
    new_out_labels = []
    for (i, label) in enumerate(out_labels):
        new_label = label
        if (out_labels.count(label) > 1):
            dup_idx = out_labels[:i].count(label)
            new_label += str((dup_idx + 1))
        new_out_labels.append(new_label)
    out_labels = new_out_labels
    if do_validation:
        callback_metrics = (copy.copy(out_labels) + [('val_' + n) for n in out_labels])
    else:
        callback_metrics = copy.copy(out_labels)
    return self._fit_loop(f, ins, out_labels=out_labels, batch_size=batch_size, nb_epoch=nb_epoch, verbose=verbose, callbacks=callbacks, val_f=val_f, val_ins=val_ins, shuffle=shuffle, callback_metrics=callback_metrics)