

def compile(self, optimizer, loss, metrics=[], loss_weights=None, sample_weight_mode=None, **kwargs):
    'Configures the model for training.\n\n        # Arguments\n            optimizer: str (name of optimizer) or optimizer object.\n                See [optimizers](/optimizers).\n            loss: str (name of objective function) or objective function.\n                See [objectives](/objectives).\n                If the model has multiple outputs, you can use a different loss\n                on each output by passing a dictionary or a list of objectives.\n            metrics: list of metrics to be evaluated by the model\n                during training and testing.\n                Typically you will use `metrics=[\'accuracy\']`.\n                To specify different metrics for different outputs of a\n                multi-output model, you could also pass a dictionary,\n                such as `metrics={\'output_a\': \'accuracy\'}`.\n            sample_weight_mode: if you need to do timestep-wise\n                sample weighting (2D weights), set this to "temporal".\n                "None" defaults to sample-wise weights (1D).\n                If the model has multiple outputs, you can use a different\n                `sample_weight_mode` on each output by passing a\n                dictionary or a list of modes.\n            kwargs: when using the Theano backend, these arguments\n                are passed into K.function. Ignored for Tensorflow backend.\n        '
    self.optimizer = optimizers.get(optimizer)
    self.sample_weight_mode = sample_weight_mode
    self.loss = loss
    self.loss_weights = loss_weights
    if (loss_weights is None):
        loss_weights_list = [1.0 for _ in range(len(self.outputs))]
    elif (type(loss_weights) is dict):
        for name in loss_weights:
            if (name not in self.output_names):
                raise Exception(((('Unknown entry in loss_weights dictionary: "' + name) + '". Only expected the following keys: ') + str(self.output_names)))
        loss_weights_list = []
        for name in self.output_names:
            loss_weights_list.append(loss_weights.get(name, 1.0))
    elif (type(loss_weights) is list):
        if (len(loss_weights) != len(self.outputs)):
            raise Exception(((('When passing a list as loss_weights, it should have one entry per model outputs. The model has ' + str(len(self.outputs))) + ' outputs, but you passed loss_weights=') + str(loss_weights)))
        loss_weights_list = loss_weights
    else:
        raise Exception(('Could not interpret loss_weights argument: ' + str(loss_weights)))
    if (type(loss) is dict):
        for name in loss:
            if (name not in self.output_names):
                raise Exception(((('Unknown entry in loss dictionary: "' + name) + '". Only expected the following keys: ') + str(self.output_names)))
        loss_functions = []
        for name in self.output_names:
            if (name not in loss):
                raise Exception((('Output "' + name) + '" missing from loss dictionary'))
            loss_functions.append(objectives.get(loss[name]))
    elif (type(loss) is list):
        if (len(loss) != len(self.outputs)):
            raise Exception(((('When passing a list as loss, it should have one entry per model outputs. The model has ' + str(len(self.outputs))) + ' outputs, but you passed loss=') + str(loss)))
        loss_functions = [objectives.get(l) for l in loss]
    else:
        loss_function = objectives.get(loss)
        loss_functions = [loss_function for _ in range(len(self.outputs))]
    self.loss_functions = loss_functions
    weighted_losses = [weighted_objective(fn) for fn in loss_functions]
    masks = self.compute_mask(self.inputs, mask=None)
    if (masks is None):
        masks = [None for _ in self.outputs]
    if (type(masks) is not list):
        masks = [masks]
    if (type(sample_weight_mode) is dict):
        for name in sample_weight_mode:
            if (name not in self.output_names):
                raise Exception(((('Unknown entry in sample_weight_mode dictionary: "' + name) + '". Only expected the following keys: ') + str(self.output_names)))
        sample_weights = []
        sample_weight_modes = []
        for name in self.output_names:
            if (name not in sample_weight_mode):
                raise Exception((('Output "' + name) + '" missing from sample_weight_modes dictionary'))
            if (sample_weight_mode.get(name) == 'temporal'):
                weight = K.placeholder(ndim=2, name=(name + '_sample_weights'))
                sample_weight_modes.append('temporal')
            else:
                weight = K.placeholder(ndim=1, name=(name + '_sample_weights'))
                sample_weight_modes.append(None)
            sample_weights.append(weight)
    elif (type(sample_weight_mode) is list):
        if (len(sample_weight_mode) != len(self.outputs)):
            raise Exception((((('When passing a list as sample_weight_mode, ' + 'it should have one entry per model outputs. The model has ') + str(len(self.outputs))) + ' outputs, but you passed sample_weight_mode=') + str(sample_weight_mode)))
        sample_weights = []
        sample_weight_modes = []
        for (mode, name) in zip(sample_weight_mode, self.output_names):
            if (mode == 'temporal'):
                weight = K.placeholder(ndim=2, name=(name + '_sample_weights'))
                sample_weight_modes.append('temporal')
            else:
                weight = K.placeholder(ndim=1, name=(name + '_sample_weights'))
                sample_weight_modes.append(None)
            sample_weights.append(weight)
    elif (sample_weight_mode == 'temporal'):
        sample_weights = [K.placeholder(ndim=2, name=(name + '_sample_weights')) for name in self.output_names]
        sample_weight_modes = ['temporal' for name in self.output_names]
    else:
        sample_weights = [K.placeholder(ndim=1, name=(name + '_sample_weights')) for name in self.output_names]
        sample_weight_modes = [None for name in self.output_names]
    self.sample_weight_modes = sample_weight_modes
    self.targets = []
    for i in range(len(self.outputs)):
        shape = self.internal_output_shapes[i]
        name = self.output_names[i]
        self.targets.append(K.placeholder(ndim=len(shape), name=(name + '_target')))
    self.metrics_names = ['loss']
    self.metrics = []
    total_loss = None
    for i in range(len(self.outputs)):
        y_true = self.targets[i]
        y_pred = self.outputs[i]
        weighted_loss = weighted_losses[i]
        sample_weight = sample_weights[i]
        mask = masks[i]
        loss_weight = loss_weights_list[i]
        output_loss = weighted_loss(y_true, y_pred, sample_weight, mask)
        if (len(self.outputs) > 1):
            self.metrics.append(output_loss)
            self.metrics_names.append((self.output_names[i] + '_loss'))
        if (total_loss is None):
            total_loss = (loss_weight * output_loss)
        else:
            total_loss += (loss_weight * output_loss)
    for r in self.regularizers:
        total_loss = r(total_loss)
    nested_metrics = collect_metrics(metrics, self.output_names)
    for i in range(len(self.outputs)):
        y_true = self.targets[i]
        y_pred = self.outputs[i]
        output_metrics = nested_metrics[i]
        for metric in output_metrics:
            if ((metric == 'accuracy') or (metric == 'acc')):
                output_shape = self.internal_output_shapes[i]
                if ((output_shape[(- 1)] == 1) or (self.loss_functions[i] == objectives.binary_crossentropy)):
                    self.metrics.append(metrics_module.binary_accuracy(y_true, y_pred))
                elif (self.loss_functions[i] == objectives.sparse_categorical_crossentropy):
                    self.metrics.append(metrics_module.sparse_categorical_accuracy(y_true, y_pred))
                else:
                    self.metrics.append(metrics_module.categorical_accuracy(y_true, y_pred))
                if (len(self.output_names) == 1):
                    self.metrics_names.append('acc')
                else:
                    self.metrics_names.append((self.output_layers[i].name + '_acc'))
            else:
                metric_fn = metrics_module.get(metric)
                self.metrics.append(metric_fn(y_true, y_pred))
                if (len(self.output_names) == 1):
                    self.metrics_names.append(metric_fn.__name__)
                else:
                    self.metrics_names.append(((self.output_layers[i].name + '_') + metric_fn.__name__))
    self.optimizer = optimizers.get(optimizer)
    self.total_loss = total_loss
    self.sample_weights = sample_weights
    self._function_kwargs = kwargs
    self.train_function = None
    self.test_function = None
    self.predict_function = None
