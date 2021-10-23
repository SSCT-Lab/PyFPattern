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
        'Authorization': 'Bearer {0}'.format(api_token),
        'Content-type': 'application/json',
    })
    response = rest.get('account')
    if (response.status_code == 401):
        module.fail_json(msg='Failed to login using api_token, please verify validity of api_token')
    if (state == 'present'):
        response = rest.get('tags/{0}'.format(name))
        status_code = response.status_code
        resp_json = response.json
        changed = False
        if ((status_code == 200) and (resp_json['tag']['name'] == name)):
            changed = False
        else:
            response = rest.post('tags', data={
                'name': name,
            })
            status_code = response.status_code
            resp_json = response.json
            if (status_code == 201):
                changed = True
            elif (status_code == 422):
                changed = False
            else:
                module.exit_json(changed=False, data=resp_json)
        if (resource_id is None):
            module.exit_json(changed=changed, data=resp_json)
        else:
            found = False
            url = '{0}?tag_name={1}'.format(resource_type, name)
            response = rest.get(url)
            status_code = response.status_code
            resp_json = response.json
            if (status_code == 200):
                for resource in resp_json['droplets']:
                    if ((not found) and (resource['id'] == int(resource_id))):
                        found = True
                        break
                if (not found):
                    url = 'tags/{0}/resources'.format(name)
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
                        module.fail_json(msg="error tagging resource '{0}': {1}".format(resource_id, response.json['message']))
                else:
                    module.exit_json(changed=False)
            else:
                module.fail_json(msg=resp_json['message'])
    elif (state == 'absent'):
        if resource_id:
            url = 'tags/{0}/resources'.format(name)
            payload = {
                'resources': [{
                    'resource_id': resource_id,
                    'resource_type': resource_type,
                }],
            }
            response = rest.delete(url, data=payload)
        else:
            url = 'tags/{0}'.format(name)
            response = rest.delete(url)
        if (response.status_code == 204):
            module.exit_json(changed=True)
        else:
            module.exit_json(changed=False, data=response.json)