

def check_ideep_available():
    'Checks if iDeep is available.\n\n    When iDeep is correctly set up, nothing happens.\n    Otherwise it raises ``RuntimeError``.\n    '
    if (_ideep_version is None):
        msg = str(_error)
        if ('cannot open shared object file' in msg):
            msg += '\n\nEnsure iDeep requirements are satisfied: https://github.com/intel/ideep'
        raise RuntimeError('iDeep is not available.\nReason: {}: {}'.format(type(_error).__name__, msg))
