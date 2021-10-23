

def update_host(module, array):
    changed = True
    if (not module.check_mode):
        init_changed = vol_changed = pers_changed = pref_changed = False
        volumes = array.list_host_connections(module.params['host'])
        if (module.params['iqn'] or module.params['wwns'] or module.params['nqn']):
            init_changed = _update_host_initiators(module, array)
        if module.params['volume']:
            current_vols = [vol['vol'] for vol in volumes]
            if (not (module.params['volume'] in current_vols)):
                vol_changed = _connect_new_volume(module, array)
        api_version = array._list_available_rest_versions()
        if (AC_REQUIRED_API_VERSION in api_version):
            if module.params['personality']:
                pers_changed = _update_host_personality(module, array)
        if (PREFERRED_ARRAY_API_VERSION in api_version):
            if module.params['preferred_array']:
                pref_changed = _update_preferred_array(module, array)
        changed = (init_changed or vol_changed or pers_changed or pref_changed)
    module.exit_json(changed=changed)
