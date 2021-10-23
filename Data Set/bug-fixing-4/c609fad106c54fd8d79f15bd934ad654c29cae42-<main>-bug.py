def main():
    argument_spec = ovirt_full_argument_spec(state=dict(type='str', default='present', choices=['absent', 'present']), network=dict(type='str', required=True), data_center=dict(type='str', required=True), description=dict(type='str'), name=dict(type='str', required=True), network_filter=dict(type='str'), custom_properties=dict(type='list'), qos=dict(type='str'), pass_through=dict(type='str', choices=['disabled', 'enabled']), port_mirroring=dict(type='bool'), migratable=dict(type='bool'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        vnic_services = connection.system_service().vnic_profiles_service()
        entitynics_module = EntityVnicPorfileModule(connection=connection, module=module, service=vnic_services)
        state = module.params['state']
        if (state == 'present'):
            ret = entitynics_module.create()
        elif (state == 'absent'):
            ret = entitynics_module.remove()
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))