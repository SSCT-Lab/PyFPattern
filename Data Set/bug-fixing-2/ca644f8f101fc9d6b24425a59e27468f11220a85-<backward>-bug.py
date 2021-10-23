

def backward(self, retain_grad=False, enable_double_backprop=False, loss_scale=None):
    'Runs error backpropagation (a.k.a.\\  backprop) from this variable.\n\n        On backprop,\n        :meth:`FunctionNode.backward() <chainer.FunctionNode.backward>`\n        is called on each :class:`~chainer.FunctionNode` object appearing in\n        the backward graph starting from this variable.\n        The backward graph is represented by backward\n        references from variable nodes to their creators, and from function\n        nodes to their input variable nodes. The backprop stops at all root\n        nodes. Some function nodes set ``None`` as gradients of some inputs,\n        where further backprop does not take place at such inputs.\n\n        This method uses :data:`grad` as the initial error array. User can\n        manually set a gradient array before calling this method.\n        If the shape of :data:`data` is ``()`` (i.e., it is scalar) and\n        :data:`grad` is ``None``, then this method automatically complements\n        1.0 as the initial error. This is useful on starting backprop from\n        some scalar loss value.\n\n        From v3, this method supports *differentiable backprop* (a.k.a. double\n        backprop, grad of grads). To enable it, pass\n        ``enable_double_backprop=True``.\n\n        Args:\n            retain_grad (bool): If ``True``, the gradient arrays of all\n                intermediate variables are kept.\n                Otherwise, :data:`~chainer.Variable.grad` of the\n                intermediate variables are set to ``None`` on appropriate\n                timing, which may reduce the maximum memory consumption.\n\n                In most cases of training some models, the purpose of backprop\n                is to compute gradients of parameters, not of all variables,\n                and therefore it is recommended to set this flag ``False``.\n            enable_double_backprop (bool): *(Added in v3.0)* If ``True``,\n                computational trace of the whole backpropagation procedure is\n                recorded to the computational graph so that one can further do\n                backpropagation from the resulting gradients. Note that\n                enabling it results in larger memory consumption needed to\n                store the gradients w.r.t intermediate variables that are\n                required for the second gradient computation.\n            loss_scale (float): Loss scaling factor. Loss scaling is a usefull\n                technique to mitigate vanishing gradient issue that tends to\n                happen when low precision data type like float16 is used during\n                training. If you set loss scaling factor, gradients of loss\n                values are to be multiplied by the factor before backprop\n                starts. The factor is propagated to whole gradients in a\n                computational graph along the backprop. The gradients of\n                parameters are divided by the factor just before the parameters\n                are to be updated.\n        '
    if self._has_chainerx_array:
        if retain_grad:
            raise RuntimeError('retain_grad is not supported for ChainerX array.')
        if (loss_scale is not None):
            raise RuntimeError('loss_scale if not supported for ChainerX array.')
        arr = self._data[0]
        assert isinstance(arr, chainerx.ndarray)
        chainerx.backward(arr, enable_double_backprop=enable_double_backprop)
        return
    if ((self.array.size == 1) and (self.grad_var is None)):
        if (self.array.ndim != 0):
            warnings.warn('Treating a variable with only one element as a scalar in Variable.backward is deprecated. A scalar variable must be a 0-dimensional array. Apply chainer.functions.squeeze to obtain a scalar variable. If the size of this variable accidentally becomes one, set zero to grad.', DeprecationWarning)
        with cuda.get_device_from_array(self.array) as device:
            if (device is cuda.DummyDevice):
                self.grad = numpy.ones_like(self.array)
            else:
                self.grad = cuda.cupy.ones_like(self.array)
        if (loss_scale is not None):
            self.grad *= loss_scale
    node = self.node
    grad_var = self.grad_var
    self.grad_var = None
    with chainer.using_config('enable_backprop', enable_double_backprop):
        _backprop_to_all([(node, grad_var)], retain_grad, loss_scale)
