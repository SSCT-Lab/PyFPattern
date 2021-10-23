def create_fs(module, blade):
    'Create Filesystem'
    if (not module.params['size']):
        module.params['size'] = '32G'
    size = human_to_bytes(module.params['size'])
    nfsv3 = (module.params['nfs'] if (module.params['nfsv3'] is None) else module.params['nfsv3'])
    if module.params['user_quota']:
        user_quota = human_to_bytes(module.params['user_quota'])
    if module.params['group_quota']:
        group_quota = human_to_bytes(module.params['group_quota'])
    if (not module.check_mode):
        try:
            api_version = blade.api_version.list_versions().versions
            if (HARD_LIMIT_API_VERSION in api_version):
                if (NFSV4_API_VERSION in api_version):
                    fs_obj = FileSystem(name=module.params['name'], provisioned=size, fast_remove_directory_enabled=module.params['fastremove'], hard_limit_enabled=module.params['hard_limit'], snapshot_directory_enabled=module.params['snapshot'], nfs=NfsRule(v3_enabled=nfsv3, v4_1_enabled=module.params['nfsv4'], rules=module.params['nfs_rules']), smb=ProtocolRule(enabled=module.params['smb']), http=ProtocolRule(enabled=module.params['http']), default_user_quota=user_quota, default_group_quota=group_quota)
                else:
                    fs_obj = FileSystem(name=module.params['name'], provisioned=size, fast_remove_directory_enabled=module.params['fastremove'], hard_limit_enabled=module.params['hard_limit'], snapshot_directory_enabled=module.params['snapshot'], nfs=NfsRule(enabled=nfsv3, rules=module.params['nfs_rules']), smb=ProtocolRule(enabled=module.params['smb']), http=ProtocolRule(enabled=module.params['http']))
            else:
                fs_obj = FileSystem(name=module.params['name'], provisioned=size, fast_remove_directory_enabled=module.params['fastremove'], snapshot_directory_enabled=module.params['snapshot'], nfs=NfsRule(enabled=module.params['nfs'], rules=module.params['nfs_rules']), smb=ProtocolRule(enabled=module.params['smb']), http=ProtocolRule(enabled=module.params['http']))
            blade.file_systems.create_file_systems(fs_obj)
            changed = True
        except Exception:
            changed = False
    module.exit_json(changed=changed)