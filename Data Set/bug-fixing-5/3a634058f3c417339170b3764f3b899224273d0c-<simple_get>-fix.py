def simple_get(module, url):
    (resp, info) = fetch_url(module, url, method='GET')
    result = {
        
    }
    try:
        content = resp.read()
    except AttributeError:
        content = info.get('body')
    if content:
        if info['content-type'].startswith('application/json'):
            try:
                result = module.from_json(content.decode('utf8'))
            except ValueError:
                module.fail_json(msg='Failed to parse the ACME response: {0} {1}'.format(url, content))
        else:
            result = content
    if (info['status'] >= 400):
        module.fail_json(msg='ACME request failed: CODE: {0} RESULT: {1}'.format(info['status'], result))
    return result