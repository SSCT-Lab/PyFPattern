

def simple_bind(self, ctx, grad_req='write', type_dict=None, **kwargs):
    "Bind current symbol to get an executor, allocate all the ndarrays needed.\n        Allows specifying data types.\n\n        This function will ask user to pass in ndarray of position\n        they like to bind to, and it will automatically allocate the ndarray\n        for arguments and auxiliary states that user did not specify explicitly.\n\n        Parameters\n        ----------\n        ctx : Context\n            The device context the generated executor to run on.\n        grad_req: string\n            {'write', 'add', 'null'}, or list of str or dict of str to str, optional\n            Specifies how we should update the gradient to the args_grad.\n            - 'write' means everytime gradient is write to specified args_grad NDArray.\n            - 'add' means everytime gradient is add to the specified NDArray.\n            - 'null' means no action is taken, the gradient may not be calculated.\n        type_dict  : dict of str->numpy.dtype\n            Input type dictionary, name->dtype\n        kwargs : dict of str->shape\n            Input shape dictionary, name->shape\n\n        Returns\n        -------\n        executor : mxnet.Executor\n            The generated Executor\n        "
    if (type_dict is None):
        type_dict = {k: mx_real_t for k in self.list_arguments()}
    (arg_shapes, _, aux_shapes) = self.infer_shape(**kwargs)
    (arg_types, _, aux_types) = self.infer_type(**type_dict)
    if ((arg_shapes is None) or (arg_types is None)):
        raise ValueError('Input node is not complete')
    arg_ndarrays = [zeros(shape, ctx, dtype=dtype) for (dtype, shape) in zip(arg_types, arg_shapes)]
    if (grad_req != 'null'):
        grad_ndarrays = {
            
        }
        for (name, shape, dtype) in zip(self.list_arguments(), arg_shapes, arg_types):
            if ((not isinstance(grad_req, dict)) or (grad_req[name] != 'null')):
                grad_ndarrays[name] = zeros(shape, ctx, dtype=dtype)
    else:
        grad_ndarrays = None
    aux_ndarrays = [zeros(shape, ctx, dtype=dtype) for (shape, dtype) in zip(aux_shapes, aux_types)]
    executor = self.bind(ctx, arg_ndarrays, grad_ndarrays, grad_req, aux_ndarrays)
    return executor
