@g_connect
def authenticate(self, github_token):
    '\n        Retrieve an authentication token\n        '
    url = ('%s/tokens/' % self.baseurl)
    args = urlencode({
        'github_token': github_token,
    })
    resp = open_url(url, data=args, validate_certs=self._validate_certs, method='POST')
    data = json.load(to_text(resp, errors='surrogate_or_strict'))
    return data