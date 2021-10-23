def run_tests(self, test_labels, extra_tests=None, **kwargs):
    self.setup_test_environment()
    try:
        suite = self.build_suite(test_labels, extra_tests)
    except AttributeError:
        traceback.print_exc()
        print()
        print("  This is often caused by a test module/class/function that doesn't exist or ")
        print('  import properly. You can usually debug in a `manage.py shell` via e.g. ')
        print('    import zerver.tests.test_messages')
        print('    from zerver.tests.test_messages import StreamMessagesTest')
        print('    StreamMessagesTest.test_message_to_stream')
        print()
        sys.exit(1)
    get_sqlalchemy_connection()
    failed = self.run_suite(suite, fatal_errors=kwargs.get('fatal_errors'))
    self.teardown_test_environment()
    return failed
    print()