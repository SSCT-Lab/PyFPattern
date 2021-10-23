

def post_annotation(module):
    user = module.params['user']
    api_key = module.params['api_key']
    name = module.params['name']
    title = module.params['title']
    url = ('https://metrics-api.librato.com/v1/annotations/%s' % name)
    params = {
        
    }
    params['title'] = title
    if (module.params['source'] is not None):
        params['source'] = module.params['source']
    if (module.params['description'] is not None):
        params['description'] = module.params['description']
    if (module.params['start_time'] is not None):
        params['start_time'] = module.params['start_time']
    if (module.params['end_time'] is not None):
        params['end_time'] = module.params['end_time']
    if (module.params['links'] is not None):
        params['links'] = module.params['links']
    json_body = module.jsonify(params)
    headers = {
        
    }
    headers['Content-Type'] = 'application/json'
    module.params['url_username'] = user
    module.params['url_password'] = api_key
    (response, info) = fetch_url(module, url, data=json_body, headers=headers)
    if (info['status'] != 200):
        module.fail_json(msg='Request Failed', reason=info.get('msg', ''), status_code=info['status'])
    response = response.read()
    module.exit_json(changed=True, annotation=response)
