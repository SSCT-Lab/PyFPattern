def _parameterize_test_case_generator(base, params):
    for (i, param) in enumerate(params):
        cls_name = _make_class_name(base.__name__, i, param)

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

        def method_generator(base_method):
            param2 = param

            @functools.wraps(base_method)
            def new_method(self, *args, **kwargs):
                try:
                    return base_method(self, *args, **kwargs)
                except unittest.SkipTest:
                    raise
                except Exception as e:
                    s = six.StringIO()
                    s.write('Parameterized test failed.\n\n')
                    s.write('Base test method: {}.{}\n'.format(base.__name__, base_method.__name__))
                    s.write('Test parameters:\n')
                    for (k, v) in six.iteritems(param2):
                        s.write('  {}: {}\n'.format(k, v))
                    utils._raise_from(e.__class__, s.getvalue(), e)
            return new_method
        (yield (cls_name, mb, method_generator))