def post(self, url, body=None, headers=None, **kwargs):
    if headers:
        headers = self.merge_dictionaries(headers, self._headers())
    else:
        headers = self._headers()
    try:
        return self.session().post(url, json=body, headers=headers)
    except getattr(requests.exceptions, 'RequestException') as inst:
        self.module.fail_json(msg=inst.message)