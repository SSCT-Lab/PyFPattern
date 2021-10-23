def create_volume(module, array):
    'Create Volume'
    changed = True
    volfact = []
    if (not module.check_mode):
        if (('/' in module.params['name']) and (not check_vgroup(module, array))):
            module.fail_json(msg='Failed to create volume {0}. Volume Group does not exist.'.format(module.params['name']))
        if (('::' in module.params['name']) and (not check_pod(module, array))):
            module.fail_json(msg='Failed to create volume {0}. Poid does not exist'.format(module.params['name']))
        api_version = array._list_available_rest_versions()
        if (module.params['bw_qos'] or module.params['iops_qos']):
            if ((module.params['bw_qos'] and (QOS_API_VERSION in api_version)) or (module.params['iops_qos'] and (IOPS_API_VERSION in api_version))):
                if (module.params['bw_qos'] and (not module.params['iops_qos'])):
                    if (549755813888 >= int(human_to_bytes(module.params['bw_qos'])) >= 1048576):
                        try:
                            volfact = array.create_volume(module.params['name'], module.params['size'], bandwidth_limit=module.params['bw_qos'])
                        except Exception:
                            module.fail_json(msg='Volume {0} creation failed.'.format(module.params['name']))
                    else:
                        module.fail_json(msg='Bandwidth QoS value {0} out of range.'.format(module.params['bw_qos']))
                elif (module.params['iops_qos'] and (not module.params['bw_qos'])):
                    if (100000000 >= int(human_to_real(module.params['iops_qos'])) >= 100):
                        try:
                            volfact = array.create_volume(module.params['name'], module.params['size'], iops_limit=module.params['iops_qos'])
                        except Exception:
                            module.fail_json(msg='Volume {0} creation failed.'.format(module.params['name']))
                    else:
                        module.fail_json(msg='IOPs QoS value {0} out of range.'.format(module.params['iops_qos']))
                else:
                    bw_qos_size = int(human_to_bytes(module.params['bw_qos']))
                    if ((100000000 >= int(human_to_real(module.params['iops_qos'])) >= 100) and (549755813888 >= bw_qos_size >= 1048576)):
                        try:
                            volfact = array.create_volume(module.params['name'], module.params['size'], iops_limit=module.params['iops_qos'], bandwidth_limit=module.params['bw_qos'])
                        except Exception:
                            module.fail_json(msg='Volume {0} creation failed.'.format(module.params['name']))
                    else:
                        module.fail_json(msg='IOPs or Bandwidth QoS value out of range.')
        else:
            try:
                volfact = array.create_volume(module.params['name'], module.params['size'])
            except Exception:
                module.fail_json(msg='Volume {0} creation failed.'.format(module.params['name']))
    module.exit_json(changed=changed, volume=volfact)