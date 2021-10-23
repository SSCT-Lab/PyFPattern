def infer_shape(self, *args, **kwargs):
    "Infers the shapes of all arguments and all outputs given the known shapes of\n        some arguments.\n\n        This function takes the known shapes of some arguments in either positional way\n        or keyword argument way as input. It returns a tuple of `None` values\n        if there is not enough information to deduce the missing shapes.\n\n        Example usage:\n        ----------\n        >>> a = mx.sym.var('a')\n        >>> b = mx.sym.var('b')\n        >>> c = a + b\n        >>> arg_shapes, out_shapes, aux_shapes = c.infer_shape(a=(3,3))\n        >>> arg_shapes\n        [(3L, 3L), (3L, 3L)]\n        >>> out_shapes\n        [(3L, 3L)]\n        >>> aux_shapes\n        []\n        >>> c.infer_shape(a=(0,3)) # 0s in shape means unknown dimensions. So, returns None.\n        (None, None, None)\n\n        Inconsistencies in the known shapes will cause an error to be raised.\n        See the following example:\n\n        >>> data = mx.sym.Variable('data')\n        >>> out = mx.sym.FullyConnected(data=data, name='fc1', num_hidden=1000)\n        >>> out = mx.sym.Activation(data=out, act_type='relu')\n        >>> out = mx.sym.FullyConnected(data=out, name='fc2', num_hidden=10)\n        >>> weight_shape= (1, 100)\n        >>> data_shape = (100, 100)\n        >>> out.infer_shape(data=data_shape, fc1_weight=weight_shape)\n        Error in operator fc1: Shape inconsistent, Provided=(1,100), inferred shape=(1000,100)\n\n        Parameters\n        ----------\n        *args :\n            Shape of arguments in a positional way.\n            Unknown shape can be marked as None.\n\n        **kwargs :\n            Keyword arguments of the known shapes.\n\n        Returns\n        -------\n        arg_shapes : list of tuple or None\n            List of argument shapes.\n            The order is same as the order of list_arguments().\n        out_shapes : list of tuple or None\n            List of output shapes.\n            The order is same as the order of list_outputs().\n        aux_shapes : list of tuple or None\n            List of auxiliary state shapes.\n            The order is same as the order of list_auxiliary_states().\n        "
    try:
        res = self._infer_shape_impl(False, *args, **kwargs)
        if (res[1] is None):
            (arg_shapes, _, _) = self._infer_shape_impl(True, *args, **kwargs)
            arg_names = self.list_arguments()
            unknowns = []
            for (name, shape) in zip(arg_names, arg_shapes):
                if ((not shape) or (not _numpy.prod(shape))):
                    if (len(unknowns) >= 10):
                        unknowns.append('...')
                        break
                    unknowns.append(('%s: %s' % (name, str(shape))))
            warnings.warn(((('Cannot decide shape for the following arguments ' + '(0s in shape means unknown dimensions). ') + 'Consider providing them as input:\n\t') + '\n\t'.join(unknowns)), stacklevel=2)
        return res
    except MXNetError:
        print('infer_shape error. Arguments:')
        for (i, arg) in enumerate(args):
            print(('  #%d: %s' % (i, arg)))
        for (k, v) in kwargs.items():
            print(('  %s: %s' % (k, v)))
        raise