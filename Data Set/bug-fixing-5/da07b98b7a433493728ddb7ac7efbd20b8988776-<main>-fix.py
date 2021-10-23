def main():
    argument_spec = openstack_full_argument_spec(size=dict(default=None, type='int'), volume_type=dict(default=None), display_name=dict(required=True, aliases=['name']), display_description=dict(default=None, aliases=['description']), image=dict(default=None), snapshot_id=dict(default=None), volume=dict(default=None), state=dict(default='present', choices=['absent', 'present']), scheduler_hints=dict(default=None, type='dict'), metadata=dict(default=None, type='dict'), bootable=dict(type='bool', default=False))
    module_kwargs = openstack_module_kwargs(mutually_exclusive=[['image', 'snapshot_id', 'volume']])
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, **module_kwargs)
    state = module.params['state']
    if ((state == 'present') and (not module.params['size'])):
        module.fail_json(msg="Size is required when state is 'present'")
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        if (state == 'present'):
            _present_volume(module, cloud)
        if (state == 'absent'):
            _absent_volume(module, cloud, sdk)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e))