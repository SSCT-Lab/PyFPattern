def optimize_loss(loss, global_step, learning_rate, optimizer, gradient_noise_scale=None, gradient_multipliers=None, clip_gradients=None, learning_rate_decay_fn=None, update_ops=None, variables=None, name=None, summaries=None, colocate_gradients_with_ops=False, increment_global_step=True):
    "Given loss and parameters for optimizer, returns a training op.\n\n  Various ways of passing optimizers include:\n\n  - by string specifying the name of the optimizer. See OPTIMIZER_CLS_NAMES\n      for full list. E.g. `optimize_loss(..., optimizer='Adam')`.\n  - by function taking learning rate `Tensor` as argument and returning an\n      `Optimizer` instance. E.g. `optimize_loss(...,\n      optimizer=lambda lr: tf.train.MomentumOptimizer(lr, momentum=0.5))`.\n    Alternatively, if `learning_rate` is `None`, the function takes no\n    arguments. E.g. `optimize_loss(..., learning_rate=None,\n      optimizer=lambda: tf.train.MomentumOptimizer(0.5, momentum=0.5))`.\n  - by a subclass of `Optimizer` having a single-argument constructor\n      (the argument is the learning rate), such as AdamOptimizer or\n      AdagradOptimizer. E.g. `optimize_loss(...,\n      optimizer=tf.train.AdagradOptimizer)`.\n  - by an instance of a subclass of `Optimizer`.\n      E.g., `optimize_loss(..., optimizer=tf.train.AdagradOptimizer(0.5))`.\n\n  Args:\n    loss: Scalar `Tensor`.\n    global_step: Scalar int `Tensor`, step counter to update on each step\n                 unless `increment_global_step` is `False`. If not supplied,\n                 it will be fetched from the default graph (see\n                 `tf.train.get_global_step` for details). If it has\n                 not been created, no step will be incremented with each weight\n                 update. `learning_rate_decay_fn` requires `global_step`.\n    learning_rate: float or `Tensor`, magnitude of update per each training\n                   step. Can be `None`.\n    optimizer: string, class or optimizer instance, used as trainer.\n               string should be name of optimizer, like 'SGD',\n                 'Adam', 'Adagrad'. Full list in OPTIMIZER_CLS_NAMES constant.\n               class should be sub-class of `tf.Optimizer` that implements\n                 `compute_gradients` and `apply_gradients` functions.\n               optimizer instance should be instantiation of `tf.Optimizer`\n                 sub-class and have `compute_gradients` and `apply_gradients`\n                 functions.\n    gradient_noise_scale: float or None, adds 0-mean normal noise scaled by this\n                          value.\n    gradient_multipliers: dict of variables or variable names to floats.\n                          If present, gradients for specified\n                          variables will be multiplied by given constant.\n    clip_gradients: float, callable or `None`. If float, is provided, a global\n      clipping is applied to prevent the norm of the gradient to exceed this\n      value. Alternatively, a callable can be provided e.g.: adaptive_clipping.\n      This callable takes a `list` of `(gradients, variables)` `tuple`s and\n      returns the same thing with the gradients modified.\n    learning_rate_decay_fn: function, takes `learning_rate` and `global_step`\n                            `Tensor`s, returns `Tensor`.\n                            Can be used to implement any learning rate decay\n                            functions.\n                            For example: `tf.train.exponential_decay`.\n                            Ignored if `learning_rate` is not supplied.\n    update_ops: list of update `Operation`s to execute at each step. If `None`,\n                uses elements of UPDATE_OPS collection. The order of execution\n                between `update_ops` and `loss` is non-deterministic.\n    variables: list of variables to optimize or\n               `None` to use all trainable variables.\n    name: The name for this operation is used to scope operations and summaries.\n    summaries: List of internal quantities to visualize on tensorboard. If not\n               set, the loss, the learning rate, and the global norm of the\n               gradients will be reported. The complete list of possible values\n               is in OPTIMIZER_SUMMARIES.\n    colocate_gradients_with_ops: If True, try colocating gradients with the\n                                 corresponding op.\n    increment_global_step: Whether to increment `global_step`. If your model\n      calls `optimize_loss` multiple times per training step (e.g. to optimize\n      different parts of the model), use this arg to avoid incrementing\n      `global_step` more times than necessary.\n\n  Returns:\n    Training op.\n\n  Raises:\n    ValueError: if:\n        * `loss` is an invalid type or shape.\n        * `global_step` is an invalid type or shape.\n        * `learning_rate` is an invalid type or value.\n        * `optimizer` has the wrong type.\n        * `clip_gradients` is neither float nor callable.\n        * `learning_rate` and `learning_rate_decay_fn` are supplied, but no\n          `global_step` is available.\n        * `gradients` is empty.\n  "
    loss = ops.convert_to_tensor(loss)
    contrib_framework.assert_scalar(loss)
    if (global_step is None):
        global_step = contrib_framework.get_global_step()
    else:
        contrib_framework.assert_global_step(global_step)
    with vs.variable_scope(name, 'OptimizeLoss', [loss, global_step]):
        if (update_ops is None):
            update_ops = set(ops.get_collection(ops.GraphKeys.UPDATE_OPS))
        if update_ops:
            loss = control_flow_ops.with_dependencies(list(update_ops), loss)
        lr = None
        if (learning_rate is not None):
            if (isinstance(learning_rate, ops.Tensor) and (learning_rate.get_shape().ndims == 0)):
                lr = learning_rate
            elif isinstance(learning_rate, float):
                if (learning_rate < 0.0):
                    raise ValueError('Invalid learning_rate %s.', learning_rate)
                lr = vs.get_variable('learning_rate', [], trainable=False, initializer=init_ops.constant_initializer(learning_rate))
            else:
                raise ValueError(('Learning rate should be 0d Tensor or float. Got %s of type %s' % (str(learning_rate), str(type(learning_rate)))))
        if (summaries is None):
            summaries = ['loss', 'learning_rate', 'global_gradient_norm']
        else:
            for summ in summaries:
                if (summ not in OPTIMIZER_SUMMARIES):
                    raise ValueError(('Summaries should be one of [%s], you provided %s.' % (', '.join(OPTIMIZER_SUMMARIES), summ)))
        if ((learning_rate is not None) and (learning_rate_decay_fn is not None)):
            if (global_step is None):
                raise ValueError('global_step is required for learning_rate_decay_fn.')
            lr = learning_rate_decay_fn(lr, global_step)
            if ('learning_rate' in summaries):
                summary.scalar('learning_rate', lr)
        if isinstance(optimizer, six.string_types):
            if (lr is None):
                raise ValueError(('Learning rate is None, but should be specified if optimizer is string (%s).' % optimizer))
            if (optimizer not in OPTIMIZER_CLS_NAMES):
                raise ValueError(('Optimizer name should be one of [%s], you provided %s.' % (', '.join(OPTIMIZER_CLS_NAMES), optimizer)))
            opt = OPTIMIZER_CLS_NAMES[optimizer](learning_rate=lr)
        elif (isinstance(optimizer, type) and issubclass(optimizer, optimizer_.Optimizer)):
            if (lr is None):
                raise ValueError(('Learning rate is None, but should be specified if optimizer is class (%s).' % optimizer))
            opt = optimizer(learning_rate=lr)
        elif isinstance(optimizer, optimizer_.Optimizer):
            opt = optimizer
        elif callable(optimizer):
            if (learning_rate is not None):
                opt = optimizer(lr)
            else:
                opt = optimizer()
            if (not isinstance(opt, optimizer_.Optimizer)):
                raise ValueError(('Unrecognized optimizer: function should return subclass of Optimizer. Got %s.' % str(opt)))
        else:
            raise ValueError(('Unrecognized optimizer: should be string, subclass of Optimizer, instance of subclass of Optimizer or function with one argument. Got %s.' % str(optimizer)))
        if (variables is None):
            variables = vars_.trainable_variables()
        gradients = opt.compute_gradients(loss, variables, colocate_gradients_with_ops=colocate_gradients_with_ops)
        if (gradient_noise_scale is not None):
            gradients = _add_scaled_noise_to_gradients(gradients, gradient_noise_scale)
        if (gradient_multipliers is not None):
            gradients = _multiply_gradients(gradients, gradient_multipliers)
            if (not gradients):
                raise ValueError('Empty list of (gradient, var) pairs encountered. This is most likely to be caused by an improper value of gradient_multipliers.')
        if (('global_gradient_norm' in summaries) or ('gradient_norm' in summaries)):
            summary.scalar('global_norm/gradient_norm', clip_ops.global_norm(list(zip(*gradients))[0]))
        if isinstance(clip_gradients, float):
            gradients = _clip_gradients_by_norm(gradients, clip_gradients)
        elif callable(clip_gradients):
            gradients = clip_gradients(gradients)
        elif (clip_gradients is not None):
            raise ValueError(('Unknown type %s for clip_gradients' % type(clip_gradients)))
        if ('loss' in summaries):
            summary.scalar('loss', loss)
        for (gradient, variable) in gradients:
            if isinstance(gradient, ops.IndexedSlices):
                grad_values = gradient.values
            else:
                grad_values = gradient
            if (grad_values is not None):
                var_name = variable.name.replace(':', '_')
                if ('gradients' in summaries):
                    summary.histogram(('gradients/%s' % var_name), grad_values)
                if ('gradient_norm' in summaries):
                    summary.scalar(('gradient_norm/%s' % var_name), clip_ops.global_norm([grad_values]))
        if ((clip_gradients is not None) and (('global_gradient_norm' in summaries) or ('gradient_norm' in summaries))):
            summary.scalar('global_norm/clipped_gradient_norm', clip_ops.global_norm(list(zip(*gradients))[0]))
        grad_updates = opt.apply_gradients(gradients, global_step=(global_step if increment_global_step else None), name='train')
        train_tensor = control_flow_ops.with_dependencies([grad_updates], loss)
        return train_tensor