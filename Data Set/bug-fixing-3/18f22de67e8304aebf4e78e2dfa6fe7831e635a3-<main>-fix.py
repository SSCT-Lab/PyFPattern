def main():
    argument_spec = openstack_full_argument_spec(name=dict(required=True), tag=dict(required=False, default=None), template=dict(default=None), environment=dict(default=None, type='list'), parameters=dict(default={
        
    }, type='dict'), rollback=dict(default=False, type='bool'), timeout=dict(default=3600, type='int'), state=dict(default='present', choices=['absent', 'present']))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=True, **module_kwargs)
    state = module.params['state']
    name = module.params['name']
    if (state == 'present'):
        for p in ['template']:
            if (not module.params[p]):
                module.fail_json(msg=('%s required with present state' % p))
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        stack = cloud.get_stack(name)
        if module.check_mode:
            module.exit_json(changed=_system_state_change(module, stack, cloud))
        if (state == 'present'):
            parameters = module.params['parameters']
            if module.params['tag']:
                parameters['tags'] = module.params['tag']
                from distutils.version import StrictVersion
                min_version = '0.28.0'
                if ((StrictVersion(sdk.version.__version__) < StrictVersion(min_version)) and stack):
                    module.warn('To update tags using os_stack module, theinstalled version of the openstacksdklibrary MUST be >={min_version}'.format(min_version=min_version))
            if (not stack):
                stack = _create_stack(module, stack, cloud, sdk, parameters)
            else:
                stack = _update_stack(module, stack, cloud, sdk, parameters)
            module.exit_json(changed=True, stack=stack, id=stack.id)
        elif (state == 'absent'):
            if (not stack):
                changed = False
            else:
                changed = True
                if (not cloud.delete_stack(name, wait=module.params['wait'])):
                    module.fail_json(msg=('delete stack failed for stack: %s' % name))
            module.exit_json(changed=changed)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=to_native(e))