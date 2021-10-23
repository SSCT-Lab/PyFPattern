def _cf_simple_api_call(self, api_call, method='GET', payload=None):
    headers = {
        'X-Auth-Email': self.account_email,
        'X-Auth-Key': self.account_api_token,
        'Content-Type': 'application/json',
    }
    data = None
    if payload:
        try:
            data = json.dumps(payload)
        except Exception as e:
            self.module.fail_json(msg=('Failed to encode payload as JSON: %s ' % to_native(e)))
    (resp, info) = fetch_url(self.module, (self.cf_api_endpoint + api_call), headers=headers, data=data, method=method, timeout=self.timeout)
    if (info['status'] not in [200, 304, 400, 401, 403, 429, 405, 415]):
        self.module.fail_json(msg='Failed API call {0}; got unexpected HTTP code {1}'.format(api_call, info['status']))
    error_msg = ''
    if (info['status'] == 401):
        error_msg = 'API user does not have permission; Status: {0}; Method: {1}: Call: {2}'.format(info['status'], method, api_call)
    elif (info['status'] == 403):
        error_msg = 'API request not authenticated; Status: {0}; Method: {1}: Call: {2}'.format(info['status'], method, api_call)
    elif (info['status'] == 429):
        error_msg = 'API client is rate limited; Status: {0}; Method: {1}: Call: {2}'.format(info['status'], method, api_call)
    elif (info['status'] == 405):
        error_msg = 'API incorrect HTTP method provided; Status: {0}; Method: {1}: Call: {2}'.format(info['status'], method, api_call)
    elif (info['status'] == 415):
        error_msg = 'API request is not valid JSON; Status: {0}; Method: {1}: Call: {2}'.format(info['status'], method, api_call)
    elif (info['status'] == 400):
        error_msg = 'API bad request; Status: {0}; Method: {1}: Call: {2}'.format(info['status'], method, api_call)
    result = None
    try:
        content = resp.read()
    except AttributeError:
        if info['body']:
            content = info['body']
        else:
            error_msg += '; The API response was empty'
    if content:
        try:
            result = json.loads(to_text(content, errors='surrogate_then_strict'))
        except (json.JSONDecodeError, UnicodeError) as e:
            error_msg += '; Failed to parse API response with error {0}: {1}'.format(to_native(e), content)
    if ((info['status'] not in [200, 304]) and (result is None)):
        self.module.fail_json(msg=error_msg)
    if (not result['success']):
        error_msg += '; Error details: '
        for error in result['errors']:
            error_msg += 'code: {0}, error: {1}; '.format(error['code'], error['message'])
            if ('error_chain' in error):
                for chain_error in error['error_chain']:
                    error_msg += 'code: {0}, error: {1}; '.format(chain_error['code'], chain_error['message'])
        self.module.fail_json(msg=error_msg)
    return (result, info['status'])