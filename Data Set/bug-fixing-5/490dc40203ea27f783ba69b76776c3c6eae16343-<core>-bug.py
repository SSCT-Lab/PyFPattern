def core(module):

    def getkeyordie(k):
        v = module.params[k]
        if (v is None):
            module.fail_json(msg=('Unable to load %s' % k))
        return v
    try:
        api_token = (module.params['api_token'] or os.environ['DO_API_TOKEN'] or os.environ['DO_API_KEY'])
    except KeyError as e:
        module.fail_json(msg=('Unable to load %s' % e.message))
    changed = True
    command = module.params['command']
    state = module.params['state']
    if (command == 'droplet'):
        Droplet.setup(api_token)
        if (state in ('active', 'present')):
            droplet = Droplet.find(id=module.params['id'])
            if ((not droplet) and module.params['unique_name']):
                droplet = Droplet.find(name=getkeyordie('name'))
            if (not droplet):
                droplet = Droplet.add(name=getkeyordie('name'), size_id=getkeyordie('size_id'), image_id=getkeyordie('image_id'), region_id=getkeyordie('region_id'), ssh_key_ids=module.params['ssh_key_ids'], virtio=module.params['virtio'], private_networking=module.params['private_networking'], backups_enabled=module.params['backups_enabled'], user_data=module.params.get('user_data'), ipv6=module.params['ipv6'])
            if droplet.is_powered_on():
                changed = False
            droplet.ensure_powered_on(wait=getkeyordie('wait'), wait_timeout=getkeyordie('wait_timeout'))
            module.exit_json(changed=changed, droplet=droplet.to_json())
        elif (state in ('absent', 'deleted')):
            droplet = Droplet.find(module.params['id'])
            if ((not droplet) and module.params['unique_name']):
                droplet = Droplet.find(name=getkeyordie('name'))
            if (not droplet):
                module.exit_json(changed=False, msg='The droplet is not found.')
            droplet.destroy()
            module.exit_json(changed=True)
    elif (command == 'ssh'):
        SSH.setup(api_token)
        name = getkeyordie('name')
        if (state in ('active', 'present')):
            key = SSH.find(name)
            if key:
                module.exit_json(changed=False, ssh_key=key.to_json())
            key = SSH.add(name, getkeyordie('ssh_pub_key'))
            module.exit_json(changed=True, ssh_key=key.to_json())
        elif (state in ('absent', 'deleted')):
            key = SSH.find(name)
            if (not key):
                module.exit_json(changed=False, msg=('SSH key with the name of %s is not found.' % name))
            key.destroy()
            module.exit_json(changed=True)