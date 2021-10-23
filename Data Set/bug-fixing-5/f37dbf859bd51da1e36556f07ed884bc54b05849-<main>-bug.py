def main():
    argument_spec = openstack_full_argument_spec(security_group=dict(required=True), protocol=dict(default=None, choices=[None, 'tcp', 'udp', 'icmp', '112', '132']), port_range_min=dict(required=False, type='int'), port_range_max=dict(required=False, type='int'), remote_ip_prefix=dict(required=False, default=None), remote_group=dict(required=False, default=None), ethertype=dict(default='IPv4', choices=['IPv4', 'IPv6']), direction=dict(default='ingress', choices=['egress', 'ingress']), state=dict(default='present', choices=['absent', 'present']), project=dict(default=None))
    module_kwargs = openstack_module_kwargs(mutually_exclusive=[['remote_ip_prefix', 'remote_group']])
    module = AnsibleModule(argument_spec, supports_check_mode=True, **module_kwargs)
    state = module.params['state']
    security_group = module.params['security_group']
    remote_group = module.params['remote_group']
    project = module.params['project']
    changed = False
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        if (project is not None):
            proj = cloud.get_project(project)
            if (proj is None):
                module.fail_json(msg=('Project %s could not be found' % project))
            project_id = proj['id']
        else:
            project_id = cloud.current_project_id
        if project_id:
            filters = {
                'tenant_id': project_id,
            }
        else:
            filters = None
        secgroup = cloud.get_security_group(security_group, filters=filters)
        if remote_group:
            remotegroup = cloud.get_security_group(remote_group, filters=filters)
        else:
            remotegroup = {
                'id': None,
            }
        if module.check_mode:
            module.exit_json(changed=_system_state_change(module, secgroup, remotegroup))
        if (state == 'present'):
            if (not secgroup):
                module.fail_json(msg=('Could not find security group %s' % security_group))
            rule = _find_matching_rule(module, secgroup, remotegroup)
            if (not rule):
                kwargs = {
                    
                }
                if project_id:
                    kwargs['project_id'] = project_id
                rule = cloud.create_security_group_rule(secgroup['id'], port_range_min=module.params['port_range_min'], port_range_max=module.params['port_range_max'], protocol=module.params['protocol'], remote_ip_prefix=module.params['remote_ip_prefix'], remote_group_id=remotegroup['id'], direction=module.params['direction'], ethertype=module.params['ethertype'], **kwargs)
                changed = True
            module.exit_json(changed=changed, rule=rule, id=rule['id'])
        if ((state == 'absent') and secgroup):
            rule = _find_matching_rule(module, secgroup, remotegroup)
            if rule:
                cloud.delete_security_group_rule(rule['id'])
                changed = True
        module.exit_json(changed=changed)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))