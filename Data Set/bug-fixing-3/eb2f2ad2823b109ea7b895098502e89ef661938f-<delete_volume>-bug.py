def delete_volume(module, array):
    ' Delete Volume'
    changed = True
    if (not module.check_mode):
        volfact = []
        try:
            array.destroy_volume(module.params['name'])
            if module.params['eradicate']:
                try:
                    volfact = array.eradicate_volume(module.params['name'])
                except Exception:
                    module.fail_json(msg='Eradicate volume {0} failed.'.format(module.params['name']))
        except Exception:
            module.fail_json(msg='Delete volume {0} failed.'.format(module.params['name']))
    module.exit_json(changed=changed, volume=volfact)