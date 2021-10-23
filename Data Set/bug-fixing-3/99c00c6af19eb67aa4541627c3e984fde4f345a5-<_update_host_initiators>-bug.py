def _update_host_initiators(module, array):
    'Change host initiator if iscsi or nvmef or add new FC WWNs'
    if (module.params['protocol'] in ['nvmef', 'mixed']):
        if module.params['nqn']:
            try:
                array.set_host(module.params['host'], nqnlist=module.params['nqn'])
            except Exception:
                module.fail_json(msg='Change of NVMeF NQN failed.')
    if (module.params['protocol'] in ['iscsi', 'mixed']):
        if module.params['iqn']:
            try:
                array.set_host(module.params['host'], iqnlist=module.params['iqn'])
            except Exception:
                module.fail_json(msg='Change of iSCSI IQN failed.')
    if (module.params['protocol'] in ['fc', 'mixed']):
        if module.params['wwns']:
            try:
                array.set_host(module.params['host'], addwwnlist=module.params['wwns'])
            except Exception:
                module.fail_json(msg='FC WWN additiona failed.')