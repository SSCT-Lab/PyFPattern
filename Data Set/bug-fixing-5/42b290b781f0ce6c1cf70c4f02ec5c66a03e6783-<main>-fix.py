def main():
    argument_spec = openstack_full_argument_spec(server=dict(required=True), action=dict(required=True, choices=['stop', 'start', 'pause', 'unpause', 'lock', 'unlock', 'suspend', 'resume', 'rebuild']), image=dict(required=False))
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, supports_check_mode=True, required_if=[('action', 'rebuild', ['image'])], **module_kwargs)
    action = module.params['action']
    wait = module.params['wait']
    timeout = module.params['timeout']
    image = module.params['image']
    (sdk, cloud) = openstack_cloud_from_module(module)
    try:
        server = cloud.get_server(module.params['server'])
        if (not server):
            module.fail_json(msg=('Could not find server %s' % server))
        status = server.status
        if module.check_mode:
            module.exit_json(changed=_system_state_change(action, status))
        if (action == 'stop'):
            if (not _system_state_change(action, status)):
                module.exit_json(changed=False)
            cloud.compute.post(_action_url(server.id), json={
                'os-stop': None,
            })
            if wait:
                _wait(timeout, cloud, server, action, module, sdk)
            module.exit_json(changed=True)
        if (action == 'start'):
            if (not _system_state_change(action, status)):
                module.exit_json(changed=False)
            cloud.compute.post(_action_url(server.id), json={
                'os-start': None,
            })
            if wait:
                _wait(timeout, cloud, server, action, module, sdk)
            module.exit_json(changed=True)
        if (action == 'pause'):
            if (not _system_state_change(action, status)):
                module.exit_json(changed=False)
            cloud.compute.post(_action_url(server.id), json={
                'pause': None,
            })
            if wait:
                _wait(timeout, cloud, server, action, module, sdk)
            module.exit_json(changed=True)
        elif (action == 'unpause'):
            if (not _system_state_change(action, status)):
                module.exit_json(changed=False)
            cloud.compute.post(_action_url(server.id), json={
                'unpause': None,
            })
            if wait:
                _wait(timeout, cloud, server, action, module, sdk)
            module.exit_json(changed=True)
        elif (action == 'lock'):
            cloud.compute.post(_action_url(server.id), json={
                'lock': None,
            })
            module.exit_json(changed=True)
        elif (action == 'unlock'):
            cloud.compute.post(_action_url(server.id), json={
                'unlock': None,
            })
            module.exit_json(changed=True)
        elif (action == 'suspend'):
            if (not _system_state_change(action, status)):
                module.exit_json(changed=False)
            cloud.compute.post(_action_url(server.id), json={
                'suspend': None,
            })
            if wait:
                _wait(timeout, cloud, server, action, module, sdk)
            module.exit_json(changed=True)
        elif (action == 'resume'):
            if (not _system_state_change(action, status)):
                module.exit_json(changed=False)
            cloud.compute.post(_action_url(server.id), json={
                'resume': None,
            })
            if wait:
                _wait(timeout, cloud, server, action, module, sdk)
            module.exit_json(changed=True)
        elif (action == 'rebuild'):
            image = cloud.get_image(image)
            if (image is None):
                module.fail_json(msg='Image does not exist')
            cloud.compute.post(_action_url(server.id), json={
                'rebuild': None,
            })
            if wait:
                _wait(timeout, cloud, server, action, module, sdk)
            module.exit_json(changed=True)
    except sdk.exceptions.OpenStackCloudException as e:
        module.fail_json(msg=str(e), extra_data=e.extra_data)