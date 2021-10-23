def eradicate_volume(module, array):
    ' Eradicate Deleted Volume'
    changed = False
    volfact = []
    if module.params['eradicate']:
        try:
            array.eradicate_volume(module.params['name'])
            changed = True
        except Exception:
            module.fail_json(msg='Eradication of volume {0} failed'.format(module.params['name']))
    module.exit_json(changed=changed, volume=volfact)