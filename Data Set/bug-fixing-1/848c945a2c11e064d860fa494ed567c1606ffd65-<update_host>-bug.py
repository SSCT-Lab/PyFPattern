

def update_host(module, array):
    changed = True
    if (not module.check_mode):
        volumes = array.list_host_connections(module.params['host'])
        if (module.params['iqn'] or module.params['wwns'] or module.params['nqn']):
            changed = _update_host_initiators(module, array)
        if module.params['volume']:
            current_vols = [vol['vol'] for vol in volumes]
            if (not (module.params['volume'] in current_vols)):
                changed = _connect_new_volume(module, array)
        api_version = array._list_available_rest_versions()
        if (AC_REQUIRED_API_VERSION in api_version):
            if module.params['personality']:
                changed = _update_host_personality(module, array)
        if (PREFERRED_ARRAY_API_VERSION in api_version):
            if module.params['preferred_array']:
                changed = _update_preferred_array(module, array)
    module.exit_json(changed=changed)
