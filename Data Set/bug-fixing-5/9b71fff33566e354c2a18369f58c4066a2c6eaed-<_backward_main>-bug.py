def _backward_main(self, retain_grad, loss_scale):
    self._node._check_old_style_gradient()
    if (self.creator_node is None):
        return
    OrderedDict = chainer.utils._collections.OrderedDict
    cand_funcs = []
    seen_set = set()
    grads = _backprop_utils.GradTable(load_if_new=True)
    if ((self.array.size == 1) and (self._grad_var is None)):
        if (self.array.ndim != 0):
            warnings.warn('Treating a scalar as a variable with only one element in Variable.backward is deprecated. A scalar variable must be a 0-dimensional array. Apply chainer.functions.squeeze to obtain a scalar variable. If the size of this variable accidentally becomes one, set zero to grad.', DeprecationWarning)
        with cuda.get_device_from_array(self.array) as device:
            if (device is cuda.DummyDevice):
                self.grad = numpy.ones_like(self.array)
            else:
                self.grad = cuda.cupy.ones_like(self.array)
        if (loss_scale is not None):
            self.grad *= loss_scale
    grads[self._node] = self._grad_var

    def add_cand(cand):
        if (cand not in seen_set):
            heapq.heappush(cand_funcs, ((- cand.rank), len(seen_set), cand))
            seen_set.add(cand)
    add_cand(self.creator_node)
    leaf_nodes = set()
    while cand_funcs:
        (_, _, func) = heapq.heappop(cand_funcs)
        inputs = func.inputs
        target_input_indexes = tuple([i for (i, x) in enumerate(inputs) if x.requires_grad])
        outputs = [y() for y in func.outputs]
        out_grad = tuple([grads.pop(y) for y in outputs])
        if (not target_input_indexes):
            continue
        in_data = tuple([x.data for x in inputs])
        out_grad_array = tuple([(None if (g is None) else g.array) for g in out_grad])
        hooks = chainer.get_function_hooks()
        if (func._n_local_function_hooks != 0):
            hooks = collections.OrderedDict(hooks)
            hooks.update(func.local_function_hooks)
        hooks = hooks.values()
        with cuda.get_device_from_array(*(in_data + out_grad_array)):
            for hook in hooks:
                hook.backward_preprocess(func, in_data, out_grad_array)
            target_inputs = [inputs[i] for i in target_input_indexes]
            in_grad = OrderedDict()
            for x in target_inputs:
                if (x not in in_grad):
                    in_grad[x] = grads.get_as_list(x)
                    x._set_grad_var_if_available(None)
            _backprop_utils.backprop_step(func, target_input_indexes, out_grad, in_grad)
            for hook in hooks:
                hook.backward_postprocess(func, in_data, out_grad_array)
        for (y, gy) in six.moves.zip(outputs, out_grad):
            if ((y is not None) and (y is not self.node)):
                y._set_grad_var_if_available((gy if retain_grad else None))
        del gy, out_grad
        for (x, gx) in in_grad.items():
            if (not gx):
                continue
            for gx_elem in gx:
                _check_grad_type(func, x, True, gx_elem, True)
            del gx_elem
            if (x.creator_node is None):
                leaf_nodes.add(x)
            else:
                add_cand(x.creator_node)
        del gx, in_grad
    for x in leaf_nodes:
        x_var = x.get_variable_or_none()
        gx = grads.pop(x)
        if (x_var is not None):
            x_var._grad_var = gx
            x_var._loss_scale = loss_scale
    grads.assert_no_grads()