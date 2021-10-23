def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent'], default='present'), id=dict(default=None), address=dict(default=None), path=dict(default=None), nfs_version=dict(default=None), nfs_timeout=dict(default=None, type='int'), nfs_retrans=dict(default=None, type='int'), mount_options=dict(default=None), password=dict(default=None), username=dict(default=None), port=dict(default=None, type='int'), target=dict(default=None), type=dict(default=None), vfs_type=dict(default=None), force=dict(type='bool', default=False), storage=dict(default=None))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        storage_connections_service = connection.system_service().storage_connections_service()
        storage_connection_module = StorageConnectionModule(connection=connection, module=module, service=storage_connections_service)
        entity = None
        if (module.params['id'] is None):
            entity = find_sc_by_attributes(module, storage_connections_service)
        state = module.params['state']
        if (state == 'present'):
            ret = storage_connection_module.create(entity=entity, update_params={
                'force': True,
            })
            storage_connection_module.post_present(ret['id'])
        elif (state == 'absent'):
            ret = storage_connection_module.remove(entity=entity)
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))