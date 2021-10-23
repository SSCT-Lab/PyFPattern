def semanage_boolean_value(module, name, state):
    value = 0
    changed = False
    if state:
        value = 1
    try:
        handle = semanage_get_handle(module)
        semanage_begin_transaction(module, handle)
        cur_value = semanage_get_boolean_value(module, handle, name)
        if (cur_value != value):
            changed = True
            if (not module.check_mode):
                semanage_set_boolean_value(module, handle, name, value)
                semanage_commit(module, handle)
        semanage_destroy_handle(module, handle)
    except Exception as e:
        module.fail_json(msg=('Failed to manage policy for boolean %s: %s' % (name, str(e))))
    return changed