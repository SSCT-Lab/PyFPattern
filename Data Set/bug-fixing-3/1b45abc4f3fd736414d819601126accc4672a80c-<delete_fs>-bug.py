def delete_fs(module, blade):
    ' Delete Filesystem'
    if (not module.check_mode):
        try:
            blade.file_systems.update_file_systems(name=module.params['name'], attributes=FileSystem(nfs=NfsRule(enabled=False), smb=ProtocolRule(enabled=False), http=ProtocolRule(enabled=False), destroyed=True))
            changed = True
            if module.params['eradicate']:
                try:
                    blade.file_systems.delete_file_systems(module.params['name'])
                    changed = True
                except Exception:
                    changed = False
        except Exception:
            changed = False
    module.exit_json(changed=changed)