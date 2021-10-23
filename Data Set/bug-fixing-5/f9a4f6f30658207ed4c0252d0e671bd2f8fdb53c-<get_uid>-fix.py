def get_uid(prefix=''):
    _UID_PREFIXES[prefix] += 1
    return _UID_PREFIXES[prefix]