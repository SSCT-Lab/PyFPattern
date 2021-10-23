def check_ideep_available():
    'Checks if iDeep is available.\n\n    When iDeep is correctly set up, nothing happens.\n    Otherwise it raises ``RuntimeError``.\n    '
    if (_ideep_version is None):
        raise RuntimeError('iDeep is not available.\nReason: {}: {}'.format(type(_error).__name__, str(_error)))