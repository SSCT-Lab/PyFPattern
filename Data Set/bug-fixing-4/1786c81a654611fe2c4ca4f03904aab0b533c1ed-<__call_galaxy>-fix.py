@g_connect
def __call_galaxy(self, url, args=None, headers=None, method=None):
    if (args and (not headers)):
        headers = self.__auth_header()
    try:
        display.vvv(url)
        resp = open_url(url, data=args, validate_certs=self._validate_certs, headers=headers, method=method, timeout=20)
        data = json.loads(to_text(resp.read(), errors='surrogate_or_strict'))
    except HTTPError as e:
        res = json.loads(to_text(e.fp.read(), errors='surrogate_or_strict'))
        raise AnsibleError(res['detail'])
    return data