def main():
    argument_spec = openstack_full_argument_spec(name=dict(required=True), tag=dict(required=False, default=None), template=dict(default=None), environment=dict(default=None, type='list'), parameters=dict(default={
        
    }, type='dict'), rollback=dict(default=False, type='bool'), timeout=dict(default=3600, type='int'), state=dict(default='present', choices=['absent', 'present']))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=True, **module_kwargs)
    min_version = '1.8.0'
    tag = module.params['tag']
    if (tag is not None):
        min_version = '1.26.0'
    state = module.params['state']
    name = module.params['name']
    if (state == 'present'):
        for p in ['template']:
            if (not module.params[p]):
                module.fail_json(msg=('%s required with present state' % p))
    (shade, cloud) = openstack_cloud_from_module(module, min_version='1.26.0')
    try:
        stack = cloud.get_stack(name)
        if module.check_mode:
            module.exit_json(changed=_system_state_change(module, stack, cloud))
        if (state == 'present'):
            if (not stack):
                stack = _create_stack(module, stack, cloud, shade)
            else:
                stack = _update_stack(module, stack, cloud, shade)
            changed = True
            module.exit_json(changed=changed, stack=stack, id=stack.id)
        elif (state == 'absent'):
            if (not stack):
                changed = False
            else:
                changed = True
                if (not cloud.delete_stack(name, wait=module.params['wait'])):
                    module.fail_json(msg=('delete stack failed for stack: %s' % name))
            module.exit_json(changed=changed)
    except shade.OpenStackCloudException as e:
        module.fail_json(msg=str(e))