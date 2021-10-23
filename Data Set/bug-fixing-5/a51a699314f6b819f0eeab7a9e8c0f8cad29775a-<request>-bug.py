def request(url, user, passwd, timeout, data=None, method=None):
    if data:
        data = json.dumps(data)
    auth = base64.encodestring(('%s:%s' % (user, passwd))).replace('\n', '')
    (response, info) = fetch_url(module, url, data=data, method=method, timeout=timeout, headers={
        'Content-Type': 'application/json',
        'Authorization': ('Basic %s' % auth),
    })
    if (info['status'] not in (200, 201, 204)):
        module.fail_json(msg=info['msg'])
    body = response.read()
    if body:
        return json.loads(body)
    else:
        return {
            
        }