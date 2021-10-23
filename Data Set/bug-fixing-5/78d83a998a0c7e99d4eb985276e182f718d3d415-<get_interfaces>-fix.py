def get_interfaces(data):
    result = []
    for (key, data) in six.iteritems(data):
        if (data is None):
            continue
        try:
            cls = get_interface(key)
        except ValueError:
            continue
        value = safe_execute(cls.to_python, data, _with_transaction=False)
        if (not value):
            continue
        result.append((key, value))
    return OrderedDict(((k, v) for (k, v) in sorted(result, key=(lambda x: x[1].get_score()), reverse=True)))