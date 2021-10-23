def generate_default_dict(array):
    default_facts = {
        
    }
    defaults = array.get()
    api_version = array._list_available_rest_versions()
    if (AC_REQUIRED_API_VERSION in api_version):
        pods = array.get_pods()
        default_facts['pods'] = len(pods)
    hosts = array.list_hosts()
    snaps = array.list_volumes(snap=True, pending=True)
    pgroups = array.list_pgroups(pending=True)
    hgroups = array.list_hgroups()
    default_facts['array_name'] = defaults['array_name']
    default_facts['purity_version'] = defaults['version']
    default_facts['hosts'] = len(hosts)
    default_facts['snapshots'] = len(snaps)
    default_facts['protection_groups'] = len(pgroups)
    default_facts['hostgroups'] = len(hgroups)
    return default_facts