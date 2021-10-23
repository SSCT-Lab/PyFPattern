

def pytest_configure(config):
    import warnings
    warnings.filterwarnings('error', '', Warning, '^(?!(|kombu|raven|sentry))')
    if any((('tests/sentry_plugins' in s) for s in config.getoption('file_or_dir'))):
        install_sentry_plugins()
