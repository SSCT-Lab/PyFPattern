def load_PEM_list(module, path, fail_on_error=True):
    '\n    Load concatenated PEM certificates from file. Return list of ``Certificate`` objects.\n    '
    try:
        with open(path, 'rb') as f:
            return parse_PEM_list(module, f.read().decode('utf-8'), source=path, fail_on_error=fail_on_error)
    except Exception as e:
        msg = 'Cannot read certificate file {0}: {1}'.format(path, e)
        if fail_on_error:
            module.fail_json(msg=msg)
        else:
            module.warn(msg)
            return []