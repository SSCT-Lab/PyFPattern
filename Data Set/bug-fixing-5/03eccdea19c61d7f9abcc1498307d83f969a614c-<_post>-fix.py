def _post(self, api_call, data=None):
    headers = self._auth_header.copy()
    if (data is not None):
        data = self._module.jsonify(data)
        headers['Content-type'] = 'application/json'
    (resp, info) = fetch_url(self._module, (API_URL + api_call), headers=headers, method='POST', data=data)
    if (info['status'] == 201):
        return json.loads(resp.read())
    elif (info['status'] == 204):
        return None
    else:
        self._module.fail_json(msg=('Failure while calling the cloudscale.ch API with POST for "%s": %s' % (api_call, info['body'])))