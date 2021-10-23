def copy_from_volume(module, array):
    'Create Volume Clone'
    changed = False
    volfact = []
    tgt = get_target(module, array)
    if (tgt is None):
        try:
            volfact = array.copy_volume(module.params['name'], module.params['target'])
            changed = True
        except Exception:
            module.fail_json(msg='Copy volume {0} to volume {1} failed.'.format(module.params['name'], module.params['target']))
    elif ((tgt is not None) and module.params['overwrite']):
        try:
            volfact = array.copy_volume(module.params['name'], module.params['target'], overwrite=module.params['overwrite'])
            changed = True
        except Exception:
            module.fail_json(msg='Copy volume {0} to volume {1} failed.'.format(module.params['name'], module.params['target']))
    module.exit_json(changed=changed, volume=volfact)