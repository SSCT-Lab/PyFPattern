def generate_default_dict(array):
    default_info = {
        
    }
    defaults = array.get()
    api_version = array._list_available_rest_versions()
    if (AC_REQUIRED_API_VERSION in api_version):
        default_info['volume_groups'] = len(array.list_vgroups())
        default_info['connected_arrays'] = len(array.list_array_connections())
        default_info['pods'] = len(array.list_pods())
        default_info['connection_key'] = array.get(connection_key=True)['connection_key']
    hosts = array.list_hosts()
    admins = array.list_admins()
    snaps = array.list_volumes(snap=True, pending=True)
    pgroups = array.list_pgroups(pending=True)
    hgroups = array.list_hgroups()
    ct0_model = array.get_hardware('CT0')['model']
    if ct0_model:
        model = ct0_model
    else:
        ct1_model = array.get_hardware('CT1')['model']
        model = ct1_model
    default_info['array_model'] = model
    default_info['array_name'] = defaults['array_name']
    default_info['purity_version'] = defaults['version']
    default_info['hosts'] = len(hosts)
    default_info['snapshots'] = len(snaps)
    default_info['protection_groups'] = len(pgroups)
    default_info['hostgroups'] = len(hgroups)
    default_info['admins'] = len(admins)
    return default_info