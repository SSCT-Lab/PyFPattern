

def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent'], default='present'), name=dict(default=None, required=True, aliases=['host']), address=dict(default=None), username=dict(default=None), password=dict(default=None, no_log=True), type=dict(default=None), port=dict(default=None, type='int'), order=dict(default=None, type='int'), options=dict(default=None, type='dict'), encrypt_options=dict(default=None, type='bool', aliases=['encrypt']))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        hosts_service = connection.system_service().hosts_service()
        host = search_by_name(hosts_service, module.params['name'])
        fence_agents_service = hosts_service.host_service(host.id).fence_agents_service()
        host_pm_module = HostPmModule(connection=connection, module=module, service=fence_agents_service)
        host_module = HostModule(connection=connection, module=module, service=hosts_service)
        state = module.params['state']
        if (state == 'present'):
            agent = host_pm_module.search_entity(search_params={
                'address': module.params['address'],
                'type': module.params['type'],
            })
            ret = host_pm_module.create(entity=agent)
            host_module.create(entity=host)
        elif (state == 'absent'):
            agent = host_pm_module.search_entity(search_params={
                'address': module.params['address'],
                'type': module.params['type'],
            })
            ret = host_pm_module.remove(entity=agent)
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))
