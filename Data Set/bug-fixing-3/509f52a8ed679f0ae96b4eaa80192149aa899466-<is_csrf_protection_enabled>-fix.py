def is_csrf_protection_enabled(module):
    (resp, info) = fetch_url(module, (module.params['url'] + '/api/json'), method='GET')
    if (info['status'] != 200):
        module.fail_json(msg=((('HTTP error ' + str(info['status'])) + ' ') + info['msg']), output='')
    content = to_native(resp.read())
    return json.loads(content).get('useCrumbs', False)