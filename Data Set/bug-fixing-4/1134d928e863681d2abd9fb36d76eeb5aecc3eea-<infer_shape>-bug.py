def infer_shape(self, *args, **kwargs):
    "Given known shapes for some arguments, infers the shapes of all arguments\n        and all outputs.\n\n        You can pass in the known shapes in either positional way or keyword argument\n        way. A tuple of ``None`` vakyes is returned if there is not enough information\n        to deduce the missing shapes.\n        Inconsistencies in the known shapes will cause an error to be raised.\n\n        Example usage:\n        ----------\n        >>> a = mxnet.sym.var('a')\n        >>> b = mxnet.sym.var('b')\n        >>> c = a + b\n        >>> c.infer_shape(a=(3,3))\n        ([(3L, 3L), (3L, 3L)], [(3L, 3L)], [])\n\n        Parameters\n        ----------\n        *args :\n            Provide shape of arguments in a positional way.\n            Unknown shape can be marked as None\n\n        **kwargs :\n            Provide keyword arguments of known shapes.\n\n        Returns\n        -------\n        arg_shapes : list of tuple or None\n            List of shapes of arguments.\n            The order is in the same order as list_arguments()\n        out_shapes : list of tuple or None\n            List of shapes of outputs.\n            The order is in the same order as list_outputs()\n        aux_shapes : list of tuple or None\n            List of shapes of outputs.\n            The order is in the same order as list_auxiliary_states()\n        "
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