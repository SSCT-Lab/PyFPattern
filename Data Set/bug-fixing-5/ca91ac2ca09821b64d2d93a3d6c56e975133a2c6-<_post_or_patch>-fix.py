def _post_or_patch(self, api_call, method, data):
    headers = self._auth_header.copy()
    if (data is not None):
        data = self._module.jsonify(data)
        headers['Content-type'] = 'application/json'
    (resp, info) = fetch_url(self._module, (API_URL + api_call), headers=headers, method=method, data=data, timeout=self._module.params['api_timeout'])
    if (info['status'] in (200, 201)):
        return self._module.from_json(to_text(resp.read(), errors='surrogate_or_strict'))
    elif (info['status'] == 204):
        return None
    else:
        self._module.fail_json(msg=('Failure while calling the cloudscale.ch API with %s for "%s".' % (method, api_call)), fetch_url_info=info)