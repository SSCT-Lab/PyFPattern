def get_crumb(module):
    (resp, info) = fetch_url(module, (module.params['url'] + '/crumbIssuer/api/json'), method='GET')
    if (info['status'] != 200):
        module.fail_json(msg=((('HTTP error ' + str(info['status'])) + ' ') + info['msg']), output='')
    content = to_native(resp.read())
    return json.loads(content)