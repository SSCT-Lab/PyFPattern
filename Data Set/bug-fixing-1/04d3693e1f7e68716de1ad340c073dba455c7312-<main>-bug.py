

def main():
    argument_spec = openstack_full_argument_spec(role=dict(required=True), user=dict(required=False), group=dict(required=False), project=dict(required=False), domain=dict(required=False), state=dict(default='present', choices=['absent', 'present']))
    module_kwargs = openstack_module_kwargs(required_one_of=[['user', 'group']])
    module = AnsibleModule(argument_spec, supports_check_mode=True, **module_kwargs)
    role = module.params.get('role')
    user = module.params.get('user')
    group = module.params.get('group')
    project = module.params.get('project')
    domain = module.params.get('domain')
    state = module.params.get('state')
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        filters = {
            
        }
        r = cloud.get_role(role)
        if (r is None):
            module.fail_json(msg=('Role %s is not valid' % role))
        filters['role'] = r['id']
        if user:
            u = cloud.get_user(user)
            if (u is None):
                module.fail_json(msg=('User %s is not valid' % user))
            filters['user'] = u['id']
        if group:
            g = cloud.get_group(group)
            if (g is None):
                module.fail_json(msg=('Group %s is not valid' % group))
            filters['group'] = g['id']
        if domain:
            d = cloud.get_domain(domain)
            if (d is None):
                module.fail_json(msg=('Domain %s is not valid' % domain))
            filters['domain'] = d['id']
        if project:
            if domain:
                p = cloud.get_project(project, domain_id=filters['domain'])
            else:
                p = cloud.get_project(project)
            if (p is None):
                module.fail_json(msg=('Project %s is not valid' % project))
            filters['project'] = p['id']
        assignment = cloud.list_role_assignments(filters=filters)
        if module.check_mode:
            module.exit_json(changed=_system_state_change(state, assignment))
        changed = False
        if (state == 'present'):
            if (not assignment):
                kwargs = _build_kwargs(user, group, project, domain)
                cloud.grant_role(role, **kwargs)
                changed = True
        elif (state == 'absent'):
            if assignment:
                kwargs = _build_kwargs(user, group, project, domain)
                cloud.revoke_role(role, **kwargs)
                changed = True
        module.exit_json(changed=changed)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))
