def eradicate_fs(module, blade):
    ' Eradicate Filesystem'
    if (not module.check_mode):
        try:
            blade.file_systems.delete_file_systems(module.params['name'])
            changed = True
        except Exception:
            changed = False
    module.exit_json(changed=changed)