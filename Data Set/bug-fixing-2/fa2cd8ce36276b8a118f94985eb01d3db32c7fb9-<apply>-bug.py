

def apply(self, inputs):
    'Computes output variables and grows the computational graph.\n\n        Basic behavior is expressed in the documentation of\n        :class:`FunctionNode`.\n\n        .. note::\n\n           If the :data:`~Variable.data` attributes of the input variables exist on\n           a GPU device, that device is made current before calling\n           :meth:`forward`, so implementers do not need to take care of device\n           selection in most cases.\n\n        Args:\n            inputs: Tuple of input variables. Each element can be either\n                :class:`~chainer.Variable` or :ref:`ndarray`. If the element\n                is an ndarray, it is automatically wrapped with\n                :class:`~chainer.Variable`.\n\n        Returns:\n            A tuple of output :class:`~chainer.Variable` objects.\n\n        '
    chainerx_in_data = None
    chainerx_device = None
    (is_chainerx, in_data) = _extract_apply_in_data(inputs)
    if is_chainerx:
        outputs = self.forward_chainerx(in_data)
        if (outputs is not chainer.Fallback):
            assert isinstance(outputs, tuple)
            return tuple([variable.Variable._init_unchecked(y, requires_grad=y.is_backprop_required(), is_chainerx_array=True) for y in outputs])
        (chainerx_in_data, in_data, chainerx_device) = self._chainerx_apply_fallback_preprocess(in_data, inputs)
        self._is_chainerx_fallback_mode = True
        self.chainerx_device = chainerx_device
    utils._check_arrays_forward_compatible(in_data, self.label)
    is_debug = chainer.is_debug()
    if is_debug:
        self.stack = traceback.extract_stack()
    if configuration.config.type_check:
        self._check_data_type_forward(in_data)
    hooks = chainer.get_function_hooks()
    if (self._n_local_function_hooks > 0):
        hooks = collections.OrderedDict(hooks)
        hooks.update(self.local_function_hooks)
    hooks = hooks.values()
    for hook in hooks:
        hook.forward_preprocess(self, in_data)
    with chainer.using_device(backend.get_device_from_array(*in_data)):
        self._input_indexes_to_retain = None
        self._output_indexes_to_retain = None
        if (chainer.config.schedule_func is not None):
            outputs = static_forward_optimizations(self, in_data)
        elif self._is_chainerx_fallback_mode:
            with _chainerx_attribute_fallback(self, chainerx_device):
                outputs = self.forward(in_data)
        else:
            outputs = self.forward(in_data)
    if (not isinstance(outputs, tuple)):
        raise TypeError('forward output must be a tuple ({})\nActual: {}'.format(self.label, type(outputs)))
    if (not chainer.is_arrays_compatible(outputs)):
        raise TypeError('incompatible array types are mixed in the forward output ({}).\nActual: {}'.format(self.label, ', '.join((str(type(x)) for x in outputs))))
    for hook in hooks:
        hook.forward_postprocess(self, in_data)
    if is_debug:
        for out in outputs:
            if ((out is not None) and chainer.backend._contains_nan(out)):
                msg = 'NaN is detected on forward computation of {}'.format(self.label)
                raise RuntimeError(msg)
    self._output_count = len(outputs)
    if self._is_chainerx_fallback_mode:
        ret = self._chainerx_apply_fallback_postprocess(chainerx_device, chainerx_in_data, inputs, outputs)
    else:
        input_vars = [chainer.as_variable(x) for x in inputs]
        requires_grad = any([x.requires_grad for x in input_vars])
        ret = tuple([variable.Variable(y, requires_grad=requires_grad) for y in outputs])
        if configuration.config.enable_backprop:
            self.rank = (max([x.rank for x in input_vars]) if input_vars else 0)
            for y in ret:
                y.creator_node = self
            self.inputs = tuple([x.node for x in input_vars])
            self.outputs = tuple([weakref.ref(y.node) for y in ret])
            if (self._input_indexes_to_retain is not None):
                for index in self._input_indexes_to_retain:
                    input_vars[index].retain_data()
            if (self._output_indexes_to_retain is not None):
                retained_data = []
                for index in self._output_indexes_to_retain:
                    ret[index].retain_data()
                    retained_data.append(outputs[index])
                self._retained_output_data = tuple(retained_data)
            self.lazy_grad_sum = configuration.config.lazy_grad_sum
    return ret
