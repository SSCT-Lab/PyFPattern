def has_boolean_value(module, name):
    bools = []
    try:
        (rc, bools) = selinux.security_get_boolean_names()
    except OSError:
        module.fail_json(msg='Failed to get list of boolean names')
    if (to_bytes(name) in bools):
        return True
    else:
        return False