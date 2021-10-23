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

    def wrap_test_method(method):

        @functools.wraps(method)
        def wrap(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except AssertionError as e:
                s = six.StringIO()
                s.write('Parameterized test failed.\n\n')
                s.write('Base test method: {}.{}\n'.format(base.__name__, method.__name__))
                s.write('Test parameters:\n')
                for (k, v) in six.iteritems(param):
                    s.write('  {}: {}\n'.format(k, v))
                s.write('\n')
                s.write('{}: {}\n'.format(type(e).__name__, e))
                raise AssertionError(s.getvalue())
        return wrap
    members = inspect.getmembers(cls, predicate=(lambda _: (inspect.ismethod(_) or inspect.isfunction(_))))
    for (name, method) in members:
        if name.startswith('test_'):
            setattr(cls, name, wrap_test_method(method))
    setattr(module, cls_name, cls)