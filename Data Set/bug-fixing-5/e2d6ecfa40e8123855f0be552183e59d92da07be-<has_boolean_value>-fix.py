def has_boolean_value(module, name):
    bools = []
    try:
        (rc, bools) = selinux.security_get_boolean_names()
    except OSError:
        module.fail_json(msg='Failed to get list of boolean names')
    if (len(bools) > 0):
        if isinstance(bools[0], binary_type):
            name = to_bytes(name)
    if (name in bools):
        return True
    else:
        return False