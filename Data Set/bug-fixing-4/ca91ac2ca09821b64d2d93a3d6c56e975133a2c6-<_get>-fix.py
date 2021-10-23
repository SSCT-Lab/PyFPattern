def _get(self, api_call):
    (resp, info) = fetch_url(self._module, (API_URL + api_call), headers=self._auth_header, timeout=self._module.params['api_timeout'])
    if (info['status'] == 200):
        return self._module.from_json(to_text(resp.read(), errors='surrogate_or_strict'))
    elif (info['status'] == 404):
        return None
    else:
        self._module.fail_json(msg=('Failure while calling the cloudscale.ch API with GET for "%s".' % api_call), fetch_url_info=info)