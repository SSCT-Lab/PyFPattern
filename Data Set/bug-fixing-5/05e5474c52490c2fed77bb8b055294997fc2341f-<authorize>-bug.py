def authorize(self, params, **kwargs):
    passwd = params['auth_pass']
    cmd = Command('enable', prompt=self.NET_PASSWD_RE, response=passwd)
    self.execute([cmd, 'no terminal pager'])