def make_host(module, array):
    changed = False
    try:
        array.create_host(module.params['host'])
        changed = True
    except:
        module.fail_json(msg='Host {0} creation failed.'.format(module.params['host']))
    try:
        _set_host_initiators(module, array)
        api_version = array._list_available_rest_versions()
        if ((AC_REQUIRED_API_VERSION in api_version) and module.params['personality']):
            _set_host_personality(module, array)
        if module.params['volume']:
            if module.params['lun']:
                array.connect_host(module.params['host'], module.params['volume'], lun=module.params['lun'])
            else:
                array.connect_host(module.params['host'], module.params['volume'])
    except:
        module.fail_json(msg='Host {0} configuration failed.'.format(module.params['host']))
    module.exit_json(changed=changed)