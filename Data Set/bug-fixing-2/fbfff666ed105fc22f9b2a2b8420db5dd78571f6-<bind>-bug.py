

def bind(self, data_shapes, label_shapes=None, for_training=True, inputs_need_grad=False, force_rebind=False, shared_module=None, grad_req='write'):
    'Binds the symbols to construct executors. This is necessary before one\n        can perform computation with the module.\n\n        Parameters\n        ----------\n        data_shapes : list of (str, tuple)\n            Typically is ``data_iter.provide_data``.\n        label_shapes : list of (str, tuple)\n            Typically is ``data_iter.provide_label``.\n        for_training : bool\n            Default is ``True``. Whether the executors should be bound for training.\n        inputs_need_grad : bool\n            Default is ``False``. Whether the gradients to the input data need to be computed.\n            Typically this is not needed. But this might be needed when implementing composition\n            of modules.\n        force_rebind : bool\n            Default is ``False``. This function does nothing if the executors are already\n            bound. But with this ``True``, the executors will be forced to rebind.\n        shared_module : Module\n            Default is ``None``. This is used in bucketing. When not ``None``, the shared module\n            essentially corresponds to a different bucket -- a module with different symbol\n            but with the same sets of parameters (e.g. unrolled RNNs with different lengths).\n        '
    if force_rebind:
        self._reset_bind()
    if self.binded:
        self.logger.warning('Already bound, ignoring bind()')
        return
    self.for_training = for_training
    self.inputs_need_grad = inputs_need_grad
    self.binded = True
    self._grad_req = grad_req
    if (not for_training):
        assert (not inputs_need_grad)
    else:
        pass
    (self._data_shapes, self._label_shapes) = _parse_data_desc(self.data_names, self.label_names, data_shapes, label_shapes)
    if (shared_module is not None):
        assert (isinstance(shared_module, Module) and shared_module.binded and shared_module.params_initialized)
        shared_group = shared_module._exec_group
        assert (len(shared_group.execs) == len(self._context))
    else:
        shared_group = None
    self._exec_group = DataParallelExecutorGroup(self._symbol, self._context, self._work_load_list, self._data_shapes, self._label_shapes, self._param_names, for_training, inputs_need_grad, shared_group, logger=self.logger, fixed_param_names=self._fixed_param_names, grad_req=grad_req, state_names=self._state_names)
    self._total_exec_bytes = self._exec_group._total_exec_bytes
    if (shared_module is not None):
        self.params_initialized = True
        self._arg_params = shared_module._arg_params
        self._aux_params = shared_module._aux_params
    elif self.params_initialized:
        self._exec_group.set_params(self._arg_params, self._aux_params)
    else:
        assert ((self._arg_params is None) and (self._aux_params is None))
        param_arrays = [zeros(shape=x[0].shape, dtype=x[0].dtype, stype=x[0].stype) for x in self._exec_group.param_arrays]
        self._arg_params = {name: arr for (name, arr) in zip(self._param_names, param_arrays)}
        aux_arrays = [zeros(x[0].shape, dtype=x[0].dtype) for x in self._exec_group.aux_arrays]
        self._aux_params = {name: arr for (name, arr) in zip(self._aux_names, aux_arrays)}
    if ((shared_module is not None) and shared_module.optimizer_initialized):
        self.borrow_optimizer(shared_module)
