def __call__(self, *args, **kwargs):
    "\n        Evaluates value of a function on given arguments.\n\n        Parameters\n        ----------\n        args : list\n            List of inputs to the function. All inputs are required, even when\n            some of them are not necessary to calculate requested subset of\n            outputs.\n\n        kwargs : dict\n            The function inputs can be passed as keyword argument. For this, use\n            the name of the input or the input instance as the key.\n            Keyword argument ``output_subset`` is a list of either indices of the\n            function's outputs or the keys belonging to the `output_keys` dict\n            and represent outputs that are requested to be calculated.\n\n        Returns\n        -------\n        list\n            List of outputs on indices/keys from ``output_subset`` or all of them,\n            if ``output_subset`` is not passed.\n        "
    profile = self.profile
    t0 = time.time()
    output_subset = kwargs.pop('output_subset', None)
    if ((output_subset is not None) and (self.output_keys is not None)):
        output_subset = [self.output_keys.index(key) for key in output_subset]
    if self.trust_input:
        i = 0
        for arg in args:
            s = self.input_storage[i]
            s.storage[0] = arg
            i += 1
    else:
        for c in self.input_storage:
            c.provided = 0
        if ((len(args) + len(kwargs)) > len(self.input_storage)):
            raise TypeError('Too many parameter passed to theano function')
        i = 0
        for arg in args:
            s = self.input_storage[i]
            if (arg is None):
                s.storage[0] = arg
            else:
                try:
                    s.storage[0] = s.type.filter(arg, strict=s.strict, allow_downcast=s.allow_downcast)
                except Exception as e:
                    function_name = 'theano function'
                    if self.name:
                        function_name += ((' with name "' + self.name) + '" ')
                    e.args = (((('Bad input argument to ' + function_name) + (' at index %d(0-based)' % i)),) + e.args)
                    raise
            s.provided += 1
            i += 1
    if kwargs:
        for (k, arg) in iteritems(kwargs):
            self[k] = arg
    if ((not self.trust_input) and getattr(self, '_check_for_aliased_inputs', True)):
        args_share_memory = []
        for i in xrange(len(self.input_storage)):
            i_var = self.maker.inputs[i].variable
            i_val = self.input_storage[i].storage[0]
            if hasattr(i_var.type, 'may_share_memory'):
                is_aliased = False
                for j in xrange(len(args_share_memory)):
                    group_j = izip([self.maker.inputs[k].variable for k in args_share_memory[j]], [self.input_storage[k].storage[0] for k in args_share_memory[j]])
                    if numpy.any([((var.type is i_var.type) and var.type.may_share_memory(val, i_val)) for (var, val) in group_j]):
                        is_aliased = True
                        args_share_memory[j].append(i)
                        break
                if (not is_aliased):
                    args_share_memory.append([i])
            for group in args_share_memory:
                if (len(group) > 1):
                    for idx in group[1:]:
                        self.input_storage[i].storage[0] = copy.copy(self.input_storage[i].storage[0])
    if (not self.trust_input):
        for c in self.input_storage:
            if (c.required and (not c.provided)):
                raise TypeError(('Missing required input: %s' % getattr(self.inv_finder[c], 'variable', self.inv_finder[c])))
            if (c.provided > 1):
                raise TypeError(('Multiple values for input: %s' % getattr(self.inv_finder[c], 'variable', self.inv_finder[c])))
            if (c.implicit and (c.provided > 0)):
                raise TypeError(('Tried to provide value for implicit input: %s' % getattr(self.inv_finder[c], 'variable', self.inv_finder[c])))
    t0_fn = time.time()
    try:
        outputs = (self.fn() if (output_subset is None) else self.fn(output_subset=output_subset))
    except Exception:
        if hasattr(self.fn, 'position_of_error'):
            thunk = None
            if hasattr(self.fn, 'thunks'):
                thunk = self.fn.thunks[self.fn.position_of_error]
            gof.link.raise_with_op(node=self.fn.nodes[self.fn.position_of_error], thunk=thunk, storage_map=getattr(self.fn, 'storage_map', None))
        else:
            raise
    dt_fn = (time.time() - t0_fn)
    self.maker.mode.fn_time += dt_fn
    if profile:
        profile.vm_call_time += dt_fn
    if (outputs is None):
        outputs = [x.data for x in self.output_storage]
    assert (len(outputs) == len(self.output_storage))
    for c in self.input_storage:
        if c.required:
            c.storage[0] = None
    if getattr(self.fn, 'allow_gc', False):
        assert (len(self.output_storage) == len(self.maker.fgraph.outputs))
        for (o_container, o_variable) in zip(self.output_storage, self.maker.fgraph.outputs):
            if (o_variable.owner is not None):
                o_container.storage[0] = None
    if getattr(self.fn, 'need_update_inputs', True):
        for (input, storage) in reversed(list(zip(self.maker.expanded_inputs, self.input_storage))):
            if (input.update is not None):
                storage.data = outputs.pop()
    else:
        outputs = outputs[:self.n_returned_outputs]
    for (i, (required, refeed, value)) in enumerate(self.defaults):
        if refeed:
            if isinstance(value, gof.Container):
                value = value.storage[0]
            self[i] = value
    dt_call = (time.time() - t0)
    self.maker.mode.call_time += dt_call
    if profile:
        profile.fct_callcount += 1
        profile.fct_call_time += dt_call
        if hasattr(self.fn, 'update_profile'):
            self.fn.update_profile(profile)
        if profile.ignore_first_call:
            profile.reset()
            profile.ignore_first_call = False
    if self.return_none:
        return None
    elif (self.unpack_single and (len(outputs) == 1) and (output_subset is None)):
        return outputs[0]
    else:
        if (self.output_keys is not None):
            assert (len(self.output_keys) == len(outputs))
            if (output_subset is None):
                return dict(izip(self.output_keys, outputs))
            else:
                return dict(((self.output_keys[index], outputs[index]) for index in output_subset))
        if (output_subset is None):
            return outputs
        else:
            return [outputs[i] for i in output_subset]