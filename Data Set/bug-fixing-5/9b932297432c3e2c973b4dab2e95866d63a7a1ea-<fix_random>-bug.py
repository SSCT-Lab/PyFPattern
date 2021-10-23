def fix_random():
    'Decorator that fixes random numbers in a test.\n\n    This decorator can be applied to either a test case class or a test method.\n    It should not be applied within ``condition.retry`` or\n    ``condition.repeat``.\n    '

    def decorator(impl):
        if (isinstance(impl, types.FunctionType) and impl.__name__.startswith('test_')):

            @functools.wraps(impl)
            def test_func(self, *args, **kw):
                _setup_random()
                try:
                    impl(self, *args, **kw)
                finally:
                    _teardown_random()
            return test_func
        elif (isinstance(impl, type) and issubclass(impl, unittest.TestCase)):
            klass = impl
            setUp_ = klass.setUp
            tearDown_ = klass.tearDown

            @functools.wrap(setUp_)
            def setUp(self):
                _setup_random()
                setUp_(self)

            @functools.wrap(tearDown_)
            def tearDown(self):
                try:
                    tearDown_(self)
                finally:
                    _teardown_random()
            klass.setUp = setUp
            klass.tearDown = tearDown
            return klass
        else:
            raise ValueError("Can't apply fix_random to {}".format(impl))
    return decorator