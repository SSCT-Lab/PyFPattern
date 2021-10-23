def _set_host_initiators(module, array):
    if (module.params['protocol'] in ['iscsi', 'mixed']):
        if module.params['iqn']:
            array.set_host(module.params['host'], addiqnlist=module.params['iqn'])
    if (module.params['protocol'] in ['fc', 'mixed']):
        if module.params['wwns']:
            array.set_host(module.params['host'], addwwnlist=module.params['wwns'])