def update_volume(module, array):
    'Update Volume size and/or QoS'
    changed = True
    volfact = []
    if (not module.check_mode):
        change = False
        api_version = array._list_available_rest_versions()
        vol = array.get_volume(module.params['name'])
        vol_qos = array.get_volume(module.params['name'], qos=True)
        if (QOS_API_VERSION in api_version):
            if (vol_qos['bandwidth_limit'] is None):
                vol_qos['bandwidth_limit'] = 0
        if (IOPS_API_VERSION in api_version):
            if (vol_qos['iops_limit'] is None):
                vol_qos['iops_limit'] = 0
        if module.params['size']:
            if (human_to_bytes(module.params['size']) != vol['size']):
                if (human_to_bytes(module.params['size']) > vol['size']):
                    try:
                        volfact = array.extend_volume(module.params['name'], module.params['size'])
                        change = True
                    except Exception:
                        module.fail_json(msg='Volume {0} resize failed.'.format(module.params['name']))
        if (module.params['bw_qos'] and (QOS_API_VERSION in api_version)):
            if (human_to_bytes(module.params['bw_qos']) != vol_qos['bandwidth_limit']):
                if (module.params['bw_qos'] == '0'):
                    try:
                        volfact = array.set_volume(module.params['name'], bandwidth_limit='')
                        change = True
                    except Exception:
                        module.fail_json(msg='Volume {0} Bandwidth QoS removal failed.'.format(module.params['name']))
                elif (549755813888 >= int(human_to_bytes(module.params['bw_qos'])) >= 1048576):
                    try:
                        volfact = array.set_volume(module.params['name'], bandwidth_limit=module.params['bw_qos'])
                        change = True
                    except Exception:
                        module.fail_json(msg='Volume {0} Bandwidth QoS change failed.'.format(module.params['name']))
                else:
                    module.fail_json(msg='Bandwidth QoS value {0} out of range.'.format(module.params['bw_qos']))
        if (module.params['iops_qos'] and (IOPS_API_VERSION in api_version)):
            if (human_to_real(module.params['iops_qos']) != vol_qos['iops_limit']):
                if (module.params['iops_qos'] == '0'):
                    try:
                        volfact = array.set_volume(module.params['name'], iops_limit='')
                        change = True
                    except Exception:
                        module.fail_json(msg='Volume {0} IOPs QoS removal failed.'.format(module.params['name']))
                elif (100000000 >= int(human_to_real(module.params['iops_qos'])) >= 100):
                    try:
                        volfact = array.set_volume(module.params['name'], iops_limit=module.params['iops_qos'])
                    except Exception:
                        module.fail_json(msg='Volume {0} IOPs QoS change failed.'.format(module.params['name']))
                else:
                    module.fail_json(msg='Bandwidth QoS value {0} out of range.'.format(module.params['bw_qos']))
        module.exit_json(changed=change, volume=volfact)
    module.exit_json(changed=changed)