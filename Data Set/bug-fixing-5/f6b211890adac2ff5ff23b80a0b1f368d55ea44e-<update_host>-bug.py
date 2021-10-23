def update_host(module, array):
    changed = False
    api_version = array._list_available_rest_versions()
    if (AC_REQUIRED_API_VERSION in api_version):
        try:
            _set_host_personality(module, array)
            changed = True
        except:
            module.fail_json(msg='Host {0} personality change failed'.format(module.params['host']))
    module.exit_json(changed=changed)