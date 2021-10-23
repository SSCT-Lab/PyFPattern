def bind(self, data_shapes, label_shapes=None, for_training=True, inputs_need_grad=False, force_rebind=False, shared_module=None, grad_req='write'):
    "Bind the symbols to construct executors. This is necessary before one\n        can perform computation with the module.\n\n        Parameters\n        ----------\n        data_shapes : list of (str, tuple)\n            Typically is `data_iter.provide_data`.\n        label_shapes : list of (str, tuple)\n            Typically is `data_iter.provide_label`.\n        for_training : bool\n            Default is `True`. Whether the executors should be bind for training.\n        inputs_need_grad : bool\n            Default is `False`. Whether the gradients to the input data need to be computed.\n            Typically this is not needed. But this might be needed when implementing composition\n            of modules.\n        force_rebind : bool\n            Default is `False`. This function does nothing if the executors are already\n            binded. But with this `True`, the executors will be forced to rebind.\n        shared_module : Module\n            Default is `None`. Currently shared module is not supported for `SequentialModule`.\n        grad_req : str, list of str, dict of str to str\n            Requirement for gradient accumulation. Can be 'write', 'add', or 'null'\n            (default to 'write').\n            Can be specified globally (str) or for each argument (list, dict).\n        "
    if (self.binded and (not force_rebind)):
        self.logger.warning('Already binded, ignoring bind()')
        return
    if inputs_need_grad:
        assert (for_training is True)
    assert (shared_module is None), 'Shared module is not supported'
    assert (len(self._modules) > 0), 'Attempting to bind an empty SequentialModule'
    self.binded = True
    self._label_shapes = label_shapes
    my_data_shapes = data_shapes
    anybody_ever_needs_label = False
    for (i_layer, module) in enumerate(self._modules):
        meta = self._metas[i_layer]
        if ((SequentialModule.META_TAKE_LABELS in meta) and meta[SequentialModule.META_TAKE_LABELS]):
            my_label_shapes = label_shapes
            anybody_ever_needs_label = True
        else:
            my_label_shapes = None
        my_inputs_need_grad = bool((inputs_need_grad or (for_training and (i_layer > 0))))
        if meta.get(SequentialModule.META_AUTO_WIRING, False):
            data_names = module.data_names
            assert (len(data_names) == len(my_data_shapes))
            my_data_shapes = [(new_name, shape) for (new_name, (_, shape)) in zip(data_names, my_data_shapes)]
        module.bind(data_shapes=my_data_shapes, label_shapes=my_label_shapes, for_training=for_training, inputs_need_grad=my_inputs_need_grad, force_rebind=force_rebind, shared_module=None, grad_req=grad_req)
        my_data_shapes = module.output_shapes
    if (not anybody_ever_needs_label):
        self._label_shapes = None