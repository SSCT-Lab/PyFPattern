def create_volume(module, array):
    'Create Volume'
    changed = False
    if module.params['qos']:
        if (549755813888 >= int(human_to_bytes(module.params['qos'])) >= 1048576):
            try:
                volume = array.create_volume(module.params['name'], module.params['size'], bandwidth_limit=module.params['qos'])
                changed = True
            except Exception:
                module.fail_json(msg='Volume {0} creation failed.'.format(module.params['name']))
        else:
            module.fail_json(msg='QoS value {0} out of range.'.format(module.params['qos']))
    else:
        try:
            volume = array.create_volume(module.params['name'], module.params['size'])
            changed = True
        except Exception:
            module.fail_json(msg='Volume {0} creation failed.'.format(module.params['name']))
    module.exit_json(changed=changed, volume=volume)