def _set_host_initiators(module, array):
    'Set host initiators.'
    if (module.params['protocol'] in ['nvme', 'mixed']):
        if module.params['nqn']:
            try:
                array.set_host(module.params['host'], nqnlist=module.params['nqn'])
            except Exception:
                module.fail_json(msg='Setting of NVMe NQN failed.')
    if (module.params['protocol'] in ['iscsi', 'mixed']):
        if module.params['iqn']:
            try:
                array.set_host(module.params['host'], iqnlist=module.params['iqn'])
            except Exception:
                module.fail_json(msg='Setting of iSCSI IQN failed.')
    if (module.params['protocol'] in ['fc', 'mixed']):
        if module.params['wwns']:
            try:
                array.set_host(module.params['host'], wwnlist=module.params['wwns'])
            except Exception:
                module.fail_json(msg='Setting of FC WWNs failed.')