def eradicate_fs(module, blade):
    ' Eradicate Filesystem'
    changed = True
    if (not module.check_mode):
        try:
            blade.file_systems.delete_file_systems(module.params['name'])
        except Exception:
            module.fail_json(msg='Failed to eradicate filesystem {0}.'.format(module.params['name']))
    module.exit_json(changed=changed)