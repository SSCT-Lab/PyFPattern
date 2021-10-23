def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent'], default='present'), name=dict(default=None), description=dict(default=None), type=dict(default=None, required=True, choices=['os_image', 'network', 'os_volume', 'foreman'], aliases=['provider']), url=dict(default=None), username=dict(default=None), password=dict(default=None, no_log=True), tenant_name=dict(default=None, aliases=['tenant']), authentication_url=dict(default=None, aliases=['auth_url']), data_center=dict(default=None, aliases=['data_center']), read_only=dict(default=None, type='bool'), network_type=dict(default='external', choices=['external', 'neutron']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_sdk(module)
    check_params(module)
    try:
        connection = create_connection(module.params.pop('auth'))
        (provider_type, external_providers_service) = _external_provider_service(provider_type=module.params.get('type'), system_service=connection.system_service())
        external_providers_module = ExternalProviderModule(connection=connection, module=module, service=external_providers_service)
        external_providers_module.provider_type(provider_type)
        state = module.params.pop('state')
        if (state == 'absent'):
            ret = external_providers_module.remove()
        elif (state == 'present'):
            ret = external_providers_module.create()
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=False)