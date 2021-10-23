def pytest_configure(config):
    import warnings
    warnings.filterwarnings('error', '', Warning, '^(?!(|kombu|raven|sentry))')
    test_targets = config.getoption('file_or_dir')
    if (test_targets and any((('tests/sentry_plugins' in s) for s in test_targets))):
        install_sentry_plugins()