

def main():
    ipv6_mode_choices = ['dhcpv6-stateful', 'dhcpv6-stateless', 'slaac']
    argument_spec = openstack_full_argument_spec(name=dict(required=True), network_name=dict(default=None), cidr=dict(default=None), ip_version=dict(default='4', choices=['4', '6']), enable_dhcp=dict(default='true', type='bool'), gateway_ip=dict(default=None), no_gateway_ip=dict(default=False, type='bool'), dns_nameservers=dict(default=None, type='list'), allocation_pool_start=dict(default=None), allocation_pool_end=dict(default=None), host_routes=dict(default=None, type='list'), ipv6_ra_mode=dict(default=None, choice=ipv6_mode_choices), ipv6_address_mode=dict(default=None, choice=ipv6_mode_choices), use_default_subnetpool=dict(default=False, type='bool'), state=dict(default='present', choices=['absent', 'present']), project=dict(default=None))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=True, **module_kwargs)
    if (not HAS_SHADE):
        module.fail_json(msg='shade is required for this module')
    state = module.params['state']
    network_name = module.params['network_name']
    cidr = module.params['cidr']
    ip_version = module.params['ip_version']
    enable_dhcp = module.params['enable_dhcp']
    subnet_name = module.params['name']
    gateway_ip = module.params['gateway_ip']
    no_gateway_ip = module.params['no_gateway_ip']
    dns = module.params['dns_nameservers']
    pool_start = module.params['allocation_pool_start']
    pool_end = module.params['allocation_pool_end']
    host_routes = module.params['host_routes']
    ipv6_ra_mode = module.params['ipv6_ra_mode']
    ipv6_a_mode = module.params['ipv6_address_mode']
    use_default_subnetpool = module.params['use_default_subnetpool']
    project = module.params.pop('project')
    if (use_default_subnetpool and (StrictVersion(shade.__version__) < StrictVersion('1.16.0'))):
        module.fail_json(msg='To utilize use_default_subnetpool, the installed version of the shade library MUST be >=1.16.0')
    if (state == 'present'):
        if (not module.params['network_name']):
            module.fail_json(msg='network_name required with present state')
        if ((not module.params['cidr']) and (not use_default_subnetpool)):
            module.fail_json(msg='cidr or use_default_subnetpool required with present state')
    if (pool_start and pool_end):
        pool = [dict(start=pool_start, end=pool_end)]
    elif (pool_start or pool_end):
        module.fail_json(msg='allocation pool requires start and end values')
    else:
        pool = None
    if (no_gateway_ip and gateway_ip):
        module.fail_json(msg='no_gateway_ip is not allowed with gateway_ip')
    try:
        cloud = shade.openstack_cloud(**module.params)
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
        subnet = cloud.get_subnet(subnet_name, filters=filters)
        if module.check_mode:
            module.exit_json(changed=_system_state_change(module, subnet, cloud))
        if (state == 'present'):
            if (not subnet):
                kwargs = dict(ip_version=ip_version, enable_dhcp=enable_dhcp, subnet_name=subnet_name, gateway_ip=gateway_ip, disable_gateway_ip=no_gateway_ip, dns_nameservers=dns, allocation_pools=pool, host_routes=host_routes, ipv6_ra_mode=ipv6_ra_mode, ipv6_address_mode=ipv6_a_mode, tenant_id=project_id)
                if use_default_subnetpool:
                    kwargs['use_default_subnetpool'] = use_default_subnetpool
                subnet = cloud.create_subnet(network_name, cidr, **kwargs)
                changed = True
            elif _needs_update(subnet, module, cloud):
                cloud.update_subnet(subnet['id'], subnet_name=subnet_name, enable_dhcp=enable_dhcp, gateway_ip=gateway_ip, disable_gateway_ip=no_gateway_ip, dns_nameservers=dns, allocation_pools=pool, host_routes=host_routes)
                changed = True
            else:
                changed = False
            module.exit_json(changed=changed, subnet=subnet, id=subnet['id'])
        elif (state == 'absent'):
            if (not subnet):
                changed = False
            else:
                changed = True
                cloud.delete_subnet(subnet_name)
            module.exit_json(changed=changed)
    except shade.OpenStackCloudException as e:
        module.fail_json(msg=str(e))
