def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent'], default='present'), name=dict(default=None, required=True), description=dict(default=None), local=dict(type='bool'), id=dict(default=None), compatibility_version=dict(default=None), quota_mode=dict(choices=['disabled', 'audit', 'enabled']), comment=dict(default=None), mac_pool=dict(default=None), force=dict(default=None, type='bool'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_sdk(module)
    check_params(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        data_centers_service = connection.system_service().data_centers_service()
        data_centers_module = DatacentersModule(connection=connection, module=module, service=data_centers_service)
        state = module.params['state']
        if (state == 'present'):
            ret = data_centers_module.create()
        elif (state == 'absent'):
            ret = data_centers_module.remove(force=module.params['force'])
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))