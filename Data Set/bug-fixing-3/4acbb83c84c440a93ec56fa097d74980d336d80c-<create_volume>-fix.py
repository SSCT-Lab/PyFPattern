def create_volume(module, array):
    'Create Volume'
    changed = False
    if (('/' in module.params['name']) and (not check_vgroup(module, array))):
        module.fail_json(msg='Failed to create volume {0}. Volume Group does not exist.'.format(module.params['name']))
    if (('::' in module.params['name']) and (not check_pod(module, array))):
        module.fail_json(msg='Failed to create volume {0}. Poid does not exist'.format(module.params['name']))
    volfact = []
    api_version = array._list_available_rest_versions()
    if (module.params['qos'] and (QOS_API_VERSION in api_version)):
        if (549755813888 >= int(human_to_bytes(module.params['qos'])) >= 1048576):
            try:
                volfact = array.create_volume(module.params['name'], module.params['size'], bandwidth_limit=module.params['qos'])
                changed = True
            except Exception:
                module.fail_json(msg='Volume {0} creation failed.'.format(module.params['name']))
        else:
            module.fail_json(msg='QoS value {0} out of range.'.format(module.params['qos']))
    else:
        try:
            volfact = array.create_volume(module.params['name'], module.params['size'])
            changed = True
        except Exception:
            module.fail_json(msg='Volume {0} creation failed.'.format(module.params['name']))
    module.exit_json(changed=changed, volume=volfact)