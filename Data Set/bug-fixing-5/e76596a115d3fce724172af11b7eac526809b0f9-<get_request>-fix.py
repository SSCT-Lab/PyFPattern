def get_request(self, uri, parse_json_result=True, headers=None):
    (resp, info) = fetch_url(self.module, uri, method='GET', headers=headers)
    try:
        content = resp.read()
    except AttributeError:
        content = info.get('body')
    if parse_json_result:
        result = {
            
        }
        if content:
            if info['content-type'].startswith('application/json'):
                try:
                    result = self.module.from_json(content.decode('utf8'))
                except ValueError:
                    raise ModuleFailException('Failed to parse the ACME response: {0} {1}'.format(uri, content))
            else:
                result = content
    else:
        result = content
    if (info['status'] >= 400):
        raise ModuleFailException('ACME request failed: CODE: {0} RESULT: {1}'.format(info['status'], result))
    return (result, info)