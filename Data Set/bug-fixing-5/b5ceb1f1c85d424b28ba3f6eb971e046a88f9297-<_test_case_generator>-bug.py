def _test_case_generator(base, method_names, params):
    if (method_names is not None):

        def method_generator(base_method):
            if (base_method.__name__ in method_names):
                return None
            return base_method
        (yield (base.__name__, {
            
        }, method_generator))
    for (i_param, param) in enumerate(params):
        backend_config = BackendConfig(param)
        marks = backend_config.get_pytest_marks()
        cls_name = '{}_{}'.format(base.__name__, backend_config.get_func_str())

        def method_generator(base_method):
            if ((method_names is not None) and (base_method.__name__ not in method_names)):
                return None
            backend_config2 = backend_config

            @functools.wraps(base_method)
            def new_method(self, *args, **kwargs):
                return base_method(self, backend_config2, *args, **kwargs)
            for mark in marks:
                mark(new_method)
            return new_method
        (yield (cls_name, {
            
        }, method_generator))