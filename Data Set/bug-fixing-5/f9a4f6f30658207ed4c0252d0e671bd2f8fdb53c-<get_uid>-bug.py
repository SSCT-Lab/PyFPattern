def get_uid(prefix=''):
    if (prefix not in _UID_PREFIXES):
        _UID_PREFIXES[prefix] = 1
        return 1
    else:
        _UID_PREFIXES[prefix] += 1
        return _UID_PREFIXES[prefix]