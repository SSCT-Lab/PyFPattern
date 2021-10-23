

def main():
    argument_spec = openstack_full_argument_spec(name=dict(required=True), password=dict(required=False, default=None), email=dict(required=False, default=None), default_project=dict(required=False, default=None), domain=dict(required=False, default=None), enabled=dict(default=True, type='bool'), state=dict(default='present', choices=['absent', 'present']), update_password=dict(default='always', choices=['always', 'on_create']))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)
    if (not HAS_SHADE):
        module.fail_json(msg='shade is required for this module')
    name = module.params['name']
    password = module.params['password']
    email = module.params['email']
    default_project = module.params['default_project']
    domain = module.params['domain']
    enabled = module.params['enabled']
    state = module.params['state']
    update_password = module.params['update_password']
    try:
        cloud = shade.openstack_cloud(**module.params)
        user = cloud.get_user(name)
        domain_id = None
        if domain:
            opcloud = shade.operator_cloud(**module.params)
            domain_id = _get_domain_id(opcloud, domain)
        if (state == 'present'):
            if (update_password in ('always', 'on_create')):
                if (not password):
                    msg = ('update_password is %s but a password value is missing' % update_password)
                    self.fail_json(msg=msg)
            default_project_id = None
            if default_project:
                default_project_id = _get_default_project_id(cloud, default_project)
            if (user is None):
                user = cloud.create_user(name=name, password=password, email=email, default_project=default_project_id, domain_id=domain_id, enabled=enabled)
                changed = True
            else:
                params_dict = {
                    'email': email,
                    'enabled': enabled,
                    'password': password,
                    'update_password': update_password,
                }
                if (domain_id is not None):
                    params_dict['domain_id'] = domain_id
                if (default_project_id is not None):
                    params_dict['default_project_id'] = default_project_id
                if _needs_update(params_dict, user):
                    if (update_password == 'always'):
                        user = cloud.update_user(user['id'], password=password, email=email, default_project=default_project_id, domain_id=domain_id, enabled=enabled)
                    else:
                        user = cloud.update_user(user['id'], email=email, default_project=default_project_id, domain_id=domain_id, enabled=enabled)
                    changed = True
                else:
                    changed = False
            module.exit_json(changed=changed, user=user)
        elif (state == 'absent'):
            if (user is None):
                changed = False
            else:
                cloud.delete_user(user['id'])
                changed = True
            module.exit_json(changed=changed)
    except shade.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)
