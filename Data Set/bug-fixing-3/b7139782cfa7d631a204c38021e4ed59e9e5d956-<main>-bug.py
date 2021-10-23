def main():
    argument_spec = openstack_full_argument_spec(state=dict(default='present', choices=['absent', 'present']), name=dict(required=True), admin_state_up=dict(type='bool', default=True), enable_snat=dict(type='bool', default=True), network=dict(default=None), interfaces=dict(type='list', default=None), external_fixed_ips=dict(type='list', default=None), project=dict(default=None))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=True, **module_kwargs)
    state = module.params['state']
    name = module.params['name']
    network = module.params['network']
    project = module.params['project']
    if (module.params['external_fixed_ips'] and (not network)):
        module.fail_json(msg='network is required when supplying external_fixed_ips')
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        if (project is not None):
            proj = cloud.get_project(project)
            if (proj is None):
                module.fail_json(msg=('Project %s could not be found' % project))
            project_id = proj['id']
            filters = {
                'tenant_id': project_id,
            }
        else:
            project_id = None
            filters = None
        router = cloud.get_router(name, filters=filters)
        net = None
        if network:
            net = cloud.get_network(network)
            if (not net):
                module.fail_json(msg=('network %s not found' % network))
        (external_ids, subnet_internal_ids, internal_portids) = _validate_subnets(module, cloud)
        if module.check_mode:
            module.exit_json(changed=_system_state_change(cloud, module, router, net, subnet_internal_ids, internal_portids))
        if (state == 'present'):
            changed = False
            if (not router):
                kwargs = _build_kwargs(cloud, module, router, net)
                if project_id:
                    kwargs['project_id'] = project_id
                router = cloud.create_router(**kwargs)
                for int_s_id in subnet_internal_ids:
                    cloud.add_router_interface(router, subnet_id=int_s_id)
                changed = True
                for int_p_id in internal_portids:
                    cloud.add_router_interface(router, port_id=int_p_id)
                changed = True
            elif _needs_update(cloud, module, router, net, subnet_internal_ids, internal_portids):
                kwargs = _build_kwargs(cloud, module, router, net)
                updated_router = cloud.update_router(**kwargs)
                if (not updated_router):
                    changed = False
                if (internal_portids or subnet_internal_ids):
                    router = updated_router
                    ports = _router_internal_interfaces(cloud, router)
                    for port in ports:
                        cloud.remove_router_interface(router, port_id=port['id'])
                if internal_portids:
                    (external_ids, subnet_internal_ids, internal_portids) = _validate_subnets(module, cloud)
                    for int_p_id in internal_portids:
                        cloud.add_router_interface(router, port_id=int_p_id)
                    changed = True
                if subnet_internal_ids:
                    for s_id in subnet_internal_ids:
                        cloud.add_router_interface(router, subnet_id=s_id)
                    changed = True
            module.exit_json(changed=changed, router=router, id=router['id'])
        elif (state == 'absent'):
            if (not router):
                module.exit_json(changed=False)
            else:
                ports = _router_internal_interfaces(cloud, router)
                router_id = router['id']
                for port in ports:
                    cloud.remove_router_interface(router, port_id=port['id'])
                cloud.delete_router(router_id)
                module.exit_json(changed=True)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))