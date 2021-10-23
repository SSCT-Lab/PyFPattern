def _update_host_initiators(module, array, answer=False):
    'Change host initiator if iscsi or nvme or add new FC WWNs'
    if (module.params['protocol'] in ['nvme', 'mixed']):
        if module.params['nqn']:
            current_nqn = array.get_host(module.params['host'])['nqn']
            if (current_nqn != module.params['nqn']):
                try:
                    array.set_host(module.params['host'], nqnlist=module.params['nqn'])
                    answer = True
                except Exception:
                    module.fail_json(msg='Change of NVMe NQN failed.')
    if (module.params['protocol'] in ['iscsi', 'mixed']):
        if module.params['iqn']:
            current_iqn = array.get_host(module.params['host'])['iqn']
            if (current_iqn != module.params['iqn']):
                try:
                    array.set_host(module.params['host'], iqnlist=module.params['iqn'])
                    answer = True
                except Exception:
                    module.fail_json(msg='Change of iSCSI IQN failed.')
    if (module.params['protocol'] in ['fc', 'mixed']):
        if module.params['wwns']:
            module.params['wwns'] = [wwn.replace(':', '') for wwn in module.params['wwns']]
            module.params['wwns'] = [wwn.upper() for wwn in module.params['wwns']]
            current_wwn = array.get_host(module.params['host'])['wwn']
            if (current_wwn != module.params['wwns']):
                try:
                    array.set_host(module.params['host'], wwnlist=module.params['wwns'])
                    answer = True
                except Exception:
                    module.fail_json(msg='FC WWN change failed.')
    return answer