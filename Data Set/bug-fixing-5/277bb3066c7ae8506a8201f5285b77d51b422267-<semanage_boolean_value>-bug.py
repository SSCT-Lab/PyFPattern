def semanage_boolean_value(module, name, state):
    rc = 0
    value = 0
    if state:
        value = 1
    handle = semanage.semanage_handle_create()
    if (handle is None):
        module.fail_json(msg='Failed to create semanage library handle')
    try:
        managed = semanage.semanage_is_managed(handle)
        if (managed < 0):
            module.fail_json(msg='Failed to determine whether policy is manage')
        if (managed == 0):
            if (os.getuid() == 0):
                module.fail_json(msg='Cannot set persistent booleans without managed policy')
            else:
                module.fail_json(msg='Cannot set persistent booleans; please try as root')
        if (semanage.semanage_connect(handle) < 0):
            module.fail_json(msg='Failed to connect to semanage')
        if (semanage.semanage_begin_transaction(handle) < 0):
            module.fail_json(msg='Failed to begin semanage transaction')
        (rc, sebool) = semanage.semanage_bool_create(handle)
        if (rc < 0):
            module.fail_json(msg='Failed to create seboolean with semanage')
        if (semanage.semanage_bool_set_name(handle, sebool, name) < 0):
            module.fail_json(msg='Failed to set seboolean name with semanage')
        semanage.semanage_bool_set_value(sebool, value)
        (rc, boolkey) = semanage.semanage_bool_key_extract(handle, sebool)
        if (rc < 0):
            module.fail_json(msg='Failed to extract boolean key with semanage')
        if (semanage.semanage_bool_modify_local(handle, boolkey, sebool) < 0):
            module.fail_json(msg='Failed to modify boolean key with semanage')
        if (semanage.semanage_bool_set_active(handle, boolkey, sebool) < 0):
            module.fail_json(msg='Failed to set boolean key active with semanage')
        semanage.semanage_bool_key_free(boolkey)
        semanage.semanage_bool_free(sebool)
        semanage.semanage_set_reload(handle, 0)
        if (semanage.semanage_commit(handle) < 0):
            module.fail_json(msg='Failed to commit changes to semanage')
        semanage.semanage_disconnect(handle)
        semanage.semanage_handle_destroy(handle)
    except Exception as e:
        module.fail_json(msg=('Failed to manage policy for boolean %s: %s' % (name, str(e))))
    return True