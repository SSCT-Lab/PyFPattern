

def main():
    argument_spec = openstack_full_argument_spec(name=dict(required=True), description=dict(required=False, default=None), domain_id=dict(required=False, default=None), state=dict(default='present', choices=['absent', 'present']))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=True, **module_kwargs)
    if (not HAS_SHADE):
        module.fail_json(msg='shade is required for this module')
    name = module.params.pop('name')
    description = module.params.pop('description')
    domain_id = module.params.pop('domain_id')
    state = module.params.pop('state')
    try:
        cloud = shade.operator_cloud(**module.params)
        if domain_id:
            group = cloud.get_group(name, filters={
                'domain_id': domain_id,
            })
        else:
            group = cloud.get_group(name)
        if module.check_mode:
            module.exit_json(changed=_system_state_change(state, description, group))
        if (state == 'present'):
            if (group is None):
                group = cloud.create_group(name=name, description=description, domain=domain_id)
                changed = True
            elif ((description is not None) and (group.description != description)):
                group = cloud.update_group(group.id, description=description)
                changed = True
            else:
                changed = False
            module.exit_json(changed=changed, group=group)
        elif (state == 'absent'):
            if (group is None):
                changed = False
            else:
                cloud.delete_group(group.id)
                changed = True
            module.exit_json(changed=changed)
    except shade.OpenStackCloudException as e:
        module.fail_json(msg=str(e))
