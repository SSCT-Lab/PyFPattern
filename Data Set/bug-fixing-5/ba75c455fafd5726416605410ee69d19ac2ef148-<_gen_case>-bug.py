def _gen_case(base, module, i, param):
    cls_name = ('%s_param_%d' % (base.__name__, i))

    def __str__(self):
        name = base.__str__(self)
        return ('%s  parameter: %s' % (name, param))
    mb = {
        '__str__': __str__,
    }
    for (k, v) in six.iteritems(param):
        if isinstance(v, types.FunctionType):

            def create_new_v():
                f = v

                def new_v(self, *args, **kwargs):
                    return f(*args, **kwargs)
                return new_v
            mb[k] = create_new_v()
        else:
            mb[k] = v
    cls = type(cls_name, (base,), mb)
    setattr(module, cls_name, cls)