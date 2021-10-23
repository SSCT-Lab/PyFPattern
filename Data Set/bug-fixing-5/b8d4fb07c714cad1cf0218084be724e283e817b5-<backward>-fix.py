def backward(self, retain_grad=False):
    'Runs error backpropagation (a.k.a. backprop) from this variable.\n\n        On backprop, :meth:`Function.backward` is called on each\n        :class:`Function` object appearing in the backward graph starting from\n        this variable. The backward graph is represented by backward references\n        from variable nodes to their creators, and from functions to their\n        input variable nodes. The backprop stops at all root nodes. Some\n        functions set ``None`` as gradients of some inputs, where further\n        backprop does not take place at such inputs.\n\n        This method uses :data:`grad` as the initial error array. User can\n        manually set a gradient array before calling this method. If\n        :data:`data` contains only one element (i.e., it is scalar) and\n        :data:`grad` is ``None``, then this method automatically complements\n        1.0 as the initial error. This is useful on starting backprop from\n        some scalar loss value.\n\n        Args:\n            retain_grad (bool): If ``True``, the gradient arrays of all\n                intermediate variables are kept. Otherwise, :data:`grad` of the\n                intermediate variables are set to ``None`` on appropriate\n                timing, which may reduce the maximum memory consumption.\n\n                In most cases of training some models, the purpose of backprop\n                is to compute gradients of parameters, not of all variables,\n                and therefore it is recommended to set this flag ``False``.\n\n        '
    if (self.creator is None):
        return
    initial_device = None
    if (cuda.available and isinstance(self.data, cuda.cupy.ndarray)):
        try:
            initial_device = cuda.Device()
        except cuda.cupy.cuda.runtime.CUDARuntimeError as e:
            if (e.status != 38):
                raise
    is_debug = chainer.is_debug()
    cand_funcs = []
    seen_set = set()
    seen_vars = set()
    need_copy = set()
    if ((self.data.size == 1) and (self.grad is None)):
        with cuda.get_device_from_array(self.data) as device:
            if (device is cuda.DummyDevice):
                self.grad = numpy.ones_like(self.data)
            else:
                self.grad = cuda.cupy.ones_like(self.data)

    def add_cand(cand):
        if (cand not in seen_set):
            heapq.heappush(cand_funcs, ((- cand.rank), len(seen_set), cand))
            seen_set.add(cand)
    add_cand(self.creator)
    while cand_funcs:
        (_, _, func) = heapq.heappop(cand_funcs)
        outputs = [y() for y in func.outputs]
        in_data = tuple([x.data for x in func.inputs])
        out_grad = tuple([(None if (y is None) else y.grad) for y in outputs])
        hooks = chainer.get_function_hooks()
        if (func._n_local_function_hooks != 0):
            hooks = collections.OrderedDict(hooks)
            hooks.update(func.local_function_hooks)
        cuda.get_device_from_array(*(in_data + out_grad)).use()
        for hook in six.itervalues(hooks):
            hook.backward_preprocess(func, in_data, out_grad)
        func.output_data = tuple([(None if (y is None) else y.data) for y in outputs])
        gxs = func.backward(in_data, out_grad)
        assert (len(gxs) == len(in_data))
        if (not getattr(func, '_retain_after_backward', False)):
            func.output_data = None
        for hook in six.itervalues(hooks):
            hook.backward_postprocess(func, in_data, out_grad)
        if is_debug:
            for gx in gxs:
                if (gx is None):
                    continue
                cuda.get_device_from_array(gx).use()
                if cuda.get_array_module(gx).isnan(gx).any():
                    msg = 'NaN is detected on backward computation of {}'.format(func.label)
                    raise RuntimeError(msg)
        if (not retain_grad):
            for y in outputs:
                if ((y is not None) and (y is not self.node)):
                    y.grad = None
        for (x, gx) in zip(func.inputs, gxs):
            if (gx is None):
                continue
            if (not x.requires_grad):
                continue
            _check_grad_type(func, x, gx)
            id_x = id(x)
            if (x.creator is None):
                if (x._grad is None):
                    x.grad = gx
                    need_copy.add(id_x)
                else:
                    cuda.get_device_from_array(gx).use()
                    if (id_x in need_copy):
                        x.grad = utils.force_array((x._grad + gx))
                        need_copy.remove(id_x)
                    else:
                        x._grad += gx
            else:
                add_cand(x.creator)
                if (id_x not in seen_vars):
                    x.grad = gx
                    seen_vars.add(id_x)
                    need_copy.add(id_x)
                else:
                    cuda.get_device_from_array(gx).use()
                    if (id_x in need_copy):
                        x.grad = utils.force_array((gx + x._grad))
                        need_copy.remove(id_x)
                    else:
                        x._grad += gx
        del gxs
        if (initial_device is not None):
            initial_device.use()