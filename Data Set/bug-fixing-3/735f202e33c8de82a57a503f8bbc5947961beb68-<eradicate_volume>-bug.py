def eradicate_volume(module, array):
    ' Eradicate Deleted Volume'
    changed = False
    try:
        volume = array.eradicate_volume(module.params['name'])
        changed = True
    except Exception:
        module.fail_json(msg='Eradication of volume {0} failed'.format(module.params['name']))
    module.exit_json(changed=changed, volume=volume)