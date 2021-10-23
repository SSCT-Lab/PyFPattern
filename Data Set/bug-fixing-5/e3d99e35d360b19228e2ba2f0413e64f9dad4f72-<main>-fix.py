def main():
    argument_spec = ovirt_full_argument_spec(state=dict(choices=['present', 'absent', 'maintenance', 'unattached', 'imported'], default='present'), id=dict(default=None), name=dict(default=None), description=dict(default=None), comment=dict(default=None), data_center=dict(default=None), domain_function=dict(choices=['data', 'iso', 'export'], default='data', aliases=['type']), host=dict(default=None), localfs=dict(default=None, type='dict'), nfs=dict(default=None, type='dict'), iscsi=dict(default=None, type='dict'), posixfs=dict(default=None, type='dict'), glusterfs=dict(default=None, type='dict'), fcp=dict(default=None, type='dict'), destroy=dict(type='bool', default=False), format=dict(type='bool', default=False), discard_after_delete=dict(type='bool', default=True))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        storage_domains_service = connection.system_service().storage_domains_service()
        storage_domains_module = StorageDomainModule(connection=connection, module=module, service=storage_domains_service)
        state = module.params['state']
        control_state(storage_domains_module)
        if (state == 'absent'):
            host_param = module.params['host']
            if (not host_param):
                host = search_by_attributes(connection.system_service().hosts_service(), status='up')
                if (host is None):
                    raise Exception(("Not possible to remove storage domain '%s' because no host found with status `up`." % module.params['name']))
                host_param = host.name
            ret = storage_domains_module.remove(destroy=module.params['destroy'], format=module.params['format'], host=host_param)
        elif ((state == 'present') or (state == 'imported')):
            sd_id = storage_domains_module.create()['id']
            storage_domains_module.post_create_check(sd_id)
            ret = storage_domains_module.action(action='activate', action_condition=(lambda s: (s.status == sdstate.MAINTENANCE)), wait_condition=(lambda s: (s.status == sdstate.ACTIVE)), fail_condition=failed_state, search_params=({
                'id': sd_id,
            } if (state == 'imported') else None))
        elif (state == 'maintenance'):
            sd_id = storage_domains_module.create()['id']
            storage_domains_module.post_create_check(sd_id)
            ret = storage_domains_module.action(action='deactivate', action_condition=(lambda s: (s.status == sdstate.ACTIVE)), wait_condition=(lambda s: (s.status == sdstate.MAINTENANCE)), fail_condition=failed_state)
        elif (state == 'unattached'):
            ret = storage_domains_module.create()
            storage_domains_module.pre_remove(storage_domain=storage_domains_service.service(ret['id']).get())
            ret['changed'] = storage_domains_module.changed
        module.exit_json(**ret)
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))