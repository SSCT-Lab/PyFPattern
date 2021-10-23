def core(module):
    try:
        api_token = (module.params['api_token'] or os.environ['DO_API_TOKEN'] or os.environ['DO_API_KEY'])
    except KeyError as e:
        module.fail_json(msg=('Unable to load %s' % e.message))
    state = module.params['state']
    name = module.params['name']
    resource_id = module.params['resource_id']
    resource_type = module.params['resource_type']
    rest = Rest(module, {
        'Authorization': 'Bearer {}'.format(api_token),
        'Content-type': 'application/json',
    })
    if (state in 'present'):
        if (name is None):
            module.fail_json(msg='parameter `name` is missing')
        response = rest.post('tags', data={
            'name': name,
        })
        status_code = response.status_code
        json = response.json
        if (status_code == 201):
            changed = True
        elif (status_code == 422):
            changed = False
        else:
            module.exit_json(changed=False, data=json)
        if (resource_id is None):
            if (json is None):
                module.exit_json(changed=changed, data=json)
            else:
                module.exit_json(changed=changed, data=json)
        else:
            url = 'tags/{}/resources'.format(name)
            payload = {
                'resources': [{
                    'resource_id': resource_id,
                    'resource_type': resource_type,
                }],
            }
            response = rest.post(url, data=payload)
            if (response.status_code == 204):
                module.exit_json(changed=True)
            else:
                module.fail_json(msg="error tagging resource '{}': {}".format(resource_id, response.json['message']))
    elif (state in 'absent'):
        if (name is None):
            module.fail_json(msg='parameter `name` is missing')
        if resource_id:
            url = 'tags/{}/resources'.format(name)
            payload = {
                'resources': [{
                    'resource_id': resource_id,
                    'resource_type': resource_type,
                }],
            }
            response = rest.delete(url, data=payload)
        else:
            url = 'tags/{}'.format(name)
            response = rest.delete(url)
        if (response.status_code == 204):
            module.exit_json(changed=True)
        else:
            module.exit_json(changed=False, data=response.json)