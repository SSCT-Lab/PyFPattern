def make_host(module, array):
    changed = True
    try:
        array.create_host(module.params['host'])
        _set_host_initiators(module, array)
        api_version = array._list_available_rest_versions()
        if (AC_REQUIRED_API_VERSION in api_version):
            _set_host_personality(module, array)
        if module.params['volume']:
            array.connect_host(module.params['host'], module.params['volume'])
    except:
        module.fail_json(msg='Host {0} creation failed.'.format(module.params['host']))
    module.exit_json(changed=changed)