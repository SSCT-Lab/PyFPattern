

def fit(self, train_data, eval_data=None, eval_metric='acc', epoch_end_callback=None, batch_end_callback=None, kvstore='local', optimizer='sgd', optimizer_params=(('learning_rate', 0.01),), eval_end_callback=None, eval_batch_end_callback=None, initializer=Uniform(0.01), arg_params=None, aux_params=None, allow_missing=False, force_rebind=False, force_init=False, begin_epoch=0, num_epoch=None, validation_metric=None, monitor=None, sparse_row_id_fn=None):
    "Trains the module parameters.\n\n        Checkout `Module Tutorial <http://mxnet.io/tutorials/basic/module.html>`_ to see\n        a end-to-end use-case.\n\n        Parameters\n        ----------\n        train_data : DataIter\n            Train DataIter.\n        eval_data : DataIter\n            If not ``None``, will be used as validation set and the performance\n            after each epoch will be evaluated.\n        eval_metric : str or EvalMetric\n            Defaults to 'accuracy'. The performance measure used to display during training.\n            Other possible predefined metrics are:\n            'ce' (CrossEntropy), 'f1', 'mae', 'mse', 'rmse', 'top_k_accuracy'.\n        epoch_end_callback : function or list of functions\n            Each callback will be called with the current `epoch`, `symbol`, `arg_params`\n            and `aux_params`.\n        batch_end_callback : function or list of function\n            Each callback will be called with a `BatchEndParam`.\n        kvstore : str or KVStore\n            Defaults to 'local'.\n        optimizer : str or Optimizer\n            Defaults to 'sgd'.\n        optimizer_params : dict\n            Defaults to ``(('learning_rate', 0.01),)``. The parameters for\n            the optimizer constructor.\n            The default value is not a dict, just to avoid pylint warning on dangerous\n            default values.\n        eval_end_callback : function or list of function\n            These will be called at the end of each full evaluation, with the metrics over\n            the entire evaluation set.\n        eval_batch_end_callback : function or list of function\n            These will be called at the end of each mini-batch during evaluation.\n        initializer : Initializer\n            The initializer is called to initialize the module parameters when they are\n            not already initialized.\n        arg_params : dict\n            Defaults to ``None``, if not ``None``, should be existing parameters from a trained\n            model or loaded from a checkpoint (previously saved model). In this case,\n            the value here will be used to initialize the module parameters, unless they\n            are already initialized by the user via a call to `init_params` or `fit`.\n            `arg_params` has a higher priority than `initializer`.\n        aux_params : dict\n            Defaults to ``None``. Similar to `arg_params`, except for auxiliary states.\n        allow_missing : bool\n            Defaults to ``False``. Indicates whether to allow missing parameters when `arg_params`\n            and `aux_params` are not ``None``. If this is ``True``, then the missing parameters\n            will be initialized via the `initializer`.\n        force_rebind : bool\n            Defaults to ``False``. Whether to force rebinding the executors if already bound.\n        force_init : bool\n            Defaults to ``False``. Indicates whether to force initialization even if the\n            parameters are already initialized.\n        begin_epoch : int\n            Defaults to 0. Indicates the starting epoch. Usually, if resumed from a\n            checkpoint saved at a previous training phase at epoch N, then this value should be\n            N+1.\n        num_epoch : int\n            Number of epochs for training.\n        sparse_row_id_fn : A callback function\n            The function  takes `data_batch` as an input and returns a dict of\n            str -> NDArray. The resulting dict is used for pulling row_sparse\n            parameters from the kvstore, where the str key is the name of the param,\n            and the value is the row id of the param to pull.\n\n        Examples\n        --------\n        >>> # An example of using fit for training.\n        >>> # Assume training dataIter and validation dataIter are ready\n        >>> # Assume loading a previously checkpointed model\n        >>> sym, arg_params, aux_params = mx.model.load_checkpoint(model_prefix, 3)\n        >>> mod.fit(train_data=train_dataiter, eval_data=val_dataiter, optimizer='sgd',\n        ...     optimizer_params={'learning_rate':0.01, 'momentum': 0.9},\n        ...     arg_params=arg_params, aux_params=aux_params,\n        ...     eval_metric='acc', num_epoch=10, begin_epoch=3)\n        "
    assert (num_epoch is not None), 'please specify number of epochs'
    self.bind(data_shapes=train_data.provide_data, label_shapes=train_data.provide_label, for_training=True, force_rebind=force_rebind)
    if (monitor is not None):
        self.install_monitor(monitor)
    self.init_params(initializer=initializer, arg_params=arg_params, aux_params=aux_params, allow_missing=allow_missing, force_init=force_init)
    self.init_optimizer(kvstore=kvstore, optimizer=optimizer, optimizer_params=optimizer_params)
    if (validation_metric is None):
        validation_metric = eval_metric
    if (not isinstance(eval_metric, metric.EvalMetric)):
        eval_metric = metric.create(eval_metric)
    for epoch in range(begin_epoch, num_epoch):
        tic = time.time()
        eval_metric.reset()
        nbatch = 0
        data_iter = iter(train_data)
        end_of_batch = False
        next_data_batch = next(data_iter)
        while (not end_of_batch):
            data_batch = next_data_batch
            if (monitor is not None):
                monitor.tic()
            self.forward_backward(data_batch)
            self.update()
            try:
                next_data_batch = next(data_iter)
                self.prepare(next_data_batch, sparse_row_id_fn=sparse_row_id_fn)
            except StopIteration:
                end_of_batch = True
            self.update_metric(eval_metric, data_batch.label)
            if (monitor is not None):
                monitor.toc_print()
            if (batch_end_callback is not None):
                batch_end_params = BatchEndParam(epoch=epoch, nbatch=nbatch, eval_metric=eval_metric, locals=locals())
                for callback in _as_list(batch_end_callback):
                    callback(batch_end_params)
            nbatch += 1
        for (name, val) in eval_metric.get_name_value():
            self.logger.info('Epoch[%d] Train-%s=%f', epoch, name, val)
        toc = time.time()
        self.logger.info('Epoch[%d] Time cost=%.3f', epoch, (toc - tic))
        (arg_params, aux_params) = self.get_params()
        self.set_params(arg_params, aux_params)
        if (epoch_end_callback is not None):
            for callback in _as_list(epoch_end_callback):
                callback(epoch, self.symbol, arg_params, aux_params)
        if eval_data:
            res = self.score(eval_data, validation_metric, score_end_callback=eval_end_callback, batch_end_callback=eval_batch_end_callback, epoch=epoch)
            for (name, val) in res:
                self.logger.info('Epoch[%d] Validation-%s=%f', epoch, name, val)
        train_data.reset()
