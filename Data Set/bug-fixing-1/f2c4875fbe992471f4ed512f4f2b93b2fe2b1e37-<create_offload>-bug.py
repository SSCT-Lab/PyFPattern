

def create_offload(module, array):
    'Create offload target'
    changed = False
    try:
        if (not array.get_network_interface('@offload.data')['enabled']):
            module.fail_json(msg='Offload Network interface not enabled. Please resolve.')
    except Exception:
        module.fail_json(msg='Offload Network interface not correctly configured. Please resolve.')
    ra_facts = {
        
    }
    if (module.params['protocol'] == 'nfs'):
        try:
            array.connect_nfs_offload(module.params['name'], mount_point=module.params['share'], address=module.params['address'], mount_options=module.params['options'])
            changed = True
        except Exception:
            module.fail_json(msg='Failed to create NFS offload {0}. Please perform diagnostic checks.'.format(module.params['name']))
    if (module.params['protocol'] == 's3'):
        try:
            array.connect_s3_offload(module.params['name'], access_key_id=module.params['access_key'], secret_access_key=module.params['secret'], bucket=module.params['bucket'], initialize=module.params['initialize'])
            changed = True
        except Exception:
            module.fail_json(msg='Failed to create S3 offload {0}. Please perform diagnostic checks.'.format(module.params['name']))
    module.exit_json(changed=changed, ansible_facts=ra_facts)
