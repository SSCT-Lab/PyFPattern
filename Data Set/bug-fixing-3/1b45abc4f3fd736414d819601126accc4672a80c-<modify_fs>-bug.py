def modify_fs(module, blade):
    'Modify Filesystem'
    changed = False
    nfsv3 = (module.params['nfs'] if (module.params['nfsv3'] is None) else module.params['nfsv3'])
    attr = {
        
    }
    if module.params['user_quota']:
        user_quota = human_to_bytes(module.params['user_quota'])
    if module.params['group_quota']:
        group_quota = human_to_bytes(module.params['group_quota'])
    if (not module.check_mode):
        api_version = blade.api_version.list_versions().versions
        fsys = get_fs(module, blade)
        if fsys.destroyed:
            attr['destroyed'] = False
            changed = True
        if module.params['size']:
            if (human_to_bytes(module.params['size']) > fsys.provisioned):
                attr['provisioned'] = human_to_bytes(module.params['size'])
                changed = True
        if (NFSV4_API_VERSION in api_version):
            if (nfsv3 and (not fsys.nfs.v3_enabled)):
                attr['nfs'] = NfsRule(v3_enabled=nfsv3)
                changed = True
            if ((not nfsv3) and fsys.nfs.v3_enabled):
                attr['nfs'] = NfsRule(v3_enabled=nfsv3)
                changed = True
            if (module.params['nfsv4'] and (not fsys.nfs.v4_1_enabled)):
                attr['nfs'] = NfsRule(v4_1_enabled=module.params['nfsv4'])
                changed = True
            if ((not module.params['nfsv4']) and fsys.nfs.v4_1_enabled):
                attr['nfs'] = NfsRule(v4_1_enabled=module.params['nfsv4'])
                changed = True
            if (nfsv3 or (module.params['nfsv4'] and fsys.nfs.v3_enabled) or fsys.nfs.v4_1_enabled):
                if (fsys.nfs.rules != module.params['nfs_rules']):
                    attr['nfs'] = NfsRule(rules=module.params['nfs_rules'])
                    changed = True
            if (module.params['user_quota'] and (user_quota != fsys.default_user_quota)):
                attr['default_user_quota'] = user_quota
                changed = True
            if (module.params['group_quota'] and (group_quota != fsys.default_group_quota)):
                attr['default_group_quota'] = group_quota
                changed = True
        else:
            if (nfsv3 and (not fsys.nfs.enabled)):
                attr['nfs'] = NfsRule(enabled=nfsv3)
                changed = True
            if ((not nfsv3) and fsys.nfs.enabled):
                attr['nfs'] = NfsRule(enabled=nfsv3)
                changed = True
            if (nfsv3 and fsys.nfs.enabled):
                if (fsys.nfs.rules != module.params['nfs_rules']):
                    attr['nfs'] = NfsRule(rules=module.params['nfs_rules'])
                    changed = True
        if (module.params['smb'] and (not fsys.smb.enabled)):
            attr['smb'] = ProtocolRule(enabled=module.params['smb'])
            changed = True
        if ((not module.params['smb']) and fsys.smb.enabled):
            attr['smb'] = ProtocolRule(enabled=module.params['smb'])
            changed = True
        if (module.params['http'] and (not fsys.http.enabled)):
            attr['http'] = ProtocolRule(enabled=module.params['http'])
            changed = True
        if ((not module.params['http']) and fsys.http.enabled):
            attr['http'] = ProtocolRule(enabled=module.params['http'])
            changed = True
        if (module.params['snapshot'] and (not fsys.snapshot_directory_enabled)):
            attr['snapshot_directory_enabled'] = module.params['snapshot']
            changed = True
        if ((not module.params['snapshot']) and fsys.snapshot_directory_enabled):
            attr['snapshot_directory_enabled'] = module.params['snapshot']
            changed = True
        if (module.params['fastremove'] and (not fsys.fast_remove_directory_enabled)):
            attr['fast_remove_directory_enabled'] = module.params['fastremove']
            changed = True
        if ((not module.params['fastremove']) and fsys.fast_remove_directory_enabled):
            attr['fast_remove_directory_enabled'] = module.params['fastremove']
            changed = True
        api_version = blade.api_version.list_versions().versions
        if (HARD_LIMIT_API_VERSION in api_version):
            if ((not module.params['hard_limit']) and fsys.hard_limit_enabled):
                attr['hard_limit_enabled'] = module.params['hard_limit']
                changed = True
        if changed:
            n_attr = FileSystem(**attr)
            try:
                blade.file_systems.update_file_systems(name=module.params['name'], attributes=n_attr)
            except Exception:
                changed = False
    module.exit_json(changed=changed)