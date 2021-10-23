def run_tests(self, test_labels, extra_tests=None, **kwargs):
    self.setup_test_environment()
    suite = self.build_suite(test_labels, extra_tests)
    get_sqlalchemy_connection()
    failed = self.run_suite(suite, fatal_errors=kwargs.get('fatal_errors'))
    self.teardown_test_environment()
    return failed
    print()