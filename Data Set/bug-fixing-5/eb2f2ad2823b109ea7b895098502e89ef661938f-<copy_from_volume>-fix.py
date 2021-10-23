def copy_from_volume(module, array):
    'Create Volume Clone'
    changed = True
    volfact = []
    if (not module.check_mode):
        tgt = get_target(module, array)
        if (tgt is None):
            try:
                volfact = array.copy_volume(module.params['name'], module.params['target'])
            except Exception:
                module.fail_json(msg='Copy volume {0} to volume {1} failed.'.format(module.params['name'], module.params['target']))
        elif ((tgt is not None) and module.params['overwrite']):
            try:
                volfact = array.copy_volume(module.params['name'], module.params['target'], overwrite=module.params['overwrite'])
            except Exception:
                module.fail_json(msg='Copy volume {0} to volume {1} failed.'.format(module.params['name'], module.params['target']))
    module.exit_json(changed=changed, volume=volfact)