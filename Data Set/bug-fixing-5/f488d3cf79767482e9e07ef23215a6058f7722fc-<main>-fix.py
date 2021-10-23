def main():
    argument_spec = openstack_full_argument_spec(server=dict(required=True), volume=dict(required=True), device=dict(default=None), state=dict(default='present', choices=['absent', 'present']))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=True, **module_kwargs)
    state = module.params['state']
    wait = module.params['wait']
    timeout = module.params['timeout']
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        server = cloud.get_server(module.params['server'])
        volume = cloud.get_volume(module.params['volume'])
        if (not volume):
            module.fail_json(msg=('volume %s is not found' % module.params['volume']))
        dev = cloud.get_volume_attach_device(volume, server.id)
        if module.check_mode:
            module.exit_json(changed=_system_state_change(state, dev))
        if (state == 'present'):
            if dev:
                module.exit_json(changed=False)
            cloud.attach_volume(server, volume, module.params['device'], wait=wait, timeout=timeout)
            server = cloud.get_server(module.params['server'])
            volume = cloud.get_volume(module.params['volume'])
            hostvars = cloud.get_openstack_vars(server)
            module.exit_json(changed=True, id=volume['id'], attachments=volume['attachments'], openstack=hostvars)
        elif (state == 'absent'):
            if (not dev):
                module.exit_json(changed=False)
            cloud.detach_volume(server, volume, wait=wait, timeout=timeout)
            module.exit_json(changed=True, result='Detached volume from server')
    except (sdk.exceptions.OpenStackCloudException, sdk.exceptions.OpenStackCloudTimeout) as e:
        module.fail_json(msg=str(e))