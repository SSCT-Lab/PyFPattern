def login(self, username, password):
    if (('KRB5CCNAME' in os.environ) and HAS_GSSAPI):
        self.use_gssapi = True
    elif (('KRB5_CLIENT_KTNAME' in os.environ) and HAS_GSSAPI):
        ccache = ('MEMORY:' + str(uuid.uuid4()))
        os.environ['KRB5CCNAME'] = ccache
        self.use_gssapi = True
    else:
        if (not password):
            self._fail('login', 'Password is required if not using GSSAPI. To use GSSAPI, please set the KRB5_CLIENT_KTNAME or KRB5CCNAME (or both)  environment variables.')
        url = ('%s/session/login_password' % self.get_base_url())
        data = ('user=%s&password=%s' % (quote(username, safe=''), quote(password, safe='')))
        headers = {
            'referer': self.get_base_url(),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain',
        }
        try:
            (resp, info) = fetch_url(module=self.module, url=url, data=to_bytes(data), headers=headers, timeout=self.timeout)
            status_code = info['status']
            if (status_code not in [200, 201, 204]):
                self._fail('login', info['msg'])
            self.headers = {
                'Cookie': resp.info().get('Set-Cookie'),
            }
        except Exception as e:
            self._fail('login', to_native(e))
    if (not self.headers):
        self.headers = dict()
    self.headers.update({
        'referer': self.get_base_url(),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    })